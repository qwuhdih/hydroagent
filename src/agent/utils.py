"""Utility functions for agent operations."""

from typing import List, Dict, Any
from langchain_core.messages import BaseMessage


def format_messages(messages: List[BaseMessage]) -> str:
    """Format messages for display or logging.
    
    Args:
        messages: List of message objects
        
    Returns:
        Formatted string representation
    """
    formatted = []
    for msg in messages:
        role = getattr(msg, "type", "unknown")
        content = getattr(msg, "content", "")
        formatted.append(f"{role}: {content}")
    
    return "\n".join(formatted)


def extract_tool_calls(messages: List[BaseMessage]) -> List[Dict[str, Any]]:
    """Extract tool calls from messages.
    
    Args:
        messages: List of message objects
        
    Returns:
        List of tool call dictionaries
    """
    tool_calls = []
    for msg in messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tool_calls.extend(msg.tool_calls)
    
    return tool_calls


def validate_state(state: Dict[str, Any]) -> bool:
    """Validate agent state structure.
    
    Args:
        state: State dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_keys = ["messages"]
    return all(key in state for key in required_keys)

