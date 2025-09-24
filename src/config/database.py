import os
from pymongo import AsyncMongoClient
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Any


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Ensure the MONGO_URI is set
if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

# Create a single, reusable client instance
client = AsyncMongoClient(MONGO_URI)

# Get a reference to your database (e.g., ClinicAI)
db = client.ClinicAI

# Get a reference to the collection where you'll store conversations
conversation_collection = db.get_collection("conversations")

async def get_user_history(sender_id: str) -> List[Dict[str, Any]]:
    history_doc = await conversation_collection.find_one({"_id": sender_id})
    if history_doc and "messages" in history_doc:
        return history_doc["messages"]
    return [] # Return an empty list if no history is found


async def add_messages_to_history(sender_id: str, user_message: str, agent_response: str):
    # Create the message objects in the format the AI expects
    messages_to_add = [
        {"role": "user", "content": user_message, "timestamp": datetime.now()},
        {"role": "assistant", "content": agent_response, "timestamp": datetime.now()}
    ]

    try:
        # Find document by sender_id and push new messages into the 'messages' array
        await conversation_collection.update_one(
            {"_id": sender_id},
            {
                "$push": {
                    "messages": {"$each": messages_to_add}
                },
                "$set": {
                    "last_updated": datetime.now()
                }
            },
            upsert=True # This is key: creates the document if it doesn't exist
        )
        print(f"Successfully updated conversation history for {sender_id}")
    except Exception as e:
        print(f"Error updating conversation history: {e}")