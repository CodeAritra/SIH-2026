# 🌿 IP-SAKTI Sahayak — RAG-Based Ayurvedic IP & Regulatory Assistant

**Smart India Hackathon 2026 Prototype** | Ministry of Ayush (Problem Statement: PS 26045)

IP-SAKTI Sahayak is a domain-specialized, RAG-grounded decision support assistant designed to help Ayurvedic startups, MSMEs, practitioners, researchers, and cultivators navigate Intellectual Property (Patents, TKDL, Geographical Indications, Trademarks) and Regulatory Obligations (ABS clearance under BDA 2023, FSSAI Ayurveda-Aahar, Drugs & Cosmetics Act).

---

## 📚 Essential Project Documentation
- 📖 **[Developer & Contributor Setup Guide](SETUP_GUIDE.md):** Complete step-by-step onboarding guide for running frontend & backend locally across Windows, macOS, and Linux.
- 🗺️ **[Master Architecture & Roadmap](ROADMAP.md):** Architectural breakdown across Phase 1 (MVP RAG + Formulation Routing), Phase 2 (Knowledge Graph / GraphRAG), and Phase 3 (Bhashini Indic Localization & DPDP Audit).
- 📜 **[Architectural Maintenance Record](AGENTS.md):** Codebase summary and architectural guidelines.

---

## 🏛️ System Architecture Flow

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              Vite + React (TypeScript) UI                              │
│  - Strict Dual Jurisdiction Switch: [ India (Domestic) | International (Export/WIPO) ] │
│  - Deterministic Formulation Intercept & Clarification Dialog                          │
│  - Mandatory Standing Disclaimer ("Informational guidance, not legal advice")          │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ POST /api/chat
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ FastAPI Backend Application (backend/main.py)                                          │
│                                                                                        │
│  1. Formulation Classifier State Machine (app/classifier.py)                           │
│     └── Intercepts query & prompts clarifying question if product is unclassified      │
│                                                                                        │
│  2. 3-Axis Qdrant Cloud Vector Retriever (app/retriever.py)                            │
│     └── Filter by: [Jurisdiction] × [IP Type] × [Formulation Category]                 │
│                                                                                        │
│  3. Grounded LLM Reasoning Engine (app/llm.py)                                         │
│     └── LangChain LCEL (ChatPromptTemplate | ChatGroq Llama 3.3 70B | StrOutputParser) │
│                                                                                        │
│  4. Hard-Gate Citation Validator (app/citation_validator.py)                           │
│     └── Verifies draft citations against retrieved text; prevents hallucinations       │
│                                                                                        │
│  5. ABS & TKDL Regulatory Checkers (app/rule_checks.py)                                 │
│     └── Biological Diversity Act (BDA 2023) clearance & TKDL prior-art warnings        │
│                                                                                        │
│  6. SQLite Audit & Benchmark Database (app/database.py)                                │
│     └── Logs query audit trails, DPDP consent, human escalations, and benchmark metrics│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Seed Statutory Corpus (17 Documents)

Every vector point in Qdrant Cloud is indexed with **3-Axis metadata** (`jurisdiction`, `ip_type`, `formulation`):

| Document Title | Jurisdiction | IP Type | Formulation Relevance | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Patents Act, 1970 (Sec 3(p), 3(j), 6, 10(4))** | India | Patent | Classical, Proprietary | **Indexed** |
| **Patents (Amendment) Rules, 2024 (Sec 13, 55)** | India | Patent | Proprietary, Phytopharma | **Indexed** |
| **Biological Diversity Act, 2002 (Amended 2023)** | India | ABS | All | **Indexed** |
| **Biological Diversity (Amendment) Rules, 2024** | India | ABS | All | **Indexed** |
| **NBA ABS Procedural Handbook & Guidelines** | India | ABS | All | **Indexed** |
| **TKDL Framework & TKRC Structure** | India | Patent | Classical, Proprietary | **Indexed** |
| **Geographical Indications of Goods Act, 1999** | India | GI | Classical, Proprietary | **Indexed** |
| **Trade Marks Act, 1999 (Sec 9, 11, 29)** | India | Trademark | All | **Indexed** |
| **Drugs and Cosmetics Act, 1940 & Rules 1945** | India | Regulatory | Classical, Proprietary, Phytopharma, Cosmetic | **Indexed** |
| **Drugs & Magic Remedies Act, 1954 (Sec 3, 4)** | India | Regulatory | Classical, Proprietary, Ayurveda-Aahar | **Indexed** |
| **FSSAI Ayurveda-Aahar Regulations, 2022/2024** | India | Regulatory | Ayurveda-Aahar | **Indexed** |
| **TRIPS Agreement (WIPO/WTO - Art 27, 22, 39)** | International | Patent/GI/Secrets | All | **Indexed** |
| **CBD (Convention on Biological Diversity)** | International | ABS | All | **Indexed** |
| **Nagoya Protocol on Access & Benefit-Sharing** | International | ABS | All | **Indexed** |
| **WIPO GRTK Treaty (2024 - Art 3, 4)** | International | Patent | Classical, Proprietary | **Indexed** |
| **PCT (Patent Cooperation Treaty - Art 3, 15)** | International | Patent | Proprietary, Phytopharma, New Drug | **Indexed** |
| **Budapest Treaty (Microorganism Deposit)** | International | Patent | Phytopharma, New Drug | **Indexed** |

---

## ⚡ Quickstart

### 1. Configure Environment (`.env`)
```env
GROQ_API_KEY="gsk_..."
QDRANT_URL="https://your-cluster-url.qdrant.tech:6333"
QDRANT_API_KEY="your_qdrant_api_key_here"
```

### 2. Backend & Ingestion
```bash
python backend/seed_corpus.py
python backend/ingest.py
python backend/main.py
# Backend runs at http://localhost:8000
```

### 3. Frontend UI
```bash
cd frontend
npm install
npm run dev
# Frontend runs at http://localhost:3000
```

---

## 🧪 Verification Tests
Run the backend test suite:
```bash
python backend/test_backend.py
```
