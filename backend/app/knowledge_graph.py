"""
Ayurvedic Herb & Statutory Knowledge Graph Engine (Phase 2 GraphRAG).
Maps Ayurvedic botanicals, First Schedule classical texts, bioactives,
statutory bars (Sec 3(p), 3(e), 3(j)), regulatory forms (NBA Form I/III, D&C Form 25D, FSSAI),
and provides multi-hop pathfinding and Section 3(e) synergy analysis.
"""

from typing import Dict, List, Any, Optional

# Canonical Ayurvedic Botanicals & Classical Text Mapping
HERB_ONTOLOGY: Dict[str, Dict[str, Any]] = {
    "ashwagandha": {
        "id": "ashwagandha",
        "common_name": "Ashwagandha",
        "botanical_name": "Withania somnifera",
        "sanskrit_name": "अश्वगन्धा (Ashwagandha)",
        "family": "Solanaceae",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 4/13)", "Sushruta Samhita (Sutra Sthana 38/44)", "Bhavaprakasha (Guduchyadi Varga)", "Ayurvedic Pharmacopoeia of India (API Vol 1)"],
        "bioactives": ["Withaferin A", "Withanolide A", "Withanolide D", "Withanone", "Sominone"],
        "therapeutic_indications": ["Rasayana (Rejuvenator)", "Balya (Strength promoter)", "Medhya (Nootropic / Stress adapter)", "Nidrajanana (Sleep enhancer)", "Anti-inflammatory"],
        "gi_tag": "Nagauri Ashwagandha (Rajasthan - GI Application / Recognized Origin)",
        "tkdl_entries": ["TKDL Identifier: RS/1024, AK/440, JA/312"],
        "nba_clearance_required": True,
        "nba_rationale": "Biological resource of Indian origin. Mandates Form I approval before commercialization or Form III before patent grant under BDA 2002 (amended 2023).",
        "sec_3p_risk": "High if claimed as raw root powder or traditional decoction (Kwatha/Churna). Barred under Sec 3(p) as traditional knowledge.",
        "sec_3e_synergy_potential": "High when combined with Bacopa monnieri (Brahmi) or Piper longum (Pippali) for enhanced neuro-modulation / bioavailability, provided Combination Index < 1 is demonstrated.",
        "recommended_ip_strategy": "Purified standardized fraction or novel synergistic composition with comparative isobologram data, plus Trademark on brand formulation."
    },
    "curcumin": {
        "id": "curcumin",
        "common_name": "Turmeric / Haridra",
        "botanical_name": "Curcuma longa",
        "sanskrit_name": "हरिद्रा (Haridra)",
        "family": "Zingiberaceae",
        "classical_texts": ["Charaka Samhita (Chikitsa Sthana 21)", "Sushruta Samhita (Sutra Sthana 38)", "Ashtanga Hridaya (Uttaratantra)", "Bhavaprakasha (Haritakyadi Varga)"],
        "bioactives": ["Curcumin (Diferuloylmethane)", "Demethoxycurcumin", "Bisdemethoxycurcumin", "Ar-turmerone", "Curcuminoids (95% standard)"],
        "therapeutic_indications": ["Kushthaghna (Skin disorders)", "Vranaropana (Wound healing)", "Krimighna (Antimicrobial)", "Anti-inflammatory", "Hepatoprotective"],
        "gi_tag": "Erode Turmeric (Tamil Nadu - GI No. 444), Kandhamal Haldi (Odisha - GI No. 610), Waigaon Turmeric (Maharashtra)",
        "tkdl_entries": ["Landmark CSIR-USPTO Turmeric Revocation (US Patent 5,401,504 revoked via TKDL prior art)"],
        "nba_clearance_required": True,
        "nba_rationale": "Indian biological resource. Requires NBA clearance for foreign applicants or commercial IP.",
        "sec_3p_risk": "Extremely High for wound healing, cosmetic topical application, or general inflammation due to extensive TKDL prior art.",
        "sec_3e_synergy_potential": "Very High when co-formulated with Piperine (Bio-enhancer) or Phospholipid / Liposomal delivery systems overcoming low aqueous solubility.",
        "recommended_ip_strategy": "Novel bioavailability-enhancing nanocarrier formulation or specific non-obvious synergistic combo with non-herbal carrier."
    },
    "brahmi": {
        "id": "brahmi",
        "common_name": "Brahmi / Water Hyssop",
        "botanical_name": "Bacopa monnieri",
        "sanskrit_name": "ब्राह्मी (Brahmi)",
        "family": "Plantaginaceae",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 4/18 - Prajasthapana)", "Sushruta Samhita (Chikitsa Sthana 28)", "Bhavaprakasha", "API Vol 2"],
        "bioactives": ["Bacoside A", "Bacoside B", "Bacopaside I-XII", "Brahmine", "Herpestine"],
        "therapeutic_indications": ["Medhya Rasayana (Cognitive enhancer)", "Smritiprada (Memory improvement)", "Unmadahara (Neuropsychiatric support)", "Anxiolytic"],
        "gi_tag": "Widely distributed in Indian wetlands; indigenous sourcing requires ABS declaration.",
        "tkdl_entries": ["TKDL Reference: MA/108, RD/542 on memory improvement & mental tranquility."],
        "nba_clearance_required": True,
        "nba_rationale": "Requires NBA Section 6 approval for patent filing (Form III) or commercial bio-survey.",
        "sec_3p_risk": "High for generic memory enhancement or anxiety indications.",
        "sec_3e_synergy_potential": "High when combined with Shankhpushpi (Convolvulus pluricaulis) or Centella asiatica (Mandukaparni).",
        "recommended_ip_strategy": "Proprietary extract standardized to enriched Bacoside ratios with clinical cognitive scores or Process Patent for selective saponin isolation."
    },
    "tulsi": {
        "id": "tulsi",
        "common_name": "Holy Basil / Tulsi",
        "botanical_name": "Ocimum sanctum (Ocimum integrity)",
        "sanskrit_name": "तुलसी (Tulasi)",
        "family": "Lamiaceae",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 27)", "Sushruta Samhita (Sutra Sthana 38)", "Bhavaprakasha (Pushpa Varga)"],
        "bioactives": ["Eugenol", "Rosmarinic acid", "Ursolic acid", "Caryophyllene", "Apigenin"],
        "therapeutic_indications": ["Kaphaghna (Respiratory decongestant)", "Shwasahara (Anti-asthmatic)", "Hridya (Cardioprotective)", "Adaptogenic", "Antiviral"],
        "gi_tag": "Indigenous sacred plant across Indian agro-climatic zones.",
        "tkdl_entries": ["TKDL Ref: AK/112 on respiratory & fever formulations."],
        "nba_clearance_required": True,
        "nba_rationale": "Cultivated and wild bio-resource requiring NBA Form I/III for commercial IP.",
        "sec_3p_risk": "High for cough, cold, immune boosting, and respiratory teas.",
        "sec_3e_synergy_potential": "Moderate to High when paired with Zingiber officinale (Sunthi) and Piper nigrum (Maricha).",
        "recommended_ip_strategy": "Ayurveda-Aahar certification for herbal teas / nutraceuticals, or proprietary extraction process patent."
    },
    "guduchi": {
        "id": "guduchi",
        "common_name": "Giloy / Guduchi / Amrita",
        "botanical_name": "Tinospora cordifolia",
        "sanskrit_name": "गुडूची (Guduchi / Amrita)",
        "family": "Menispermaceae",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 4/16 - Vayasthapana)", "Sushruta Samhita (Sutra Sthana 38)", "Bhavaprakasha (Guduchyadi Varga)"],
        "bioactives": ["Tinosporide", "Cordifolioside A", "Berberine", "Palmatine", "Tinocordiside"],
        "therapeutic_indications": ["Jvarahara (Antipyretic)", "Rasayana (Immunomodulator)", "Pramehaghna (Anti-diabetic)", "Dhatuvardhaka"],
        "gi_tag": "Indigenous climber of Indian subcontinent.",
        "tkdl_entries": ["TKDL Reference: JA/901 on fever, metabolic disorders, and immune tonic."],
        "nba_clearance_required": True,
        "nba_rationale": "Mandates NBA Section 3 / Section 6 declaration for patent applications.",
        "sec_3p_risk": "Very High for immunity tonics (Satva / Ghanavati) without substantial technological modification.",
        "sec_3e_synergy_potential": "High in polyherbal combinations (e.g., Sanshamani Vati formulation equivalents).",
        "recommended_ip_strategy": "Section 3(e) synergistic adjuvant formulation for insulin sensitization or proprietary D&C Form 25D license."
    },
    "shatavari": {
        "id": "shatavari",
        "common_name": "Shatavari",
        "botanical_name": "Asparagus racemosus",
        "sanskrit_name": "शतावरी (Shatavari)",
        "family": "Asparagaceae",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 4/18 - Balya)", "Sushruta Samhita (Sutra Sthana 38)", "Bhavaprakasha"],
        "bioactives": ["Shatavarin I-IV", "Sarsasapogenin", "Diosgenin", "Asparagamine A", "Isoflavones"],
        "therapeutic_indications": ["Stanyajanana (Galactagogue)", "Rasayana (Female reproductive tonic)", "Vayasthapana (Anti-aging)", "Gastric ulcer protection"],
        "gi_tag": "Indigenous Himalayan and Deccan woodland species.",
        "tkdl_entries": ["TKDL Ref: MS/402 for lactation and hormonal balance."],
        "nba_clearance_required": True,
        "nba_rationale": "NBA Section 6 Form III mandatory before Indian or PCT patent grant.",
        "sec_3p_risk": "High for lactation enhancement or general vitality.",
        "sec_3e_synergy_potential": "High when combined with Ashwagandha or Yashtimadhu.",
        "recommended_ip_strategy": "Proprietary extract with standardized saponin fraction or Ayurveda-Aahar wellness beverage."
    },
    "triphala": {
        "id": "triphala",
        "common_name": "Triphala (Haritaki + Bibhitaki + Amalaki)",
        "botanical_name": "Terminalia chebula + Terminalia bellirica + Phyllanthus emblica",
        "sanskrit_name": "त्रिफला (Triphala)",
        "family": "Combretaceae & Phyllanthaceae",
        "classical_texts": ["Charaka Samhita (Chikitsa Sthana 1/3)", "Sushruta Samhita (Sutra Sthana 38/56)", "Ashtanga Hridaya (Uttaratantra 40)", "Sarangadhara Samhita"],
        "bioactives": ["Chebulagic acid", "Chebulinic acid", "Gallic acid", "Ellagic acid", "Ascorbic acid (Vitamin C)", "Corilagin"],
        "therapeutic_indications": ["Chakshushya (Ophthalmic tonic)", "Deepana-Pachana (Digestive)", "Virechana (Mild laxative)", "Rasayana (Antioxidant)", "Lekhaniya (Hypolipidemic)"],
        "gi_tag": "Contains Indian Gooseberry (Pratapgarh Amla - GI tag) and Chebulic Myrobalan.",
        "tkdl_entries": ["TKDL Core Reference: TK/101, RS/094, CD/320. One of the most documented Ayurvedic formulations in TKDL."],
        "nba_clearance_required": True,
        "nba_rationale": "Multi-resource Indian biological mixture requiring Section 6 ABS approval.",
        "sec_3p_risk": "100% Barred for traditional 1:1:1 Churna or Kwatha under Section 3(p) as public domain classical prior art.",
        "sec_3e_synergy_potential": "Synergy must be established against individual Chebula, Bellirica, and Emblica extracts under strict CI metrics.",
        "recommended_ip_strategy": "Novel sustained-release oral colon-delivery micro-pellets or pure process patent for high-potency tannin recovery."
    },
    "neem": {
        "id": "neem",
        "common_name": "Neem",
        "botanical_name": "Azadirachta indica",
        "sanskrit_name": "निम्ब (Nimba)",
        "family": "Meliaceae",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 27)", "Sushruta Samhita (Sutra Sthana 38)", "Bhavaprakasha"],
        "bioactives": ["Azadirachtin", "Nimbin", "Nimbidin", "Salannin", "Mahmoodin"],
        "therapeutic_indications": ["Kushthaghna (Dermatological)", "Krimighna (Pesticidal / Antimicrobial)", "Pramehaghna (Glycemic)", "Vranashodhana (Antiseptic)"],
        "gi_tag": "Indigenous tree across India.",
        "tkdl_entries": ["Historic EPO Patent EP0436257 (W.R. Grace) revoked following Indian Traditional Knowledge opposition."],
        "nba_clearance_required": True,
        "nba_rationale": "Requires NBA Form I/III clearance. SBB intimation mandatory for commercial processing.",
        "sec_3p_risk": "Extremely High for insecticidal, anti-fungal, dental (Datun), and skin applications.",
        "sec_3e_synergy_potential": "High for synergistic biopesticides with Karanja (Pongamia pinnata) or topical skin formulations with Haridra.",
        "recommended_ip_strategy": "Purified stabilized azadirachtin derivative or novel synthetic analog (not raw biological isolate)."
    },
    "pippali": {
        "id": "pippali",
        "common_name": "Long Pepper / Pippali",
        "botanical_name": "Piper longum",
        "sanskrit_name": "पिप्पली (Pippali)",
        "family": "Piperaceae",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 4/11 - Triptighna)", "Sushruta Samhita (Sutra Sthana 38)", "Bhavaprakasha"],
        "bioactives": ["Piperine", "Piperlongumine (Piplartine)", "Piperlonguminine", "Retrorefractamide"],
        "therapeutic_indications": ["Deepana (Digestive fire stimulant)", "Kaphahara (Mucolytic)", "Yogavahi (Bioavailability enhancer)", "Rasayana"],
        "gi_tag": "Assam / Meghalaya Long Pepper (Recognized geographical origin).",
        "tkdl_entries": ["TKDL Ref: TS/221 on Yogavahi bio-enhancing principles (Trikatu component)."],
        "nba_clearance_required": True,
        "nba_rationale": "Biological resource of India requiring NBA compliance.",
        "sec_3p_risk": "High for traditional Trikatu mixtures.",
        "sec_3e_synergy_potential": "Exceptional as a statutory Section 3(e) bio-enhancer that boosts pharmacokinetic Cmax/AUC of co-administered bioactives.",
        "recommended_ip_strategy": "Bioavailability enhancement composition patent with comparative pharmacokinetic AUC curve data."
    },
    "kalmegh": {
        "id": "kalmegh",
        "common_name": "Kalmegh / Green Chiretta",
        "botanical_name": "Andrographis paniculata",
        "sanskrit_name": "कालमेघ / भूनिम्ब (Kalamegha / Bhunimba)",
        "family": "Acanthaceae",
        "classical_texts": ["Bhavaprakasha (Guduchyadi Varga)", "Ayurvedic Pharmacopoeia of India (API Vol 2)"],
        "bioactives": ["Andrographolide", "Neoandrographolide", "14-Deoxy-11,12-didehydroandrographolide", "Andrographanin"],
        "therapeutic_indications": ["Yakrit-Plihodara (Hepatoprotective)", "Jvarahara (Antipyretic)", "Krimighna (Antiparasitic)", "Immune enhancer"],
        "gi_tag": "Indigenous across Central and Southern India.",
        "tkdl_entries": ["TKDL Reference: KL/410 for liver disorders and bitter tonic."],
        "nba_clearance_required": True,
        "nba_rationale": "Mandates NBA Section 6 approval before Indian patent grant.",
        "sec_3p_risk": "High for hepatitis and viral fever formulations.",
        "sec_3e_synergy_potential": "High when combined with Katuki (Picrorhiza kurroa) or Bhumyamalaki (Phyllanthus niruri).",
        "recommended_ip_strategy": "Phytopharmaceutical Drug (CDSCO Chapter IV-A / Form 44) with purified diterpene lactone fraction."
    }
}

