from fastapi import APIRouter, Request, HTTPException, Query, BackgroundTasks
from dotenv import load_dotenv
import os

from ..helpers.whatsapp.message_handler import handle_message
from ..helpers.whatsapp.audio_handler import audio_handler


load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

router = APIRouter()


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
async def handle_webhook(request: Request, background_tasks: BackgroundTasks): 
    # triggered when the bot's message is sent, delivered and read by the user and also when a user sends a message to the bot
    # every message should have four request (user's message, bot's message sent, delivered and read)
    data = await request.json()

    if data:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                message_data = value.get("messages", [])
                for message in message_data:
                    message_type = message.get("type")
                    if message_type == "audio":
                        # audio_info = message.get("audio", {})
                        # audio_id = audio_info.get("id")
                        # background_tasks.add_task(audio_handler, audio_id)
                        background_tasks.add_task(audio_handler, message)


                    elif message_type == "text":
                        background_tasks.add_task(handle_message, message)

        



    return {"status": "EVENT_RECEIVED"}