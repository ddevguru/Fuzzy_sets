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
    return jsonify(
        {
            "session_id": sid,
            "reply": msg("en", "ask_language"),
            "stage": "ASK_LANGUAGE",
            "language": None,
            "data": None,
        }
    )


@app.route("/api/message", methods=["POST"])
def message():
    body = request.get_json(force=True) or {}
    sid = body.get("session_id")
    text = body.get("text", "")

    if text.strip().lower() == "restart":
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
                "stage": s["stage"],
                "language": lang,
                "data": None,
            }
        )

    result, status = conv.process_message(sid, text)
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
