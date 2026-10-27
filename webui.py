"""Serves the aria-frontend web UI and its two API endpoints for main.py."""
import base64
import json
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import cv2
import numpy as np

from assistant import script_language
from chat.prompts2 import build_message, system_rules
from config import ASSISTANT_GENDER, HISTORY_MESSAGES
from llm.prompts import SYSTEM_PROMPT

FRONTEND_DIR = Path(__file__).parent / "aria-frontend"
HOST, PORT = "127.0.0.1", 8000


def _reply_json(text):
    paragraphs = [p.strip() for p in (text or "").split("\n\n") if p.strip()]
    return {"t": paragraphs, "s": []} if paragraphs else None


class _Handler(SimpleHTTPRequestHandler):
    session = None
    llm = None
    history = []
    lock = threading.Lock()

    def log_message(self, *args):
        pass

    def _send(self, payload, status=200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            size = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(size) or b"{}")
            query = (data.get("q") or "").strip()
            if self.path == "/api/ask":
                self._send(self._answer(query, []))
            elif self.path == "/api/ask_image":
                self._send(self._answer(query or "What do you see? What is it used for?",
                                        self._labels_in(data.get("img", ""))))
            else:
                self._send({"error": "not found"}, 404)
        except Exception as error:
            print(f"[web] error: {error}")
            self._send(None, 500)

    def _labels_in(self, data_url):
        detector = self.session.detector
        if not data_url or detector is None or detector.model is None:
            return []
        raw = base64.b64decode(data_url.split(",", 1)[-1])
        frame = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        return detector.labels_in(frame) if frame is not None else []

    def _answer(self, query, objects):
        if not query:
            return None
        if self.llm is None:
            from llm.model import LabAssistantLLM
            type(self).llm = LabAssistantLLM()
        language = script_language(query)
        with self.lock:
            reply = self.llm.generate_response(
                user_message=build_message(query, objects),
                system_prompt=SYSTEM_PROMPT + "\n\n" + system_rules(language, ASSISTANT_GENDER),
                conversation_history=self.history,
                max_history_turns=HISTORY_MESSAGES,
            )
            self.history += [{"role": "user", "content": query},
                             {"role": "assistant", "content": reply}]
        return _reply_json(reply)


def start_web_ui(session, open_browser=True):
    _Handler.session = session
    handler = partial(_Handler, directory=str(FRONTEND_DIR))
    server = ThreadingHTTPServer((HOST, PORT), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://{HOST}:{PORT}/index.html"
    print(f"[ARIA] UI running at {url}")
    if open_browser:
        webbrowser.open(url)
    return server
