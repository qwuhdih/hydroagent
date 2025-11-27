"""Agent state schema definition."""

from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State schema for the agent graph.

    This defines the structure of state that flows through the graph.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    """Chat message history."""
    
    # Add additional state fields as needed
    # current_step: str
    # tool_results: list
    # user_context: dict

