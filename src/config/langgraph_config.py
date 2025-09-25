from urllib import response
from dotenv import load_dotenv
import os
from typing import Annotated

from typing_extensions import TypedDict
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from ..models.response_model import ClinicAIAssistantResponse
from ..models.state_model import State


# class State(TypedDict):
#     # Messages have the type "list". The `add_messages` function
#     # in the annotation defines how this state key should be updated
#     # (in this case, it appends messages to the list, rather than overwriting them)
#     messages: Annotated[list, add_messages]




load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GOOGLE_API_KEY, temperature=0)
gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=GOOGLE_API_KEY, temperature=0)
llm = gemini.with_structured_output(ClinicAIAssistantResponse)

def chatbot_node(state: State): # current state
    response = llm.invoke(state["messages"])
    return {
        # Create a new AIMessage to add to the history for the next turn
        "messages": [AIMessage(content=response.agent_response)],
        # Update the other state fields with the parsed data
        "agent_response": response.agent_response,
        "patient_info": response.patient_info,
        "collected_data": response.collected_data,
        "triage_complete": response.triage_complete,
    } #calling the LLM with the current messages and appending the response to messages



graph_builder = StateGraph(State)

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot_node)

# Define the edges between the nodes
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()
