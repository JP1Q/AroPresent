import json
import webbrowser
from typing import Callable
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .parser import SlideParser, SlideDeck
from .renderer import MarkdownRenderer
from .templates import VIEWS_DIR, build_editor_html, build_present_html, load_slide_templates

STATIC_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
}


class WebServerApp:
    def __init__(self, deck: SlideDeck | None, title: str, port: int, mode: str, open_browser: bool,
                 on_started: Callable[[int], None] | None = None) -> None:
        self._deck = deck
        self._title = title
        self._port = port
        self._mode = mode
        self._open_browser = open_browser
        self._on_started = on_started
        self._renderer = MarkdownRenderer()

    def run(self) -> None:
        handler = self._make_handler()
        server = ThreadingHTTPServer(("127.0.0.1", self._port), handler)
        base_url = f"http://127.0.0.1:{server.server_port}"
        url = f"{base_url}/present" if self._mode == "present" else base_url

        if self._open_browser:
            webbrowser.open(url)

        print(f"Serving on: {url}")
        if self._on_started is not None:
            self._on_started(server.server_port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()

    def _make_handler(self):
        renderer = self._renderer
        title = self._title
        deck = self._deck

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = urlparse(self.path).path
                if path == "/":
                    self._send_html(build_editor_html(title))
                    return
                if path == "/present":
                    self._send_html(build_present_html(title))
                    return
                if path == "/slides":
                    if deck is None:
                        self._send_text("Presentation file not provided.", HTTPStatus.NOT_FOUND)
                        return
                    slides_data = [{"html": renderer.render(slide.content), "animation": slide.animation} for slide in deck.slides]
                    self._send_json({"slides": slides_data})
                    return
                if path == "/slide_templates":
                    self._send_json({"templates": load_slide_templates()})
                    return
                if path.startswith("/static/"):
                    self._send_static(path[len("/static/"):])
                    return
                self._send_text("Not found", HTTPStatus.NOT_FOUND)

            def do_POST(self):
                path = urlparse(self.path).path
                if path == "/render":
                    length = int(self.headers.get("Content-Length", "0"))
                    body = self.rfile.read(length).decode("utf-8")
                    try:
                        slides = SlideParser.parse(body)
                    except ValueError as exc:
                        self._send_json({"error": str(exc), "slides": []}, HTTPStatus.BAD_REQUEST)
                        return
                    slides_data = [{"html": renderer.render(slide.content), "animation": slide.animation} for slide in slides]
                    self._send_json({"slides": slides_data})
                    return
                if path == "/parse_raw":
                    length = int(self.headers.get("Content-Length", "0"))
                    body = self.rfile.read(length).decode("utf-8")
                    try:
                        slides = SlideParser.parse(body)
                    except ValueError as exc:
                        self._send_json({"error": str(exc), "slides": []}, HTTPStatus.BAD_REQUEST)
                        return
                    self._send_json({"slides": [{"content": slide.content, "animation": slide.animation} for slide in slides]})
                    return

                self._send_text("Not found", HTTPStatus.NOT_FOUND)

            def _send_html(self, html: str, status: HTTPStatus = HTTPStatus.OK) -> None:
                self.send_response(status)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))

            def _send_static(self, name: str) -> None:
                file = (VIEWS_DIR / name).resolve()
                content_type = STATIC_TYPES.get(file.suffix)
                if content_type is None or not file.is_relative_to(VIEWS_DIR) or not file.is_file():
                    self._send_text("Not found", HTTPStatus.NOT_FOUND)
                    return
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", content_type)
                self.end_headers()
                self.wfile.write(file.read_bytes())

            def _send_text(self, text: str, status: HTTPStatus = HTTPStatus.OK) -> None:
                self.send_response(status)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(text.encode("utf-8"))

            def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
                data = json.dumps(payload)
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(data.encode("utf-8"))

            def log_message(self, format, *args):
                return

        return Handler