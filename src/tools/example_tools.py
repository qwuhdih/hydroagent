"""Example tools for the agent using LangChain's @tool decorator."""

from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A string describing the weather in the city
    """
    # 这是一个示例工具，实际应该调用真实的天气 API
    return f"It's always sunny in {city}!"


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
        
    Returns:
        The result of the calculation as a string
    """
    try:
        # 注意：生产环境应该使用更安全的计算方法
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


@tool
def get_current_time() -> str:
    """Get the current time.
    
    Returns:
        Current time as a string
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

