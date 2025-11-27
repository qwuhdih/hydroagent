"""Pydantic schemas for data validation."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AgentRequest(BaseModel):
    """Request schema for agent invocation."""

    message: str = Field(..., description="User message to process")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class AgentResponse(BaseModel):
    """Response schema for agent invocation."""

    response: str = Field(..., description="Agent's response message")
    session_id: str = Field(..., description="Session ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ToolCall(BaseModel):
    """Schema for tool call information."""

    tool_name: str = Field(..., description="Name of the tool to call")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters")
    result: Optional[Any] = Field(None, description="Tool execution result")


class ConversationMessage(BaseModel):
    """Schema for a conversation message."""

    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None


class Conversation(BaseModel):
    """Schema for a conversation session."""

    session_id: str = Field(..., description="Unique session identifier")
    messages: List[ConversationMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

