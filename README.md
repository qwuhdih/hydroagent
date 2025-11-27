# HydroAgent

A LangGraph-based intelligent agent system with modular architecture.

## Project Structure

```
hydroagent/
├── .env                       # 环境变量 (API Keys, DB URL)
├── .gitignore
├── pyproject.toml             # 依赖管理
├── README.md
├── docker-compose.yml         # 部署数据库、Redis等依赖
├── notebooks/                 # 实验和原型验证用的 Jupyter Notebooks
│   └── prototype_v1.ipynb
├── tests/                     # 测试代码
│   ├── unit/                  # 单元测试
│   └── integration/           # 集成测试
└── src/                       # 核心源码目录
    ├── __init__.py
    ├── config.py              # 全局配置加载
    ├── main.py                # 入口文件
    ├── agent/                 # 智能体逻辑层
    │   ├── __init__.py
    │   ├── graph.py           # 定义图结构
    │   ├── nodes.py           # 定义具体的节点逻辑
    │   ├── state.py           # 定义状态 Schema
    │   └── utils.py           # 智能体专用的辅助函数
    ├── tools/                 # 工具层 (Function Calling)
    │   ├── __init__.py
    │   ├── base.py            # 工具基类或装饰器
    │   ├── search_tools.py    # 搜索工具
    │   ├── data_tools.py      # 数据库查询工具
    │   └── api_tools.py       # 外部API调用工具
    ├── prompts/               # 提示词管理
    │   ├── __init__.py
    │   ├── templates/         # 提示词模板
    │   │   ├── system_prompt.yaml
    │   │   └── planner_prompt.txt
    │   └── loader.py          # 加载和渲染提示词的逻辑
    ├── models/                # 数据模型层
    │   ├── __init__.py
    │   ├── schemas.py         # Pydantic 模型
    │   └── db.py              # 数据库连接逻辑
    └── storage/               # 记忆与持久化
        ├── checkpointer.py    # LangGraph Checkpointer 配置
        └── memory.py          # 长期记忆 (RAG) 的逻辑
```

## Setup

### Prerequisites

- Python 3.10+
- Poetry or uv (for dependency management)
- Docker and Docker Compose (for local development)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hydroagent
```

2. Install dependencies:
```bash
#conda环境
pip install -e .
# Or using uv
uv pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. Start dependencies (PostgreSQL, Redis):
```bash
docker-compose up -d
```

5. Run the application:
```bash
# FastAPI server
uvicorn src.main:app --reload

# Or CLI
python -m src.main
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src tests
ruff check src tests
```

## License

MIT

