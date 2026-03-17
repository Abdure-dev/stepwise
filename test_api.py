import os
import requests

url = os.getenv("MODEL_API_URL", "").strip()
key = os.getenv("MODEL_API_KEY", "").strip()
model = os.getenv("MODEL_NAME", "").strip()

if not url or not key or not model:
    raise ValueError("Missing MODEL_API_URL, MODEL_API_KEY, or MODEL_NAME")

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
}

payload = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Reply with exactly: hello from nvidia"}
    ],
    "temperature": 0.1,
    "max_tokens": 20,
}

r = requests.post(url, headers=headers, json=payload, timeout=60)
print("status:", r.status_code)
print(r.text)