from pydantic import BaseModel
from typing_extensions import TypedDict, List
from langgraph.graph.message import add_messages
from typing import Annotated

class State(TypedDict):
    """
    Represent structure of sate used in the graph
    """
    messages:Annotated[List, add_messages]