from __future__ import annotations
import os, json
from pathlib import Path
from typing import Any, Dict

DEFAULT_MODEL = os.environ.get("MR_MODEL", "gpt-4o-mini")
CONFIG_PATH = Path.home() / ".mister-dev" / "config.json"

def load_settings() -> Dict[str, Any]:
    settings: Dict[str, Any] = {"model": DEFAULT_MODEL}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text())
            if isinstance(data, dict):
                settings.update(data)
        except Exception:
            pass
    # Env has highest precedence
    if "OPENAI_API_KEY" in os.environ:
        settings["api_key"] = os.environ["OPENAI_API_KEY"]
    return settings
