import os
import requests
from fastapi import APIRouter, BackgroundTasks, HTTPException
from dotenv import load_dotenv
from fastapi import Request


load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
API_VERSION = os.getenv("API_VERSION")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID") # número que envia a mensagem
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID") # número que recebe a mensagem
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN") # token de verificação do webhook


router = APIRouter()

@router.post("/send-first-message")
async def send_first_message():
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,  
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}},
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as err:
        print(f"Error from Whatsapp API: {err.response.status_code} - {err.response.text}")
        raise HTTPException(
            status_code=err.response.status_code,
            detail=err.response.json()
        )
    
    except requests.exceptions.RequestException as e:
        print(f"Network Request Exception: {e}")
        raise HTTPException(
            status_code=503, # Service Unavailable
            detail=f"Failed to communicate with the Facebook API: {e}"
        )


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


    try:
        response = requests.post(url, headers=headers, json=data, timeout=10) # manda a requisição para a API do whatsapp
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as err:
        print(f"Error from Whatsapp API: {err.response.status_code} - {err.response.text}")
        raise HTTPException(
            status_code=err.response.status_code,
            detail=err.response.json()
        )
    
    except requests.exceptions.RequestException as e:
        print(f"Network Request Exception: {e}")
        raise HTTPException(
            status_code=503, # Service Unavailable
            detail=f"Failed to communicate with the Facebook API: {e}"
        )
    

    

