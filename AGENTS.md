# AGENTS.md — Codebase Summary & Architectural Record

## Project Overview
**IP-SAKTI Sahayak** is a domain-specific RAG decision-support system created for Smart India Hackathon 2026 (Ministry of Ayush, PS 26045). It provides grounded Intellectual Property (Patents, TKDL, Geographical Indications, Trademarks) and Regulatory Guidance (ABS under BDA 2023, FSSAI Ayurveda-Aahar, Drugs & Cosmetics Act) for Ayurvedic innovators.

---

## Codebase Architecture (LangChain + Qdrant Cloud)

```
                                  ┌───────────────────────────────┐
                                  │      Vite React + TS UI       │
                                  │  (India / Intl Toggle & Tabs) │
                                  └───────────────┬───────────────┘
                                                  │ POST /api/chat
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ FastAPI Backend Server (backend/main.py) — loads root .env                                        │
│                                                                                                 │
│  1. Formulation Classifier State Machine (app/classifier.py)                                     │
│     └── Deterministic decision tree (Classical / Proprietary / Phytopharma / Ayurveda-Aahar / Cosmetic)│
│                                                                                                 │
│  2. Qdrant Cloud Vector Retriever (app/retriever.py) — loads root .env                           │
│     └── QdrantVectorStore with 3-axis metadata filter (Jurisdiction, IP, Formulation)            │
│                                                                                                 │
│  3. Grounded LLM Reasoning Engine (app/llm.py)                                                  │
│     └── LangChain LCEL Chain (ChatPromptTemplate | ChatGroq Llama 3.3 70B | StrOutputParser)       │
│                                                                                                 │
│  4. Hard-Gate Citation Enforcement Gate (app/citation_validator.py)                             │
│     └── Verifies draft claims against retrieved section text; forces safe abstention if ungrounded │
│                                                                                                 │
│  5. ABS & TKDL Regulatory Pointers (app/rule_checks.py)                                          │
│     └── NBA Biological Diversity Act clearance alerts & TKDL prior-art warnings                 │
│                                                                                                 │
│  6. SQLite Audit & Benchmark Database (app/database.py)                                          │
│     └── Logs query audit trail, human escalations, and evaluation metrics                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions & Vector Architecture

1. **Decoupled Environment Configurations:** Backend modules (`main.py`, `ingest.py`, `retriever.py`) load `backend/.env` while frontend uses `frontend/.env` (`VITE_API_BASE_URL`), creating strict isolation between client-side assets and backend secret keys (`GROQ_API_KEY`, `QDRANT_API_KEY`).
2. **Dedicated Qdrant Cloud Vector Database:** Vector ingestion (`ingest.py`) and retrieval (`retriever.py`) connect directly to **Qdrant Cloud** managed vector store (`ayush_ip_corpus_langchain`). Local JSON vector store fallback has been completely removed as requested.
3. **LangChain LCEL Pipeline:** The reasoning pipeline utilizes LangChain Expression Language (`ChatPromptTemplate | ChatGroq | StrOutputParser`) and `langchain_core.documents.Document` wrappers.
4. **Deterministic Classifier State Machine:** Product categorization is handled via a rule-based decision tree state machine in Python (`app/classifier.py`), not an LLM prompt.
5. **Hard-Gate Citation Validator:** Citation enforcement is a strict gate (`app/citation_validator.py`). Any draft answer containing ungrounded claims or hallucinated section citations is completely blocked and replaced with a safe abstention notice.

---

## Directory & Module Map

```
prototype/
├── AGENTS.md                     # Codebase architectural record & maintenance state
├── PROMPT.md                     # Hackathon prompt & requirement specification
├── README.md                     # Developer setup, API keys, and seed corpus audit table
├── render.yaml                   # Render Blueprint config for FastAPI backend
├── .gitignore                    # Git exclusion patterns (ignores backend/.env and frontend/.env)
├── corpus/                       # Section-chunked legal seed documents (17 files)
│   └── manifest.json             # 3-axis document metadata catalog
├── backend/
│   ├── .env                      # Backend environment secrets (ignored by git)
│   ├── .env.example              # Backend environment template
│   ├── main.py                   # FastAPI server entrypoint (loads backend/.env)
│   ├── requirements.txt          # Python packages (FastAPI, LangChain, Groq, Qdrant, Gunicorn)
│   ├── seed_corpus.py            # 3-axis seed corpus document generator
│   ├── ingest.py                 # LangChain Document chunker & Qdrant Cloud indexer (loads backend/.env)
│   ├── test_backend.py           # Backend verification suite
│   ├── app/
│   │   ├── classifier.py         # Formulation decision tree state machine
│   │   ├── retriever.py          # Qdrant Cloud retriever with 3-axis metadata filter (loads backend/.env)
│   │   ├── llm.py                # LangChain ChatGroq LCEL grounded reasoning engine
│   │   ├── citation_validator.py # Hard-block citation enforcement validator
│   │   ├── rule_checks.py        # ABS compliance & TKDL prior-art pointers
│   │   ├── database.py           # SQLite database for audit logs & metrics
│   │   └── eval_engine.py        # Benchmark engine for P@k, MRR, citation validity
│   └── data/
│       └── ipsakti.db            # SQLite database (audit logs & metrics)
└── frontend/
    ├── .env                      # Frontend environment config (VITE_API_BASE_URL)
    ├── .env.example              # Frontend environment template
    ├── vercel.json               # Vercel SPA deployment configuration
    ├── index.html                # HTML entrypoint
    ├── vite.config.ts            # Vite config with API proxy
    ├── tailwind.config.js        # Tailwind CSS theme
    ├── src/
    │   ├── main.tsx              # React DOM mounting & Axios baseURL config
    │   ├── App.tsx               # Root app layout & state management
    │   ├── types.ts              # TypeScript interface definitions
    │   ├── index.css             # Glassmorphism & badge styles
    │   └── components/
    │       ├── Header.tsx        # Top navbar & jurisdiction toggle
    │       ├── ChatInterface.tsx # Interactive chat stream & answer cards
    │       ├── ClassifierModal.tsx # Inline formulation classifier UI
    │       ├── EscalateModal.tsx # Human expert escalation form modal
    │       └── EvalDashboard.tsx # Dev metrics dashboard (/metrics)
```

---

## Current State
- **Status:** Decoupled environment setup complete (`backend/.env` and `frontend/.env`). Render blueprint (`render.yaml`) and Vercel configuration (`frontend/vercel.json`) ready for cloud deployment.

- **Ingestion & Search:** `ingest.py` uploads directly to Qdrant Cloud (`QdrantVectorStore`), and `retriever.py` queries Qdrant Cloud with 3-axis metadata filtering.
