# uploader/deepseek_utils.py

import os
import json
import requests
from io import BytesIO
from docx import Document as DocxReader
import pdfplumber
import openpyxl

# ---------------- DeepSeek config ----------------
DEEPSEEK_BASE = os.getenv("DEEPSEEK_BASE", "https://api.deepseek.com")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")


def _require_key():
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY not set in environment")


# ---------------- TEXT EXTRACTION ----------------
def extract_text_from_file(file_or_path):
    """
    Supports:
      - Django UploadedFile objects
      - plain file paths (str)
    Returns extracted text as a string.
    """
    # get bytes + name
    if isinstance(file_or_path, str):
        with open(file_or_path, "rb") as fh:
            b = fh.read()
        name = file_or_path.lower()
    else:
        # UploadedFile-like
        try:
            file_or_path.seek(0)
        except Exception:
            pass
        b = file_or_path.read()
        name = getattr(file_or_path, "name", "").lower()

    bio = BytesIO(b)

    # DOCX
    if name.endswith(".docx"):
        bio.seek(0)
        doc = DocxReader(bio)
        return "\n".join(p.text for p in doc.paragraphs)

    # PDF
    if name.endswith(".pdf"):
        bio.seek(0)
        text = ""
        with pdfplumber.open(bio) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text

    # Excel
    if name.endswith((".xlsx", ".xlsm", ".xls")):
        bio.seek(0)
        wb = openpyxl.load_workbook(bio, data_only=True)
        sheet = wb.active
        out = ""
        for row in sheet.iter_rows(values_only=True):
            out += " ".join(str(c) for c in row if c is not None) + "\n"
        return out

    # Fallback: treat as text
    try:
        return b.decode("utf-8", errors="ignore")
    except Exception:
        return str(b)


# ---------------- OPTIONAL: upload file to DeepSeek ----------------
def upload_file_to_deepseek(file_bytes, filename, metadata=None):
    """
    Best-effort file upload. If DeepSeek account doesn't support this,
    it will just return an error dict but NOT crash your app.
    """
    _require_key()

    url = f"{DEEPSEEK_BASE}/v1/files"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    files = {"file": (filename, file_bytes)}
    data = {"purpose": "rag", "metadata": json.dumps(metadata or {})}

    try:
        r = requests.post(url, headers=headers, files=files, data=data, timeout=30)
    except requests.RequestException as e:
        return {"error": f"request_failed: {e}", "endpoint": url}

    if r.status_code >= 400:
        try:
            body = r.json()
        except Exception:
            body = r.text
        return {"error": f"{r.status_code} {r.reason}", "body": body, "endpoint": url}

    try:
        return r.json()
    except Exception:
        return {"error": "invalid_json", "body": r.text, "endpoint": url}


# ---------------- MAIN: ask DeepSeek with chat completions ----------------
def ask_deepseek(question, context=None, timeout=20):
    """
    Call DeepSeek chat model.

    question: user question (string)
    context: long text from your uploaded documents (string, optional)
    Returns a dict:
      - {"result": "<answer text>", "raw": <full_json>}
      - or {"error": "...", ...}
    """
    _require_key()

    url = f"{DEEPSEEK_BASE}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    if context:
        user_content = f"Context:\n{context}\n\nQuestion: {question}"
    else:
        user_content = question

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant that answers strictly using the provided context.",
            },
            {"role": "user", "content": user_content},
        ],
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)
    except requests.RequestException as e:
        return {"error": f"request_failed: {e}", "endpoint": url}

    if r.status_code >= 400:
        try:
            body = r.json()
        except Exception:
            body = r.text
        return {"error": f"{r.status_code} {r.reason}", "body": body, "endpoint": url}

    try:
        data = r.json()
    except Exception:
        return {"error": "invalid_json", "body": r.text}

    # extract assistant text
    assistant_text = None
    try:
        assistant_text = data["choices"][0]["message"]["content"]
    except Exception:
        try:
            assistant_text = data["choices"][0].get("text")
        except Exception:
            assistant_text = None

    if assistant_text:
        return {"result": assistant_text, "raw": data}

    return {"error": "no_text_in_response", "raw": data}
