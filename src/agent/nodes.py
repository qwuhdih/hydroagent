"""Node definitions for the agent graph.

Each function here represents a node in the LangGraph workflow.
"""

from typing import Any
from langchain_core.messages import HumanMessage, AIMessage
from src.agent.state import AgentState
from src.config import settings


async def start_node(state: AgentState) -> AgentState:
    """Initial node that processes the user input."""
    # Extract the last user message
    messages = state.get("messages", [])
    if messages:
        last_message = messages[-1]
        # Process the message here
        pass
    
    return state


async def llm_node(state: AgentState) -> AgentState:
    """Node that calls the LLM to generate a response."""
    from langchain_openai import ChatOpenAI
    
    messages = state.get("messages", [])
    
    # 优先使用 CSTCloud，如果没有则使用 OpenAI
    if settings.CSTCLOUD_API_KEY:
        llm = ChatOpenAI(
            model=settings.CSTCLOUD_MODEL,
            temperature=0.7,
            api_key=settings.CSTCLOUD_API_KEY,
            base_url=settings.CSTCLOUD_BASE_URL,
        )
    elif settings.OPENAI_API_KEY:
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY,
        )
    else:
        raise ValueError("请配置 API Key (CSTCLOUD_API_KEY 或 OPENAI_API_KEY)")
    
    # Generate response
    response = await llm.ainvoke(messages)
    
    # Add response to state
    return {
        "messages": [response],
    }


async def tool_node(state: AgentState) -> AgentState:
    """Node that executes tools/function calls."""
    messages = state.get("messages", [])
    
    # Check if the last message contains tool calls
    # Execute tools and add results to state
    
    return state


async def end_node(state: AgentState) -> AgentState:
    """Final node that prepares the response."""
    # Final processing before returning to user
    return state


def should_continue(state: AgentState) -> str:
    """Conditional edge function to determine next node."""
    messages = state.get("messages", [])
    
    if not messages:
        return "end"
    
    last_message = messages[-1]
    
    # Check if tool calls are needed
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return "end"

