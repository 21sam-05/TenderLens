

import { useEffect, useState } from "react";

import {
  getTenders,
  getTenderOverview,
  loginUser,
  getDashboardStats,
  createTender,
  askTenderQuestion,
  getTenderRisk,
  deleteTender,
} from "./api/api";

import "./App.css";

function App() {
  const [tenders, setTenders] = useState([]);
  const [dashboardStats, setDashboardStats] = useState({
    total_tenders: 0,
    bid_ready: 0,
    needs_attention: 0,
  });

  const [tenderOverviews, setTenderOverviews] = useState({});

  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem("accessToken"))
  );

  const [loginError, setLoginError] = useState("");

  const [selectedTender, setSelectedTender] = useState(null);
  const [selectedTenderId, setSelectedTenderId] = useState(null);
  const [tenderRisk, setTenderRisk] = useState(null);
  const [deleteTenderId, setDeleteTenderId] = useState(null);

  const [searchTerm, setSearchTerm] = useState("");
  const [readinessFilter, setReadinessFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  const [showUploadForm, setShowUploadForm] = useState(false);
  const [uploadTitle, setUploadTitle] = useState("");
  const [uploadDescription, setUploadDescription] = useState("");
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadError, setUploadError] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
  const [uploading, setUploading] = useState(false);

  const [question, setQuestion] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [askingQuestion, setAskingQuestion] = useState(false);
  const [questionError, setQuestionError] = useState("");

  const loadTenders = async () => {
    const token = localStorage.getItem("accessToken");

    if (!token) {
      return;
    }

    try {
      const data = await getTenders(token);

      setTenders(data);

      const overviewEntries = await Promise.all(
        data.map(async (tender) => {
          try {
            const overview = await getTenderOverview(
              tender.id,
              token
            );

            return [tender.id, overview];
          } catch (error) {
            console.error(
              `Failed to load overview for tender ${tender.id}:`,
              error
            );

            return [tender.id, null];
          }
        })
      );

      setTenderOverviews(
        Object.fromEntries(overviewEntries)
      );
    } catch (error) {
      console.error("Failed to load tenders:", error);
    }
  };

  const loadDashboardStats = async () => {
    const token = localStorage.getItem("accessToken");

    if (!token) {
      return;
    }

    try {
      const data = await getDashboardStats(token);

      setDashboardStats(data);
    } catch (error) {
      console.error(
        "Failed to load dashboard stats:",
        error
      );
    }
  };

  const loadTenderOverview = async (tenderId) => {
    const token = localStorage.getItem("accessToken");

    if (!token) {
      return;
    }

    try {
      setSelectedTenderId(tenderId);
      setSelectedTender(null);
      setTenderRisk(null);
      setChatMessages([]);
      setQuestion("");
      setQuestionError("");

      const [overview, risk] = await Promise.all([
        getTenderOverview(tenderId, token),
        getTenderRisk(tenderId),
      ]);

      setSelectedTender(overview);
      setTenderRisk(risk);
    } catch (error) {
      console.error(
        "Failed to load tender details:",
        error
      );

      setTenderRisk(null);
    }
  };

  const handleTenderUpload = async (event) => {
    event.preventDefault();

    setUploadError("");
    setUploadSuccess("");
    setUploadStatus("");

    if (!uploadTitle.trim()) {
      setUploadError("Please enter a tender title.");
      return;
    }

    if (!uploadFile) {
      setUploadError("Please select a PDF file.");
      return;
    }

    try {
      setUploading(true);
      setUploadStatus("Uploading tender...");

      const accessToken =
        localStorage.getItem("accessToken");

      await createTender(
        uploadTitle,
        uploadDescription,
        uploadFile,
        accessToken
      );

      setUploadStatus("Processing tender...");

      await Promise.all([
        loadTenders(),
        loadDashboardStats(),
      ]);

      setUploadStatus("");

      setUploadSuccess(
        "Tender uploaded and processed successfully."
      );

      setUploadTitle("");
      setUploadDescription("");
      setUploadFile(null);

      setTimeout(() => {
        setShowUploadForm(false);
        setUploadSuccess("");
      }, 1800);
    } catch (error) {
      setUploadStatus("");

      setUploadError(
        error.message || "Failed to upload tender."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteTender = async (tenderId) => {
    setDeleteTenderId(tenderId);
  };

  const confirmDeleteTender = async () => {
    const tenderId = deleteTenderId;

    if (!tenderId) {
      return;
    }

    try {
      await deleteTender(tenderId);

      setTenders((currentTenders) =>
        currentTenders.filter(
          (tender) => tender.id !== tenderId
        )
      );

      setTenderOverviews((currentOverviews) => {
        const updatedOverviews = {
          ...currentOverviews,
        };

        delete updatedOverviews[tenderId];

        return updatedOverviews;
      });

      if (selectedTenderId === tenderId) {
        setSelectedTender(null);
        setSelectedTenderId(null);
        setTenderRisk(null);
        setChatMessages([]);
        setQuestion("");
        setQuestionError("");
      }

      await loadDashboardStats();
      setDeleteTenderId(null);
    } catch (error) {
      console.error(
        "Delete tender failed:",
        error
      );

      alert(
        error.message ||
          "Failed to delete tender."
      );
      setDeleteTenderId(null);
    }
  };

  const handleLogin = async (event) => {
    event.preventDefault();

    const formData = new FormData(
      event.currentTarget
    );

    const email = formData.get("email");
    const password = formData.get("password");

    try {
      setLoginError("");

      const data = await loginUser(
        email,
        password
      );

      localStorage.setItem(
        "accessToken",
        data.access
      );

      localStorage.setItem(
        "refreshToken",
        data.refresh
      );

      setIsLoggedIn(true);
    } catch (error) {
      console.error(
        "Login failed:",
        error
      );

      setLoginError(
        error.message ||
          "Invalid email or password."
      );
    }
  };

  const handleLogout = () => {
    localStorage.removeItem(
      "accessToken"
    );

    localStorage.removeItem(
      "refreshToken"
    );

    setIsLoggedIn(false);
    setTenders([]);
    setTenderOverviews({});
    setSelectedTender(null);
    setSelectedTenderId(null);
    setTenderRisk(null);
    setChatMessages([]);
    setQuestion("");
    setQuestionError("");
  };

  const handleAskQuestion = async (event) => {
    event.preventDefault();

    if (
      !question.trim() ||
      !selectedTenderId
    ) {
      return;
    }

    try {
      setAskingQuestion(true);
      setQuestionError("");

      const currentQuestion =
        question.trim();

      const conversationHistory = [];

      chatMessages.forEach((message) => {
        if (message.question) {
          conversationHistory.push({
            role: "user",
            content: message.question,
          });
        }

        if (message.answer) {
          conversationHistory.push({
            role: "assistant",
            content: message.answer,
          });
        }
      });

      const data =
        await askTenderQuestion(
          selectedTenderId,
          currentQuestion,
          conversationHistory
        );

      setChatMessages(
        (previousMessages) => [
          ...previousMessages,
          {
            question: currentQuestion,
            answer: data.answer,
            sources: data.sources || [],
          },
        ]
      );

      setQuestion("");
    } catch (error) {
      console.error(
        "Failed to ask tender question:",
        error
      );

      setQuestionError(
        error.message ||
          "Failed to get an answer."
      );
    } finally {
      setAskingQuestion(false);
    }
  };

  const renderRequirement = (
    requirement
  ) => {
    if (typeof requirement === "string") {
      return requirement;
    }

    if (
      !requirement ||
      typeof requirement !== "object"
    ) {
      return String(
        requirement ?? ""
      );
    }

    if (requirement.requirement) {
      return requirement.requirement;
    }

    if (requirement.description) {
      return requirement.description;
    }

    return Object.entries(
      requirement
    )
      .map(([key, value]) => {
        if (
          typeof value === "object"
        ) {
          return `${key}: ${JSON.stringify(
            value
          )}`;
        }

        return `${key}: ${value}`;
      })
      .join(" • ");
  };

  useEffect(() => {
    if (isLoggedIn) {
      loadTenders();
      loadDashboardStats();
    }
  }, [isLoggedIn]);

  const filteredTenders =
    tenders.filter((tender) => {
      const overview =
        tenderOverviews[tender.id];

      const title =
        tender.title?.toLowerCase() ||
        "";

      const description =
        tender.description?.toLowerCase() ||
        "";

      const search =
        searchTerm.toLowerCase();

      const matchesSearch =
        title.includes(search) ||
        description.includes(search);

      const readiness =
        overview?.readiness?.readiness ||
        overview?.bid_readiness?.readiness ||
        overview?.readiness;

      const bidReady =
        overview?.readiness?.bid_ready ??
        overview?.bid_readiness?.bid_ready ??
        false;

      const matchesReadiness =
        readinessFilter === "all" ||
        readiness?.toLowerCase() ===
          readinessFilter.toLowerCase();

      const matchesStatus =
        statusFilter === "all" ||
        (statusFilter === "ready" &&
          bidReady) ||
        (statusFilter === "attention" &&
          !bidReady);

      return (
        matchesSearch &&
        matchesReadiness &&
        matchesStatus
      );
    });

  if (!isLoggedIn) {
    return (
      <div className="login-page">
        <div className="login-card">
          <div className="login-brand">
            <div className="brand-mark">
              TL
            </div>

            <div>
              <h1>TenderLens</h1>

              <span>
                Tender Intelligence Platform
              </span>
            </div>
          </div>

          <div className="login-heading">
            <h2>Welcome back</h2>

            <p>
              Sign in to manage tenders and
              evaluate bid readiness.
            </p>
          </div>

          <form
            className="login-form"
            onSubmit={handleLogin}
          >
            <div className="form-group">
              <label>Email</label>

              <input
                type="email"
                name="email"
                placeholder="Enter your email"
                required
              />
            </div>

            <div className="form-group">
              <label>Password</label>

              <input
                type="password"
                name="password"
                placeholder="Enter your password"
                required
              />
            </div>

            <button
              className="primary-button login-button"
              type="submit"
            >
              Sign In
            </button>
          </form>

          {loginError && (
            <div className="login-error">
              {loginError}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="navbar-brand">
          <div className="brand-mark">
            TL
          </div>

          <div>
            <h1>TenderLens</h1>

            <span>
              Tender Intelligence Platform
            </span>
          </div>
        </div>

        <button
          className="secondary-button"
          onClick={handleLogout}
        >
          Logout
        </button>
      </nav>

      <main className="dashboard">
        <header className="dashboard-header">
          <div>
            <p className="eyebrow">
              TENDER MANAGEMENT
            </p>

            <h2>Dashboard</h2>

            <p className="dashboard-subtitle">
              Monitor tenders, assess bid readiness,
              and identify submission risks.
            </p>
          </div>

          <button
            className="primary-button"
            onClick={() =>
              setShowUploadForm(
                !showUploadForm
              )
            }
          >
            {showUploadForm
              ? "Close Upload"
              : "+ Upload Tender"}
          </button>
        </header>

        {showUploadForm && (
          <section className="upload-card">
            <div className="section-header">
              <div>
                <p className="eyebrow">
                  NEW TENDER
                </p>

                <h3>
                  Upload Tender Document
                </h3>

                <p>
                  Upload a tender PDF to extract
                  intelligence and analyze bid
                  readiness.
                </p>
              </div>
            </div>

            <form
              className="upload-form"
              onSubmit={handleTenderUpload}
            >
              <div className="form-group">
                <label>
                  Tender title
                </label>

                <input
                  type="text"
                  placeholder="Enter tender title"
                  value={uploadTitle}
                  onChange={(event) =>
                    setUploadTitle(
                      event.target.value
                    )
                  }
                />
              </div>

              <div className="form-group">
                <label>
                  Description
                </label>

                <textarea
                  placeholder="Enter a short description"
                  value={uploadDescription}
                  onChange={(event) =>
                    setUploadDescription(
                      event.target.value
                    )
                  }
                />
              </div>

              <div className="form-group">
                <label>
                  PDF document
                </label>

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(event) =>
                    setUploadFile(
                      event.target.files?.[0] ||
                        null
                    )
                  }
                />
              </div>

              <div className="upload-actions">
                <button
                  className="primary-button"
                  type="submit"
                  disabled={uploading}
                >
                  {uploading
                    ? "Processing..."
                    : "Upload Tender"}
                </button>
              </div>

              {uploadError && (
                <div className="upload-message upload-error">
                  {uploadError}
                </div>
              )}

              {uploadStatus && (
                <div className="upload-message upload-processing">
                  {uploadStatus}
                </div>
              )}

              {uploadSuccess && (
                <div className="upload-message upload-success">
                  {uploadSuccess}
                </div>
              )}
            </form>
          </section>
        )}

        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">
              Total Tenders
            </div>

            <div className="stat-value">
              {dashboardStats.total_tenders}
            </div>

            <div className="stat-description">
              Tenders in your workspace
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-label">
              Bid Ready
            </div>

            <div className="stat-value">
              {dashboardStats.bid_ready}
            </div>

            <div className="stat-description">
              Tenders meeting readiness criteria
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-label">
              Needs Attention
            </div>

            <div className="stat-value">
              {dashboardStats.needs_attention}
            </div>

            <div className="stat-description">
              Tenders requiring action
            </div>
          </div>
        </section>

        <section className="intelligence-summary">
          <div>
            <p className="eyebrow">
              AI-POWERED ANALYSIS
            </p>

            <h3>
              Tender Intelligence
            </h3>

            <p>
              Review eligibility, financial
              requirements, technical requirements,
              deadlines, risks, and bid readiness
              from one workspace.
            </p>
          </div>

          <div className="summary-count">
            <strong>
              {filteredTenders.length}
            </strong>

            <span>
              tenders shown
            </span>
          </div>
        </section>

        <section className="filters-section">
          <div className="section-header compact">
            <div>
              <h3>
                Tender Portfolio
              </h3>

              <p>
                Search and filter your tender
                collection.
              </p>
            </div>
          </div>

          <div className="filters">
            <div className="search-wrapper">
              <input
                type="text"
                placeholder="Search by title or description..."
                value={searchTerm}
                onChange={(event) =>
                  setSearchTerm(
                    event.target.value
                  )
                }
              />
            </div>

            <select
              value={readinessFilter}
              onChange={(event) =>
                setReadinessFilter(
                  event.target.value
                )
              }
            >
              <option value="all">
                All Readiness
              </option>

              <option value="high">
                High
              </option>

              <option value="moderate">
                Moderate
              </option>

              <option value="low">
                Low
              </option>
            </select>

            <select
              value={statusFilter}
              onChange={(event) =>
                setStatusFilter(
                  event.target.value
                )
              }
            >
              <option value="all">
                All Status
              </option>

              <option value="ready">
                Bid Ready
              </option>

              <option value="attention">
                Needs Attention
              </option>
            </select>
          </div>
        </section>

        <section className="workspace">
          <div className="tender-list-panel">
            <div className="panel-header">
              <div>
                <h3>
                  Your Tenders
                </h3>

                <p>
                  Select a tender to view its
                  analysis.
                </p>
              </div>

              <span className="count-badge">
                {filteredTenders.length}
              </span>
            </div>

            <div className="tender-list">
              {filteredTenders.length === 0 ? (
                <div className="empty-state">
                  <h4>
                    No tenders found
                  </h4>

                  <p>
                    Try changing your search
                    or filters.
                  </p>
                </div>
              ) : (
                filteredTenders.map(
                  (tender) => {
                    const overview =
                      tenderOverviews[
                        tender.id
                      ];

                    const readiness =
                      overview?.readiness
                        ?.readiness ||
                      overview
                        ?.bid_readiness
                        ?.readiness ||
                      overview?.readiness ||
                      "Unknown";

                    const score =
                      overview?.readiness
                        ?.score ??
                      overview
                        ?.bid_readiness
                        ?.score ??
                      0;

                    return (
                      <div
                        className={`tender-card ${
                          selectedTenderId ===
                          tender.id
                            ? "selected"
                            : ""
                        }`}
                        key={tender.id}
                      >
                        <button
                          className="tender-card-main"
                          onClick={() =>
                            loadTenderOverview(
                              tender.id
                            )
                          }
                        >
                          <div className="tender-card-top">
                            <h4>
                              {tender.title}
                            </h4>

                            <span
                              className={`readiness-pill readiness-${String(
                                readiness
                              ).toLowerCase()}`}
                            >
                              {readiness}
                            </span>
                          </div>

                          <p>
                            {tender.description ||
                              "No description available."}
                          </p>

                          <div className="tender-card-footer">
                            <span>
                              Readiness Score
                            </span>

                            <strong>
                              {score}
                            </strong>
                          </div>
                        </button>

                        <div className="tender-card-actions">
                          <button
                            className="delete-button"
                            onClick={() =>
                              handleDeleteTender(
                                tender.id
                              )
                            }
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    );
                  }
                )
              )}
            </div>
          </div>

          {selectedTender ? (
            <div className="tender-detail">
              <div className="detail-header">
                <div>
                  <p className="eyebrow">
                    TENDER ANALYSIS
                  </p>

                  <h2>
                    {selectedTender.title}
                  </h2>

                  <p>
                    {selectedTender.description ||
                      "No description available."}
                  </p>
                </div>
              </div>

              <section className="overview-section">
                <div className="section-header">
                  <div>
                    <h3>
                      Bid Readiness
                    </h3>

                    <p>
                      Company readiness against
                      tender requirements.
                    </p>
                  </div>
                </div>

                <div className="readiness-grid">
                  <div className="metric-card">
                    <span>
                      Readiness Score
                    </span>

                    <strong>
                      {selectedTender
                        .readiness
                        ?.score ??
                        selectedTender
                          .bid_readiness
                          ?.score ??
                        0}
                    </strong>
                  </div>

                  <div className="metric-card">
                    <span>
                      Readiness Level
                    </span>

                    <strong>
                      {selectedTender
                        .readiness
                        ?.readiness ??
                        selectedTender
                          .bid_readiness
                          ?.readiness ??
                        "Unknown"}
                    </strong>
                  </div>

                  <div className="metric-card">
                    <span>
                      Bid Status
                    </span>

                    <strong>
                      {(
                        selectedTender
                          .readiness
                          ?.bid_ready ??
                        selectedTender
                          .bid_readiness
                          ?.bid_ready
                      )
                        ? "Ready"
                        : "Attention"}
                    </strong>
                  </div>
                </div>
              </section>

              {tenderRisk && (
                <section className="risk-section">
                  <div className="section-header">
                    <div>
                      <h3>
                        Risk & Deadline
                        Intelligence
                      </h3>

                      <p>
                        Key factors that may affect
                        bid preparation.
                      </p>
                    </div>

                    <span
                      className={`risk-badge risk-${String(
                        tenderRisk.overall_risk
                      ).toLowerCase()}`}
                    >
                      {tenderRisk.overall_risk}{" "}
                      Risk
                    </span>
                  </div>

                  <div className="risk-grid">
                    <div className="risk-card deadline-card">
                      <span className="risk-label">
                        Submission Deadline
                      </span>

                      <strong>
                        {tenderRisk.deadline
                          ?.days_remaining !==
                          null &&
                        tenderRisk.deadline
                          ?.days_remaining !==
                          undefined
                          ? `${tenderRisk.deadline.days_remaining} days`
                          : "Unknown"}
                      </strong>

                      <p>
                        {tenderRisk.deadline
                          ?.message ||
                          "Deadline information unavailable."}
                      </p>
                    </div>

                    {tenderRisk.risks?.map(
                      (risk, index) => (
                        <div
                          className="risk-card"
                          key={`${risk.type}-${index}`}
                        >
                          <div className="risk-card-header">
                            <span className="risk-label">
                              {risk.type}
                            </span>

                            <span
                              className={`risk-level risk-${String(
                                risk.level
                              ).toLowerCase()}`}
                            >
                              {risk.level}
                            </span>
                          </div>

                          <p>
                            {risk.message}
                          </p>
                        </div>
                      )
                    )}
                  </div>
                </section>
              )}

              <section className="overview-section">
                <div className="section-header">
                  <div>
                    <h3>
                      Critical Missing
                      Requirements
                    </h3>

                    <p>
                      Requirements that may prevent
                      successful bid submission.
                    </p>
                  </div>
                </div>

                {selectedTender
                  .readiness
                  ?.critical_missing_requirements
                  ?.length > 0 ||
                selectedTender
                  .bid_readiness
                  ?.critical_missing_requirements
                  ?.length > 0 ? (
                  <ul className="requirement-list">
                    {(
                      selectedTender
                        .readiness
                        ?.critical_missing_requirements ||
                      selectedTender
                        .bid_readiness
                        ?.critical_missing_requirements ||
                      []
                    ).map(
                      (
                        requirement,
                        index
                      ) => (
                        <li key={index}>
                          {renderRequirement(
                            requirement
                          )}
                        </li>
                      )
                    )}
                  </ul>
                ) : (
                  <div className="inline-empty">
                    No critical missing
                    requirements.
                  </div>
                )}
              </section>

              <section className="overview-section">
                <div className="section-header">
                  <div>
                    <h3>
                      Tender Intelligence
                    </h3>

                    <p>
                      Structured information extracted
                      from the tender document.
                    </p>
                  </div>
                </div>

                {selectedTender.intelligence ? (
                  <div className="intelligence-grid">
                    <div className="intelligence-card">
                      <h4>
                        Eligibility
                      </h4>

                      <ul>
                        {(
                          selectedTender
                            .intelligence
                            .eligibility_requirements ||
                          []
                        ).map(
                          (
                            item,
                            index
                          ) => (
                            <li
                              key={index}
                            >
                              {renderRequirement(
                                item
                              )}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div className="intelligence-card">
                      <h4>
                        Financial
                        Requirements
                      </h4>

                      <ul>
                        {Array.isArray(
                          selectedTender
                            .intelligence
                            .financial_requirements
                        )
                          ? selectedTender.intelligence.financial_requirements.map(
                              (
                                item,
                                index
                              ) => (
                                <li
                                  key={
                                    index
                                  }
                                >
                                  {renderRequirement(
                                    item
                                  )}
                                </li>
                              )
                            )
                          : Object.entries(
                              selectedTender
                                .intelligence
                                .financial_requirements ||
                                {}
                            ).map(
                              (
                                [
                                  key,
                                  value,
                                ]
                              ) => (
                                <li
                                  key={
                                    key
                                  }
                                >
                                  <strong>
                                    {
                                      key
                                    }
                                    :
                                  </strong>{" "}
                                  {renderRequirement(
                                    value
                                  )}
                                </li>
                              )
                            )}
                      </ul>
                    </div>

                    <div className="intelligence-card">
                      <h4>
                        Technical
                        Requirements
                      </h4>

                      <ul>
                        {(
                          selectedTender
                            .intelligence
                            .technical_requirements ||
                          []
                        ).map(
                          (
                            item,
                            index
                          ) => (
                            <li
                              key={index}
                            >
                              {renderRequirement(
                                item
                              )}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div className="intelligence-card">
                      <h4>
                        Experience
                        Requirements
                      </h4>

                      <ul>
                        {(
                          selectedTender
                            .intelligence
                            .experience_requirements ||
                          []
                        ).map(
                          (
                            item,
                            index
                          ) => (
                            <li
                              key={index}
                            >
                              {renderRequirement(
                                item
                              )}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div className="intelligence-card">
                      <h4>
                        Required Documents
                      </h4>

                      <ul>
                        {(
                          selectedTender
                            .intelligence
                            .required_documents ||
                          []
                        ).map(
                          (
                            item,
                            index
                          ) => (
                            <li
                              key={index}
                            >
                              {renderRequirement(
                                item
                              )}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div className="intelligence-card">
                      <h4>
                        Deadlines
                      </h4>

                      <ul>
                        {(
                          selectedTender
                            .intelligence
                            .deadlines ||
                          []
                        ).map(
                          (
                            item,
                            index
                          ) => (
                            <li
                              key={index}
                            >
                              {renderRequirement(
                                item
                              )}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div className="intelligence-card">
                      <h4>
                        Penalties
                      </h4>

                      <ul>
                        {(
                          selectedTender
                            .intelligence
                            .penalties ||
                          []
                        ).map(
                          (
                            item,
                            index
                          ) => (
                            <li
                              key={index}
                            >
                              {renderRequirement(
                                item
                              )}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div className="intelligence-card">
                      <h4>
                        Project Duration
                      </h4>

                      <p>
                        {renderRequirement(
                          selectedTender
                            .intelligence
                            .project_duration
                        )}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="inline-empty">
                    Tender intelligence is not
                    available.
                  </div>
                )}
              </section>

              <section className="overview-section">
                <div className="section-header">
                  <div>
                    <h3>
                      Bid Analysis
                    </h3>

                    <p>
                      AI-generated assessment of the
                      tender against company readiness.
                    </p>
                  </div>
                </div>

                {selectedTender.bid_analysis ? (
                  <div className="bid-analysis">
                    <div className="analysis-summary">
                      <div>
                        <span>
                          Recommendation
                        </span>

                        <strong>
                          {selectedTender
                            .bid_analysis
                            .recommendation ||
                            "Not available"}
                        </strong>
                      </div>

                      <div>
                        <span>
                          Summary
                        </span>

                        <p>
                          {selectedTender
                            .bid_analysis
                            .summary ||
                            "No summary available."}
                        </p>
                      </div>
                    </div>

                    <div className="analysis-grid">
                      <div className="analysis-card">
                        <h4>
                          Critical Blockers
                        </h4>

                        <ul>
                          {(
                            selectedTender
                              .bid_analysis
                              .critical_blockers ||
                            []
                          ).map(
                            (
                              item,
                              index
                            ) => (
                              <li
                                key={
                                  index
                                }
                              >
                                {renderRequirement(
                                  item
                                )}
                              </li>
                            )
                          )}
                        </ul>
                      </div>

                      <div className="analysis-card">
                        <h4>
                          Priority Actions
                        </h4>

                        <ul>
                          {(
                            selectedTender
                              .bid_analysis
                              .priority_actions ||
                            []
                          ).map(
                            (
                              item,
                              index
                            ) => (
                              <li
                                key={
                                  index
                                }
                              >
                                {renderRequirement(
                                  item
                                )}
                              </li>
                            )
                          )}
                        </ul>
                      </div>

                      <div className="analysis-card">
                        <h4>
                          Strengths
                        </h4>

                        <ul>
                          {(
                            selectedTender
                              .bid_analysis
                              .strengths ||
                            []
                          ).map(
                            (
                              item,
                              index
                            ) => (
                              <li
                                key={
                                  index
                                }
                              >
                                {renderRequirement(
                                  item
                                )}
                              </li>
                            )
                          )}
                        </ul>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="inline-empty">
                    Bid analysis is not
                    available.
                  </div>
                )}
              </section>

              <section className="overview-section chat-section">
                <div className="section-header">
                  <div>
                    <p className="eyebrow">
                      AI ASSISTANT
                    </p>

                    <h3>
                      Ask TenderLens
                    </h3>

                    <p>
                      Ask questions about this tender
                      and receive answers grounded in
                      the tender document.
                    </p>
                  </div>
                </div>

                {chatMessages.length >
                  0 && (
                  <div className="chat-messages">
                    {chatMessages.map(
                      (
                        message,
                        index
                      ) => (
                        <div
                          className="chat-message"
                          key={index}
                        >
                          <div className="chat-question">
                            <div className="chat-avatar user-avatar">
                              You
                            </div>

                            <div className="chat-content">
                              <span className="chat-author">
                                You
                              </span>

                              <p>
                                {
                                  message.question
                                }
                              </p>
                            </div>
                          </div>

                          <div className="chat-answer">
                            <div className="chat-avatar ai-avatar">
                              TL
                            </div>

                            <div className="chat-content">
                              <span className="chat-author">
                                TenderLens
                              </span>

                              <p>
                                {
                                  message.answer
                                }
                              </p>

                              {message
                                .sources
                                ?.length >
                                0 && (
                                <div className="chat-sources">
                                  <span>
                                    Sources
                                  </span>

                                  <ul>
                                    {message.sources.map(
                                      (
                                        source,
                                        sourceIndex
                                      ) => (
                                        <li
                                          key={
                                            sourceIndex
                                          }
                                        >
                                          Page{" "}
                                          {
                                            source.page
                                          }
                                          {" • "}
                                          Chunk{" "}
                                          {
                                            source.chunk_id
                                          }

                                          {source.section
                                            ? ` • ${source.section}`
                                            : ""}
                                        </li>
                                      )
                                    )}
                                  </ul>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                )}

                <div className="suggested-questions">
                  <span>
                    Suggested questions
                  </span>

                  <div className="suggested-question-list">
                    {[
                      "What is the minimum annual turnover required?",
                      "What documents are required?",
                      "What is the project duration?",
                      "What is the submission deadline?",
                    ].map(
                      (
                        suggestedQuestion
                      ) => (
                        <button
                          key={
                            suggestedQuestion
                          }
                          type="button"
                          onClick={() =>
                            setQuestion(
                              suggestedQuestion
                            )
                          }
                        >
                          {
                            suggestedQuestion
                          }
                        </button>
                      )
                    )}
                  </div>
                </div>

                <form
                  onSubmit={
                    handleAskQuestion
                  }
                  className="chat-form"
                >
                  <input
                    type="text"
                    placeholder="Ask a question about this tender..."
                    value={question}
                    onChange={(event) =>
                      setQuestion(
                        event.target.value
                      )
                    }
                    disabled={
                      askingQuestion
                    }
                  />

                  <button
                    className="primary-button"
                    type="submit"
                    disabled={
                      askingQuestion ||
                      !question.trim()
                    }
                  >
                    {askingQuestion
                      ? "Asking..."
                      : "Ask"}
                  </button>
                </form>

                {questionError && (
                  <div className="login-error">
                    {questionError}
                  </div>
                )}
              </section>
            </div>
          ) : (
            <div className="tender-detail empty-detail">
              <div className="empty-detail-content">
                <div className="empty-detail-icon">
                  TL
                </div>

                <h3>
                  Select a tender
                </h3>

                <p>
                  Choose a tender from the list to
                  view intelligence, readiness, risk
                  analysis, and AI-powered answers.
                </p>
              </div>
            </div>
          )}
        </section>

        {deleteTenderId && (
          <div
            className="delete-modal-overlay"
            onClick={() => setDeleteTenderId(null)}
          >
            <div
              className="delete-modal"
              onClick={(event) => event.stopPropagation()}
            >
              <div className="delete-modal-icon">
                !
              </div>

              <h3>Delete Tender?</h3>

              <p>
                Are you sure you want to delete this tender? This action
                cannot be undone.
              </p>

              <div className="delete-modal-actions">
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => setDeleteTenderId(null)}
                >
                  Cancel
                </button>

                <button
                  type="button"
                  className="delete-confirm-button"
                  onClick={confirmDeleteTender}
                >
                  Delete Tender
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;


