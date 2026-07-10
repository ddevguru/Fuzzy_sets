"""
Optional LangFuse tracing (https://langfuse.com - open source, free self-host
or free cloud tier). If LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY are not set,
tracing silently no-ops so the app works fine without it.

Setup:
    pip install langfuse
    export LANGFUSE_PUBLIC_KEY=pk-...
    export LANGFUSE_SECRET_KEY=sk-...
    export LANGFUSE_HOST=https://cloud.langfuse.com   # or your self-hosted URL
"""
import os

try:
    from langfuse import Langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False


class Tracer:
    def __init__(self):
        self.enabled = False
        if LANGFUSE_AVAILABLE and os.environ.get("LANGFUSE_PUBLIC_KEY"):
            try:
                self.client = Langfuse(
                    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
                    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
                    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
                )
                self.enabled = True
            except Exception:
                self.enabled = False

    def log(self, prompt, output, model):
        if not self.enabled:
            return
        try:
            self.client.generation(
                name="fuzzy-agent-narration",
                model=model,
                input=prompt,
                output=output,
            )
            self.client.flush()
        except Exception:
            pass


tracer = Tracer()
