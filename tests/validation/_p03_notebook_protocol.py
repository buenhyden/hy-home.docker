"""Controlled, value-free Ollama protocol server for isolated P03 fixtures."""

OLLAMA_PROTOCOL_SERVER = r"""import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

EVENTS = Path("/events/events.jsonl")
MODELS = {
    "gemma4:e2b": {"family": "gemma4", "size": 1},
    "embeddinggemma-2:740m": {"family": "embeddinggemma", "size": 1},
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, _format, *_args):
        return

    def send_json(self, status, value):
        body = json.dumps(value, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length < 0 or length > 65536:
            raise ValueError("request size")
        return json.loads(self.rfile.read(length))

    def event(self, kind, model, dimension=None):
        row = {"kind": kind, "model": model}
        if dimension is not None:
            row["dimension"] = dimension
        with EVENTS.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, separators=(",", ":")) + "\n")

    def do_GET(self):
        if self.path == "/api/version":
            self.send_json(200, {"version": "0.40.12-p03-controlled"})
        elif self.path == "/api/tags":
            self.send_json(200, {"models": [
                {"name": name, "model": name, "size": value["size"],
                 "digest": "sha256:" + ("1" if "embedding" not in name else "2") * 64,
                 "details": {"family": value["family"]}}
                for name, value in MODELS.items()]})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        try:
            payload = self.read_json()
        except Exception:
            self.send_json(400, {"error": "invalid request"})
            return
        model = payload.get("model")
        if model not in MODELS:
            self.send_json(404, {"error": "model not found"})
            return
        if self.path == "/api/show":
            self.send_json(200, {"details": {"family": MODELS[model]["family"]},
                                 "capabilities": ["embedding"] if "embedding" in model else ["completion"]})
        elif self.path in {"/api/embed", "/api/embeddings"}:
            self.event("embedding", model, 768)
            vector = [0.001] * 768
            response = {"model": model, "embeddings": [vector]}
            if self.path.endswith("embeddings"):
                response = {"embedding": vector}
            self.send_json(200, response)
        elif self.path == "/api/chat":
            self.event("chat", model)
            self.send_json(200, {"model": model, "created_at": "synthetic",
                                 "message": {"role": "assistant", "content": "P03 controlled reply"},
                                 "done": True, "done_reason": "stop"})
        else:
            self.send_json(404, {"error": "not found"})

ThreadingHTTPServer(("0.0.0.0", 11434), Handler).serve_forever()
"""
