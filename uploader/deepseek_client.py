# uploader/deepseek_client.py
import os
import requests
import json

DEEPSEEK_API_URL = os.environ.get("DEEPSEEK_API_URL", "https://api.deepseek.example/v1/generate")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

def generate_with_deepseek(system_prompt: str, user_prompt: str, model: str = "default", timeout: int = 60):
    """
    Simple wrapper to call DeepSeek-like REST API.
    - Replace DEEPSEEK_API_URL and payload shape with the real docs from DeepSeek.
    """
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY not set!")

    # sanitize
    system_prompt = system_prompt.replace("\x00", "")
    user_prompt = user_prompt.replace("\x00", "")

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "prompt": full_prompt,
        "max_tokens": 512,
        # other fields the API expects e.g. temperature, top_p...
    }

    resp = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    # adapt to DeepSeek response shape. Example assumes data["text"] contains the answer:
    if isinstance(data, dict):
        if "text" in data:
            return data["text"]
        # Some APIs return choices: [{"text": "..."}]
        if "choices" in data and len(data["choices"])>0:
            return data["choices"][0].get("text") or data["choices"][0].get("message") or str(data["choices"][0])
    return json.dumps(data)
