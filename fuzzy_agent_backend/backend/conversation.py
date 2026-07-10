import re
import uuid
from fuzzy_logic import FORMULAS, OPERATIONS_ORDER, compute_all, steps_for, format_set
from i18n import SUPPORTED, msg
from knowledge import ARCHITECTURE_DIAGRAM, get_topic
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
    "en": ["start calculation", "calculate", "start calc", "begin calculation", "compute"],
    "hi": [
        "start calculation", "calculate", "ganana", "ganana shuru",
        "गणना", "गणना शुरू", "गणना शुरू करो", "कैलकुलेट",
    ],
    "mr": [
        "start calculation", "calculate", "ganana", "ganana suru",
        "गणना", "गणना सुरू", "गणना सुरू करा",
    ],
}

HELP_WORDS = {
    "en": ["help", "commands", "what can you do"],
    "hi": ["help", "madad", "मदद", "सहायता", "कमांड"],
    "mr": ["help", "madat", "मदत", "सहाय्य", "कमांड"],
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
        r"architecture",
        r"diagram",
        r"आर्किटेक्चर",
        r"डायग्राम",
        r"आकृती",
        r"structure",
        r"system\s+design",
    ],
    "use_cases": [
        r"use\s*case",
        r"real\s*life",
        r"example",
        r"application",
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


def _narrate(fixed_text, lang="en"):
    system = SYSTEM_PROMPT + f" Respond in {lang}."
    narrated = ask_ollama(fixed_text, system=system, trace=tracer)
    return narrated if narrated else fixed_text


def _parse_membership(text):
    # support spoken decimals: "zero point seven", "point seven"
    t = text.lower().strip()
    spoken = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "point": ".", "dot": ".",
        "शून्य": "0", "एक": "1", "दो": "2", "तीन": "3", "चार": "4",
        "पांच": "5", "छह": "6", "सात": "7", "आठ": "8", "नौ": "9",
        "बिंदु": ".", "दशांश": ".",
    }
    for word, digit in spoken.items():
        t = re.sub(rf"\b{word}\b", digit, t)
    t = t.replace(",", ".")
    try:
        val = float(t)
        if 0 <= val <= 1:
            return round(val, 2)
    except ValueError:
        pass
    return None


def _norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _detect_language(text):
    t = _norm(text)
    for code, aliases in LANG_ALIASES.items():
        for alias in aliases:
            if alias in t or t == code:
                return code
    return None


def _matches_any(text, word_lists):
    t = _norm(text)
    for words in word_lists:
        for w in words:
            if w in t:
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


def _detect_qa_topic(text):
    t = _norm(text)
    for topic, patterns in QA_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, t, re.IGNORECASE):
                return topic
    return None


def _reply(s, text, data=None, lang=None):
    lang = lang or s.get("lang") or "en"
    return {
        "reply": text,
        "stage": s["stage"],
        "language": lang,
        "data": data,
    }, 200


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
        data["diagram"] = ARCHITECTURE_DIAGRAM.strip()
        data["diagram_title"] = {
            "en": "Fuzzy Logic Tutor — Architecture",
            "hi": "फ़ज़ी लॉजिक ट्यूटर — आर्किटेक्चर",
            "mr": "फझी लॉजिक ट्यूटर — आर्किटेक्चर",
        }.get(lang, "Architecture")
    elif topic == "use_cases":
        body = get_topic(lang, "use_cases")
    elif topic == "advantages_disadvantages":
        body = get_topic(lang, "advantages_disadvantages")
    else:
        body = get_topic(lang, "what_is_fuzzy_logic")

    reply = f"{msg(lang, 'qa_ack')} {body}"
    return _reply(s, reply, data=data)


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
        return {"error": "Session not found"}, 404

    text = (text or "").strip()
    stage = s["stage"]

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

    # help / Q&A available in MAIN and after DONE
    if stage in ("MAIN", "DONE"):
        if _is_start_calc(text):
            s["stage"] = "ASK_COUNT"
            s["n"] = 0
            s["universe"] = []
            s["A"] = []
            s["B"] = []
            s["current_index"] = 0
            s["op_index"] = 0
            s["results"] = None
            intro = msg(lang, "start_calc")
            question = msg(lang, "ask_count")
            return _reply(s, f"{intro} {question}")

        qa = _handle_qa_or_help(s, text)
        if qa:
            return qa

        if stage == "DONE":
            return _reply(s, msg(lang, "all_done"))

        # MAIN but unrecognized — nudge user
        return _reply(
            s,
            f"{msg(lang, 'confused')} {msg(lang, 'help')}",
        )

    # Q&A during calculation stages (don't change stage)
    if stage in ("ASK_COUNT", "ASK_UNIVERSE", "ASK_A", "ASK_B", "EXPLAIN"):
        qa = _handle_qa_or_help(s, text)
        if qa:
            return qa

    # ---- 1. how many elements ----
    if stage == "ASK_COUNT":
        try:
            # extract first integer from speech
            nums = re.findall(r"\d+", text)
            n = int(nums[0]) if nums else int(text)
            if n <= 0:
                raise ValueError
        except (ValueError, IndexError):
            return _reply(s, msg(lang, "invalid_count"))
        s["n"] = n
        s["stage"] = "ASK_UNIVERSE"
        s["current_index"] = 0
        return _reply(s, msg(lang, "ask_universe", n=1))

    # ---- 2. universe element names ----
    if stage == "ASK_UNIVERSE":
        if not text:
            return _reply(s, msg(lang, "empty_name"))
        s["universe"].append(text)
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
        narration = _narrate(
            f"{meta['name']}. Formula: {meta['formula']}. {meta['explanation']}",
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
            f"{narration} "
            + "; ".join(steps)
            + f". {meta['name']} = {result_set}."
        )
        if s["op_index"] < len(OPERATIONS_ORDER):
            reply_text += f" {msg(lang, 'say_next')}"
        return _reply(s, reply_text, data=payload)

    return _reply(s, msg(lang, "confused"))
