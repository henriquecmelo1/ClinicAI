from typing_extensions import TypedDict, Annotated
from typing import Optional
from langgraph.graph.message import add_messages
from ..models.response_model import ClinicAIAssistantResponse, PatientInfo, CollectedData

class State(TypedDict):
    messages: Annotated[list, add_messages]
    agent_response: Optional[str]
    patient_info: Optional[PatientInfo]
    collected_data: Optional[CollectedData]
    triage_complete: Optional[bool]