# 🗺️ IP-SAKTI Sahayak — Master Architecture & Deployment Roadmap

**Project:** IP-SAKTI Sahayak (Smart India Hackathon 2026, Ministry of Ayush — PS 26045)  
**System Type:** Domain-Specific RAG Decision Support System for Ayurvedic Intellectual Property & Regulatory Compliance

---

## 🎯 Strategic Objective
Empower Ayurvedic innovators, researchers, practitioners, and MSMEs to navigate complex, fragmented statutory frameworks:
1. **Intellectual Property:** Indian Patents Act 1970 (Sec 3(p) TK bar, Sec 3(e) synergy, Sec 3(j)), TKDL prior-art clearance, Geographical Indications (GI), Trade Marks, and Designs.
2. **Biodiversity & ABS:** Biological Diversity Act 2002 (amended 2023) and 2024 Rules (National Biodiversity Authority Form I/III approval).
3. **Drug & Food Regulatory:** Drugs & Cosmetics Act 1940 (Chapter IV-A), Drugs & Magic Remedies Act 1954, and FSSAI Ayurveda-Aahar Regulations (2022/2024).
4. **International Filings:** WIPO GRATK Treaty (2024), Nagoya Protocol on ABS, TRIPS, PCT, and Madrid System.

---

## 🏗️ Architectural Phases

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               PHASE 1: CORE RAG & ROUTING (CURRENT)                    │
│                                                                                        │
│  [Legal Ingestion] ──► [3-Axis Qdrant Index] ──► [Formulation State Machine]          │
│                                                          │                             │
│  [Safe Audit Store] ◄── [Hard Citation Gate] ◄── [LangChain LCEL Llama 3.3]           │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              PHASE 2: GRAPHRAG KNOWLEDGE GRAPH                         │
│                                                                                        │
│  - Relational Entity Graph: (Classical Text) -[barred_by]-> (Section 3(p))             │
│  - Multi-Hop Cross-Act Reasoning: (Ayush Patent) -[mandates]-> (NBA Section 6 ABS)     │
│  - Neo4j / NetworkX integration for dynamic regulatory pathfinding                    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 3: BHASHINI MULTILINGUAL & ENTERPRISE                    │
│                                                                                        │
│  - Bhashini ULCA Indic Translation API (Hindi, Tamil, Telugu, Gujarati, Marathi, etc.) │
│  - Consent-gated Paid IP Database Connectors (Indian Patent Office / WIPO Patentscope) │
│  - DPDP Act 2023 Cryptographic Audit Trail & Automated Legal Escalation Dispatcher    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📅 Roadmap Breakdown

### ✅ Phase 1: Core Grounded RAG & Formulation Routing (Completed)
- [x] **Corpus Curation:** 17 section-chunked statutory seed documents across India Code and WIPO treaties.
- [x] **3-Axis Metadata Tagging:** `[jurisdiction]` × `[ip_type]` × `[formulation_category]`.
- [x] **Qdrant Cloud Integration:** Cloud-managed vector store for low-latency similarity search.
- [x] **Deterministic Formulation Classifier:** 5-category state machine (Classical, Proprietary, Phytopharmaceutical, Ayurveda-Aahar, Cosmetic).
- [x] **Grounded LLM Reasoning Engine:** LangChain LCEL pipeline with ChatGroq Llama-3.3-70B.
- [x] **Hard-Gate Citation Validator:** Rejects hallucinated citations and forces safe abstention when grounding is absent.
- [x] **Territorial Switch:** Strict India vs International jurisdiction toggle in React UI.
- [x] **Evaluation Engine:** Automated benchmark testing calculating Precision@k, MRR, and Citation Validity.
- [x] **Audit Database:** SQLite persistent store logging queries, citations, and human escalations.

---

### 🔄 Phase 2: GraphRAG & Multi-Hop Legal Knowledge Graph (In Progress)
- [ ] **Knowledge Graph Construction:**
  - Map Ayurvedic herbs to First Schedule texts (*Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*).
  - Map statutory triggers: Herb formulation -> Form I NBA approval -> Patent Form 1 declaration.
- [ ] **Hybrid Search:** Combine Qdrant semantic dense embeddings with Neo4j/NetworkX graph traversal.
- [ ] **Synergy Evidence Assistant:** Assist proprietary medicine applicants with Section 3(e) non-obviousness and synergistic experimental framing.

---

### 🔮 Phase 3: Bhashini Indic Localization & DPDP Enterprise Alignment
- [ ] **Bhashini API Pipeline:**
  - Regional Indic query -> Bhashini Translation -> English Grounded RAG -> Bhashini Indic Response.
  - Support for 12+ official Indian languages for grassroots Ayurvedic Vaidyas and MSMEs.
- [ ] **DPDP Act 2023 Explicit Consent Gate:**
  - Consent tracking modal prior to connecting to external patent search APIs.
  - Anonymized audit export and compliance reporting.
- [ ] **Automated Human Escalation Workflow:**
  - Direct ticket sync with Ministry of Ayush & IP facilitator panels.

---

## 🛡️ Mandatory Compliance Guardrails
1. **Standing Disclaimer:** Every AI response is prepended/appended with:  
   *`"This is informational guidance, not legal advice."`*
2. **Zero-Hallucination Policy:** If similarity score or citation validity fails, the assistant returns safe abstention with contact links to Ayush IP facilitation cells.
