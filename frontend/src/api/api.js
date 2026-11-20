const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function getTenders(accessToken) {
  const response = await fetch(`${API_BASE_URL}/tenders/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch tenders");
  }

  return response.json();
}

export async function getTenderOverview(tenderId, accessToken) {
  const response = await fetch(
    `${API_BASE_URL}/tenders/${tenderId}/overview/`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch tender overview");
  }

  return response.json();
}

export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  if (!response.ok) {
    throw new Error("Invalid email or password");
  }

  return response.json();
}

export async function getDashboardStats(accessToken) {
  const response = await fetch(
    `${API_BASE_URL}/tenders/dashboard-stats/`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch dashboard stats");
  }

  return response.json();
}

export async function createTender(
  title,
  description,
  document,
  accessToken
) {
  const formData = new FormData();

  formData.append("title", title);
  formData.append("description", description);

  if (document) {
    formData.append("document", document);
  }

  const response = await fetch(
    `${API_BASE_URL}/tenders/`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      body: formData,
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));

    throw new Error(
      errorData.detail ||
      "Failed to create tender"
    );
  }

  return response.json();
}


export const deleteTender = async (tenderId) => {
  const token = localStorage.getItem("accessToken");

  const response = await fetch(
    `${API_BASE_URL}/tenders/${tenderId}/`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));

    throw new Error(
      data.detail || "Failed to delete tender."
    );
  }

  return true;
};

export const askTenderQuestion = async (
  tenderId,
  question,
  history = []
) => {
  const token = localStorage.getItem("accessToken");

  const response = await fetch(
    `http://127.0.0.1:8000/api/tenders/${tenderId}/ask/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        question: question,
        history: history,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        data.question?.[0] ||
        "Failed to ask question"
    );
  }

  return data;
};

export const getTenderRisk = async (tenderId) => {
  const token = localStorage.getItem("accessToken");

  const response = await fetch(
    `http://127.0.0.1:8000/api/tenders/${tenderId}/risk/`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to load tender risk"
    );
  }

  return data;
};