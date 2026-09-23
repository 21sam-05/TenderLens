# TenderLens

### AI-Powered Tender Intelligence & Bid Readiness Platform

TenderLens is a full-stack AI platform that helps small businesses and contractors analyze government and enterprise tender documents, understand requirements, ask questions about tender contents, identify risks, and determine whether their company is ready to submit a bid.

The platform combines **Django REST Framework, PostgreSQL, pgvector, Gemini AI, RAG, OCR, and React** into an end-to-end tender analysis system.

---

## 🚀 Problem

Tender documents are often lengthy, unstructured PDF documents containing important information such as:

* Eligibility requirements
* Financial requirements
* Technical specifications
* Previous experience requirements
* Required documents
* Bid security
* Project value
* Deadlines
* Penalties
* Project duration

Manually reviewing these documents can be time-consuming and makes it easy to miss critical requirements.

TenderLens converts this unstructured tender information into structured, searchable, and actionable insights.

---

## ✨ Key Features

### 📄 Tender Upload & Processing

* Upload tender PDF documents
* Extract text from PDFs using PyMuPDF
* OCR support for scanned documents
* Clean and normalize extracted text
* Split documents into meaningful overlapping chunks
* Store processed document information for retrieval

### 🧠 AI-Powered Tender Intelligence

TenderLens uses Gemini to extract structured information from tender documents, including:

* Eligibility requirements
* Financial requirements
* Technical requirements
* Experience requirements
* Required documents
* Important deadlines
* Penalties
* Project duration

### 🔎 Semantic Search & RAG

TenderLens implements a Retrieval-Augmented Generation pipeline:

```text
Tender PDF
    ↓
Text Extraction
    ↓
Text Cleaning
    ↓
Section-Aware Chunking
    ↓
Gemini Embeddings
    ↓
PostgreSQL + pgvector
    ↓
Semantic Similarity Search
    ↓
Relevant Tender Context
    ↓
Gemini
    ↓
Grounded Answer
```

The system uses `gemini-embedding-001` embeddings and PostgreSQL with `pgvector` for vector similarity search.

### 💬 Tender Q&A

Users can ask natural-language questions about a tender.

For example:

```text
What is the minimum annual turnover required?

What is the bid security amount?

What documents are required?

What is the project duration?

What is the submission deadline?
```

The system retrieves relevant document chunks and generates an answer using the retrieved tender context.

### 📊 Bid Readiness Analysis

TenderLens compares tender requirements against the company's profile.

Company information can include:

* Annual turnover
* Years of experience
* Number of similar projects
* Construction license
* Tax registration

The system produces:

* Readiness score
* Readiness level
* Bid-ready status
* Requirement-level analysis

Example:

```text
Score: 100
Readiness: High
Bid Ready: Yes
```

### ⚠️ Tender Risk Analysis

TenderLens analyzes tender information to identify potentially important risk factors and presents them through the application.

### 🔐 Authentication

The backend uses JWT-based authentication with:

* Email-based user authentication
* Access tokens
* Refresh tokens
* Protected API endpoints

### 🖥️ Full-Stack Dashboard

The React frontend provides:

* Dashboard statistics
* Tender upload
* Tender listing
* Tender overview
* Search and filtering
* Bid readiness information
* Risk information
* Tender Q&A
* Tender deletion

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       React UI      │
                         │     Vite + React    │
                         └──────────┬──────────┘
                                    │
                                    │ REST API
                                    ▼
                         ┌─────────────────────┐
                         │   Django + DRF      │
                         │                     │
                         │ Authentication      │
                         │ Tender APIs         │
                         │ Readiness APIs      │
                         │ Risk APIs           │
                         │ Q&A APIs            │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
           ┌────────────┐    ┌─────────────┐   ┌──────────────┐
           │ PostgreSQL │    │ Gemini API  │   │ PDF / OCR    │
           │ + pgvector │    │             │   │ Processing   │
           └─────┬──────┘    └─────────────┘   └──────────────┘
                 │
                 ▼
          Vector Embeddings
          & Similarity Search
```

---

## 🧠 RAG Architecture

TenderLens uses RAG to answer questions from the actual contents of uploaded tender documents.

### 1. Document Ingestion

The user uploads a tender PDF.

### 2. Text Extraction

Text is extracted from the PDF using PyMuPDF.

For scanned or image-based content, OCR processing can be used.

### 3. Text Cleaning

Extracted text is normalized and cleaned before processing.

### 4. Chunking

The document is divided into smaller overlapping chunks while preserving useful section context.

### 5. Embedding Generation

Each chunk is converted into a vector representation using Gemini embeddings.

```text
Tender Chunk
     ↓
Gemini Embedding Model
     ↓
3072-dimensional vector
```

### 6. Vector Storage

Embeddings are stored in PostgreSQL using `pgvector`.

### 7. Retrieval

When the user asks a question:

```text
User Question
      ↓
Question Embedding
      ↓
Vector Similarity Search
      ↓
