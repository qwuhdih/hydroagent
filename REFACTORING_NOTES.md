# 重构说明

## 重构内容

项目已按照 LangChain 官方推荐的方式重构，使用 `create_agent` API 替代手动构建 LangGraph。

## 主要变更

### 1. `src/agent/graph.py`
- ✅ 使用 `create_agent` API（官方推荐）
- ✅ 自动处理工具调用和状态管理
- ✅ 代码更简洁，从 50+ 行减少到 30+ 行
- ✅ 添加了导入错误处理

### 2. `src/main.py`
- ✅ 使用全局 agent 实例（避免重复创建）
- ✅ 保持 FastAPI 接口不变
- ✅ 改进错误处理

### 3. `src/tools/example_tools.py`（新增）
- ✅ 使用 `@tool` 装饰器创建工具
- ✅ 包含示例工具：天气查询、计算器、获取时间

### 4. `src/tools/__init__.py`
- ✅ 导出示例工具

## 依赖要求

确保安装了最新版本的 langchain：

```bash
pip install -U langchain langgraph
```

如果遇到 `ModuleNotFoundError: No module named 'langchain'`，请运行：

```bash
pip install -e .
```

## 使用方式

### 方式 1：通过 FastAPI（推荐）

```bash
# 启动服务器
python -m src.main

# 发送请求
curl -X POST "http://localhost:8000/agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "session_id": "user_123"}'
```

### 方式 2：直接使用 Python

```python
from src.agent.graph import create_agent_graph

# 创建 agent
agent = create_agent_graph()

# 调用
result = agent.invoke(
    {"messages": [{"role": "user", "content": "你好"}]},
    config={"configurable": {"thread_id": "test_1"}}
)

print(result["messages"][-1].content)
```

### 方式 3：测试脚本

```bash
python test_refactored_agent.py
```

## 优势

1. **代码更简洁**：使用官方 API，减少手动管理
2. **自动工具调用**：无需手动处理工具调用逻辑
3. **更好的维护性**：遵循官方最佳实践
4. **向后兼容**：FastAPI 接口保持不变

## 配置

确保 `.env` 文件中配置了 API Key：

```env
CSTCLOUD_API_KEY=your-api-key
CSTCLOUD_BASE_URL=https://uni-api.cstcloud.cn/v1
CSTCLOUD_MODEL=deepseek-r1:671b
```

## 故障排除

### 问题：ModuleNotFoundError: No module named 'langchain'

**解决方案**：
```bash
pip install -U langchain langgraph
```

### 问题：ImportError: create_agent is not available

**解决方案**：
确保安装了最新版本的 langchain：
```bash
pip install -U "langchain>=0.3.0"
```

## 下一步

- 添加更多工具（在 `src/tools/example_tools.py`）
- 自定义系统提示词（在 `src/agent/graph.py`）
- 添加结构化输出（参考官方文档）
