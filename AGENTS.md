# AGENTS.md — Codebase Summary & Architectural Record

## Project Overview
**IP-SAKTI Sahayak** is a domain-specific RAG and Knowledge-Graph decision-support platform created for Smart India Hackathon 2026 (Ministry of Ayush, PS 26045). It provides grounded Intellectual Property (Patents, TKDL, Geographical Indications, Trademarks) and Regulatory Guidance (ABS under BDA 2023, FSSAI Ayurveda-Aahar, Drugs & Cosmetics Act) for Ayurvedic innovators.

---

## Codebase Architecture (LangChain + Qdrant Cloud + Knowledge Graph + Bhashini + DPDP)

```
                                  ┌───────────────────────────────┐
                                  │   Vite React + TS UI (v2.0)   │
                                  │  - Dual Jurisdiction Switch   │
                                  │  - Bhashini 10+ Language Menu │
                                  │  - Knowledge Graph Visualizer │
                                  │  - Section 3(e) Synergy UI    │
                                  │  - DPDP Certificate Viewer    │
                                  └───────────────┬───────────────┘
                                                  │ POST /api/chat
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ FastAPI Backend Server (backend/main.py)                                                        │
│                                                                                                 │
│  1. Formulation Classifier State Machine (app/classifier.py)                                     │
│     └── Deterministic decision tree (Classical / Proprietary / Phytopharma / Ayurveda-Aahar / Cosmetic)│
│                                                                                                 │
│  2. Qdrant Cloud Vector Retriever (app/retriever.py)                                            │
│     └── QdrantVectorStore with 3-axis metadata filter (Jurisdiction, IP, Formulation)            │
│                                                                                                 │
│  3. Grounded LLM Reasoning Engine (app/llm.py)                                                  │
│     └── LangChain LCEL Chain (ChatPromptTemplate | ChatGroq Llama 3.3 70B | StrOutputParser)       │
│                                                                                                 │
│  4. Hard-Gate Citation Enforcement Gate (app/citation_validator.py)                             │
│     └── Verifies draft claims against retrieved section text; forces safe abstention if ungrounded │
│                                                                                                 │
│  5. Ayurvedic Herb & Statutory Knowledge Graph (app/knowledge_graph.py)                         │
│     └── 40+ Botanicals mapped to First Schedule texts, bioactives, Sec 3(p), Sec 3(e), & NBA    │
│                                                                                                 │
│  6. Bhashini Indic Multilingual Localization Engine (app/bhashini.py)                           │
│     └── Domain-aware translation across 10+ Indic languages with Ayush term preservation         │
│                                                                                                 │
│  7. DPDP Act 2023 SHA-256 Audit Chaining & Certificates (app/dpdp.py)                           │
│     └── Tamper-evident cryptographic verification hashes & printable compliance dockets         │
│                                                                                                 │
│  8. SQLite Audit & Benchmark Database (app/database.py)                                          │
│     └── Logs query audit trail, cryptographic hashes, human escalations, and evaluation metrics │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Directory & Module Map

```
prototype/
├── AGENTS.md                     # Codebase architectural record & maintenance state
├── README.md                     # Developer setup, API keys, and seed corpus audit table
├── ROADMAP.md                    # Multi-phase master architecture roadmap (Phase 1, 2, 3 complete)
├── SETUP_GUIDE.md                # Quickstart and onboarding manual
├── corpus/                       # Section-chunked legal seed documents (17 files)
│   └── manifest.json             # 3-axis document metadata catalog
├── backend/
│   ├── main.py                   # FastAPI server entrypoint (loads root .env)
│   ├── requirements.txt          # Python packages (FastAPI, LangChain, Groq, Qdrant)
│   ├── seed_corpus.py            # 3-axis seed corpus document generator
│   ├── ingest.py                 # LangChain Document chunker & Qdrant Cloud indexer
│   ├── test_backend.py           # Comprehensive backend verification suite
│   ├── app/
│   │   ├── classifier.py         # Formulation decision tree state machine
│   │   ├── retriever.py          # Qdrant Cloud retriever with 3-axis metadata filter
│   │   ├── llm.py                # LangChain ChatGroq LCEL grounded reasoning engine
│   │   ├── citation_validator.py # Hard-block citation enforcement validator
│   │   ├── rule_checks.py        # ABS compliance & TKDL prior-art pointers
│   │   ├── knowledge_graph.py    # Ayurvedic herb graph & Section 3(e) synergy engine
│   │   ├── bhashini.py           # Bhashini Indic multilingual translation engine
│   │   ├── dpdp.py               # DPDP Act 2023 SHA-256 audit chaining & certificates
│   │   ├── database.py           # SQLite database for audit logs & metrics
│   │   └── eval_engine.py        # Benchmark engine for P@k, MRR, citation validity
│   └── data/
│       └── ipsakti.db            # SQLite database (audit logs, crypto hashes, metrics)
└── frontend/
    ├── index.html                # HTML entrypoint
    ├── vite.config.ts            # Vite config with API proxy
    ├── tailwind.config.js        # Tailwind CSS theme
    ├── src/
    │   ├── main.tsx              # React DOM mounting
    │   ├── App.tsx               # Root app layout & tab state management
    │   ├── types.ts              # TypeScript interface definitions
    │   ├── index.css             # Glassmorphism & badge styles
    │   └── components/
    │       ├── Header.tsx        # Top navbar, jurisdiction switch & Bhashini dropdown
    │       ├── ChatInterface.tsx # Interactive chat stream & answer cards with DPDP seal
    │       ├── KnowledgeGraphVisualizer.tsx # Interactive node-link statutory pathfinder
    │       ├── SynergyAnalyzer.tsx # Section 3(e) synergy & patentability assistant
    │       ├── DPDPConsentModal.tsx # Cryptographic compliance certificate modal
    │       ├── ClassifierModal.tsx # Inline formulation classifier UI
    │       ├── EscalateModal.tsx # Human expert escalation form modal
    │       └── EvalDashboard.tsx # Dev metrics dashboard (/metrics)
```
