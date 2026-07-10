"""Educational content about fuzzy logic in English, Hindi, and Marathi."""

ARCHITECTURE_DIAGRAM = """
┌─────────────────────────────────────────────────────────────┐
│                    FLUTTER MOBILE APP                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Speech-to-  │  │ Text-to-    │  │  Chat UI + Formula  │  │
│  │ Text (Mic)  │  │ Speech      │  │  Cards + Diagrams   │  │
│  └──────┬──────┘  └──────▲──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          │ REST API (JSON)                   │
└──────────────────────────┼───────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              PYTHON FLASK BACKEND (Google Cloud)             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Conversation Manager (State Machine)        │   │
│  │  • Language selection (EN / HI / MR)                  │   │
│  │  • Voice command parsing                              │   │
│  │  • Q&A about fuzzy logic                              │   │
│  └────────┬─────────────────────────────┬───────────────┘   │
│           │                             │                    │
│           ▼                             ▼                    │
│  ┌─────────────────┐          ┌─────────────────────┐       │
│  │  fuzzy_logic.py │          │   knowledge.py      │       │
│  │  (Deterministic │          │   Explanations,     │       │
│  │   Math — 9 ops) │          │   Diagrams, Use Cases│       │
│  └─────────────────┘          └─────────────────────┘       │
└─────────────────────────────────────────────────────────────┘

FUZZY LOGIC CONCEPT FLOW:
  Crisp Input → Fuzzification → Fuzzy Rules → Inference → Defuzzification → Output

FUZZY SET OPERATIONS (this app):
  Universe U = {x1, x2, ...}
  Set A = { μA(x1)/x1 + μA(x2)/x2 + ... }
  Set B = { μB(x1)/x1 + μB(x2)/x2 + ... }
  Operations: Union, Intersection, Complement, Difference,
               Algebraic Sum/Product, Bounded Sum/Difference
"""

