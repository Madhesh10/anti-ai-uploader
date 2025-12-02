# test_deepseek.py
import requests, json, os

API_KEY = "sk-0f81a41fe1c14d1c981608ca053fd278"   # replace if different
INDEX = "anti_ai_uploader"                       # replace with exact index name
BASE = "https://api.deepseek.com"

def try_endpoint(path, payload):
    url = BASE + path
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    print("->", url)
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print("Status:", r.status_code)
        print("Response:", r.text[:4000])
    except Exception as e:
        print("Request failed:", repr(e))

# try /v1/search
try_endpoint("/v1/search", {"index": INDEX, "query": "Who am I?"})

# try /v1/query
try_endpoint("/v1/query", {"index": INDEX, "query": "Who am I?"})

# try a files list endpoint (optional - depending on API)
try_endpoint("/v1/files", {})
