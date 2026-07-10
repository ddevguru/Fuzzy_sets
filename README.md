# Fuzzy Logic Voice Tutor

Android voice app jo fuzzy set theory sikhata hai — **English, Hindi, aur Marathi** mein.

## Features

- **Language selection** — agent pehle puchta hai: English, Hindi, ya Marathi
- **Voice commands** — mic se baat karo, har jawab voice mein suno
- **Auto-listen** — agent bolna khatam karte hi mic khud chalu ho jata hai
- **Fuzzy set calculations** — 9 operations step-by-step (union, intersection, complement, etc.)
- **Educational Q&A** — pucho:
  - "fuzzy logic kya hai?"
  - "architecture diagram banao"
  - "use cases batao"
  - "advantages and disadvantages"
- **Architecture diagram** — screen par ASCII diagram dikhta hai

## Project Structure

```
fuzzy/
├── fuzzy_agent_backend/backend/     ← Python Flask API (Google Cloud par host karo)
│   ├── app.py
│   ├── conversation.py              ← language + voice commands + Q&A
│   ├── fuzzy_logic.py               ← deterministic math (9 operations)
│   ├── i18n.py                      ← EN / HI / MR translations
│   ├── knowledge.py                 ← fuzzy logic explanations + diagram
│   └── requirements.txt
├── fuzzy_agent_flutter/fuzzy_app_agent/  ← Flutter Android app
│   └── lib/
│       ├── screens/home_screen.dart
│       └── services/                ← STT, TTS, API
├── GCP_DEPLOY.md                    ← Google Cloud hosting steps (Hindi)
└── README.md
```

---

## 1. Backend (local test)

```bash
cd fuzzy_agent_backend/backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py
# → http://0.0.0.0:5000
```

Test:
```bash
curl -X POST http://localhost:5000/api/session
```

### Optional: Ollama (natural narration)
```bash
ollama pull llama3.2
ollama serve
```
Bina Ollama ke bhi app chalega — fixed factual text use hota hai.

---

## 2. Flutter App

```bash
cd fuzzy_agent_flutter/fuzzy_app_agent
flutter pub get
flutter run
```

### Backend URL (`lib/services/api_service.dart`)

| Device | URL |
|--------|-----|
| Android Emulator | `http://10.0.2.2:5000` |
| Real phone (same Wi-Fi) | `http://YOUR_LAN_IP:5000` |
| Google Cloud VM | `http://YOUR_GCP_EXTERNAL_IP:5000` |

---

## 3. Voice Commands

| English | Hindi | Marathi | Action |
|---------|-------|---------|--------|
| English / Hindi / Marathi | — | — | Language select |
| start calculation | गणना शुरू करो | गणना सुरू करा | Begin fuzzy math |
| what is fuzzy logic | फ़ज़ी लॉजिक क्या है | फझी लॉजिक म्हणजे काय | Explanation |
| architecture diagram | आर्किटेक्चर डायग्राम | आर्किटेक्चर डायग्राम | Show diagram |
| use cases | उपयोग के उदाहरण | वापराची उदाहरणे | Real-life examples |
| advantages and disadvantages | फायदे और नुकसान | फायदे आणि तोटे | Pros & cons |
| next | अगला | पुढे | Next operation |
| restart | फिर से शुरू | पुन्हा सुरू | Start over |
| help | मदद | मदत | List commands |

---

## 4. Google Cloud Deployment

Poori step-by-step guide: **[GCP_DEPLOY.md](GCP_DEPLOY.md)**

Short version:
1. GCP VM banao (Ubuntu, `e2-micro`)
2. Firewall port 5000 kholo
3. Code upload karo
4. `pip install -r requirements.txt`
5. systemd + gunicorn se service chalao
6. Flutter mein VM External IP set karo
7. `flutter build apk --release`

---

## 5. App Usage Flow

1. App khulte hi agent puchta hai: **"Which language?"** → bolo "Hindi"
2. Agent Hindi mein baat karega
3. Pucho **"fuzzy logic kya hai"** → voice + screen par explanation
4. Bolo **"गणना शुरू करो"** → universe, Set A, Set B values do
5. Har operation ke liye **"अगला"** bolo
6. **"आर्किटेक्चर डायग्राम"** → diagram screen par dikhega

---

## Notes

- Saari fuzzy math **deterministic Python** mein hai — numbers kabhi galat nahi honge
- Ollama sirf narration ke liye hai (optional)
- Sessions memory mein hain — server restart par reset honge
- Hindi/Marathi TTS ke liye phone par language pack install hona chahiye