CONTENT = {
    "en": {
        "what_is_fuzzy_logic": (
            "Fuzzy logic is a form of many-valued logic where truth is not just "
            "true or false, but any value between 0 and 1. In classical sets, an "
            "element either belongs to a set or it does not. In fuzzy sets, an element "
            "has a membership degree — for example 0.7 means it belongs 70 percent. "
            "This models real-world uncertainty: weather can be partly cloudy, a person "
            "can be somewhat tall, or water can be warm but not hot. Fuzzy logic was "
            "introduced by Lotfi Zadeh in 1965. It powers washing machines, air "
            "conditioners, medical diagnosis systems, and traffic signal controllers."
        ),
        "use_cases": (
            "Real-life use cases of fuzzy logic: "
            "One, automatic washing machines that adjust water level and wash time based "
            "on how dirty clothes are. "
            "Two, air conditioners that smoothly control temperature instead of "
            "switching fully on or off. "
            "Three, anti-lock braking systems in cars that prevent wheel lock under "
            "varying road conditions. "
            "Four, medical expert systems that diagnose diseases from partial symptoms. "
            "Five, elevator controllers that optimize waiting time. "
            "Six, camera autofocus that handles blurry boundaries. "
            "Seven, stock market prediction using uncertain trends. "
            "Eight, agricultural irrigation systems that decide water amount from soil "
            "moisture and weather."
        ),
        "advantages_disadvantages": (
            "Advantages: Fuzzy logic handles uncertainty and imprecision naturally. "
            "It works with human language rules like 'if temperature is hot then fan "
            "is fast'. It does not need exact mathematical models. It is robust to "
            "noisy sensor data. Systems built with it are often easier to understand. "
            "Disadvantages: Results can be hard to verify mathematically. Rule design "
            "depends on expert knowledge and can be subjective. Computation can be "
            "slower than crisp logic for very large systems. It is not ideal when "
            "exact precision is legally or scientifically required. Combining many "
            "rules can become complex without careful design."
        ),
        "architecture_intro": (
            "Here is the architecture of this fuzzy logic tutor system. "
            "The Flutter app on your phone handles voice input and output. "
            "It sends your spoken words as text to the Python Flask backend on "
            "Google Cloud. The backend has a conversation manager that understands "
            "your language and voice commands. All fuzzy math is computed in pure "
            "Python so numbers are always correct. Educational answers come from a "
            "built-in knowledge base. See the diagram on screen for the full picture."
        ),
    },
    "hi": {
        "what_is_fuzzy_logic": (
            "फ़ज़ी लॉजिक एक बहु-मूल्य तर्क है जहाँ सच सिर्फ सही या गलत नहीं, "
            "बल्कि 0 और 1 के बीच कोई भी मान हो सकता है। क्लासिकल सेट में कोई एलिमेंट "
            "या तो सेट में होता है या नहीं। फ़ज़ी सेट में हर एलिमेंट की मेंबरशिप "
            "डिग्री होती है — जैसे 0.7 का मतलब 70 प्रतिशत सदस्यता। "
            "यह वास्तविक दुनिया की अनिश्चितता को मॉडल करता है: मौसम आंशिक रूप से "
            "बादल वाला हो सकता है, कोई व्यक्ति कुछ हद तक लंबा हो सकता है। "
            "फ़ज़ी लॉजिक को लॉटफ़ी ज़ादेह ने 1965 में प्रस्तुत किया। "
            "यह वॉशिंग मशीन, एसी, मेडिकल डायग्नोसिस और ट्रैफिक सिग्नल में इस्तेमाल होता है।"
        ),
        "use_cases": (
            "फ़ज़ी लॉजिक के वास्तविक उपयोग: "
            "एक, ऑटोमैटिक वॉशिंग मशीन जो कपड़ों की गंदगी के अनुसार पानी और समय तय करती है। "
            "दो, एयर कंडीशनर जो तापमान को धीरे-धीरे नियंत्रित करते हैं। "
            "तीन, कार में एंटी-लॉक ब्रेकिंग सिस्टम। "
            "चार, मेडिकल एक्सपर्ट सिस्टम जो आंशिक लक्षणों से बीमारी पहचानते हैं। "
            "पांच, लिफ्ट कंट्रोलर जो प्रतीक्षा समय कम करते हैं। "
            "छह, कैमरा ऑटोफोकस। "
            "सात, शेयर बाजार की अनिश्चित प्रवृत्तियों का विश्लेषण। "
            "आठ, कृषि सिंचाई जो मिट्टी की नमी और मौसम से पानी तय करती है।"
        ),
        "advantages_disadvantages": (
            "फायदे: फ़ज़ी लॉजिक अनिश्चितता और अस्पष्टता को स्वाभाविक रूप से संभालता है। "
            "यह मानव भाषा के नियमों से काम करता है जैसे 'अगर तापमान गर्म है तो पंखा तेज़'। "
            "इसे सटीक गणितीय मॉडल की ज़रूरत नहीं। शोर वाले सेंसर डेटा पर मजबूत है। "
            "नुकसान: परिणामों की गणितीय पुष्टि कठिन हो सकती है। "
            "नियम डिज़ाइन विशेषज्ञ ज्ञान पर निर्भर है। बड़े सिस्टम में गणना धीमी हो सकती है। "
            "जहाँ कानूनी या वैज्ञानिक सटीकता ज़रूरी है, वहाँ यह कम उपयुक्त है।"
        ),
        "architecture_intro": (
            "यह है इस फ़ज़ी लॉजिक ट्यूटर सिस्टम का आर्किटेक्चर। "
            "आपके फोन पर Flutter ऐप वॉइस इनपुट और आउटपुट संभालता है। "
            "यह Google Cloud पर Python Flask बैकएंड को टेक्स्ट भेजता है। "
            "बैकएंड में कन्वर्सेशन मैनेजर आपकी भाषा और वॉइस कमांड समझता है। "
            "सारी फ़ज़ी गणित pure Python में होती है ताकि संख्याएँ हमेशा सही रहें। "
            "स्क्रीन पर डायग्राम देखें।"
        ),
    },
    "mr": {
        "what_is_fuzzy_logic": (
            "फझी लॉजिक हा बहु-मूल्य तर्क आहे जिथे सत्य फक्त खरे किंवा खोटे नसते, "
            "तर 0 आणि 1 दरम्यान कोणतीही किंमत असू शकते. क्लासिकल सेटमध्ये एलिमेंट "
            "किंवा तर सेटमध्ये असतो किंवा नाही. फझी सेटमध्ये प्रत्येक एलिमेंटची "
            "मेंबरशिप डिग्री असते — उदा. 0.7 म्हणजे 70 टक्के सदस्यत्व. "
            "हे वास्तविक जगातील अनिश्चितता मॉडेल करते: हवामान अंशतः ढगाळ असू शकते, "
            "व्यक्ती काही प्रमाणात उंच असू शकते. फझी लॉजिक लॉटफी झादेह यांनी "
            "1965 मध्ये सादर केले. वॉशिंग मशीन, एसी, वैद्यकीय निदान आणि ट्रॅफिक सिग्नलमध्ये वापरले जाते."
        ),
        "use_cases": (
            "फझी लॉजिकची वास्तविक उदाहरणे: "
            "एक, ऑटोमॅटिक वॉशिंग मशीन जी कपड्यांच्या घाणीवर आधारित पाणी आणि वेळ ठरवते. "
            "दोन, एअर कंडिशनर जे तापमान हळूहळू नियंत्रित करतात. "
            "तीन, कारमधील अँटी-लॉक ब्रेकिंग सिस्टम. "
            "चार, वैद्यकीय एक्सपर्ट सिस्टम जी आंशिक लक्षणांवरून रोग ओळखतात. "
            "पाच, लिफ्ट कंट्रोलर जे प्रतीक्षा वेळ कमी करतात. "
            "सहा, कॅमेरा ऑटोफोकस. "
            "सात, शेअर बाजारातील अनिश्चित ट्रेंडचे विश्लेषण. "
            "आठ, शेती सिंचन जे मातीची ओलसरता आणि हवामानावरून पाणी ठरवते."
        ),
        "advantages_disadvantages": (
            "फायदे: फझी लॉजिक अनिश्चितता आणि अस्पष्टता नैसर्गिकरित्या हाताळते. "
            "ते मानवी भाषेतील नियमांसह काम करते जसे 'तापमान गरम असेल तर पंखा जलद'. "
            "याला अचूक गणितीय मॉडेलची गरज नाही. गोंगाट असलेल्या सेन्सर डेटावर मजबूत आहे. "
            "तोटे: निकालांची गणितीय पडताळणी कठीण असू शकते. "
            "नियम डिझाइन तज्ज्ञ ज्ञानावर अवलंबून आहे. मोठ्या सिस्टममध्ये गणना मंद असू शकते. "
            "जिथे कायदेशीर किंवा वैज्ञानिक अचूकता आवश्यक आहे तिथे कमी योग्य आहे."
        ),
        "architecture_intro": (
            "हे आहे या फझी लॉजिक ट्यूटर सिस्टमचे आर्किटेक्चर. "
            "तुमच्या फोनवरील Flutter अॅप व्हॉइस इनपुट आणि आउटपुट हाताळते. "
            "ते Google Cloud वरील Python Flask बॅकएंडला मजकूर पाठवते. "
            "बॅकएंडमध्ये कन्व्हर्सेशन मॅनेजर तुमची भाषा आणि व्हॉइस कमांड समजतो. "
            "सर्व फझी गणित pure Python मध्ये होते म्हणून संख्या नेहमी बरोबर असतात. "
            "स्क्रीनवरील आकृती पहा."
        ),
    },
}


def get_topic(lang, topic):
    lang = lang if lang in CONTENT else "en"
    return CONTENT[lang].get(topic, CONTENT["en"].get(topic, ""))
