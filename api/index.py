from fastapi import FastAPI
from curl_cffi import requests

app = FastAPI()

URL = "https://phones.clloving.com/contents"

HEADERS = {
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

@app.post("/phones")
def get_phones(payload: dict):
    try:
        response = requests.post(
            URL,
            headers=HEADERS,
            json=payload,
            impersonate="chrome",
            timeout=15,
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
