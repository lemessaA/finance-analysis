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
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.memory import BaseMemory

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
        
        # Keep only last 50 messages to prevent memory issues
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
        
        # Keep only last 20 queries
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
        
        # Chat prompts
        self.system_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent database assistant that helps users interact with company data through natural language conversations.

Your capabilities:
- Convert natural language questions into SQL queries
- Analyze query results and provide insights
- Generate data visualizations
- Maintain conversation context
- Suggest follow-up questions
- Provide explanations and recommendations

Database Context:
{database_context}

Recent Conversation:
{recent_context}

Guidelines:
1. Always consider the database schema when generating queries
2. Provide clear explanations of your analysis
3. Suggest relevant visualizations for data insights
4. Maintain context across multiple questions
5. Ask clarifying questions if the query is ambiguous
6. Provide confidence scores for your responses
7. Generate follow-up questions based on the data

Respond in a helpful, conversational tone while providing accurate data insights."""),
            ("human", "{user_query}"),
        ])
        
        self.query_generation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a SQL expert. Convert natural language questions into SQL queries.

Database Schema:
{schema_info}

Rules:
1. Generate only valid SQL queries for the database type
2. Use appropriate table and column names from the schema
3. Include proper JOIN conditions if needed
4. Add LIMIT clauses for large datasets
5. Consider performance and use appropriate indexes
6. Handle NULL values properly
7. Return only the SQL query, no explanations

Examples:
Q: "Show me all users from California"
A: SELECT * FROM users WHERE state = 'CA' LIMIT 100;

Q: "What are our total sales by month?"
A: SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as total_sales FROM orders GROUP BY month ORDER BY month;

Schema: {schema_info}
Question: {question}
SQL:"),
            ("human", "{question}"),
        ])
        
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a data analyst. Analyze query results and provide insights.

Query: {query}
Results: {results}
Database Context: {database_context}

Provide:
1. Key insights from the data
2. Trends or patterns you notice
3. Recommendations based on the data
4. Potential follow-up questions
5. Confidence in your analysis (0-1)

Be concise but thorough in your analysis."""),
            ("human", "Analyze these results and provide insights."),
        ])
        
        self.visualization_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a data visualization expert. Suggest appropriate charts for the given data.

Data: {data}
Query: {query}
Context: {context}

Suggest:
1. Best chart type (bar, line, pie, scatter, area, donut)
2. X-axis and Y-axis recommendations
3. Grouping or filtering suggestions
4. Chart title and labels
5. Color recommendations

