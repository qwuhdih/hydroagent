"""Base tool class and registry for function calling."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from langchain_core.tools import BaseTool as LangChainBaseTool


class BaseTool(ABC):
    """Base class for all agent tools.
    
    Tools should inherit from this class and implement the execute method.
    """

    name: str
    description: str

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            Tool execution result
        """
        pass

    def to_langchain_tool(self) -> LangChainBaseTool:
        """Convert to LangChain tool format."""
        from langchain_core.tools import tool
        
        @tool(name=self.name, description=self.description)
        async def tool_func(**kwargs: Any) -> Any:
            return await self.execute(**kwargs)
        
        return tool_func


# Tool registry
tool_registry: Dict[str, BaseTool] = {}


def register_tool(tool: BaseTool) -> None:
    """Register a tool in the global registry.
    
    Args:
        tool: Tool instance to register
    """
    tool_registry[tool.name] = tool


def get_tool(name: str) -> Optional[BaseTool]:
    """Get a tool by name from the registry.
    
    Args:
        name: Tool name
        
    Returns:
        Tool instance or None if not found
    """
    return tool_registry.get(name)


def get_all_tools() -> List[BaseTool]:
    """Get all registered tools.
    
    Returns:
        List of all registered tool instances
    """
    return list(tool_registry.values())

