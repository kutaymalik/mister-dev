from __future__ import annotations
from typing import List, Dict, Any
from .config import load_settings
from openai import OpenAI

def get_client():
    cfg = load_settings()
    api_key = cfg.get("api_key")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Export it or put it in ~/.mister-dev/config.json")
    return OpenAI(api_key=api_key), cfg.get("model", "gpt-3.5-turbo")

def chat_json(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    client, model = get_client()
    # Ask the model to return *valid* JSON.
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        # Newer SDK supports strict JSON. If server/model doesn't, we'll try to json.loads later.
        response_format={"type": "json_object"}
    )
    content = completion.choices[0].message.content or "{}"
    import json
    try:
        return json.loads(content)
    except Exception:
        # Best-effort fallback: wrap in a generic object
        return {"raw": content}