# Graph Node & Edge Structure for Visualizer & Pathfinding
def get_herb_catalog() -> List[Dict[str, Any]]:
    """Return all available Ayurvedic botanicals in the knowledge graph."""
    return list(HERB_ONTOLOGY.values())

def lookup_herb(herb_query: str) -> Optional[Dict[str, Any]]:
    """Lookup a single herb by common, botanical, or sanskrit name."""
    query_lower = herb_query.lower().strip()
    for key, data in HERB_ONTOLOGY.items():
        if (key in query_lower or 
            data["common_name"].lower() in query_lower or 
            data["botanical_name"].lower() in query_lower or 
            herb_query in data["sanskrit_name"]):
            return data
    return None

def compute_multi_herb_pathway(herb_ids: List[str], target_ip: str = "patent", jurisdiction: str = "india") -> Dict[str, Any]:
    """
    Dynamic Multi-Hop Regulatory Pathfinding for multi-herb formulations.
    Traverses:
    [Herb Nodes] -> [First Schedule Texts] -> [Statutory Bars: Sec 3(p), 3(e), 3(j)]
                 -> [ABS Clearance: NBA Form I / III] -> [Filing Strategy]
    """
    matched_herbs: List[Dict[str, Any]] = []
    for hid in herb_ids:
        clean_id = hid.lower().strip()
        if clean_id in HERB_ONTOLOGY:
            matched_herbs.append(HERB_ONTOLOGY[clean_id])
        else:
            found = lookup_herb(clean_id)
            if found:
                matched_herbs.append(found)

    if not matched_herbs:
        # Fallback to default popular combo if none found
        matched_herbs = [HERB_ONTOLOGY["ashwagandha"], HERB_ONTOLOGY["curcumin"]]

    nodes = []
    edges = []

    # 1. Add Herb Nodes
    all_texts = set()
    all_bioactives = set()
    nba_required = False
    high_sec3p_risk = False
    gi_tags = []

    for idx, herb in enumerate(matched_herbs):
        node_id = f"herb_{herb['id']}"
        nodes.append({
            "id": node_id,
            "label": herb["common_name"],
            "sublabel": herb["botanical_name"],
            "type": "herb",
            "color": "#10b981", # Emerald
            "details": {
                "sanskrit": herb["sanskrit_name"],
                "family": herb["family"],
                "indications": herb["therapeutic_indications"]
            }
        })

        if herb["nba_clearance_required"]:
            nba_required = True
        if "High" in herb["sec_3p_risk"]:
            high_sec3p_risk = True
        if herb.get("gi_tag"):
            gi_tags.append({"herb": herb["common_name"], "gi": herb["gi_tag"]})

        # Add Classical Text Nodes & Edges
        for text in herb["classical_texts"]:
            text_id = f"text_{abs(hash(text)) % 10000}"
            all_texts.add((text_id, text))
            edges.append({
                "source": node_id,
                "target": text_id,
                "label": "MENTIONED_IN",
                "color": "#8b5cf6"
            })

        # Add Bioactive Nodes & Edges
        for bio in herb["bioactives"][:2]: # top 2
            bio_id = f"bio_{abs(hash(bio)) % 10000}"
            all_bioactives.add((bio_id, bio))
            edges.append({
                "source": node_id,
                "target": bio_id,
                "label": "CONTAINS_BIOACTIVE",
                "color": "#06b6d4"
            })

    # Add Text Nodes
    for text_id, text_label in all_texts:
        nodes.append({
            "id": text_id,
            "label": text_label.split(" (")[0],
            "sublabel": text_label,
            "type": "classical_text",
            "color": "#8b5cf6", # Purple
            "details": {"source": text_label}
        })

    # Add Bioactive Nodes
    for bio_id, bio_label in all_bioactives:
        nodes.append({
            "id": bio_id,
            "label": bio_label,
            "sublabel": "Phytoconstituent",
            "type": "bioactive",
            "color": "#06b6d4", # Cyan
            "details": {"compound": bio_label}
        })

    # 2. Add Statutory Bar Nodes (Sec 3(p), Sec 3(e), Sec 3(j))
    nodes.append({
        "id": "statute_sec3p",
        "label": "Section 3(p) Bar",
        "sublabel": "Patents Act 1970: Traditional Knowledge Bar",
        "type": "statutory_bar",
        "color": "#ef4444" if high_sec3p_risk else "#f59e0b",
        "details": {
            "law": "Indian Patents Act 1970 Section 3(p)",
            "impact": "Claims covering traditional use or mere duplication of First Schedule classical texts are strictly non-patentable."
        }
    })

    nodes.append({
        "id": "statute_sec3e",
        "label": "Section 3(e) Synergism Gate",
        "sublabel": "Mere Admixture vs Synergistic Efficacy",
        "type": "statutory_bar",
        "color": "#3b82f6",
        "details": {
            "law": "Indian Patents Act 1970 Section 3(e)",
            "impact": "Requires proof that multi-herb combination yields unexpected synergistic efficacy (Combination Index < 1) beyond additive sum of parts."
        }
    })

    # 3. Add Regulatory Approval Nodes (NBA Form I/III, D&C Act, FSSAI)
    nodes.append({
        "id": "nba_abs",
        "label": "NBA ABS Clearance",
        "sublabel": "Biological Diversity Act 2023 (Sec 6)",
        "type": "regulatory_mandate",
        "color": "#f97316", # Orange
        "details": {
            "forms": "Form I (Commercial Utilization) / Form III (Patent Application Approval)",
            "authority": "National Biodiversity Authority (Chennai) / State Biodiversity Boards"
        }
    })

    # Connect texts to Section 3(p)
    for text_id, _ in all_texts:
        edges.append({
            "source": text_id,
            "target": "statute_sec3p",
            "label": "TRIGGERS_TK_BAR",
            "color": "#ef4444"
        })

    # Connect herbs to Section 3(e)
    for herb in matched_herbs:
        edges.append({
            "source": f"herb_{herb['id']}",
            "target": "statute_sec3e",
            "label": "REQUIRES_SYNERGY_PROOF",
            "color": "#3b82f6"
        })
        if nba_required:
            edges.append({
                "source": f"herb_{herb['id']}",
                "target": "nba_abs",
                "label": "MANDATES_ABS_FORM_III",
                "color": "#f97316"
            })

    # 4. Synthesize Legal Decision Path
    is_multi_herb = len(matched_herbs) > 1
    pathway_summary = {
        "formulation_type": "Polyherbal Formulation" if is_multi_herb else "Single Botanical Extract",
        "herbs_analyzed": [h["common_name"] for h in matched_herbs],
        "sec_3p_tk_risk": "High" if high_sec3p_risk else "Medium",
        "sec_3e_synergy_mandate": "MANDATORY" if is_multi_herb else "NOT_APPLICABLE (Single Herb)",
        "nba_approval_required": nba_required,
        "nba_form": "Form III (Approval for Patent Application) under BDA 2023 Sec 6",
        "gi_opportunities": gi_tags,
        "recommended_path": (
            "1. File NBA Form III prior to Patent grant.\n"
            "2. Conduct in-vitro / in-vivo comparative synergy experiments (Combination Index CI < 1.0) to overcome Patents Act Section 3(e).\n"
            "3. Draft claims focused on purified standardized fractions or proprietary delivery matrix to avoid Section 3(p) TKDL revocation.\n"
            "4. File Trademark for brand protection under Trade Marks Act 1999."
        )
    }

    return {
        "nodes": nodes,
        "edges": edges,
        "pathway_summary": pathway_summary,
        "matched_herbs": matched_herbs
    }

