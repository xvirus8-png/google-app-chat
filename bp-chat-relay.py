import json
import time
import urllib.request
import urllib.error
import os
import sys

FIREBASE_URL = "https://kashf-system-default-rtdb.firebaseio.com"
ZEN_API = "https://opencode.ai/zen/v1/chat/completions"
POLL_INTERVAL = 2
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relay_log.txt")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    print(msg)

def firebase_get(path):
    url = f"{FIREBASE_URL}/{path}.json"
    req = urllib.request.Request(url, method="GET",
        headers={"User-Agent": "BPRelay/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        log(f"GET error {path}: {e}")
        return None

def firebase_patch(path, data):
    url = f"{FIREBASE_URL}/{path}.json"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="PATCH",
        headers={"Content-Type": "application/json", "User-Agent": "BPRelay/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        log(f"PATCH error {path}: {e}")
        return None

def call_zen(messages, api_key):
    data = json.dumps({
        "model": "big-pickle",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4096
    }).encode()
    req = urllib.request.Request(ZEN_API, data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            result = json.loads(r.read().decode())
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        err = ""
        if e.fp:
            try: err = json.loads(e.fp.read().decode()).get("error", {}).get("message", str(e.code))
            except: err = str(e.code)
        return f"⚠️ خطأ {e.code}: {err}"
    except Exception as e:
        return f"⚠️ خطأ اتصال: {e}"

log("Relay started - watching Firebase for chat requests...")
processed = set()

while True:
    try:
        data = firebase_get("bp_chat")
        if data and isinstance(data, dict):
            for key, entry in data.items():
                if key in processed:
                    continue
                if not isinstance(entry, dict) or entry.get("status") != "pending":
                    continue

                processed.add(key)
                msgs = entry.get("messages", [])
                key_val = entry.get("apiKey", "")

                if not msgs or not key_val:
                    firebase_patch(f"bp_chat/{key}", {"status": "done", "error": "بيانات ناقصة", "response": ""})
                    continue

                log(f"Processing {key}: {msgs[-1]['content'][:60]}...")
                reply = call_zen(msgs, key_val)

                firebase_patch(f"bp_chat/{key}", {
                    "response": reply,
                    "status": "done",
                    "apiKey": ""
                })
                log(f"Done {key}")
    except Exception as e:
        log(f"Loop error: {e}")

    time.sleep(POLL_INTERVAL)
