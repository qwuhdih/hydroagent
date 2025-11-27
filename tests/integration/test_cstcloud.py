from src.config import settings
from langchain_openai import ChatOpenAI

# 检查配置
print(f"CSTCloud API Key: {settings.CSTCLOUD_API_KEY[:10]}..." if settings.CSTCLOUD_API_KEY else "未设置")
print(f"CSTCloud Base URL: {settings.CSTCLOUD_BASE_URL}")
print(f"CSTCloud Model: {settings.CSTCLOUD_MODEL}")

# 测试连接
if settings.CSTCLOUD_API_KEY:
    llm = ChatOpenAI(
        model=settings.CSTCLOUD_MODEL,
        api_key=settings.CSTCLOUD_API_KEY,
        base_url=settings.CSTCLOUD_BASE_URL,
    )
    response = llm.invoke("你好")
    print(f"响应: {response.content}")