Return as JSON format:
{{
    "chart_type": "bar|line|pie|scatter|area|donut",
    "title": "Chart Title",
    "x_axis": "column_name",
    "y_axis": "column_name",
    "group_by": "column_name",
    "suggestions": ["suggestion1", "suggestion2"]
}}"""),
            ("human", "Suggest visualization for this data."),
        ])
        
        self.suggestions_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful database assistant. Suggest relevant questions based on the available data.

Database Schema: {schema_info}
Recent Queries: {recent_queries}
Current Context: {context}

Generate 5 relevant questions that:
1. Explore the available data meaningfully
2. Build upon previous conversations
3. Provide business value
4. Are answerable with the available data
5. Vary in complexity (simple to analytical)

Return as a JSON array of strings."""),
            ("human", "Suggest relevant questions for this database."),
        ])
    
    async def run(self, input_text: str, filename: str = "") -> Dict[str, Any]:
        """
        Run the intelligent chat agent - required abstract method implementation.
        
        For the IntelligentChatAgent, this method provides a simple interface for chat operations.
        """
        try:
            input_lower = input_text.lower()
            
            if "sessions" in input_lower or "active" in input_lower:
                # List active sessions
                return {
                    "success": True,
                    "operation": "list_sessions",
                    "active_sessions": len(self.conversations),
                    "current_database": self.current_database,
                    "sessions": list(self.conversations.keys())
                }
            
            elif "clear" in input_lower or "reset" in input_lower:
                # Clear all conversations
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
                # Get agent status
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
                # Default operation - return agent info
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
            # Get database schema
            stats = await database_agent.get_database_stats(database_id)
            
            # Update conversation context
            conversation = self.get_or_create_conversation(session_id)
            conversation.update_database_context(stats.get("statistics", {}).get("tables", []))
            
            self.current_database = database_id
            
            logger.info(f"Initialized database context for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error initializing database context: {e}")
            raise
    
    async def process_message(
        self, 
        session_id: str, 
        user_query: str,
        include_visualization: bool = True
    ) -> ChatResponse:
        """Process user message and generate intelligent response."""
        
        try:
            conversation = self.get_or_create_conversation(session_id)
            
            # Add user message to history
            conversation.add_message(HumanMessage(content=user_query))
            
            # Generate SQL query
            sql_query = await self._generate_sql_query(user_query, conversation)
            
            # Execute query
            query_result = await self._execute_query(sql_query)
            
            # Analyze results
            analysis = await self._analyze_results(user_query, query_result, conversation)
            
            # Generate visualization if requested
            visualization = None
            if include_visualization and query_result.get("success") and query_result.get("rows"):
                visualization = await self._suggest_visualization(query_result, user_query, conversation)
            
            # Generate suggestions
            suggestions = await self._generate_suggestions(conversation)
            
            # Generate follow-up questions
            follow_up_questions = await self._generate_follow_up_questions(user_query, query_result, conversation)
            
            # Create response
            response = ChatResponse(
                message=analysis.get("message", "I've processed your request."),
                data=query_result if query_result.get("success") else None,
                visualization=visualization,
                suggestions=suggestions,
                query_info={
                    "sql": sql_query,
                    "type": self._classify_query(sql_query),
                    "execution_time": query_result.get("execution_time")
                },
                context_used=self._extract_context_used(conversation),
                confidence_score=analysis.get("confidence", 0.8),
                follow_up_questions=follow_up_questions
            )
            
            # Add AI response to history
            conversation.add_message(AIMessage(content=response.message))
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            
            error_response = ChatResponse(
                message=f"I encountered an error while processing your request: {str(e)}",
                confidence_score=0.0,
                suggestions=["Try rephrasing your question", "Check if the database is connected"]
            )
            
            return error_response
    
    async def _generate_sql_query(self, user_query: str, conversation: ConversationContext) -> str:
        """Generate SQL query from natural language."""
        try:
            # Prepare schema information
            schema_info = json.dumps(conversation.database_context.get("tables", []), indent=2)
            
            # Generate query
            chain = self.query_generation_prompt | self.llm
            result = await chain.ainvoke({
                "schema_info": schema_info,
                "question": user_query
            })
            
            # Clean up the result
            sql_query = result.content.strip()
            
            # Remove any markdown formatting
            sql_query = re.sub(r'```sql\s*', '', sql_query)
            sql_query = re.sub(r'```\s*$', '', sql_query)
            
            # Basic validation
            if not sql_query or not sql_query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE')):
                raise ValueError("Generated query is not a valid SELECT query")
            
            return sql_query
            
        except Exception as e:
            logger.error(f"Error generating SQL query: {e}")
            raise
    
    async def _execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query on the current database."""
        try:
            if not self.current_database:
                raise ValueError("No database selected")
            
            start_time = asyncio.get_event_loop().time()
            
            # Execute query
            result = await database_agent.execute_query(self.current_database, sql_query)
            
            # Add execution time
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
            result["execution_time"] = execution_time
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return {
                "success": False,
                "error": str(e),
                "execution_time": 0
            }
    
    async def _analyze_results(
        self, 
        query: str, 
        result: Dict[str, Any], 
        conversation: ConversationContext
    ) -> Dict[str, Any]:
        """Analyze query results and generate insights."""
        try:
            if not result.get("success"):
                return {
                    "message": f"I couldn't retrieve the data: {result.get('error', 'Unknown error')}",
                    "confidence": 0.0
                }
            
            # Prepare analysis prompt
            chain = self.analysis_prompt | self.llm
            analysis_result = await chain.ainvoke({
                "query": query,
                "results": json.dumps(result.get("rows", [])[:10]),  # Limit to first 10 rows
                "database_context": json.dumps(conversation.database_context)
            })
            
            return {
                "message": analysis_result.content,
                "confidence": 0.8  # Default confidence
            }
            
        except Exception as e:
            logger.error(f"Error analyzing results: {e}")
            return {
                "message": f"Here are the results from your query: {len(result.get('rows', []))} rows returned.",
                "confidence": 0.6
            }
    
    async def _suggest_visualization(
        self, 
        result: Dict[str, Any], 
        query: str, 
        conversation: ConversationContext
    ) -> Optional[Dict[str, Any]]:
        """Suggest data visualization for query results."""
        try:
            if not result.get("rows") or len(result.get("rows", [])) == 0:
                return None
            
            # Prepare visualization prompt
            chain = self.visualization_prompt | self.llm
            viz_result = await chain.ainvoke({
                "data": json.dumps(result.get("rows", [])[:5]),  # Sample first 5 rows
                "query": query,
                "context": json.dumps(conversation.database_context)
            })
            
            # Parse JSON response
            try:
                viz_suggestion = json.loads(viz_result.content)
                
                return {
                    "chart_type": viz_suggestion.get("chart_type", "bar"),
                    "title": viz_suggestion.get("title", "Data Visualization"),
                    "x_axis": viz_suggestion.get("x_axis"),
                    "y_axis": viz_suggestion.get("y_axis"),
                    "group_by": viz_suggestion.get("group_by"),
                    "data": result.get("rows", []),
                    "suggestions": viz_suggestion.get("suggestions", [])
                }
                
            except json.JSONDecodeError:
                # Fallback visualization
                return {
                    "chart_type": "table",
                    "title": "Query Results",
                    "data": result.get("rows", []),
                    "suggestions": ["Try different chart types", "Add filters for better visualization"]
                }
            
        except Exception as e:
            logger.error(f"Error suggesting visualization: {e}")
            return None
    
    async def _generate_suggestions(self, conversation: ConversationContext) -> List[str]:
        """Generate relevant question suggestions."""
        try:
            # Prepare suggestions prompt
            chain = self.suggestions_prompt | self.llm
            
            recent_queries = [q["query"] for q in conversation.query_history[-5:]]
            
            result = await chain.ainvoke({
                "schema_info": json.dumps(conversation.database_context.get("tables", [])),
                "recent_queries": json.dumps(recent_queries),
                "context": json.dumps(conversation.database_context)
            })
            
            try:
                suggestions = json.loads(result.content)
                return suggestions if isinstance(suggestions, list) else []
            except json.JSONDecodeError:
                # Fallback suggestions
                return [
                    "Show me recent data trends",
                    "What are the key metrics?",
                    "Can you summarize the data?",
                    "Are there any outliers?",
                    "What insights can you provide?"
                ]
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return []
    
    async def _generate_follow_up_questions(
        self, 
        query: str, 
        result: Dict[str, Any], 
        conversation: ConversationContext
    ) -> List[str]:
        """Generate follow-up questions based on query and results."""
        try:
            if not result.get("success") or not result.get("rows"):
                return ["Try a different question", "Check the database connection"]
            
            # Generate contextual follow-up questions
            base_questions = [
                "Can you break this down by category?",
                "What are the trends over time?",
                "How does this compare to previous periods?",
                "What are the top performers?",
                "Are there any anomalies in the data?"
            ]
            
            # Select relevant questions based on query type
            query_lower = query.lower()
            relevant_questions = []
            
            if any(word in query_lower for word in ["total", "sum", "count"]):
                relevant_questions.extend([
                    "What's the average value?",
                    "How does this compare to last month?",
                    "What's the distribution like?"
                ])
            
            if any(word in query_lower for word in ["recent", "latest", "new"]):
                relevant_questions.extend([
                    "What were the results from the same period last year?",
                    "Is this trending up or down?",
                    "What factors might be influencing this?"
                ])
            
            # Add base questions if no specific ones
            if not relevant_questions:
                relevant_questions = base_questions[:3]
            
            return relevant_questions[:3]  # Return top 3 questions
            
        except Exception as e:
            logger.error(f"Error generating follow-up questions: {e}")
            return []
    
    def _classify_query(self, sql_query: str) -> str:
        """Classify the type of SQL query."""
        query_upper = sql_query.upper()
        
        if "GROUP BY" in query_upper or any(agg in query_upper for agg in ["SUM", "COUNT", "AVG", "MAX", "MIN"]):
            return "aggregate"
        elif "JOIN" in query_upper or query_upper.count("FROM") > 1:
            return "analytical"
        elif "LIMIT" in query_upper and "ORDER BY" in query_upper:
            return "select"
        else:
            return "basic"
    
    def _extract_context_used(self, conversation: ConversationContext) -> List[str]:
        """Extract context elements used in the conversation."""
        context_used = []
        
        if conversation.database_context.get("table_names"):
            context_used.append(f"Tables: {', '.join(conversation.database_context['table_names'][:3])}")
        
        if conversation.query_history:
            context_used.append(f"Previous queries: {len(conversation.query_history)}")
        
        if len(conversation.messages) > 2:
            context_used.append("Conversation history")
        
        return context_used
    
    async def export_conversation(
        self, 
        session_id: str, 
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export conversation history and results."""
        try:
            conversation = self.get_or_create_conversation(session_id)
            
            export_data = {
                "session_id": session_id,
                "session_start": conversation.session_start.isoformat(),
                "database_context": conversation.database_context,
                "messages": [
                    {
                        "type": "human" if isinstance(msg, HumanMessage) else "ai",
                        "content": msg.content,
                        "timestamp": datetime.now().isoformat()
                    }
                    for msg in conversation.messages
                ],
                "query_history": conversation.query_history,
                "visualization_requests": conversation.visualization_requests,
                "user_preferences": conversation.user_preferences
            }
            
            if format == "csv":
                # Convert to CSV format for query results
                csv_data = []
                for query_result in conversation.query_history:
                    if query_result.get("result", {}).get("success"):
                        rows = query_result["result"].get("rows", [])
                        if rows:
                            csv_data.extend(rows)
                
                return {
                    "format": "csv",
                    "data": csv_data,
                    "headers": list(csv_data[0].keys()) if csv_data else []
                }
            
            return {
                "format": format,
                "data": export_data
            }
            
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
                "successful_queries": len([q for q in conversation.query_history if q.get("result", {}).get("success")]),
                "tables_accessed": list(set(
                    table for query in conversation.query_history 
                    for table in query.get("result", {}).get("tables_accessed", [])
                )),
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
