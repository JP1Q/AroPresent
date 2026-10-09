import os
import socket
import sys
import threading
from pathlib import Path

# Windowed PyInstaller builds have no stdout/stderr; the server and templates print to them.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import webview

from aropresent.server import WebServerApp

TITLE = "AroPresent"
# localStorage is keyed by origin (including the port), so a stable port is needed for saved
# slides to survive restarts. If it is taken, fall back to a free port (data won't carry over).
PREFERRED_PORT = 47615


def _pick_port() -> int:
    with socket.socket() as probe:
        try:
            probe.bind(("127.0.0.1", PREFERRED_PORT))
        except OSError:
            return 0
    return PREFERRED_PORT


def _dialog_type(name: str):
    """webview.FileDialog.<name> on pywebview >= 5, the legacy <NAME>_DIALOG constant before."""
    file_dialog = getattr(webview, "FileDialog", None)
    if file_dialog is not None:
        return getattr(file_dialog, name)
    return getattr(webview, f"{name}_DIALOG")


class DesktopApi:
    """Exposed to the editor and presentation pages as window.pywebview.api."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._main_window = None
        self._present_window = None
        self._save_path: Path | None = None

    def attach(self, main_window) -> None:
        self._main_window = main_window

    def open_present(self) -> None:
        if self._present_window is not None:
            return
        self._present_window = webview.create_window(
            TITLE, f"{self._base_url}/present", js_api=self, fullscreen=True
        )
        self._present_window.events.closed += self._on_present_closed

    def close_present(self) -> None:
        if self._present_window is not None:
            self._present_window.destroy()

    def _on_present_closed(self) -> None:
        self._present_window = None

    def save_pmd(self, text: str, suggested_name: str) -> dict | None:
        """Write to the file used last time; ask for a location only on the first save."""
        if self._save_path is None:
            chosen = self._main_window.create_file_dialog(
                _dialog_type("SAVE"),
                save_filename=suggested_name,
                file_types=("AroPresent files (*.pmd)", "All files (*.*)"),
            )
            if not chosen:
                return None
            path = Path(chosen if isinstance(chosen, str) else chosen[0])
            if not path.suffix:
                path = path.with_suffix(".pmd")
            self._save_path = path
        try:
            self._save_path.write_text(text, encoding="utf-8")
        except OSError as exc:
            return {"error": f"Could not save {self._save_path}: {exc}"}
        return {"name": self._save_path.name}

    def open_pmd(self) -> dict | None:
        chosen = self._main_window.create_file_dialog(
            _dialog_type("OPEN"),
            file_types=("AroPresent files (*.pmd)", "All files (*.*)"),
        )
        if not chosen:
            return None
        path = Path(chosen[0])
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            return {"error": f"Could not open {path}: {exc}"}
        self._save_path = path
        return {"name": path.name, "text": text}


def main() -> int:
    started = threading.Event()
    port_holder: list[int] = []

    def on_started(port: int) -> None:
        port_holder.append(port)
        started.set()

    server = WebServerApp(deck=None, title=TITLE, port=_pick_port(), mode="editor", open_browser=False, on_started=on_started)
    threading.Thread(target=server.run, daemon=True).start()
    if not started.wait(timeout=10):
        return 1

    base_url = f"http://127.0.0.1:{port_holder[0]}"
    api = DesktopApi(base_url)
    window = webview.create_window(TITLE, base_url, js_api=api, width=1400, height=850)
    api.attach(window)
    # private_mode=False keeps localStorage (saved slides, panel sizes) across restarts.
    webview.start(private_mode=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
