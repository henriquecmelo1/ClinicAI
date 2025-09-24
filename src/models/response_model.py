from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, Any

class ClinicAIAssistantResponse(BaseModel):
    """
    The structured response from the ClinicAI assistant. 
    This format must be used for every single turn in the conversation.
    """
    agent_response: str = Field(
        description="The text response that should be shown to the user."
    )
    collected_data: Dict[str, Any] = Field(
        description=(
            "A dictionary containing the patient's information collected so far. "
            "This dictionary should be progressively updated throughout the conversation."
        )
    )