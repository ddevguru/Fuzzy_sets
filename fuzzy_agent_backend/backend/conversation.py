import re
import os
import uuid
from fuzzy_logic import FORMULAS, OPERATIONS_ORDER, compute_all, steps_for, format_set
from i18n import SUPPORTED, msg
from knowledge import FUZZY_LOGIC_ARCHITECTURE_DIAGRAM, get_topic
from ollama_client import ask_ollama
from langfuse_tracer import tracer

SESSIONS = {}

SYSTEM_PROMPT = (
    "You are a friendly voice assistant that teaches fuzzy set theory. "
    "Rephrase the given factual explanation in a warm, conversational, spoken "
    "style, under 3 short sentences. Do NOT change any numbers or formulas. "
    "Do not invent facts that were not given to you. Reply in the same language "
    "as the input text."
)

# ---- language detection ----
LANG_ALIASES = {
    "en": ["english", "angrezi", "angreji", "इंग्लिश", "इंग्रजी"],
    "hi": ["hindi", "hind", "हिंदी", "हिन्दी"],
    "mr": ["marathi", "marathi language", "मराठी"],
}

# ---- voice command patterns (lowercase) ----
NEXT_WORDS = {
    "en": ["next", "continue", "go on", "proceed"],
    "hi": ["next", "agla", "aage", "aagla", "अगला", "आगे", "जारी"],
    "mr": ["next", "pudhe", "pude", "pudhil", "पुढे", "पुढील"],
}

RESTART_WORDS = {
    "en": ["restart", "start over", "reset", "new"],
    "hi": ["restart", "phir se", "dobara", "naya", "फिर से", "दोबारा", "नया", "रीस्टार्ट"],
    "mr": ["restart", "punha", "navin", "पुन्हा", "नवीन", "रीस्टार्ट"],
}

START_CALC_WORDS = {
    "en": [
        "start calculation", "startcalculation", "start calculating", "startcalculating",
        "calculate", "calculating", "calculation", "start calc", "startcalc",
        "begin calculation", "begincalculation", "compute", "lets calculate",
        "let's calculate", "do calculation",
    ],
    "hi": [
        "start calculation", "startcalculation", "calculate", "ganana", "ganana shuru",
        "gananashuru", "shuru karo", "shurukaro", "ganana shuru karo",
        "गणना", "गणना शुरू", "गणना शुरू करो", "गणनाशुरू", "कैलकुलेट", "कैलकुलेशन",
    ],
    "mr": [
        "start calculation", "startcalculation", "calculate", "ganana", "ganana suru",
        "gananasuru", "suru kara", "surukara",
        "गणना", "गणना सुरू", "गणना सुरू करा", "गणनासुरू",
    ],
}

HELP_WORDS = {
    "en": ["help", "commands", "what can you do"],
    "hi": ["help", "madad", "मदद", "सहायता", "कमांड"],
    "mr": ["help", "madat", "मदत", "सहाय्य", "कमांड"],
}

STOP_WORDS = {
    "en": ["stop", "quiet", "silence", "cancel listening", "shut up"],
    "hi": ["stop", "ruk", "ruko", "band karo", "chup", "बंद", "रुको", "रुक", "चुप"],
    "mr": ["stop", "thamb", "band", "thamba", "थांब", "बंद", "शांत"],
}

CHANGE_LANG_WORDS = {
    "en": ["change language", "switch language", "other language", "new language"],
    "hi": [
        "change language", "bhasha badlo", "bhasha change",
        "भाषा बदलो", "भाषा बदल", "दूसरी भाषा",
    ],
    "mr": [
        "change language", "bhasha badla", "dusri bhasha",
        "भाषा बदला", "दुसरी भाषा",
    ],
}

QA_PATTERNS = {
    "what_is_fuzzy_logic": [
        r"fuzzy\s*logic",
        r"what\s+is\s+fuzzy",
        r"fuzzy\s+kya",
        r"fuzzy\s+logic\s+kya",
        r"फ़?ज़?ी\s*लॉजिक",
        r"फझी\s*लॉजिक",
        r"फजी\s*लॉजिक",
        r"explain\s+fuzzy",
        r"फ़?ज़?ी\s*लॉजिक\s*क्या",
        r"फझी\s*लॉजिक\s*म्हणजे",
    ],
    "architecture": [
        r"fuzzy\s*logic\s*(system\s*)?(architecture|diagram|structure)",
        r"architecture\s*(of\s*)?fuzzy",
        r"fuzzy\s*system\s*diagram",
        r"फ़?ज़?ी\s*लॉजिक\s*(का\s*)?(आर्किटेक्चर|डायग्राम|संरचना)",
        r"फझी\s*लॉजिक\s*(चे\s*)?(आर्किटेक्चर|आकृती)",
        r"फ़?ज़?ी\s*सिस्टम\s*डायग्राम",
    ],
    "use_cases": [
        r"use\s*case",
        r"real\s*life",
        r"real\s*world\s*example",
        r"उपयोग",
        r"उदाहरण",
        r"वापर",
        r"उदाहरणे",
    ],
    "advantages_disadvantages": [
        r"advantage",
        r"disadvantage",
        r"pros?\s+and\s+cons",
        r"फायदे",
        r"नुकसान",
        r"तोटे",
        r"फायदे\s+और",
        r"फायदे\s+आणि",
    ],
}


