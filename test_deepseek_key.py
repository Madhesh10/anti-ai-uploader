# test_deepseek_key.py
import requests
key = "sk-e5851de8b83d42ca86f6b1f36fe275d7"   # <- paste the exact key from Render (temporarily)
url = "https://api.deepseek.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {key}"}
payload = {
  "model": "deepseek-chat",
  "messages": [{"role": "user", "content": "hello"}]
}
r = requests.post(url, headers=headers, json=payload, timeout=15)
print(r.status_code)
try:
    print(r.json())
except:
    print(r.text)
