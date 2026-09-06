"""
Bhashini Indic Multilingual Localization Engine (Phase 3).
Provides multi-lingual query translation and localized answers across 10+ Indian languages
while preserving critical Ayush terminology, statutory sections, and legal grounding.
"""

import os
from typing import Dict, Any, Optional

SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "native": "English", "code": "en"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "code": "hi"},
    "bn": {"name": "Bengali", "native": "বাংলা", "code": "bn"},
    "ta": {"name": "Tamil", "native": "தமிழ்", "code": "ta"},
    "te": {"name": "Telugu", "native": "తెలుగు", "code": "te"},
    "mr": {"name": "Marathi", "native": "मराठी", "code": "mr"},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી", "code": "gu"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "code": "kn"},
    "ml": {"name": "Malayalam", "native": "മലയാളം", "code": "ml"},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "code": "pa"},
    "or": {"name": "Odia", "native": "ଓଡ଼ିଆ", "code": "or"}
}

# Key UI Translations for Indian Languages
UI_DICTIONARY = {
    "hi": {
        "title": "आईपी-शक्ति सहायक",
        "subtitle": "आयुर्वेदिक बौद्धिक संपदा और नियामक निर्णय समर्थन प्रणाली",
        "disclaimer": "यह केवल सूचनात्मक मार्गदर्शन है, कानूनी सलाह नहीं।",
        "placeholder": "आयुर्वेदिक पेटेंट, TKDL, जैव विविधता अधिनियम या FSSAI के बारे में पूछें...",
        "india_toggle": "भारत (घरेलू)",
        "intl_toggle": "अंतर्राष्ट्रीय (WIPO / निर्यात)",
        "knowledge_graph": "ज्ञान ग्राफ एवं मार्ग",
        "synergy_checker": "धारा 3(e) तालमेल विश्लेषक",
        "dpdp_audit": "DPDP ऑडिट एवं प्रमाण पत्र",
        "high_confidence": "उच्च विश्वसनीयता",
        "medium_confidence": "मध्यम विश्वसनीयता",
        "abstention_notice": "सटीक वैधानिक ग्राउंडिंग के अभाव में सुरक्षित उत्तर अस्वीकृति।"
    },
    "bn": {
        "title": "আইপি-শক্তি সহায়ক",
        "subtitle": "আয়ুর্বেদিক মেধা সম্পদ ও নিয়ন্ত্রক সিদ্ধান্ত সহায়তা ব্যবস্থা",
        "disclaimer": "এটি কেবল তথ্যগত নির্দেশিকা, আইনি পরামর্শ নয়।",
        "placeholder": "আয়ুর্বেদিক পেটেন্ট, TKDL, জৈব বৈচিত্র্য আইন বা FSSAI সম্পর্কে জিজ্ঞাসা করুন...",
        "india_toggle": "ভারত (অভ্যন্তরীণ)",
        "intl_toggle": "আন্তর্জাতিক (WIPO / রপ্তানি)",
        "knowledge_graph": "জ্ঞান গ্রাফ ও পথ",
        "synergy_checker": "ধারা 3(e) সমন্বয় বিশ্লেষক",
        "dpdp_audit": "DPDP অডিট ও সার্টিফিকেট",
        "high_confidence": "উচ্চ বিশ্বাসযোগ্যতা",
        "medium_confidence": "মাঝারি বিশ্বাসযোগ্যতা",
        "abstention_notice": "সঠিক বিধিবদ্ধ তথ্যের অনুপস্থিতিতে নিরাপদ অস্বীকৃতি।"
    },
    "ta": {
        "title": "ஐபி-சக்தி சஹாயக்",
        "subtitle": "ஆயுர்வேத அறிவுசார் சொத்து & ஒழுங்குமுறை வழிகாட்டுதல்",
        "disclaimer": "இது தகவல் வழிகாட்டுதல் மட்டுமே, சட்ட ஆலோசனை அல்ல.",
        "placeholder": "ஆயுர்வேத காப்புரிமை, TKDL, பல்லுயிர் சட்டம் அல்லது FSSAI பற்றி கேட்கவும்...",
        "india_toggle": "இந்தியா (உள்நாட்டு)",
        "intl_toggle": "சர்வதேசம் (WIPO / ஏற்றுமதி)",
        "knowledge_graph": "அறிவு வரைபடம்",
        "synergy_checker": "பிரிவு 3(e) சினெர்ஜி ஆய்வாளர்",
        "dpdp_audit": "DPDP தணிக்கை மற்றும் சான்றிதழ்",
        "high_confidence": "உயர் நம்பகத்தன்மை",
        "medium_confidence": "நடுத்தர நம்பகத்தன்மை",
        "abstention_notice": "சட்டப்பூர்வ சான்றுகள் இல்லாததால் பாதுகாப்பான நிராகரிப்பு."
    },
    "te": {
        "title": "ఐపి-శక్తి సహాయక్",
        "subtitle": "ఆయుర్వేద మేధో సంపత్తి & నియంత్రణ నిర్ణయ మద్దతు వ్యవస్థ",
        "disclaimer": "ఇది కేవలం సమాచార మార్గదర్శకత్వం మాత్రమే, చట్టపరమైన సలహా కాదు.",
        "placeholder": "ఆయుర్వేద పేటెంట్లు, TKDL, జీవవైవిధ్య చట్టం లేదా FSSAI గురించి అడగండి...",
        "india_toggle": "భారతదేశం (దేశీయ)",
        "intl_toggle": "అంతర్జాతీయ (WIPO / ఎగుమతి)",
        "knowledge_graph": "జ్ఞాన గ్రాఫ్",
        "synergy_checker": "సెక్షన్ 3(e) సినర్జీ ఎనలైజర్",
        "dpdp_audit": "DPDP ఆడిట్ & సర్టిఫికేట్లు",
        "high_confidence": "అధిక విశ్వసనీయత",
        "medium_confidence": "మధ్యస్థ విశ్వసనీయత",
        "abstention_notice": "చట్టబద్ధమైన ఆధారం లేకపోవడం వల్ల సురక్షిత తిరస్కరణ."
    },
    "mr": {
        "title": "आयपी-शक्ती सहायक",
        "subtitle": "आयुर्वेदिक बौद्धिक संपदा आणि नियामक निर्णय समर्थन प्रणाली",
        "disclaimer": "हे केवळ माहितीपर मार्गदर्शन आहे, कायदेशीर सल्ला नाही.",
        "placeholder": "आयुर्वेदिक पेटेंट, TKDL, जैवविविधता कायदा किंवा FSSAI बद्दल विचारा...",
        "india_toggle": "भारत (अंतर्गत)",
        "intl_toggle": "आंतरराष्ट्रीय (WIPO / निर्यात)",
        "knowledge_graph": "ज्ञान आलेख आणि मार्ग",
        "synergy_checker": "कलम 3(e) सिनर्जी विश्लेषक",
        "dpdp_audit": "DPDP ऑडिट आणि प्रमाणपत्र",
        "high_confidence": "उच्च विश्वासार्हता",
        "medium_confidence": "मध्यम विश्वासार्हता",
        "abstention_notice": "योग्य वैधानिक पुराव्यांच्या अभावामुळे सुरक्षित नकार."
    },
    "gu": {
        "title": "આઈપી-શક્તિ સહાયક",
        "subtitle": "આયુર્વેદિક બૌદ્ધિક સંપદા અને નિયમનકારી નિર્ણય સહાય પ્રણાલી",
        "disclaimer": "આ માત્ર માહિતીપ્રદ માર્ગદર્શન છે, કાનૂની સલાહ નથી.",
        "placeholder": "આયુર્વેદિક પેટન્ટ, TKDL, જૈવવિવિધતા અધિનિયમ અથવા FSSAI વિશે પૂછો...",
        "india_toggle": "ભારત (સ્થાનિક)",
        "intl_toggle": "આંતરરાષ્ટ્રીય (WIPO / નિકાસ)",
        "knowledge_graph": "જ્ઞાન આલેખ અને માર્ગો",
        "synergy_checker": "કલમ 3(e) સિનર્જી વિશ્લેષક",
        "dpdp_audit": "DPDP ઓડિટ અને પ્રમાણપત્ર",
        "high_confidence": "ઉચ્ચ વિશ્વસનીયતા",
        "medium_confidence": "મધ્યમ વિશ્વસનીયતા",
        "abstention_notice": "કાયદાકીય પુરાવાના અભાવે સુરક્ષિત અસ્વીકાર."
    }
}

