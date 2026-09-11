# 🚀 IP-SAKTI Sahayak — Teammate & Contributor Setup Guide

Welcome to **IP-SAKTI Sahayak**! This guide walks any developer or teammate through cloning the repository, configuring environment variables, setting up the Python AI backend, running the Vite React frontend, and running automated test suites on **Windows**, **macOS**, and **Linux**.

---

## 📋 Prerequisites

Ensure you have the following installed on your local machine:

- **Python 3.10+** (verify with `python --version` or `python3 --version`)
- **Node.js 18+ & npm** (verify with `node -v` and `npm -v`)
- **Git** (verify with `git --version`)
- API Keys:
  - **Groq API Key** (from [Groq Console](https://console.groq.com/)) for Llama-3.3-70B reasoning.
  - **Qdrant Cloud Cluster** (from [Qdrant Cloud](https://cloud.qdrant.io/)) URL & API Key.
  - _(Optional)_ Gemini API Key.

---

## 🛠️ Step-by-Step Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/CodeAritra/SIH-2026.git
cd SIH-2026
```

---

### 2. Configure Environment Variables

#### A. Backend Environment (`backend/.env`)
Create `backend/.env` by copying `backend/.env.example`:

**Windows (PowerShell):**
```powershell
Copy-Item backend\.env.example backend\.env
```

**macOS / Linux (Bash):**
```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and fill in your keys:
```env
# Groq API for Fast Grounded LLM Inference
GROQ_API_KEY="gsk_your_groq_api_key_here"

# Qdrant Cloud Managed Vector Database
QDRANT_URL="https://your-cluster-url.qdrant.tech"
QDRANT_API_KEY="your_qdrant_api_key_here"

# Optional / Fallback
GEMINI_API_KEY="AIzaSy..."
```

#### B. Frontend Environment (`frontend/.env`)
Create `frontend/.env` by copying `frontend/.env.example`:

**Windows (PowerShell):**
```powershell
Copy-Item frontend\.env.example frontend\.env
```

**macOS / Linux (Bash):**
```bash
cp frontend/.env.example frontend/.env
```

For local development, leave `VITE_API_BASE_URL=""` so Vite uses the local proxy (`http://localhost:8000`). For production on Vercel, set `VITE_API_BASE_URL="https://ip-sakti-backend.onrender.com"`.


---

### 3. Backend Setup (Python + FastAPI + LangChain)

#### A. Create and Activate Virtual Environment

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### B. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

#### C. Ingest the Legal Corpus into Qdrant Cloud

Generate the seed legal documents and chunk them into Qdrant Cloud with strict 3-axis metadata (`jurisdiction`, `ip_type`, `formulation`):

```bash
# 1. Generate statutory corpus files
python backend/seed_corpus.py

# 2. Ingest document chunks into Qdrant Cloud collection
python backend/ingest.py
```

#### D. Run the Backend Verification Suite

Verify all components (retriever, formulation classifier, citation gate, ABS/TKDL rule checkers):

```bash
python backend/test_backend.py
```

#### E. Start the Backend API Server

```bash
python backend/main.py
```

_The FastAPI backend will start on **`http://localhost:8000`** (Swagger docs available at `http://localhost:8000/docs`)._

---

### 4. Frontend Setup (React + Vite + Tailwind CSS)

Open a **new terminal tab/window**:

```bash
cd frontend
npm install
npm run dev
```

_The React UI will start on **`http://localhost:3000`** (or `http://localhost:5173` depending on port availability) and automatically proxies API requests to `http://localhost:8000`._

---

## 🧪 Testing and Verification Checklist

| Test Item                     | Command                                 | Expected Outcome                                          |
| :---------------------------- | :-------------------------------------- | :-------------------------------------------------------- |
| **Backend Integration**       | `python backend/test_backend.py`        | `SUCCESS: All LangChain backend tests passed clean!`      |
| **Frontend Production Build** | `cd frontend && npm run build`          | `dist/` created with 0 TypeScript/Lint errors             |
| **Health API**                | `GET http://localhost:8000/api/health`  | `{"status": "online", "service": "IP-SAKTI Sahayak API"}` |
| **Metrics Benchmark**         | `GET http://localhost:8000/api/metrics` | Returns evaluation benchmark runs and query logs          |

---

## 📁 Key Directories & Architecture Map

- **`backend/seed_corpus.py`**: Generates 17 statutory seed documents across Patents, Biological Diversity, Drugs & Cosmetics, TKDL, FSSAI, and WIPO treaties.
- **`backend/ingest.py`**: Chunks documents hierarchically and indexes them into Qdrant Cloud.
- **`backend/app/classifier.py`**: Deterministic decision tree state machine for Ayurvedic product classification.
- **`backend/app/retriever.py`**: 3-Axis metadata vector retriever connecting to Qdrant Cloud.
- **`backend/app/llm.py`**: LangChain LCEL grounded reasoning chain with ChatGroq Llama-3.3-70B.
- **`backend/app/citation_validator.py`**: Hard-gate citation validator that halts hallucinations.
- **`backend/app/rule_checks.py`**: NBA Access & Benefit Sharing (ABS) and TKDL prior-art checkers.
- **`backend/app/database.py`**: SQLite audit logging store for DPDP alignment and benchmark analytics.
- **`frontend/src/App.tsx`**: Main UI controller connecting chat, formulation classifier, and evaluation metrics dashboard.

---

## 🤝 Troubleshooting & Common Fixes

1. **`ModuleNotFoundError: No module named 'app'`**: Ensure you run backend scripts from the repository root using `python backend/test_backend.py` or `python backend/main.py`.
2. **Qdrant Connection Timeout / Auth Error**: Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env` are accurate and not enclosed in extra quotes.
3. **Groq Rate Limits / Missing Key**: Ensure `GROQ_API_KEY` is present in root `.env`.
