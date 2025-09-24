import json

from ...routers.whatsapp_router import send_whatsapp_message
from ...config.langgraph_config import graph
from ..ai.prompt import PROMPT
from ...config.database import add_messages_to_history, get_user_history
from ..ai.response_helper import handle_agent_response

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

    await add_messages_to_history(sender_id, text, stored_response)

    await send_whatsapp_message(response_message)