def evaluate_section_3e_synergy(
    herb_names: List[str],
    extraction_method: str = "Hydroalcoholic Standardized Extract",
    therapeutic_claim: str = "Anti-inflammatory and Neuroprotective",
    has_experimental_data: bool = False,
    combination_index: Optional[float] = None
) -> Dict[str, Any]:
    """
    Automated Section 3(e) Synergistic Evidence & Novelty Assessment Analyzer.
    Provides rigorous patentability risk assessment for Ayurvedic multi-herb formulations.
    """
    matched_herbs = []
    for name in herb_names:
        herb = lookup_herb(name)
        if herb:
            matched_herbs.append(herb)

    # Calculate statutory risk scores (0-100)
    sec_3p_score = 85 if any("High" in h["sec_3p_risk"] for h in matched_herbs) else 45
    sec_3e_score = 90 if (len(matched_herbs) > 1 and not has_experimental_data) else (20 if combination_index and combination_index < 0.9 else 65)
    sec_3j_score = 75 if "whole plant" in extraction_method.lower() else 30
    nba_score = 95 if len(matched_herbs) > 0 else 0

    # Determine patentability status
    if has_experimental_data and combination_index and combination_index < 0.85:
        patentability_verdict = "FAVORABLE (Strong Synergistic Defense under Sec 3(e))"
        verdict_color = "emerald"
    elif has_experimental_data and combination_index and combination_index >= 1.0:
        patentability_verdict = "HIGH RISK OF REJECTION (Antagonistic / Purely Additive Admixture under Sec 3(e))"
        verdict_color = "red"
    else:
        patentability_verdict = "EVIDENCE DEFICIT (Action Required: Generate Comparative Synergy Data)"
        verdict_color = "amber"

    # Prescribed Experimental Protocol
    protocol_steps = [
        {
            "step": "1. Single-Herb Baseline Quantification",
            "description": "Determine ED50 / IC50 values for each individual herbal extract independently across biological target assays."
        },
        {
            "step": "2. Chou-Talalay Combination Index (CI) Calculation",
            "description": "Calculate CI = (D1 / Dx1) + (D2 / Dx2). CI < 1.0 proves synergism, CI = 1.0 indicates additive effect (barred under Sec 3(e)), CI > 1.0 indicates antagonism."
        },
        {
            "step": "3. Isobologram Analysis Plotting",
            "description": "Plot experimental combination data points below the additive isobole line to submit as technical evidence in Patent Form 1 reply to FER."
        },
        {
            "step": "4. Bioactive Fingerprinting (HPTLC / HPLC-MS)",
            "description": "Establish chromatographic fingerprint showing stable phytoconstituent ratios to establish reproducibility."
        }
    ]

    return {
        "herbs_evaluated": [h["common_name"] for h in matched_herbs] if matched_herbs else herb_names,
        "therapeutic_claim": therapeutic_claim,
        "extraction_method": extraction_method,
        "patentability_verdict": patentability_verdict,
        "verdict_color": verdict_color,
        "risk_radar": {
            "sec_3p_traditional_knowledge_risk": sec_3p_score,
            "sec_3e_mere_admixture_risk": sec_3e_score,
            "sec_3j_biological_substance_risk": sec_3j_score,
            "nba_abs_clearance_mandate": nba_score
        },
        "recommended_ip_filing_route": (
            "Proprietary Ayurvedic Medicine License (Form 25D under D&C Act) + "
            "Section 48 Process Patent (Selective Extraction Technology) + "
            "Trademark Registration on Brand Name."
        ),
        "protocol_steps": protocol_steps
    }
