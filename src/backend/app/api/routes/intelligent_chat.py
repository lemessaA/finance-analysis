"""
Intelligent Chat Interface API Routes

This module provides REST API endpoints for:
- Natural language database queries
- Multi-turn conversations with context
- Data visualization generation
- Query suggestions and insights
- Conversation export and management
"""

from __future__ import annotations

import uuid
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field

from app.agents.chat_agent import intelligent_chat_agent, ChatResponse
from app.agents.database_agent import database_agent
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


# Request/Response Models
class ChatMessageRequest(BaseModel):
    """Request model for chat message."""
    session_id: str = Field(..., description="Session ID for conversation")
    message: str = Field(..., description="User message")
    include_visualization: bool = Field(True, description="Include data visualization suggestions")
    database_id: Optional[str] = Field(None, description="Database ID to use")


class ChatSessionRequest(BaseModel):
    """Request model for creating chat session."""
    database_id: str = Field(..., description="Database ID to connect to")
    session_name: Optional[str] = Field(None, description="Optional session name")


class QuerySuggestionRequest(BaseModel):
    """Request model for query suggestions."""
    session_id: str = Field(..., description="Session ID")
    context: Optional[str] = Field(None, description="Additional context for suggestions")


class ExportRequest(BaseModel):
    """Request model for exporting conversation."""
    session_id: str = Field(..., description="Session ID")
    format: str = Field("json", description="Export format: json, csv, pdf")


# Helper functions
def generate_session_id() -> str:
    """Generate unique session ID."""
    return str(uuid.uuid4())


# API Endpoints
@router.post("/sessions", response_model=Dict[str, Any])
async def create_chat_session(session_request: ChatSessionRequest):
    """
    Create a new chat session with database connection.
    
    This endpoint initializes a conversation session and connects to the specified database.
    """
    try:
        session_id = generate_session_id()
        
        # Initialize database context
        await intelligent_chat_agent.initialize_database_context(session_id, session_request.database_id)
        
        # Get database info
        db_config = await database_agent.get_database_config(session_request.database_id)
        if not db_config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database configuration not found"
            )
        
        logger.info(f"Created chat session {session_id} for database {db_config.name}")
        
        return {
            "success": True,
            "session_id": session_id,
            "database_name": db_config.name,
            "database_type": db_config.type,
            "session_name": session_request.session_name or f"Chat Session {session_id[:8]}",
            "created_at": str(uuid.uuid4())  # Using as timestamp placeholder
        }
        
    except ValueError as e:
        logger.error(f"Error creating chat session: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating chat session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chat session: {str(e)}"
        )


@router.post("/chat", response_model=Dict[str, Any])
async def send_message(message_request: ChatMessageRequest):
    """
    Send a message to the intelligent chat interface.
    
    This endpoint processes natural language queries and returns intelligent responses with data insights.
    """
    try:
        # Process message
        response = await intelligent_chat_agent.process_message(
            session_id=message_request.session_id,
            user_query=message_request.message,
            include_visualization=message_request.include_visualization
        )
        
        # Prepare response
        response_data = {
            "success": True,
            "session_id": message_request.session_id,
            "message": response.message,
            "confidence_score": response.confidence_score
        }
        
        # Add data if available
        if response.data:
            response_data["data"] = response.data
            response_data["query_info"] = response.query_info
        
        # Add visualization if available
        if response.visualization:
            response_data["visualization"] = response.visualization
        
        # Add suggestions
        if response.suggestions:
            response_data["suggestions"] = response.suggestions
        
        # Add follow-up questions
        if response.follow_up_questions:
            response_data["follow_up_questions"] = response.follow_up_questions
        
        # Add context information
        if response.context_used:
            response_data["context_used"] = response.context_used
        
        logger.info(f"Processed chat message for session {message_request.session_id}")
        
        return response_data
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.get("/sessions/{session_id}/summary", response_model=Dict[str, Any])
async def get_session_summary(session_id: str):
    """Get summary of chat session."""
    try:
        summary = await intelligent_chat_agent.get_conversation_summary(session_id)
        
        return {
            "success": True,
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"Error getting session summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session summary: {str(e)}"
        )


@router.get("/sessions/{session_id}/history", response_model=Dict[str, Any])
async def get_conversation_history(session_id: str, limit: int = 50):
    """Get conversation history for session."""
    try:
        conversation = intelligent_chat_agent.get_or_create_conversation(session_id)
        
        messages = []
        for msg in conversation.messages[-limit:]:
            messages.append({
                "type": "human" if hasattr(msg, 'content') and not hasattr(msg, 'additional_kwargs') else "ai",
                "content": msg.content,
                "timestamp": str(uuid.uuid4())  # Using as timestamp placeholder
            })
        
        return {
            "success": True,
            "session_id": session_id,
            "messages": messages,
            "total_messages": len(conversation.messages),
            "query_count": len(conversation.query_history)
        }
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation history: {str(e)}"
        )


