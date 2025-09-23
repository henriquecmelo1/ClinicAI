import os
from pymongo import AsyncMongoClient
from datetime import datetime
from dotenv import load_dotenv

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

async def add_messages_to_history(sender_id: str, user_message: str, agent_response: str):
    """
    Upserts a conversation, adding the new user message and agent response to the
    'messages' array.
    """
    # Create the message objects in the format the AI expects
    messages_to_add = [
        {"role": "user", "content": user_message, "timestamp": datetime.utcnow()},
        {"role": "assistant", "content": agent_response, "timestamp": datetime.utcnow()}
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
                    "last_updated": datetime.utcnow()
                }
            },
            upsert=True # This is key: creates the document if it doesn't exist
        )
        print(f"Successfully updated conversation history for {sender_id}")
    except Exception as e:
        print(f"Error updating conversation history: {e}")