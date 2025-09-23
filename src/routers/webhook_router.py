from fastapi import APIRouter, Request, HTTPException, Query, BackgroundTasks
from dotenv import load_dotenv
import os
import json

from .whatsapp_router import send_whatsapp_message
from ..services.ai.langgraph_config import graph
from ..services.ai.prompt import PROMPT
from ..services.database import add_messages_to_history

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

router = APIRouter()

async def handle_agent_response(state):
    response_message = (state["messages"][-1].content)
    json_body = ""

    cleaned_str = response_message.strip()
    if cleaned_str.startswith("```json") and cleaned_str.endswith("```"):
    # Removemos o prefixo '```json' (7 caracteres) e o sufixo '```' (3 caracteres)
        json_body = cleaned_str[7:-3].strip()
    else:
    # Se não tiver o bloco de código, assumimos que a string já é o JSON
        json_body = cleaned_str

    try:
        agent_response = json.loads(json_body)
        
    except Exception as e:
        print("Falha ao analisar JSON:", e)
        # Usar repr() é ótimo para depurar, pois mostra caracteres invisíveis como \n
        print("String que causou a falha:", repr(json_body))

    return agent_response


async def handle_message(message, phone_number_id):
    print("Received message:", message)
    sender_id = message["from"]
    print("Sender ID:", sender_id)
    text = (message.get("text", {}).get("body", "No text")).lower()
    state = graph.invoke(
        {"messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": text}
        ]}
    )
    response_content = await handle_agent_response(state)
    response_message = response_content["agent_response"]

    await add_messages_to_history(sender_id, text, response_message)
    
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
async def handle_webhook(request: Request, background_tasks: BackgroundTasks): 
    # triggered when the bot's message is sent, delivered and read by the user and also when a user sends a message to the bot
    # every message should have four request (user's message, bot's message sent, delivered and read)
    data = await request.json()

    if data:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                phone_number_id = value.get("metadata", {}).get("phone_number_id")
                message_data = value.get("messages", [])
                for message in message_data:
                    background_tasks.add_task(handle_message, message, phone_number_id)

    return {"status": "EVENT_RECEIVED"}