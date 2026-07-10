"""Multilingual strings for English, Hindi, and Marathi."""

SUPPORTED = ("en", "hi", "mr")

TTS_LOCALE = {"en": "en-US", "hi": "hi-IN", "mr": "mr-IN"}
STT_LOCALE = {"en": "en_US", "hi": "hi_IN", "mr": "mr_IN"}

MESSAGES = {
    "en": {
        "ask_language": (
            "Welcome! I am your Fuzzy Logic voice tutor. "
            "Which language would you like? Say English, Hindi, or Marathi."
        ),
        "language_set": "Great! I will speak in English. You can ask me anything about fuzzy logic, or say 'start calculation' to compute fuzzy set operations.",
        "invalid_language": "Please say English, Hindi, or Marathi.",
        "help": (
            "Voice commands you can use: "
            "'start calculation' to begin fuzzy set math, "
            "'what is fuzzy logic' for an explanation, "
            "'fuzzy logic architecture diagram' for the fuzzy system diagram, "
            "'use cases' for real-life examples, "
            "'advantages and disadvantages', "
            "'next' during calculations, "
            "'stop' to stop speaking and listening, "
            "'change language' to switch English, Hindi, or Marathi, and "
            "'restart' to start over."
        ),
        "ask_count": "How many elements are in your universe of discourse?",
        "invalid_count": "Please tell me a whole number greater than zero.",
        "ask_universe": "What is the name of element {n}?",
        "empty_name": "I did not catch a name. Please say the element name.",
        "ask_a": "On a scale of 0 to 1, what is the membership value of {x} in Set A?",
        "ask_b": "What is the membership value of {x} in Set B?",
        "invalid_membership": "Please give a number between 0 and 1, for example 0.7.",
        "ready_explain": (
            "Perfect! Fuzzy Set A equals {setA}. Fuzzy Set B equals {setB}. "
            "Say 'next' and I will explain each fuzzy operation one at a time."
        ),
        "say_next": "Say 'next' when you are ready for the next operation.",
        "all_done": "That is all nine operations! Say 'restart' to try new numbers, or ask me any fuzzy logic question.",
        "restart": "Starting fresh! How many elements are in your universe?",
        "session_lost": "Session not found. Please restart the app.",
        "confused": "Sorry, I got confused. Say 'help' for commands or 'restart' to start over.",
        "qa_ack": "Here is what I know:",
        "start_calc": "Let's begin the fuzzy set calculation.",
        "stopped": "Stopped. Say 'help' when you need me, or tap the mic to speak again.",
        "change_language": "Sure! Which language would you like? Say English, Hindi, or Marathi.",
        "session_recovered": "Connection was refreshed. Please continue.",
    },
    "hi": {
        "ask_language": (
            "नमस्ते! मैं आपका फ़ज़ी लॉजिक वॉइस ट्यूटर हूँ। "
            "आप किस भाषा में बात करना चाहेंगे? कहें — English, Hindi, या Marathi।"
        ),
        "language_set": (
            "बढ़िया! अब मैं हिंदी में बात करूँगा। "
            "आप फ़ज़ी लॉजिक के बारे में कुछ भी पूछ सकते हैं, "
            "या 'गणना शुरू करो' कहकर फ़ज़ी सेट ऑपरेशन शुरू करें।"
        ),
        "invalid_language": "कृपया English, Hindi, या Marathi में से एक भाषा बताएं।",
        "help": (
            "आप ये वॉइस कमांड इस्तेमाल कर सकते हैं: "
            "'गणना शुरू करो' — फ़ज़ी सेट गणना, "
            "'फ़ज़ी लॉजिक क्या है' — समझाने के लिए, "
            "'फ़ज़ी लॉजिक आर्किटेक्चर' — फ़ज़ी सिस्टम डायग्राम, "
            "'उपयोग के उदाहरण', 'फायदे और नुकसान', "
            "'अगला' — अगला ऑपरेशन, "
            "'रुको' — बोलना बंद करने के लिए, "
            "'भाषा बदलो' — English/Hindi/Marathi, "
            "'फिर से शुरू' — नए सिरे से।"
        ),
        "ask_count": "आपके यूनिवर्स में कितने एलिमेंट हैं?",
        "invalid_count": "कृपया शून्य से बड़ी कोई पूर्ण संख्या बताएं।",
        "ask_universe": "एलिमेंट {n} का नाम क्या है?",
        "empty_name": "नाम सुनाई नहीं दिया। कृपया एलिमेंट का नाम बताएं।",
        "ask_a": "0 से 1 के बीच, सेट A में {x} की मेंबरशिप वैल्यू क्या है?",
        "ask_b": "सेट B में {x} की मेंबरशिप वैल्यू क्या है?",
        "invalid_membership": "कृपया 0 और 1 के बीच कोई संख्या दें, जैसे 0.7।",
        "ready_explain": (
            "बढ़िया! फ़ज़ी सेट A बराबर {setA}। फ़ज़ी सेट B बराबर {setB}। "
            "'अगला' कहें और मैं हर ऑपरेशन एक-एक करके समझाऊँगा।"
        ),
        "say_next": "अगला ऑपरेशन सुनने के लिए 'अगला' कहें।",
        "all_done": (
            "सभी नौ ऑपरेशन पूरे! नई गणना के लिए 'फिर से शुरू' कहें, "
            "या फ़ज़ी लॉजिक के बारे में कुछ भी पूछें।"
        ),
        "restart": "ठीक है, नए सिरे से शुरू करते हैं! यूनिवर्स में कितने एलिमेंट हैं?",
        "session_lost": "सेशन नहीं मिला। कृपया ऐप दोबारा खोलें।",
        "confused": "माफ़ करें, समझ नहीं आया। 'मदद' कहें या 'फिर से शुरू' कहें।",
        "qa_ack": "यह रहा जवाब:",
        "start_calc": "चलिए फ़ज़ी सेट गणना शुरू करते हैं।",
        "stopped": "रुक गया। ज़रूरत हो तो 'मदद' कहें या माइक दबाएं।",
        "change_language": "ठीक है! कौन सी भाषा चाहिए? कहें — English, Hindi, या Marathi।",
        "session_recovered": "कनेक्शन रीफ़्रेश हो गया। कृपया जारी रखें।",
    },
    "mr": {
        "ask_language": (
            "नमस्कार! मी तुमचा फझी लॉजिक व्हॉइस ट्यूटर आहे. "
            "तुम्हाला कोणत्या भाषेत बोलायचे आहे? सांगा — English, Hindi, किंवा Marathi."
        ),
        "language_set": (
            "छान! आता मी मराठीत बोलेन. "
            "तुम्ही फझी लॉजिकबद्दल काहीही विचारू शकता, "
            "किंवा 'गणना सुरू करा' म्हणून फझी सेट ऑपरेशन्स सुरू करा."
        ),
        "invalid_language": "कृपया English, Hindi, किंवा Marathi पैकी एक भाषा सांगा.",
        "help": (
            "तुम्ही हे व्हॉइस कमांड वापरू शकता: "
            "'गणना सुरू करा', 'फझी लॉजिक म्हणजे काय', "
            "'फझी लॉजिक आर्किटेक्चर' — आकृतीसाठी, "
            "'वापराची उदाहरणे', 'फायदे आणि तोटे', "
            "'पुढे', 'थांब' — बोलणे थांबवण्यासाठी, "
            "'भाषा बदला' — English/Hindi/Marathi, "
            "'पुन्हा सुरू'."
        ),
        "ask_count": "तुमच्या युनिव्हर्समध्ये किती एलिमेंट्स आहेत?",
        "invalid_count": "कृपया शून्यापेक्षा मोठी पूर्ण संख्या सांगा.",
        "ask_universe": "एलिमेंट {n} चे नाव काय आहे?",
        "empty_name": "नाव ऐकू आले नाही. कृपया एलिमेंटचे नाव सांगा.",
        "ask_a": "0 ते 1 दरम्यान, सेट A मध्ये {x} ची मेंबरशिप व्हॅल्यू काय आहे?",
        "ask_b": "सेट B मध्ये {x} ची मेंबरशिप व्हॅल्यू काय आहे?",
        "invalid_membership": "कृपया 0 आणि 1 दरम्यान संख्या द्या, उदा. 0.7.",
        "ready_explain": (
            "उत्तम! फझी सेट A म्हणजे {setA}. फझी सेट B म्हणजे {setB}. "
            "'पुढे' म्हणा आणि मी प्रत्येक ऑपरेशन एक-एक करून सांगेन."
        ),
        "say_next": "पुढील ऑपरेशन ऐकण्यासाठी 'पुढे' म्हणा.",
        "all_done": (
            "सर्व नऊ ऑपरेशन्स पूर्ण! नवीन गणनेसाठी 'पुन्हा सुरू' म्हणा, "
            "किंवा फझी लॉजिकबद्दल काहीही विचारा."
        ),
        "restart": "ठीक आहे, नव्याने सुरू करूया! युनिव्हर्समध्ये किती एलिमेंट्स आहेत?",
        "session_lost": "सेशन सापडले नाही. कृपया अॅप पुन्हा उघडा.",
        "confused": "माफ करा, समजले नाही. 'मदत' म्हणा किंवा 'पुन्हा सुरू' म्हणा.",
        "qa_ack": "हे आहे उत्तर:",
        "start_calc": "चला फझी सेट गणना सुरू करूया.",
        "stopped": "थांबले. गरज असेल तर 'मदत' म्हणा किंवा माइक दाबा.",
        "change_language": "ठीक आहे! कोणती भाषा हवी? सांगा — English, Hindi, किंवा Marathi.",
        "session_recovered": "कनेक्शन रीफ्रेश झाले. कृपया पुढे चालू ठेवा.",
    },
}


def msg(lang, key, **kwargs):
    text = MESSAGES.get(lang, MESSAGES["en"]).get(key, MESSAGES["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text
