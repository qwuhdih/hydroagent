"""Main entry point for the HydroAgent application."""

import asyncio
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.config import settings
from src.agent.graph import create_agent_graph

# FastAPI app
app = FastAPI(
    title="HydroAgent",
    description="A LangGraph-based intelligent agent system using official create_agent API",
    version="0.1.0",
)

# Global agent instance (avoid recreating on each request)
_agent = None


def get_agent():
    """Get or create agent instance.
    
    Returns:
        Agent instance
    """
    global _agent
    if _agent is None:
        _agent = create_agent_graph()
    return _agent


class AgentRequest(BaseModel):
    """Request model for agent invocation."""

    message: str
    session_id: Optional[str] = None


class AgentResponse(BaseModel):
    """Response model for agent invocation."""

    response: str
    session_id: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "HydroAgent",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
        "description": "Using official LangChain create_agent API",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/agent/invoke", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    """Invoke the agent with a message.
    
    This endpoint uses the official LangChain create_agent API,
    which automatically handles tool calling and state management.
    """
    try:
        agent = get_agent()
        session_id = request.session_id or "default"

        # Use official recommended invoke way
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config={"configurable": {"thread_id": session_id}},
        )

        # Get the last message content
        messages = result.get("messages", [])
        if not messages:
            raise ValueError("No messages in response")
        
        last_message = messages[-1]
        
        # Extract content from message
        if hasattr(last_message, "content"):
            response_text = last_message.content
        elif isinstance(last_message, dict):
            response_text = last_message.get("content", str(last_message))
        else:
            response_text = str(last_message)

        return AgentResponse(
            response=response_text,
            session_id=session_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
    )
