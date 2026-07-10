"""Educational content about fuzzy logic in English, Hindi, and Marathi."""

FUZZY_LOGIC_ARCHITECTURE_DIAGRAM = """
        ┌─────────────────────────────────────────────────────┐
        │              FUZZY LOGIC SYSTEM                      │
        │                                                      │
        │              ┌──────────┐                            │
        │              │  Rules   │  (IF-THEN knowledge base)  │
        │              └────┬─────┘                            │
        │                   │                                  │
  Crisp │    ┌──────────┐   │   ┌──────────────┐   ┌──────────┐ │  Crisp
  Input├───▶│Fuzzifier │───┼──▶│ Intelligence │──▶│Defuzzifier├──▶│ Output
        │    └──────────┘   │   │  (Inference) │   └──────────┘ │
        │         │         │   └──────────────┘         ▲       │
        │         │ Fuzzy   │         ▲                  │       │
        │         │ Input   │    Fuzzy Output            │       │
        │         │ Set     │       Set                  │       │
        │         └─────────┘         └──────────────────┘       │
        └─────────────────────────────────────────────────────┘

  1. Crisp Input   → exact sensor/value (e.g. temperature 28°C)
  2. Fuzzifier     → converts to fuzzy sets (Hot:0.6, Warm:0.4)
  3. Rules         → expert IF-THEN rules (IF Hot THEN Fan Fast)
  4. Intelligence  → inference engine applies rules to fuzzy input
  5. Defuzzifier   → converts fuzzy output to crisp number (fan 72%)
  6. Crisp Output  → actionable result for actuator/controller
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
            "Here is the fuzzy logic system architecture. "
            "Crisp Input enters the Fuzzifier which converts exact values into fuzzy sets. "
            "Rules from the knowledge base define IF-THEN logic. "
            "The Intelligence block is the inference engine that applies rules to fuzzy input. "
            "The Defuzzifier converts the fuzzy output set back to a Crisp Output. "
            "See the diagram on screen — Rules, Fuzzifier, Intelligence, and Defuzzifier."
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
            "यह है फ़ज़ी लॉजिक सिस्टम का आर्किटेक्चर। "
            "Crisp Input Fuzzifier में जाता है जो exact values को fuzzy sets में बदलता है। "
            "Rules knowledge base से IF-THEN logic देते हैं। "
            "Intelligence inference engine है जो rules को fuzzy input पर लगाता है। "
            "Defuzzifier fuzzy output को Crisp Output में बदलता है। "
            "स्क्रीन पर diagram देखें — Rules, Fuzzifier, Intelligence, Defuzzifier।"
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
            "हे आहे फझी लॉजिक सिस्टमचे आर्किटेक्चर. "
            "Crisp Input Fuzzifier मध्ये जातो जो exact values ला fuzzy sets मध्ये रूपांतरित करतो. "
            "Rules knowledge base मधून IF-THEN logic देतात. "
            "Intelligence हा inference engine आहे. "
            "Defuzzifier fuzzy output ला Crisp Output मध्ये बदलतो. "
            "स्क्रीनवर diagram पहा — Rules, Fuzzifier, Intelligence, Defuzzifier."
        ),
    },
}


def get_topic(lang, topic):
    lang = lang if lang in CONTENT else "en"
    return CONTENT[lang].get(topic, CONTENT["en"].get(topic, ""))
