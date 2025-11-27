"""Test script for refactored agent using official create_agent API."""

from src.agent.graph import create_agent_graph

def test_agent():
    """Test the refactored agent."""
    print("=" * 60)
    print("测试重构后的 Agent (使用官方 create_agent API)")
    print("=" * 60)
    
    # Create agent
    print("\n1. 创建 Agent...")
    agent = create_agent_graph()
    print("   ✓ Agent 创建成功")
    
    # Test basic conversation
    print("\n2. 测试基本对话...")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "你好，介绍一下你自己"}]},
        config={"configurable": {"thread_id": "test_1"}}
    )
    
    last_message = result["messages"][-1]
    response = last_message.content if hasattr(last_message, "content") else str(last_message)
    print(f"   用户: 你好，介绍一下你自己")
    print(f"   AI: {response}")
    
    # Test tool calling
    print("\n3. 测试工具调用...")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "北京今天天气怎么样？"}]},
        config={"configurable": {"thread_id": "test_1"}}
    )
    
    last_message = result["messages"][-1]
    response = last_message.content if hasattr(last_message, "content") else str(last_message)
    print(f"   用户: 北京今天天气怎么样？")
    print(f"   AI: {response}")
    
    # Test calculation tool
    print("\n4. 测试计算工具...")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "帮我计算 123 + 456"}]},
        config={"configurable": {"thread_id": "test_1"}}
    )
    
    last_message = result["messages"][-1]
    response = last_message.content if hasattr(last_message, "content") else str(last_message)
    print(f"   用户: 帮我计算 123 + 456")
    print(f"   AI: {response}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_agent()