def get_supported_languages() -> Dict[str, Dict[str, str]]:
    """Return dictionary of supported languages."""
    return SUPPORTED_LANGUAGES

def get_ui_translations(lang_code: str) -> Dict[str, str]:
    """Get translated UI labels for the requested language code."""
    return UI_DICTIONARY.get(lang_code, {})

def translate_indic_text(text: str, target_lang: str) -> str:
    """
    Translates text into the target Indic language using LLM with statutory preservation constraints.
    Preserves section references (e.g., Section 3(p), Section 3(e)), form names, and Sanskrit text titles.
    """
    if not text or target_lang == "en" or target_lang not in SUPPORTED_LANGUAGES:
        return text

    target_lang_name = SUPPORTED_LANGUAGES[target_lang]["name"]
    target_native_name = SUPPORTED_LANGUAGES[target_lang]["native"]

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return text

    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        llm = ChatGroq(
            temperature=0.0,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=api_key,
            max_tokens=1500
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an expert Indic legal translator specialized in Ministry of Ayush regulations and Indian Intellectual Property.\n"
                f"Translate the following text accurately into {target_lang_name} ({target_native_name}).\n\n"
                "CRITICAL CONSTRAINTS:\n"
                "1. Keep all legal citations, section numbers, and act titles EXACT (e.g. 'Section 3(p)', 'Section 3(e)', 'Patents Act 1970', 'Biological Diversity Act 2023', 'Form III', 'TKDL', 'FSSAI').\n"
                "2. Preserve classical Sanskrit terms in their standard Devanagari / regional transliteration (e.g. Charaka Samhita, Sushruta Samhita, Rasayana, Medhya).\n"
                "3. Ensure the tone is formal, authoritative, and natural in the target language.\n"
                "4. Output ONLY the translated text without introductory commentary."
            )),
            ("user", "{input_text}")
        ])

        chain = prompt | llm | StrOutputParser()
        translated = chain.invoke({"input_text": text})
        return translated.strip() if translated else text
    except Exception as e:
        # Fallback if langchain_groq is not available in environment
        return text
