# deepseek_probe.py
import os, requests, json
DEEPSEEK_BASE = os.getenv("DEEPSEEK_BASE", "https://api.deepseek.com")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type":"application/json"}
endpoints = ["/v1/search","/v1/query","/v1/retrieve","/v1/answers","/v1/chat/completions","/v1/completions"]
payload = {"index":"default-index","query":"hello, check endpoint"}
for ep in endpoints:
    url = DEEPSEEK_BASE + ep
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(url, r.status_code)
        try:
            print(json.dumps(r.json(), indent=2)[:2000])
        except Exception:
            print(r.text[:2000])
    except Exception as e:
        print(url, "->", repr(e))
