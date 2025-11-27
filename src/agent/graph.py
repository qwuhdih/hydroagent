"""Agent graph definition using LangChain's create_agent (official recommended way)."""

try:
    from langchain.agents import create_agent
except ImportError:
    # Fallback for older versions or if langchain.agents doesn't exist
    try:
        from langchain_core.agents import create_agent
    except ImportError:
        # If create_agent is not available, we'll use a compatibility layer
        create_agent = None

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

from src.config import settings
from src.storage.checkpointer import get_checkpointer
from src.tools.example_tools import get_weather, calculate, get_current_time


def get_model():
    """Get configured model instance.
    
    Returns:
        Configured chat model instance
    """
    # 优先使用 CSTCloud
    if settings.CSTCLOUD_API_KEY:
        return ChatOpenAI(
            model=settings.CSTCLOUD_MODEL,
            temperature=0.7,
            api_key=settings.CSTCLOUD_API_KEY,
            base_url=settings.CSTCLOUD_BASE_URL,
        )
    elif settings.OPENAI_API_KEY:
        return ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY,
        )
    elif settings.ANTHROPIC_API_KEY:
        return init_chat_model(
            "claude-sonnet-4-5-20250929",
            temperature=0.7,
            api_key=settings.ANTHROPIC_API_KEY,
        )
    else:
        raise ValueError(
            "请配置 API Key (CSTCLOUD_API_KEY, OPENAI_API_KEY 或 ANTHROPIC_API_KEY)"
        )


def create_agent_graph():
    """Create agent using official recommended create_agent API.
    
    This is the recommended way according to LangChain documentation.
    It automatically handles tool calling, state management, and conversation flow.
    
    Returns:
        Agent instance that can be invoked with .invoke() or .ainvoke()
    """
    # Get model
    model = get_model()
    
    # Define tools list
    tools = [get_weather, calculate, get_current_time]
    
    # Get checkpointer for memory
    checkpointer = get_checkpointer()
    
    # System prompt
    system_prompt = """You are a helpful AI assistant. 
You can help users with various tasks using available tools.
Always be polite, accurate, and provide clear information.
When using tools, make sure to use them correctly and explain the results to the user."""
    
    # Check if create_agent is available
    if create_agent is None:
        raise ImportError(
            "create_agent is not available. Please install the latest version of langchain:\n"
            "pip install -U langchain langgraph"
        )
    
    # Use official recommended create_agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
    )
    
    return agent
