import json


async def handle_agent_response(state):
    response_message = state["messages"][-1].content
    
    return response_message
        
    