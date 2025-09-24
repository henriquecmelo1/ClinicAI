import json

from ...routers.whatsapp_router import send_whatsapp_message
from ...config.langgraph_config import graph
from ...config.prompt import PROMPT
from ...config.database import add_messages_to_history, get_user_history, add_conversation_summary
from ..ai.response_helper import handle_agent_response
from .end_of_triage import end_of_triage

async def handle_message(message):
    sender_id = message["from"]
    text = (message.get("text", {}).get("body", "No text")).lower()

    user_history = await get_user_history(sender_id)

    messages_for_agent = [{"role": "system", "content": PROMPT}]
    messages_for_agent.extend(user_history)
    messages_for_agent.append({"role": "user", "content": text})

    state = graph.invoke(
        {"messages": messages_for_agent }
    )

    response_content = await handle_agent_response(state)
    response_message = response_content["agent_response"]
    stored_response = json.dumps(response_content, ensure_ascii=False)

    conversation_id = await add_messages_to_history(sender_id, text, stored_response)

    triage_finished = response_content["triage_complete"]
    if triage_finished:
        # await add_conversation_summary(conversation_id, sender_id, response_content["collected_data"])
        await end_of_triage(conversation_id, sender_id, response_content["collected_data"])


    formatted_sender_id = sender_id
    #whatsapp api sends number without the 9, but only accepts as receiver id with it
    #if it says your number is not in the list because of this piece of code, comment it
    formatted_sender_id = sender_id[:4]+"9"+sender_id[4:]

    await send_whatsapp_message(response_message, formatted_sender_id)