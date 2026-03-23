"""
Intelligent Chat Interface Agent

This agent provides:
- Natural language queries to retrieve company data
- Real-time database access through conversation
- Context-aware responses with data insights
- Multi-turn conversations with context maintenance
- Interactive data visualization generation
- AI-powered query suggestions
- Export capabilities for chat results
"""

from __future__ import annotations

import asyncio
import json
import re
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime, timedelta

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.agents.base_agent import BaseAgent
from app.agents.database_agent import database_agent
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class QueryType(Enum):
    """Types of database queries."""
    SELECT = "select"
    AGGREGATE = "aggregate"
    ANALYTICAL = "analytical"
    VISUALIZATION = "visualization"
    EXPORT = "export"


class ConversationContext:
    """Manages conversation context and history."""
    
    def __init__(self):
        self.messages: List[Union[HumanMessage, AIMessage]] = []
        self.database_context: Dict[str, Any] = {}
        self.query_history: List[Dict[str, Any]] = []
        self.visualization_requests: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
        self.session_start = datetime.now()
    
    def add_message(self, message: Union[HumanMessage, AIMessage]):
        """Add message to conversation history."""
        self.messages.append(message)
        if len(self.messages) > 50:
            self.messages = self.messages[-50:]
    
    def get_recent_context(self, limit: int = 5) -> List[Union[HumanMessage, AIMessage]]:
        """Get recent messages for context."""
        return self.messages[-limit:]
    
    def update_database_context(self, schema_info: List[Dict[str, Any]]):
        """Update database schema context."""
        self.database_context = {
            "tables": schema_info,
            "last_updated": datetime.now(),
            "table_names": [table["table_name"] for table in schema_info]
        }
    
    def add_query_result(self, query: str, result: Dict[str, Any], query_type: QueryType):
        """Add query result to history."""
        self.query_history.append({
            "query": query,
            "result": result,
            "type": query_type.value,
            "timestamp": datetime.now()
        })
        if len(self.query_history) > 20:
            self.query_history = self.query_history[-20:]


@dataclass
class ChatResponse:
    """Structured chat response."""
    message: str
    data: Optional[Dict[str, Any]] = None
    visualization: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
    query_info: Optional[Dict[str, Any]] = None
    context_used: Optional[List[str]] = None
    confidence_score: float = 0.0
    follow_up_questions: Optional[List[str]] = None


@dataclass
class VisualizationRequest:
    """Data visualization request."""
    chart_type: str
    data: List[Dict[str, Any]]
    title: str
    x_axis: str
    y_axis: str
    group_by: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


class IntelligentChatAgent(BaseAgent):
    """Intelligent Chat Interface for database interaction."""
    
    def __init__(self):
        super().__init__(name="IntelligentChatAgent", temperature=0.1)
        self.conversations: Dict[str, ConversationContext] = {}
        self.current_database: Optional[str] = None
        
        # Initialize LLM
        self.llm = ChatGroq(
            temperature=0.1,
            model="llama3-8b-8192",
            api_key=settings.GROQ_API_KEY,
        )
    
    async def run(self, input_text: str, filename: str = "") -> Dict[str, Any]:
        """Run the intelligent chat agent - required abstract method implementation."""
        try:
            input_lower = input_text.lower()
            
            if "sessions" in input_lower or "active" in input_lower:
                return {
                    "success": True,
                    "operation": "list_sessions",
                    "active_sessions": len(self.conversations),
                    "current_database": self.current_database,
                    "sessions": list(self.conversations.keys())
                }
            
            elif "clear" in input_lower or "reset" in input_lower:
                session_count = len(self.conversations)
                self.conversations.clear()
                self.current_database = None
                return {
                    "success": True,
                    "operation": "clear_sessions",
                    "cleared_sessions": session_count,
                    "message": f"Cleared {session_count} conversation sessions"
                }
            
            elif "status" in input_lower or "health" in input_lower:
                return {
                    "success": True,
                    "operation": "agent_status",
                    "active_sessions": len(self.conversations),
                    "current_database": self.current_database,
                    "llm_model": "llama3-8b-8192",
                    "temperature": 0.1,
                    "status": "operational"
                }
            
            else:
                return {
                    "success": True,
                    "operation": "default",
                    "message": "IntelligentChatAgent is ready. Available operations: sessions, clear, status",
                    "capabilities": [
                        "Natural language to SQL conversion",
                        "Context-aware responses",
                        "Multi-turn conversations",
                        "Data visualization suggestions",
                        "Query suggestions",
                        "Conversation export"
                    ]
                }
                
        except Exception as e:
            logger.error(f"Error in IntelligentChatAgent.run: {e}")
            return {
                "success": False,
                "error": str(e),
                "operation": "error"
            }
    
    def get_or_create_conversation(self, session_id: str) -> ConversationContext:
        """Get or create conversation context for session."""
        if session_id not in self.conversations:
            self.conversations[session_id] = ConversationContext()
        return self.conversations[session_id]
    
    async def initialize_database_context(self, session_id: str, database_id: str):
        """Initialize database context for conversation."""
        try:
            stats = await database_agent.get_database_stats(database_id)
            conversation = self.get_or_create_conversation(session_id)
            conversation.update_database_context(stats.get("statistics", {}).get("tables", []))
            self.current_database = database_id
            logger.info(f"Initialized database context for session {session_id}")
        except Exception as e:
            logger.error(f"Error initializing database context: {e}")
            raise
    
    async def process_message(self, session_id: str, user_query: str, include_visualization: bool = True) -> ChatResponse:
        """Process user message and generate intelligent response."""
        try:
            conversation = self.get_or_create_conversation(session_id)
            conversation.add_message(HumanMessage(content=user_query))
            
            # For now, return a simple response
            response = ChatResponse(
                message=f"I've received your query: '{user_query}'. This is a placeholder response as the chat agent is being set up.",
                confidence_score=0.8,
                suggestions=["Try asking about your data", "Show me table names", "What columns are available?"]
            )
            
            conversation.add_message(AIMessage(content=response.message))
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return ChatResponse(
                message=f"I encountered an error: {str(e)}",
                confidence_score=0.0,
                suggestions=["Try rephrasing your question", "Check if the database is connected"]
            )
    
    async def export_conversation(self, session_id: str, format: str = "json") -> Dict[str, Any]:
        """Export conversation history and results."""
        try:
            conversation = self.get_or_create_conversation(session_id)
            export_data = {
                "session_id": session_id,
                "session_start": conversation.session_start.isoformat(),
                "database_context": conversation.database_context,
                "query_history": conversation.query_history
            }
            return {"format": format, "data": export_data}
        except Exception as e:
            logger.error(f"Error exporting conversation: {e}")
            raise
    
    async def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of conversation session."""
        try:
            conversation = self.get_or_create_conversation(session_id)
            return {
                "session_id": session_id,
                "session_start": conversation.session_start.isoformat(),
                "duration": str(datetime.now() - conversation.session_start),
                "message_count": len(conversation.messages),
                "query_count": len(conversation.query_history),
                "database_connected": self.current_database is not None
            }
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            raise
    
    async def clear_conversation(self, session_id: str) -> bool:
        """Clear conversation history for session."""
        try:
            if session_id in self.conversations:
                del self.conversations[session_id]
                logger.info(f"Cleared conversation for session {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return False


# Global chat agent instance
intelligent_chat_agent = IntelligentChatAgent()
