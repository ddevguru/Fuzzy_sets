"""
Thin wrapper around a locally running Ollama server (https://ollama.com).
Used ONLY to make the agent's spoken narration sound natural - all the actual
fuzzy-set math happens in fuzzy_logic.py, never inside the LLM.

Setup on your machine:
    1. Install Ollama:  https://ollama.com/download
    2. Pull a small, fast model:   ollama pull llama3.2
    3. Start the server:           ollama serve   (usually auto-starts)
"""
import os
import requests

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")


def ask_ollama(prompt, system=None, trace=None):
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system
    try:
        resp = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=30)
        resp.raise_for_status()
        text = resp.json().get("response", "").strip()
        if trace:
            trace.log(prompt=prompt, output=text, model=OLLAMA_MODEL)
        return text
    except Exception as e:
        if trace:
            trace.log(prompt=prompt, output=f"ERROR: {e}", model=OLLAMA_MODEL)
        # Safe fallback: caller will use the fixed factual text instead
        return None