@router.post("/sessions/{session_id}/suggestions", response_model=Dict[str, Any])
async def get_query_suggestions(session_id: str, request: QuerySuggestionRequest):
    """Get AI-powered query suggestions."""
    try:
        conversation = intelligent_chat_agent.get_or_create_conversation(session_id)
        
        # Generate suggestions
        suggestions = await intelligent_chat_agent._generate_suggestions(conversation)
        
        return {
            "success": True,
            "session_id": session_id,
            "suggestions": suggestions,
            "context": {
                "database_connected": intelligent_chat_agent.current_database is not None,
                "tables_available": len(conversation.database_context.get("tables", [])),
                "previous_queries": len(conversation.query_history)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting query suggestions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get suggestions: {str(e)}"
        )


@router.post("/sessions/{session_id}/export", response_model=Dict[str, Any])
async def export_conversation(session_id: str, export_request: ExportRequest):
    """Export conversation history and results."""
    try:
        export_data = await intelligent_chat_agent.export_conversation(
            session_id, 
            export_request.format
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "format": export_request.format,
            "export_data": export_data
        }
        
    except Exception as e:
        logger.error(f"Error exporting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export conversation: {str(e)}"
        )


@router.delete("/sessions/{session_id}", response_model=Dict[str, Any])
async def clear_conversation(session_id: str):
    """Clear conversation history for session."""
    try:
        success = await intelligent_chat_agent.clear_conversation(session_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        logger.info(f"Cleared conversation for session {session_id}")
        
        return {
            "success": True,
            "message": "Conversation cleared successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear conversation: {str(e)}"
        )


@router.get("/sessions/{session_id}/context", response_model=Dict[str, Any])
async def get_database_context(session_id: str):
    """Get current database context for session."""
    try:
        conversation = intelligent_chat_agent.get_or_create_conversation(session_id)
        
        return {
            "success": True,
            "session_id": session_id,
            "database_context": conversation.database_context,
            "current_database": intelligent_chat_agent.current_database,
            "session_duration": str(uuid.uuid4())  # Using as placeholder
        }
        
    except Exception as e:
        logger.error(f"Error getting database context: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get database context: {str(e)}"
        )


@router.post("/sessions/{session_id}/visualize", response_model=Dict[str, Any])
async def generate_visualization(session_id: str, data: Dict[str, Any]):
    """Generate data visualization for query results."""
    try:
        # This would integrate with a charting library
        # For now, return a placeholder response
        
        return {
            "success": True,
            "session_id": session_id,
            "visualization": {
                "chart_type": data.get("chart_type", "bar"),
                "title": data.get("title", "Data Visualization"),
                "data": data.get("data", []),
                "chart_config": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "plugins": {
                        "legend": {
                            "position": "top"
                        }
                    }
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate visualization: {str(e)}"
        )


@router.get("/capabilities", response_model=Dict[str, Any])
async def get_chat_capabilities():
    """Get chat interface capabilities and features."""
    try:
        capabilities = {
            "query_types": [
                {
                    "type": "select",
                    "description": "Basic data retrieval",
                    "examples": ["Show all users", "Get recent orders"]
                },
                {
                    "type": "aggregate",
                    "description": "Data aggregation and summaries",
                    "examples": ["Total sales by month", "Average order value"]
                },
                {
                    "type": "analytical",
                    "description": "Complex analytical queries",
                    "examples": ["Top performing products", "Customer segmentation analysis"]
                }
            ],
            "visualization_types": [
                {"type": "bar", "description": "Bar charts for comparisons"},
                {"type": "line", "description": "Line charts for trends"},
                {"type": "pie", "description": "Pie charts for proportions"},
                {"type": "scatter", "description": "Scatter plots for correlations"},
                {"type": "area", "description": "Area charts for cumulative data"}
            ],
            "export_formats": ["json", "csv", "pdf"],
            "features": [
                "Natural language to SQL conversion",
                "Context-aware responses",
                "Multi-turn conversations",
                "Data visualization suggestions",
                "Query suggestions",
                "Conversation export",
                "Real-time database access"
            ],
            "supported_databases": [
                "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Oracle", "SQL Server"
            ]
        }
        
        return {
            "success": True,
            "capabilities": capabilities
        }
        
    except Exception as e:
        logger.error(f"Error getting chat capabilities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get capabilities: {str(e)}"
        )


@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check for chat interface."""
    try:
        return {
            "success": True,
            "status": "healthy",
            "active_sessions": len(intelligent_chat_agent.conversations),
            "current_database": intelligent_chat_agent.current_database,
            "agent_status": "operational"
        }
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }
