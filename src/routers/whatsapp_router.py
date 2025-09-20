import os
import requests
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv


# --- Configuration ---
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
API_VERSION = os.getenv("API_VERSION")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID") # número que envia a mensagem
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID") # número que recebe a mensagem


router = APIRouter()



# --- The Main API Endpoint ---
@router.post("/send-message")
async def send_whatsapp_message(message):

    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": RECIPIENT_WAID,  
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message,  
        },
    }
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Request Data: {data}")

    # 4. Make the POST request to the Facebook Graph API
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        # This will raise an exception for 4xx and 5xx status codes
        response.raise_for_status()

        print(f"Facebook API Success Response: {response.json()}")
        return response.json()

    except requests.exceptions.HTTPError as err:
        # If Facebook returns an error, forward it to the client
        print(f"HTTP Error from Facebook: {err.response.status_code} - {err.response.text}")
        raise HTTPException(
            status_code=err.response.status_code,
            detail=err.response.json()
        )
    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection timeout)
        print(f"Network Request Exception: {e}")
        raise HTTPException(
            status_code=503, # Service Unavailable
            detail=f"Failed to communicate with the Facebook API: {e}"
        )