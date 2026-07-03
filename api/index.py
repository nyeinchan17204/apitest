from fastapi import FastAPI, HTTPException, Request
from curl_cffi import requests

# Create the instance Vercel searches for
app = FastAPI(title="Phone Proxy API for Vercel")

@app.post("/api/phones")
async def get_phone_list(request: Request):
    try:
        # 1. Parse JSON payload directly from your APK request
        apk_payload = await request.json()
    except Exception:
        # Fallback parameters if the APK sends an empty body
        apk_payload = {"pageNo": 1, "pageSize": 10, "brand": "", "search": ""}

    url = "https://phones.clloving.com/contents"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referrer": "https://phones.clloving.com/?user=MSN"
    }

    try:
        # 2. Issue Chrome impersonation request via curl_cffi
        response = requests.post(
            url,
            headers=headers,
            json=apk_payload,
            impersonate="chrome",
            timeout=15
        )
        response.raise_for_status()
        
        full_data = response.json()

        # 3. Extract the clean JSON array list block
        phone_list = full_data.get("data", {}).get("list", [])
        
        if not phone_list and isinstance(full_data, list):
            phone_list = full_data

        # 4. Return the clean JSON list back to your APK
        return phone_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")

# Fallback root path
@app.get("/")
def home():
    return {"status": "online", "message": "Vercel Python API running."}
