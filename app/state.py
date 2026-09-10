from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    user_input: str
    intent: str
    answer: str
    messages: Annotated[list, add_messages]