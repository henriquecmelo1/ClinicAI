from fastapi import APIRouter, Request, HTTPException, Query
from dotenv import load_dotenv
import os

from .whatsapp_router import send_whatsapp_message
from ..services.ai.langgraph_config import graph

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

router = APIRouter()

async def handle_message(message, phone_number_id):
    sender_id = message["from"]
    text = (message.get("text", {}).get("body", "No text")).lower()
    state = graph.invoke({"messages": [{"role": "user", "content": text}]})
    response_message = state["messages"][-1].content
    print(response_message)
    
    await send_whatsapp_message(response_message)
    


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
    # triggered when the bot's message is sent, delivered and read by the user and also when a user sends a message to the bot
    # every message should have four request (user's message, bot's message sent, delivered and read)
    data = await request.json()
    print(data)

    if data:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                phone_number_id = value.get("metadata", {}).get("phone_number_id")
                message_data = value.get("messages", [])
                for message in message_data:
                     await handle_message(message, phone_number_id)

    return {"status": "EVENT_RECEIVED"}