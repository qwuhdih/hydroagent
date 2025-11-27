"""Tools module - Function calling tools for the agent."""

from src.tools.base import BaseTool, tool_registry, get_all_tools
from src.tools.example_tools import get_weather, calculate, get_current_time

__all__ = [
    "BaseTool",
    "tool_registry",
    "get_all_tools",
    "get_weather",
    "calculate",
    "get_current_time",
]
