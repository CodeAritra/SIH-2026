# IP-SAKTI Sahayak — RAG-Based Ayurvedic IP & Regulatory Assistant

**Smart India Hackathon 2026 Prototype** | Ministry of Ayush (PS 26045)

IP-SAKTI Sahayak is a domain-specialized, RAG-grounded decision support assistant designed to help Ayurvedic startups, MSMEs, practitioners, and cultivators navigate Intellectual Property (Patents, TKDL, Geographical Indications, Trademarks) and Regulatory Obligations (ABS clearance under BDA 2023, FSSAI Ayurveda-Aahar, Drugs & Cosmetics Act).

---

## Dedicated Qdrant Cloud Vector Database Architecture

Vector ingestion (`backend/ingest.py`) and semantic similarity retrieval (`backend/app/retriever.py`) connect directly to **Qdrant Cloud Managed Vector Store** (`ayush_ip_corpus_langchain`). Local vector store file fallbacks have been completely removed.

### 3-Axis Metadata Filtering in Qdrant Cloud

Every vector point in Qdrant Cloud is indexed with **3-Axis metadata**:

1. **Jurisdiction:** `india` | `international`
2. **IP Type:** `patent` | `gi` | `trademark` | `copyright` | `design` | `trade_secret` | `plant_variety` | `abs` | `drug_regulatory`
3. **Formulation Category Relevance:** `classical` | `proprietary` | `new_drug` | `phytopharma` | `ayurveda_aahar` | `cosmetic` | `all`

---

## Seed Document Catalog (17 Documents)

| Document Title | Jurisdiction | IP Type | Formulation Relevance | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Patents Act, 1970 (Sec 3(p), 3(j), 6, 10(4))** | India | Patent | Classical, Proprietary | **Real Text** |
| **Patents (Amendment) Rules, 2024 (Sec 13, 55)** | India | Patent | Proprietary, Phytopharma | **Real Text** |
| **Biological Diversity Act, 2002 (Amended 2023)** | India | ABS | All | **Real Text** |
| **Biological Diversity (Amendment) Rules, 2024** | India | ABS | All | **Real Text** |
| **NBA ABS Procedural Handbook & Guidelines** | India | ABS | All | **Real Text** |
| **TKDL Framework & TKRC Structure** | India | Patent | Classical, Proprietary | **Real Text** |
| **Geographical Indications of Goods Act, 1999** | India | GI | Classical, Proprietary | **Real Text** |
| **Trade Marks Act, 1999 (Sec 9, 11, 29)** | India | Trademark | All | **Real Text** |
| **Drugs and Cosmetics Act, 1940 & Rules 1945** | India | Regulatory | Classical, Proprietary, Phytopharma, Cosmetic | **Real Text** |
| **Drugs & Magic Remedies Act, 1954 (Sec 3, 4)** | India | Regulatory | Classical, Proprietary, Ayurveda-Aahar | **Real Text** |
| **FSSAI Ayurveda-Aahar Regulations, 2022/2024** | India | Regulatory | Ayurveda-Aahar | **Real Text** |
| **TRIPS Agreement (WIPO/WTO - Art 27, 22, 39)** | International | Patent/GI/Secrets | All | **Real Text** |
| **CBD (Convention on Biological Diversity)** | International | ABS | All | **Real Text** |
| **Nagoya Protocol on Access & Benefit-Sharing** | International | ABS | All | **Real Text** |
| **WIPO GRTK Treaty (2024 - Art 3, 4)** | International | Patent | Classical, Proprietary | **Real Text** |
| **PCT (Patent Cooperation Treaty - Art 3, 15)** | International | Patent | Proprietary, Phytopharma, New Drug | **Real Text** |
| **Budapest Treaty (Microorganism Deposit)** | International | Patent | Phytopharma, New Drug | **Real Text** |

---

## Environment Configuration

Provide your Qdrant Cloud URL and API Key in `.env` at the project root:

```env
GROQ_API_KEY="gsk_..."                         # Groq Llama 3.3 70B reasoning
GEMINI_API_KEY="AIzaSy..."                     # Gemini text-embedding-004
QDRANT_URL="https://your-cluster-url.qdrant.tech" # Qdrant Cloud Cluster URL
QDRANT_API_KEY="your_qdrant_api_key_here"      # Qdrant Cloud API Key
```

---

## Local Development Setup

### 1. Backend Service (FastAPI + Qdrant Cloud)
```bash
python backend/seed_corpus.py
python backend/ingest.py
python backend/main.py
# API runs on http://localhost:8000
```

### 2. Frontend Application (Vite + React)
```bash
cd frontend
npm install
npm run dev
# App runs on http://localhost:3000
```
