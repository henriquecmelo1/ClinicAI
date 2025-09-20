from fastapi import APIRouter, Request, HTTPException, Query
from dotenv import load_dotenv
import os

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

router = APIRouter()

def handle_message(message, phone_number_id):
    sender_id = message["from"]

    # Send a simple automated reply
    print(sender_id, "Hey, your bot is up!", phone_number_id)


@router.get("/")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Forbidden")

# Handle incoming messages
@router.post("/")
async def handle_webhook(request: Request):
    data = await request.json()
    print("Received webhook:", data)

    if data:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                phone_number_id = value.get("metadata", {}).get("phone_number_id")
                message_data = value.get("messages", [])
                for message in message_data:
                    handle_message(message, phone_number_id)

    return {"status": "EVENT_RECEIVED"}