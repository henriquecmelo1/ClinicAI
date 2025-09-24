import json


async def handle_agent_response(state):
    response_message = state["messages"][-1].content

    json_body = ""
    cleaned_str = response_message.strip()

    if cleaned_str.startswith("```json") and cleaned_str.endswith("```"):
        # Remove '```json' prefix (7 chars) and '```' suffix (3 chars)
        json_body = cleaned_str[7:-3].strip()
    else:
        # If there's no '```json' block, assume it's already JSON (or an empty string)
        json_body = cleaned_str

    if not json_body:
        print("Empty JSON body.")
        raise ValueError("Empty JSON body")

    try:
        agent_response = json.loads(json_body)
        return agent_response
        
    except json.JSONDecodeError as e:
        print("Falha ao analisar JSON:", e)
        print("String que causou a falha:", repr(json_body))
        return None  # Return None or handle the error accordingly