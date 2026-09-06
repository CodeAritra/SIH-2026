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

INDIC_PHRASES = {
    "hi": {
        "Based on": "के आधार पर",
        "legal framework for": "के लिए विधिक ढाँचा",
        "Under": "के अंतर्गत",
        "Note: Ensure full compliance with State Licensing Authorities and National Biodiversity Authority protocols prior to commercial dispatch.": "सूचना: वाणिज्यिक प्रेषण से पूर्व राज्य लाइसेंसिंग प्राधिकरणों और राष्ट्रीय जैव विविधता प्राधिकरण के नियमों का पूर्ण अनुपालन सुनिश्चित करें।",
        "This is informational guidance, not legal advice.": "यह केवल सूचनात्मक मार्गदर्शन है, विधिक सलाह नहीं।",
        "I don't have a grounded source in the current legal/regulatory corpus to answer this question accurately.": "सटीक उत्तर देने के लिए वर्तमान वैधानिक संदर्भ में पर्याप्त आधार उपलब्ध नहीं है।",
        "To prevent legal misguidance, I am withholding an answer.": "विधिक भ्रांति से बचने के लिए, मैं उत्तर रोक रहा हूँ।",
        "Please consider using the 'Escalate to Expert' option below to submit your query to Ayush & IP regulatory advisors.": "कृपया अपने प्रश्न को आयुष एवं आईपी सलाहकारों के समक्ष प्रस्तुत करने के लिए नीचे 'विशेषज्ञ को अग्रेषित करें' विकल्प का उपयोग करें।"
    },
    "bn": {
        "Based on": "ভিত্তিতে",
        "legal framework for": "এর জন্য আইনি কাঠামো",
        "Under": "অধীনে",
        "Note: Ensure full compliance with State Licensing Authorities and National Biodiversity Authority protocols prior to commercial dispatch.": "দ্রষ্টব্য: বাণিজ্যিক প্রেরণের আগে রাজ্য লাইসেন্সিং কর্তৃপক্ষ এবং জাতীয় জীববৈচিত্র্য কর্তৃপক্ষের প্রোটোকল সম্পূর্ণ মেনে চলা নিশ্চিত করুন।",
        "This is informational guidance, not legal advice.": "এটি কেবল তথ্যমূলক নির্দেশিকা, আইনি পরামর্শ নয়।",
        "I don't have a grounded source in the current legal/regulatory corpus to answer this question accurately.": "এই প্রশ্নের সঠিক উত্তর দেওয়ার জন্য বর্তমান আইনি তথ্যে পর্যাপ্ত উৎস নেই।",
        "To prevent legal misguidance, I am withholding an answer.": "আইনি বিভ্রান্তি এড়াতে আমি উত্তর প্রদান থেকে বিরত থাকছি।"
    },
    "ta": {
        "Based on": "அடிப்படையில்",
        "legal framework for": "க்கான சட்ட கட்டமைப்பு",
        "Under": "இன் கீழ்",
        "Note: Ensure full compliance with State Licensing Authorities and National Biodiversity Authority protocols prior to commercial dispatch.": "குறிப்பு: வணிக விநியோகத்திற்கு முன் மாநில உரிம அதிகாரிகள் மற்றும் தேசிய பல்லுயிர் ஆணைய நெறிமுறைகளை முழுமையாக பின்பற்றுவதை உறுதிசெய்யவும்.",
        "This is informational guidance, not legal advice.": "இது தகவல் வழிகாட்டுதல் மட்டுமே, சட்ட ஆலோசனை அல்ல.",
        "I don't have a grounded source in the current legal/regulatory corpus to answer this question accurately.": "இந்த கேள்விக்கு துல்லியமாக பதிலளிக்க போதுமான சட்ட சான்றுகள் கிடைக்கவில்லை.",
        "To prevent legal misguidance, I am withholding an answer.": "சட்ட ரீதியான தவறான வழிகாட்டுதலைத் தவிர்க்க நான் பதிலை நிறுத்தி வைக்கிறேன்."
    },
    "mr": {
        "Based on": "च्या आधारे",
        "legal framework for": "साठी कायदेशीर चौकट",
        "Under": "च्या अंतर्गत",
        "Note: Ensure full compliance with State Licensing Authorities and National Biodiversity Authority protocols prior to commercial dispatch.": "टीप: व्यावसायिक वितरणापूर्वी राज्य परवाना प्राधिकरण आणि राष्ट्रीय जैवविविधता प्राधिकरणाच्या नियमांचे पूर्ण पालन सुनिश्चित करा.",
        "This is informational guidance, not legal advice.": "हे केवळ माहितीपर मार्गदर्शन आहे, कायदेशीर सल्ला नाही.",
        "I don't have a grounded source in the current legal/regulatory corpus to answer this question accurately.": "या प्रश्नाचे अचूक उत्तर देण्यासाठी सध्याच्या कायदेशीर संदर्भात पुरेसे पुरावे उपलब्ध नाहीत.",
        "To prevent legal misguidance, I am withholding an answer.": "कायदेशीर गैरसमज टाळण्यासाठी मी उत्तर रोखत आहे."
    }
}

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
    if api_key:
        try:
            from langchain_groq import ChatGroq
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.output_parsers import StrOutputParser

            candidate_models = [
                os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                "llama-3.1-8b-instant",
                "llama3-70b-8192"
            ]

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

            for model_name in candidate_models:
                try:
                    llm = ChatGroq(
                        temperature=0.0,
                        model_name=model_name,
                        groq_api_key=api_key,
                        max_tokens=1500
                    )
                    chain = prompt | llm | StrOutputParser()
                    translated = chain.invoke({"input_text": text})
                    if translated and len(translated.strip()) > 10:
                        return translated.strip()
                except Exception:
                    continue
        except Exception:
            pass

    # Offline dictionary-based phrase translation fallback
    translated_text = text
    dict_map = INDIC_PHRASES.get(target_lang, {})
    for en_phrase, indic_phrase in dict_map.items():
        translated_text = translated_text.replace(en_phrase, indic_phrase)

    return translated_text
