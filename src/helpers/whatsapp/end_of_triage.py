from ...config.database import add_conversation_summary
from ...routers.whatsapp_router import send_whatsapp_message
import dotenv
import os

dotenv.load_dotenv()

RECIPIENT_WAID = os.getenv("RECIPIENT_WAID") # número que recebe a mensagem (médico)

async def end_of_triage(conversation_id, sender_id: str, collected_data: str):
    try:
        await add_conversation_summary(conversation_id, sender_id, collected_data)

        formatted_string = "\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in collected_data.items()])

        await send_whatsapp_message(formatted_string, RECIPIENT_WAID)
    except Exception as e:
        print(f"Error adding conversation summary: {e}")