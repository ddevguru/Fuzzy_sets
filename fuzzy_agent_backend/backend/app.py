from flask import Flask, request, jsonify
from flask_cors import CORS
import conversation as conv
from i18n import msg

app = Flask(__name__)
CORS(app)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/session", methods=["POST"])
def start_session():
    sid = conv.new_session()
    reply = msg("en", "ask_language")
    return jsonify(
        {
            "session_id": sid,
            "reply": reply,
            "voice_reply": reply,
            "stage": "ASK_LANGUAGE",
            "language": None,
            "data": None,
        }
    )


@app.route("/api/message", methods=["POST"])
def message():
    body = request.get_json(force=True) or {}
    sid = body.get("session_id")
    text = (body.get("text") or "").strip()
    lang_hint = body.get("language")

    if not text:
        return jsonify({"error": "Empty message"}), 400

    if text.lower() == "restart":
        old = conv.SESSIONS.get(sid, {})
        lang = old.get("lang")
        conv.reset_session(sid)
        new_sid = conv.new_session()
        s = conv.SESSIONS[new_sid]
        if lang:
            s["lang"] = lang
            s["stage"] = "ASK_COUNT"
            reply = msg(lang, "restart")
        else:
            reply = msg("en", "ask_language")
        return jsonify(
            {
                "session_id": new_sid,
                "reply": reply,
                "voice_reply": reply,
                "stage": s["stage"],
                "language": lang,
                "data": None,
            }
        )

    # Session missing or expired — recover AND process this message
    if not sid or sid not in conv.SESSIONS:
        new_sid, (result, status) = conv.recover_and_process(sid, text, lang_hint)
        if status != 200:
            return jsonify(result), status
        result["session_id"] = new_sid
        result["recovered"] = True
        return jsonify(result), 200

    result, status = conv.process_message(sid, text)
    if status == 404 and result.get("recoverable"):
        new_sid, (result, status) = conv.recover_and_process(sid, text, lang_hint)
        if status != 200:
            return jsonify(result), status
        result["session_id"] = new_sid
        result["recovered"] = True
        return jsonify(result), 200

    if status != 200:
        return jsonify(result), status
    result["session_id"] = sid
    return jsonify(result), 200


@app.route("/api/reset", methods=["POST"])
def reset():
    body = request.get_json(force=True) or {}
    conv.reset_session(body.get("session_id"))
    return jsonify({"ok": True})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
