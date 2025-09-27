from ..config.database import db
from typing import List, Dict, Any
from datetime import datetime


conversation_collection = db.get_collection("conversations")
summary_collection = db.get_collection("summaries")

async def get_user_history(sender_id: str) -> List[Dict[str, Any]]:
    history_doc = await conversation_collection.find_one({"sender_id": sender_id})
    if history_doc and "messages" in history_doc:
        return history_doc["messages"]
    return [] # Return an empty list if no history is found


async def add_messages_to_history(sender_id: str, user_message: str, agent_response: str):
    
    messages_to_add = [
        {"role": "user", "content": user_message, "timestamp": datetime.now()},
        {"role": "assistant", "content": agent_response, "timestamp": datetime.now()}
    ]

    try:
        conversation = await conversation_collection.find_one({"sender_id": sender_id})

        if conversation:
            conversation_id = conversation["_id"]
            await conversation_collection.update_one(
                {"_id": conversation_id},
                {
                    "$push": {"messages": {"$each": messages_to_add}},
                    "$set": {"last_updated": datetime.now()}
                }
            )
            print(f"Successfully updated conversation history for sender {sender_id}")
        else:
            new_conversation_doc = {
                "sender_id": sender_id,
                "messages": messages_to_add,
                "created_at": datetime.now(),
                "last_updated": datetime.now()
            }
            result = await conversation_collection.insert_one(new_conversation_doc)
            conversation_id = result.inserted_id
            print(f"Successfully created a new conversation for sender {sender_id}")
            
        return conversation_id
    except Exception as e:
            print(f"Error updating conversation history: {e}")
            # Depending on your application's needs, you might want to raise the exception
            # or handle it differently. Returning None for simplicity.
            return None

async def add_conversation_summary(conversation_id, sender_id: str, summary: str):
    try:
        await summary_collection.update_one(
            {"_id": sender_id},
            {
                "$set": {
                    "summary": summary,
                    "last_updated": datetime.now(),
                    "conversation_id": conversation_id
                }
            },
            upsert=True
        )
        print(f"Successfully updated summary for {sender_id}")
    except Exception as e:
        print(f"Error updating summary: {e}")
    