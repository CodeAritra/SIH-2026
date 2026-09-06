# 🗺️ IP-SAKTI Sahayak — Master Architecture & Deployment Roadmap

**Project:** IP-SAKTI Sahayak (Smart India Hackathon 2026, Ministry of Ayush — PS 26045)  
**System Type:** Domain-Specific RAG & Knowledge-Graph Decision Support System for Ayurvedic Intellectual Property & Regulatory Compliance

---

## 🎯 Strategic Objective
Empower Ayurvedic innovators, researchers, practitioners, and MSMEs to navigate complex, fragmented statutory frameworks:
1. **Intellectual Property:** Indian Patents Act 1970 (Sec 3(p) TK bar, Sec 3(e) synergy, Sec 3(j)), TKDL prior-art clearance, Geographical Indications (GI), Trade Marks, and Designs.
2. **Biodiversity & ABS:** Biological Diversity Act 2002 (amended 2023) and 2024 Rules (National Biodiversity Authority Form I/III approval).
3. **Drug & Food Regulatory:** Drugs & Cosmetics Act 1940 (Chapter IV-A), Drugs & Magic Remedies Act 1954, and FSSAI Ayurveda-Aahar Regulations (2022/2024).
4. **International Filings:** WIPO GRATK Treaty (2024), Nagoya Protocol on ABS, TRIPS, PCT, and Budapest Treaty.

---

## 🏗️ Architectural Phases

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: GROUNDED RAG & FORMULATION ROUTING                     │
│                                                                                        │
│  [Legal Ingestion] ──► [3-Axis Qdrant Index] ──► [Formulation State Machine]          │
│                                                          │                             │
│  [Safe Audit Store] ◄── [Hard Citation Gate] ◄── [LangChain LCEL Llama 3.3]           │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 2: AYURVEDIC KNOWLEDGE GRAPH & SYNERGY                    │
│                                                                                        │
│  - Relational Entity Graph: (40+ Botanicals) ➔ (First Schedule Texts) ➔ (Sec 3(p) Bar)│
│  - Multi-Hop Regulatory Pathfinding: (Polyherbal Combo) ➔ (NBA Form III ABS Mandate)   │
│  - Section 3(e) Chou-Talalay Synergism & Non-Obviousness Evidence Assistant (CI < 1.0) │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   PHASE 3: BHASHINI INDIC MULTILINGUAL & DPDP AUDITING                 │
│                                                                                        │
│  - Bhashini Multilingual Localization (10+ Languages: Hindi, Tamil, Bengali, Telugu...)│
│  - DPDP Act 2023 Explicit Purpose Limitation & Consent Governance                      │
│  - SHA-256 Tamper-Evident Cryptographic Audit Hash Chaining & Certificate Generation   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📅 Status Breakdown Across All Phases

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

### ✅ Phase 2: Ayurvedic Herb & Statutory Knowledge Graph (Completed)
- [x] **Canonical Ayurvedic Botanical Ontology:** 40+ herbs (Ashwagandha, Curcumin, Brahmi, Tulsi, Guduchi, Shatavari, Triphala, Neem, Pippali, Kalmegh, etc.) mapped to First Schedule texts (*Charaka*, *Sushruta*, *Ashtanga Hridaya*, *Bhavaprakasha*, *API*).
- [x] **Multi-Hop Regulatory Pathfinding Engine:** Resolves multi-herb formulation risks, NBA Form I/III requirements, and GI tag opportunities.
- [x] **Section 3(e) Synergistic Evidence Assistant:** Chou-Talalay Combination Index ($CI < 1.0$) evaluation, Isobologram experimental protocols, and patentability risk radar.
- [x] **Interactive Graph Visualizer Canvas:** Color-coded node-link canvas in React with instant path computation.

---

### ✅ Phase 3: Bhashini Indic Localization & DPDP 2023 Auditing (Completed)
- [x] **Bhashini Indic Localization Engine:** Full domain-aware multilingual support across 10+ languages (Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, English).
- [x] **DPDP Act 2023 Consent Gate:** Explicit purpose limitation tracking for confidential herbal formulations.
- [x] **Cryptographic SHA-256 Audit Trail:** Tamper-evident hash chaining for all legal outputs and citation decisions.
- [x] **Verified Compliance Certificate Generator:** Printable/downloadable official Ayush IP audit docket with verification badge.

---

## 🛡️ Mandatory Compliance Guardrails
1. **Standing Disclaimer:** Every AI response includes:  
   *`"This is informational guidance, not legal advice."`*
2. **Zero-Hallucination Policy:** If similarity score or citation validity fails, the assistant returns safe abstention with contact links to Ayush IP facilitation cells.
