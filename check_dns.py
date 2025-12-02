import socket, requests, os, sys

name = "api.deepseek.com"
print("Resolving:", name)
try:
    print("gethostbyname:", socket.gethostbyname(name))
except Exception as e:
    print("DNS resolution failed:", repr(e))

print("\nTry HTTPS request (timeout 5s):")
try:
    r = requests.get(f"https://{name}/v1/query", timeout=5)
    print("Status:", r.status_code)
    try:
        print("Response (trim):", r.text[:500])
    except Exception:
        pass
except Exception as e:
    print("HTTP request failed:", repr(e))

# optional: check general internet
try:
    print("\nGoogle resolve test:", socket.gethostbyname("google.com"))
except Exception as e:
    print("google.com resolve failed:", repr(e))
