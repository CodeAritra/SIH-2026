"""
Formulation Classifier State Machine for IP-SAKTI Sahayak.
Deterministic rule-based decision tree for classifying Ayurvedic and herbal products.
"""

from typing import Dict, Any, List, Optional

CLASSIFIER_QUESTIONS = {
    "q1_base": {
        "id": "q1_base",
        "question": "To give you precise legal & IP guidance, please select the formulation basis of your product:",
        "options": [
            {
                "key": "classical",
                "label": "Classical Ayurvedic Text Formula",
                "desc": "Formulated strictly according to authoritative texts in 1st Schedule of Drugs & Cosmetics Act"
            },
            {
                "key": "patent_proprietary",
                "label": "Proprietary / Modern Ayurvedic Blend",
                "desc": "Traditional herbs in a novel ratio, modified extract form, or proprietary capsule/tablet"
            },
            {
                "key": "phytopharma",
                "label": "Purified Phytopharmaceutical Extract",
                "desc": "Purified, standardized botanical extract fraction for modern clinical development"
            },
            {
                "key": "food_wellness",
                "label": "Oral Food / Health Supplement",
                "desc": "Intended as an oral wellness product, health drink, or dietary supplement"
            },
            {
                "key": "topical_beauty",
                "label": "Topical Cosmetic / Skincare",
                "desc": "Intended for external embellishment, skincare, or cosmetic grooming"
            }
        ]
    },
    "q2_food": {
        "id": "q2_food",
        "question": "Is your food supplement prepared using ingredients listed in authoritative Ayurvedic books?",
        "options": [
            {"key": "yes", "label": "Yes, uses traditional Ayurvedic ingredients", "desc": "Complies with FSSAI Ayurveda-Aahar schedules"},
            {"key": "no", "label": "No, uses generic food/nutritional ingredients", "desc": "Standard food/dietary supplement"}
        ]
    },
    "q2_patent": {
        "id": "q2_patent",
        "question": "Does your formulation contain any synthetic novel chemical entity (NCE) or synthetic active ingredient?",
        "options": [
            {"key": "yes", "label": "Yes, combined with synthetic drugs", "desc": "Subject to New Drug regulatory approval"},
            {"key": "no", "label": "No, 100% botanical/herbal ingredients", "desc": "Ayurvedic Proprietary Medicine"}
        ]
    }
}

CATEGORIES = {
    "classical": "Classical Ayurvedic Formulation",
    "proprietary": "Proprietary Ayurvedic Medicine",
    "phytopharma": "Phytopharmaceutical Drug",
    "ayurveda_aahar": "Ayurveda-Aahar (Nutraceutical)",
    "general_food": "General Food / Dietary Supplement",
    "new_drug": "New Drug / Modern Pharmaceutical",
    "cosmetic": "Cosmetic Formulation"
}

def get_initial_question() -> Dict[str, Any]:
    return CLASSIFIER_QUESTIONS["q1_base"]

def process_classification_step(answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Evaluates current answers state machine.
    Returns either next question OR final classification.
    """
    q1 = answers.get("q1_base")
    if not q1:
        return {"status": "in_progress", "next_question": CLASSIFIER_QUESTIONS["q1_base"]}

    if q1 == "classical":
        return {
            "status": "completed",
            "category_key": "classical",
            "category_name": CATEGORIES["classical"],
            "summary": "Your product is a Classical Ayurvedic Formulation listed in authoritative texts."
        }
    elif q1 == "phytopharma":
        return {
            "status": "completed",
            "category_key": "phytopharma",
            "category_name": CATEGORIES["phytopharma"],
            "summary": "Your product is a Purified Phytopharmaceutical Drug requiring clinical trial proof."
        }
    elif q1 == "topical_beauty":
        return {
            "status": "completed",
            "category_key": "cosmetic",
            "category_name": CATEGORIES["cosmetic"],
            "summary": "Your product is classified as an Ayurvedic Cosmetic Product."
        }
    elif q1 == "food_wellness":
        q2 = answers.get("q2_food")
        if not q2:
            return {"status": "in_progress", "next_question": CLASSIFIER_QUESTIONS["q2_food"]}
        if q2 == "yes":
            return {
                "status": "completed",
                "category_key": "ayurveda_aahar",
                "category_name": CATEGORIES["ayurveda_aahar"],
                "summary": "Your product is classified under FSSAI Ayurveda-Aahar (Nutraceutical) rules."
            }
        else:
            return {
                "status": "completed",
                "category_key": "general_food",
                "category_name": CATEGORIES["general_food"],
                "summary": "Your product is a General Food/Dietary Supplement."
            }
    elif q1 == "patent_proprietary":
        q2 = answers.get("q2_patent")
        if not q2:
            return {"status": "in_progress", "next_question": CLASSIFIER_QUESTIONS["q2_patent"]}
        if q2 == "yes":
            return {
                "status": "completed",
                "category_key": "new_drug",
                "category_name": CATEGORIES["new_drug"],
                "summary": "Your product contains synthetic active entities and is classified as a New Drug."
            }
        else:
            return {
                "status": "completed",
                "category_key": "proprietary",
                "category_name": CATEGORIES["proprietary"],
                "summary": "Your product is classified as a Proprietary Ayurvedic Medicine."
            }

    return {"status": "in_progress", "next_question": CLASSIFIER_QUESTIONS["q1_base"]}

def is_classification_dependent(query: str) -> bool:
    """Detects if query requires formulation classification context to give accurate legal IP advice."""
    keywords = [
        "patent", "patentable", "can i patent", "ip protection", "ipr",
        "license", "approval", "ayush license", "fssai", "drug license",
        "register formulation", "classical text", "proprietary medicine",
        "phytopharmaceutical", "ayurveda aahar", "cosmetic"
    ]
    query_lower = query.lower()
    return any(k in query_lower for k in keywords)