def new_session():
    sid = str(uuid.uuid4())
    SESSIONS[sid] = _blank_state()
    return sid


def _blank_state():
    return {
        "stage": "ASK_LANGUAGE",
        "lang": None,
        "n": 0,
        "universe": [],
        "A": [],
        "B": [],
        "current_index": 0,
        "op_index": 0,
        "results": None,
    }


def reset_session(sid):
    SESSIONS.pop(sid, None)


def recover_and_process(old_sid, text, lang_hint=None):
    """New session + actually process the user's message (no lost input)."""
    SESSIONS.pop(old_sid, None)
    new_sid = new_session()
    s = SESSIONS[new_sid]
    if lang_hint in ("en", "hi", "mr") and not _detect_language(text):
        s["lang"] = lang_hint
        s["stage"] = "MAIN"
    return new_sid, process_message(new_sid, text)


def _narrate(fixed_text, lang="en"):
    if not os.environ.get("USE_OLLAMA_NARRATION", "0").lower() in ("1", "true", "yes"):
        return fixed_text
    system = SYSTEM_PROMPT + f" Respond in {lang}."
    narrated = ask_ollama(fixed_text, system=system, trace=tracer)
    return narrated if narrated else fixed_text


def _voice_short(text, max_len=220):
    """Shorten long text for TTS — keep first sentence(s) under max_len."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    cut = text[:max_len]
    for sep in (". ", "। ", "? ", "! "):
        idx = cut.rfind(sep)
        if idx > 60:
            return cut[: idx + 1].strip()
    return cut.rstrip() + "…"


def _normalize_spoken_numbers(text):
    """Turn voice like 'three', 'zero point seven', '०.७' into '3', '0.7'."""
    t = (text or "").strip().lower()
    for i, ch in enumerate("०१२३४५६७८९"):
        t = t.replace(ch, str(i))
    spoken = {
        "zero": "0", "oh": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
        "point": ".", "dot": ".", "decimal": ".",
        "शून्य": "0", "एक": "1", "दो": "2", "दोन": "2", "तीन": "3", "चार": "4",
        "पांच": "5", "पाच": "5", "छह": "6", "सात": "7", "आठ": "8", "नौ": "9",
        "दहा": "10", "बिंदु": ".", "दशांश": ".",
    }
    for word in sorted(spoken, key=len, reverse=True):
        t = re.sub(rf"\b{re.escape(word)}\b", spoken[word], t)
    t = t.replace(",", ".")
    t = re.sub(r"\s+", "", t)
    return t


def _parse_count(text):
    t = _normalize_spoken_numbers(text)
    nums = re.findall(r"\d+", t)
    if nums:
        n = int(nums[0])
        if n > 0:
            return n
    try:
        n = int(float(t))
        if n > 0:
            return n
    except ValueError:
        pass
    return None


def _parse_membership(text):
    t = _normalize_spoken_numbers(text)
    if not t:
        return None
    try:
        val = float(t)
        if 0 <= val <= 1:
            return round(val, 2)
    except ValueError:
        pass
    return None


def _normalize_element_name(text):
    t = re.sub(r"\s+", "", (text or "").strip())
    m = re.match(r"^(?:ex|x)(\d+)$", t, re.IGNORECASE)
    if m:
        return f"x{m.group(1)}"
    return t


def _norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _norm_compact(text):
    return re.sub(r"\s+", "", _norm(text))


def _detect_language(text):
    t = _norm(text)
    for code, aliases in LANG_ALIASES.items():
        for alias in aliases:
            if alias in t or t == code:
                return code
    return None


def _matches_any(text, word_lists):
    t = _norm(text)
    tc = _norm_compact(text)
    for words in word_lists:
        for w in words:
            wn = _norm(w)
            wc = _norm_compact(w)
            if wn in t or wc in tc:
                return True
    return False


def _is_next(text, lang):
    lists = [NEXT_WORDS.get(lang, []), NEXT_WORDS["en"]]
    return _matches_any(text, lists)


def _is_restart(text):
    return _matches_any(text, list(RESTART_WORDS.values()))


def _is_start_calc(text):
    return _matches_any(text, list(START_CALC_WORDS.values()))


def _is_help(text):
    return _matches_any(text, list(HELP_WORDS.values()))


def _is_stop(text):
    return _matches_any(text, list(STOP_WORDS.values()))


def _is_change_language(text):
    return _matches_any(text, list(CHANGE_LANG_WORDS.values()))


def _detect_qa_topic(text):
    t = _norm(text)
    for topic, patterns in QA_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, t, re.IGNORECASE):
                return topic
    return None


def _reply(s, text, data=None, lang=None, action=None, voice_reply=None):
    lang = lang or s.get("lang") or "en"
    payload = {
        "reply": text,
        "voice_reply": voice_reply if voice_reply is not None else _voice_short(text),
        "stage": s["stage"],
        "language": lang,
        "data": data,
    }
    if action:
        payload["action"] = action
    return payload, 200


def _full_results_payload(s):
    out = {
        "setA": format_set(s["universe"], s["A"]),
        "setB": format_set(s["universe"], s["B"]),
    }
    for op in OPERATIONS_ORDER:
        out[op] = format_set(s["universe"], s["results"][op])
    return out


def _answer_qa(s, topic):
    lang = s.get("lang") or "en"
    data = {"topic": topic}

    if topic == "what_is_fuzzy_logic":
        body = get_topic(lang, "what_is_fuzzy_logic")
    elif topic == "architecture":
        body = get_topic(lang, "architecture_intro")
        data["diagram"] = FUZZY_LOGIC_ARCHITECTURE_DIAGRAM.strip()
        data["diagram_image"] = "assets/images/fuzzy_logic_architecture.png"
        data["diagram_title"] = {
            "en": "Fuzzy Logic System Architecture",
            "hi": "फ़ज़ी लॉजिक सिस्टम आर्किटेक्चर",
            "mr": "फझी लॉजिक सिस्टम आर्किटेक्चर",
        }.get(lang, "Fuzzy Logic Architecture")
    elif topic == "use_cases":
        body = get_topic(lang, "use_cases")
    elif topic == "advantages_disadvantages":
        body = get_topic(lang, "advantages_disadvantages")
    else:
        body = get_topic(lang, "what_is_fuzzy_logic")

    reply = f"{msg(lang, 'qa_ack')} {body}"
    voice = _voice_short(body, max_len=280)
    return _reply(s, reply, data=data, voice_reply=f"{msg(lang, 'qa_ack')} {voice}")


def _begin_calculation(s, lang, count=None):
    s["n"] = 0
    s["universe"] = []
    s["A"] = []
    s["B"] = []
    s["current_index"] = 0
    s["op_index"] = 0
    s["results"] = None
    if count is not None:
        s["n"] = count
        s["stage"] = "ASK_UNIVERSE"
        return _reply(s, msg(lang, "ask_universe", n=1))
    s["stage"] = "ASK_COUNT"
    intro = msg(lang, "start_calc")
    question = msg(lang, "ask_count")
    return _reply(s, f"{intro} {question}")


def _handle_qa_or_help(s, text):
    if _is_help(text):
        return _reply(s, msg(s["lang"], "help"))

    topic = _detect_qa_topic(text)
    if topic:
        return _answer_qa(s, topic)
    return None


def process_message(sid, text):
    s = SESSIONS.get(sid)
    if not s:
        return {"error": "Session not found", "recoverable": True}, 404

    text = (text or "").strip()
    stage = s["stage"]
    lang = s.get("lang") or "en"

    # ---- global: stop (any stage) ----
    if _is_stop(text):
        return _reply(s, msg(lang, "stopped"), action="stop")

    # ---- global: change language (any stage except first pick) ----
    if stage != "ASK_LANGUAGE" and _is_change_language(text):
        s["stage"] = "ASK_LANGUAGE"
        s["lang"] = None
        return _reply(s, msg("en", "change_language"), lang="en", action="change_language")

    # global restart (except during language selection)
    if stage != "ASK_LANGUAGE" and _is_restart(text):
        lang = s.get("lang")
        s.clear()
        s.update(_blank_state())
        s["lang"] = lang
        s["stage"] = "ASK_COUNT" if lang else "ASK_LANGUAGE"
        if lang:
            return _reply(s, msg(lang, "restart"))
        return _reply(s, msg("en", "ask_language"))

    # ---- 0. language selection ----
    if stage == "ASK_LANGUAGE":
        code = _detect_language(text)
        if not code:
            return _reply(s, msg("en", "invalid_language"), lang="en")
        s["lang"] = code
        s["stage"] = "MAIN"
        return _reply(s, msg(code, "language_set"), lang=code)

    lang = s.get("lang") or "en"
    if stage in ("MAIN", "DONE"):
        if _is_start_calc(text):
            count = _parse_count(text)
            return _begin_calculation(s, lang, count if count is not None else None)

        count = _parse_count(text)
        if count is not None:
            return _begin_calculation(s, lang, count)

        qa = _handle_qa_or_help(s, text)
        if qa:
            return qa

        if stage == "DONE":
            return _reply(s, msg(lang, "all_done"))

        return _reply(s, msg(lang, "confused"))

    # Q&A during calculation stages (don't change stage)
    if stage in ("ASK_COUNT", "ASK_UNIVERSE", "ASK_A", "ASK_B", "EXPLAIN"):
        qa = _handle_qa_or_help(s, text)
        if qa:
            return qa

    # ---- 1. how many elements ----
    if stage == "ASK_COUNT":
        n = _parse_count(text)
        if n is None:
            return _reply(s, msg(lang, "invalid_count"))
        s["n"] = n
        s["stage"] = "ASK_UNIVERSE"
        s["current_index"] = 0
        return _reply(s, msg(lang, "ask_universe", n=1))

    # ---- 2. universe element names ----
    if stage == "ASK_UNIVERSE":
        name = _normalize_element_name(text)
        if not name:
            return _reply(s, msg(lang, "empty_name"))
        s["universe"].append(name)
        s["current_index"] += 1
        if s["current_index"] < s["n"]:
            return _reply(s, msg(lang, "ask_universe", n=s["current_index"] + 1))
        s["stage"] = "ASK_A"
        s["current_index"] = 0
        first = s["universe"][0]
        return _reply(s, msg(lang, "ask_a", x=first))

    # ---- 3. Set A membership values ----
    if stage == "ASK_A":
        val = _parse_membership(text)
        if val is None:
            return _reply(s, msg(lang, "invalid_membership"))
        s["A"].append(val)
        s["current_index"] += 1
        if s["current_index"] < s["n"]:
            nxt = s["universe"][s["current_index"]]
            return _reply(s, msg(lang, "ask_a", x=nxt))
        s["stage"] = "ASK_B"
        s["current_index"] = 0
        first = s["universe"][0]
        return _reply(s, msg(lang, "ask_b", x=first))

    # ---- 4. Set B membership values ----
    if stage == "ASK_B":
        val = _parse_membership(text)
        if val is None:
            return _reply(s, msg(lang, "invalid_membership"))
        s["B"].append(val)
        s["current_index"] += 1
        if s["current_index"] < s["n"]:
            nxt = s["universe"][s["current_index"]]
            return _reply(s, msg(lang, "ask_b", x=nxt))

        s["results"] = compute_all(s["universe"], s["A"], s["B"])
        s["stage"] = "EXPLAIN"
        s["op_index"] = 0
        setA = format_set(s["universe"], s["A"])
        setB = format_set(s["universe"], s["B"])
        return _reply(
            s,
            msg(lang, "ready_explain", setA=setA, setB=setB),
            data={"setA": setA, "setB": setB},
        )

    # ---- 5. explain each operation — only on "next" ----
    if stage == "EXPLAIN":
        if not _is_next(text, lang):
            return _reply(s, msg(lang, "say_next"))

        if s["op_index"] >= len(OPERATIONS_ORDER):
            s["stage"] = "DONE"
            return _reply(
                s,
                msg(lang, "all_done"),
                data=_full_results_payload(s),
            )

        op = OPERATIONS_ORDER[s["op_index"]]
        meta = FORMULAS[op]
        result = s["results"][op]
        steps = steps_for(
            op, s["universe"], s["A"], s["B"],
            s["results"]["complement_a"], s["results"]["complement_b"], result,
        )
        result_set = format_set(s["universe"], result)
        brief = f"{meta['name']}. {meta['formula']}. Result {result_set}."
        narration = _narrate(
            f"{meta['name']}. {meta['explanation']}",
            lang=lang,
        )
        s["op_index"] += 1

        payload = {
            "operation": meta["name"],
            "formula": meta["formula"],
            "explanation": meta["explanation"],
            "steps": steps,
            "result_set": result_set,
        }
        reply_text = (
            f"{meta['name']}. Formula: {meta['formula']}. "
            + "; ".join(steps)
            + f". Result: {result_set}."
        )
        voice_text = f"{narration} Result {result_set}."
        if s["op_index"] < len(OPERATIONS_ORDER):
            reply_text += f" {msg(lang, 'say_next')}"
            voice_text += f" {msg(lang, 'say_next')}"
        return _reply(s, reply_text, data=payload, voice_reply=_voice_short(voice_text, 200))

    return _reply(s, msg(lang, "confused"))
