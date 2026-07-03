from fastapi import FastAPI, HTTPException, Request
from curl_cffi import requests

app = FastAPI(title="Phone Contents List API")

@app.post("/api/phones")
async def get_phone_list(request: Request):
    try:
        # Get the payload sent from your APK
        apk_payload = await request.json()
    except Exception:
        # Default payload if APK sends an empty body
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
        # Fetch data from the remote server using Chrome impersonation
        response = requests.post(
            url,
            headers=headers,
            json=apk_payload,
            impersonate="chrome",
            timeout=15
        )
        response.raise_for_status()
        
        full_data = response.json()

        # Extract only the list array from the response object
        # Note: If the API nests it differently (e.g., full_data["list"]), update this key.
        phone_list = full_data.get("data", {}).get("list", [])
        
        # If the root response itself is already the list, fallback to full_data
        if not phone_list and isinstance(full_data, list):
            phone_list = full_data

        # Directly returns a clean JSON Array `[...]` back to your APK
        return phone_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch phone list: {str(e)}")

@app.get("/")
def health_check():
    return {"status": "healthy"}