Top Relevant Chunks
```

### 8. Generation

The retrieved chunks are passed to Gemini along with the user's question.

The model generates an answer grounded in the retrieved tender content.

---

## 🛠️ Tech Stack

### Backend

* Python
* Django
* Django REST Framework
* JWT Authentication

### Database

* PostgreSQL
* pgvector

### AI

* Google Gemini API
* Gemini Embeddings
* Retrieval-Augmented Generation (RAG)
* Structured JSON generation

### Document Processing

* PyMuPDF
* OCR processing
* Text cleaning
* Section-aware chunking

### Frontend

* React
* Vite
* JavaScript
* CSS

### Development

* Git
* GitHub
* REST APIs
* Postman

---

## 📁 Project Structure

```text
TenderLens/
│
├── backend/
│   │
│   ├── accounts/
│   ├── companies/
│   ├── tenders/
│   ├── documents/
│   │
│   ├── config/
│   ├── document_processor.py
│   ├── generation_service.py
│   ├── rag_service.py
│   ├── tender_intelligence.py
│   ├── ocr_service.py
│   ├── risk_service.py
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   │   ├── api/
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 🔑 Core API Endpoints

### Authentication

```text
POST /api/auth/login/
POST /api/auth/register/
POST /api/auth/refresh/
```

### Company

```text
GET  /api/company/
PUT  /api/company/
```

### Tenders

```text
GET    /api/tenders/
POST   /api/tenders/
GET    /api/tenders/<id>/
DELETE /api/tenders/<id>/
```

### Tender Intelligence

```text
GET /api/tenders/<id>/overview/
GET /api/tenders/<id>/readiness/
GET /api/tenders/<id>/bid-analysis/
GET /api/tenders/<id>/risk/
POST /api/tenders/<id>/ask/
```

---

## ⚙️ Local Setup

### Prerequisites

Make sure the following are installed:

* Python
* Node.js
* PostgreSQL
* pgvector extension
* Git

You will also need a Gemini API key.

---

### 1. Clone the Repository

```cmd
git clone https://github.com/21sam-05/TenderLens.git
cd TenderLens
```

---

### 2. Backend Setup

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file containing the required environment variables.

The `.env` file is intentionally excluded from Git.

---

### 3. Database Setup

Configure PostgreSQL and enable the `pgvector` extension.

Then run:

```cmd
python manage.py migrate
```

---

### 4. Start Django

```cmd
python manage.py runserver
```

The backend will run on:

```text
http://127.0.0.1:8000/
```

---

### 5. Frontend Setup

Open another CMD terminal:

```cmd
cd frontend
npm install
npm run dev
```

The Vite development server will provide the frontend URL.

---

## 🔐 Environment Variables

TenderLens uses environment variables for sensitive configuration.

Example:

```text
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_django_secret_key
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

**Never commit your `.env` file or API keys to GitHub.**

---

## 📈 Example Tender Analysis

A processed tender can provide information such as:

```text
Bid Security:
₹5,00,000

Project Value:
₹4.8 Crore

Minimum Annual Turnover:
₹2 Crore

Project Duration:
12 months from date of work order

Submission Deadline:
15 October 2026, 18:00 IST
```

TenderLens then compares these requirements against the company's profile to determine bid readiness.

---

## 🎯 Why TenderLens?

TenderLens combines several real-world engineering concepts into a single application:

* Full-stack development
* REST API design
* Authentication
* PostgreSQL
* Vector databases
* Embeddings
* Semantic search
* RAG
* LLM-based information extraction
* OCR
* AI-assisted risk analysis
* Frontend application development

The project is designed around a realistic business workflow rather than a standalone AI demo.

---

## 🔮 Future Improvements

Potential future improvements include:

* Multi-tender comparison
* Advanced requirement matching
* Better OCR pipelines
* Tender recommendation
* Automated document checklist generation
* Email notifications for deadlines
* Background processing with Celery
* Redis-based caching
* Role-based access control
* Production deployment
* Observability and monitoring
* More advanced hybrid keyword + vector retrieval

---
## Screenshots
<img width="927" height="905" alt="Screenshot 2026-09-19 151909" src="https://github.com/user-attachments/assets/ebd6d15e-64dc-42dc-b28b-51927572f1b0" />
<img width="1379" height="709" alt="Screenshot 2026-09-19 114252" src="https://github.com/user-attachments/assets/2b2cbffb-0703-4922-a865-966cbad2ae1e" />
<img width="1887" height="963" alt="Screenshot 2026-09-22 191641" src="https://github.com/user-attachments/assets/f3b78af5-3d6f-4144-863b-1905ac0718d9" />
<img width="1916" height="899" alt="Screenshot 2026-09-19 152117" src="https://github.com/user-attachments/assets/5bef23c7-e26b-4954-ad69-02dfdb58eb6e" />


## 👨‍💻 Author

**Sam**

B.Tech Computer Science & Engineering (AI/ML)

GitHub:

https://github.com/21sam-05

---

## 📌 Project Status

**Completed — September 2026**

TenderLens was developed as a practical full-stack AI project combining backend engineering, document processing, RAG, vector search, LLM integration, and frontend development.
