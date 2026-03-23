"""
Database Configuration API Routes

This module provides REST API endpoints for:
- Database connection management
- Schema discovery
- Connection testing
- Multi-database support
"""

from __future__ import annotations

import uuid
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field, validator

from app.agents.database_agent import database_agent, DatabaseConfig, DatabaseType, ConnectionStatus
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


# Request/Response Models
class DatabaseConfigRequest(BaseModel):
    """Request model for database configuration."""
    name: str = Field(..., description="Database configuration name")
    type: str = Field(..., description="Database type (postgresql, mysql, sqlite, etc.)")
    host: Optional[str] = Field(None, description="Database host")
    port: Optional[int] = Field(None, description="Database port")
    database: str = Field(..., description="Database name or file path")
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")
    ssl_mode: Optional[str] = Field(None, description="SSL mode")
    connection_string: Optional[str] = Field(None, description="Full connection string (alternative to individual params)")
    is_active: bool = Field(True, description="Whether this configuration is active")
    
    @validator('type')
    def validate_database_type(cls, v):
        try:
            DatabaseType(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid database type: {v}. Valid types: {[t.value for t in DatabaseType]}")
    
    @validator('ssl_mode')
    def validate_ssl_mode(cls, v):
        if v is None:
            return v
        valid_modes = ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"]
        if v not in valid_modes:
            raise ValueError(f"Invalid SSL mode: {v}. Valid options: {', '.join(valid_modes)}")
        return v


class DatabaseConfigUpdate(BaseModel):
    """Request model for updating database configuration."""
    name: Optional[str] = Field(None, description="Database configuration name")
    host: Optional[str] = Field(None, description="Database host")
    port: Optional[int] = Field(None, description="Database port")
    database: Optional[str] = Field(None, description="Database name or file path")
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")
    ssl_mode: Optional[str] = Field(None, description="SSL mode")
    connection_string: Optional[str] = Field(None, description="Full connection string")
    is_active: Optional[bool] = Field(None, description="Whether this configuration is active")


class QueryRequest(BaseModel):
    """Request model for executing queries."""
    query: str = Field(..., description="SQL query to execute")
    database_id: str = Field(..., description="Database configuration ID")


class ConnectionTestRequest(BaseModel):
    """Request model for connection testing."""
    name: str = Field(..., description="Database configuration name")
    type: str = Field(..., description="Database type")
    host: Optional[str] = Field(None, description="Database host")
    port: Optional[int] = Field(None, description="Database port")
    database: str = Field(..., description="Database name")
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")
    ssl_mode: Optional[str] = Field(None, description="SSL mode")
    connection_string: Optional[str] = Field(None, description="Full connection string")


# Helper functions
def config_to_dict(config: DatabaseConfig) -> Dict[str, Any]:
    """Convert DatabaseConfig to dictionary (excluding sensitive data)."""
    data = {
        "id": config.id,
        "name": config.name,
        "type": config.type.value,
        "host": config.host,
        "port": config.port,
        "database": config.database,
        "username": config.username,
        "password": "***" if config.password else None,  # Hide password
        "ssl_mode": config.ssl_mode,
        "connection_string": "***" if config.connection_string else None,  # Hide if contains password
        "is_active": config.is_active,
        "created_at": config.created_at,
        "last_tested": config.last_tested,
        "status": config.status.value
    }
    return data


# API Endpoints
@router.post("/configurations", response_model=Dict[str, Any])
async def add_database_configuration(config_data: DatabaseConfigRequest):
    """
    Add a new database configuration.
    
    This endpoint creates a new database connection configuration and tests the connection.
    """
    try:
        # Generate ID
        config_data_dict = config_data.dict()
        config_data_dict["id"] = str(uuid.uuid4())
        config_data_dict["created_at"] = str(uuid.uuid4())  # Using as timestamp placeholder
        
        # Add configuration
        config = await database_agent.add_database_config(config_data_dict)
        
        logger.info(f"Added database configuration: {config.name}")
        
        return {
            "success": True,
            "message": f"Database configuration '{config.name}' added successfully",
            "configuration": config_to_dict(config)
        }
        
    except ValueError as e:
        logger.error(f"Validation error adding database config: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error adding database configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add database configuration: {str(e)}"
        )


@router.get("/configurations", response_model=Dict[str, Any])
async def get_database_configurations():
    """Get all database configurations."""
    try:
        configs = await database_agent.get_database_configurations()
        
        return {
            "success": True,
            "configurations": [config_to_dict(config) for config in configs],
            "total_count": len(configs)
        }
        
    except Exception as e:
        logger.error(f"Error getting database configurations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get database configurations: {str(e)}"
        )


@router.get("/configurations/{config_id}", response_model=Dict[str, Any])
async def get_database_configuration(config_id: str):
    """Get specific database configuration."""
    try:
        config = await database_agent.get_database_config(config_id)
        
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database configuration not found"
            )
        
        return {
            "success": True,
            "configuration": config_to_dict(config)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting database configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get database configuration: {str(e)}"
        )


@router.put("/configurations/{config_id}", response_model=Dict[str, Any])
async def update_database_configuration(config_id: str, updates: DatabaseConfigUpdate):
    """Update database configuration."""
    try:
        # Filter out None values
        update_data = {k: v for k, v in updates.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        config = await database_agent.update_database_config(config_id, update_data)
        
        logger.info(f"Updated database configuration: {config.name}")
        
        return {
            "success": True,
            "message": f"Database configuration '{config.name}' updated successfully",
            "configuration": config_to_dict(config)
        }
        
    except ValueError as e:
        logger.error(f"Validation error updating database config: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating database configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update database configuration: {str(e)}"
        )


@router.delete("/configurations/{config_id}", response_model=Dict[str, Any])
async def delete_database_configuration(config_id: str):
    """Delete database configuration."""
    try:
        success = await database_agent.remove_database_config(config_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database configuration not found"
            )
        
        logger.info(f"Deleted database configuration: {config_id}")
        
        return {
            "success": True,
            "message": "Database configuration deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting database configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete database configuration: {str(e)}"
        )


@router.post("/test-connection", response_model=Dict[str, Any])
async def test_database_connection(test_data: ConnectionTestRequest):
    """
    Test database connection without saving configuration.
    
    This endpoint tests connection parameters and returns detailed results including schema information.
    """
    try:
        # Create temporary config for testing
        temp_config = DatabaseConfig(
            id="test",
            name=test_data.name,
            type=DatabaseType(test_data.type),
            host=test_data.host,
            port=test_data.port,
            database=test_data.database,
            username=test_data.username,
            password=test_data.password,
            ssl_mode=test_data.ssl_mode,
            connection_string=test_data.connection_string,
            is_active=False
        )
        
        # Test connection
        result = await database_agent.test_connection(temp_config)
        
        # Prepare response
        response_data = {
            "success": result.success,
            "message": result.message,
            "response_time_ms": result.response_time_ms
        }
        
        if result.error_details:
            response_data["error_details"] = result.error_details
        
        if result.schema_info:
            response_data["schema_info"] = [
                {
                    "table_name": table.table_name,
                    "columns": table.columns,
                    "row_count": table.row_count,
                    "indexes": table.indexes,
                    "foreign_keys": table.foreign_keys,
                    "primary_keys": table.primary_keys
                }
                for table in result.schema_info
            ]
            response_data["table_count"] = len(result.schema_info)
        
        logger.info(f"Connection test for {test_data.name}: {'Success' if result.success else 'Failed'}")
        
        return response_data
        
    except ValueError as e:
        logger.error(f"Validation error testing connection: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error testing database connection: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to test connection: {str(e)}"
        )


@router.post("/test-connection/{config_id}", response_model=Dict[str, Any])
async def test_existing_connection(config_id: str):
    """Test existing database configuration."""
    try:
        config = await database_agent.get_database_config(config_id)
        
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database configuration not found"
            )
        
        # Test connection
        result = await database_agent.test_connection(config)
        
        response_data = {
            "success": result.success,
            "message": result.message,
            "response_time_ms": result.response_time_ms,
            "configuration": config_to_dict(config)
        }
        
        if result.error_details:
            response_data["error_details"] = result.error_details
        
        logger.info(f"Connection test for existing config {config_id}: {'Success' if result.success else 'Failed'}")
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error testing existing connection: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to test connection: {str(e)}"
        )


@router.post("/switch/{config_id}", response_model=Dict[str, Any])
async def switch_database(config_id: str):
    """Switch to a different database configuration."""
    try:
        config = await database_agent.switch_database(config_id)
        
        logger.info(f"Switched to database: {config.name}")
        
        return {
            "success": True,
            "message": f"Switched to database '{config.name}'",
            "configuration": config_to_dict(config)
        }
        
    except ValueError as e:
        logger.error(f"Error switching database: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error switching database: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to switch database: {str(e)}"
        )


@router.post("/query", response_model=Dict[str, Any])
async def execute_query(query_request: QueryRequest):
    """Execute a query on the specified database."""
    try:
        # Validate query for safety (basic SQL injection prevention)
        query = query_request.query.strip()
        
        # Basic safety checks
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE"]
        query_upper = query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Query contains potentially dangerous keyword: {keyword}. Only SELECT queries are allowed."
                )
        
        if not query_upper.startswith("SELECT"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only SELECT queries are allowed for security reasons."
            )
        
        # Execute query
        result = await database_agent.execute_query(query_request.database_id, query)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Query execution failed: {result.get('error', 'Unknown error')}"
            )
        
        logger.info(f"Executed query on database {query_request.database_id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute query: {str(e)}"
        )


@router.get("/stats/{config_id}", response_model=Dict[str, Any])
async def get_database_statistics(config_id: str):
    """Get database statistics."""
    try:
        stats = await database_agent.get_database_stats(config_id)
        
        return {
            "success": True,
            "statistics": stats
        }
        
    except ValueError as e:
        logger.error(f"Error getting database stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting database statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get database statistics: {str(e)}"
        )


@router.post("/validate-parameters", response_model=Dict[str, Any])
async def validate_connection_parameters(config_data: DatabaseConfigRequest):
    """Validate connection parameters without testing connection."""
    try:
        validation_result = await database_agent.validate_connection_parameters(config_data.dict())
        
        return validation_result
        
    except Exception as e:
        logger.error(f"Error validating connection parameters: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate parameters: {str(e)}"
        )


@router.get("/supported-types", response_model=Dict[str, Any])
async def get_supported_database_types():
    """Get list of supported database types with default ports."""
    try:
        supported_types = []
        
        for db_type in DatabaseType:
            type_info = {
                "value": db_type.value,
                "name": db_type.value.title(),
                "description": f"{db_type.value.title()} database support"
            }
            
            # Add default port for non-SQLite databases
            if db_type != DatabaseType.SQLITE:
                type_info["default_port"] = database_agent.default_ports.get(db_type)
            
            supported_types.append(type_info)
        
        return {
            "success": True,
            "supported_types": supported_types
        }
        
    except Exception as e:
        logger.error(f"Error getting supported database types: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get supported database types: {str(e)}"
        )


@router.get("/ssl-modes", response_model=Dict[str, Any])
async def get_ssl_modes():
    """Get available SSL modes."""
    try:
        ssl_modes = [
            {"value": "disable", "description": "No SSL"},
            {"value": "allow", "description": "Allow SSL if server wants it"},
            {"value": "prefer", "description": "Prefer SSL, but allow non-SSL"},
            {"value": "require", "description": "Require SSL"},
            {"value": "verify-ca", "description": "Require SSL and verify CA certificate"},
            {"value": "verify-full", "description": "Require SSL and verify full certificate chain"}
        ]
        
        return {
            "success": True,
            "ssl_modes": ssl_modes
        }
        
    except Exception as e:
        logger.error(f"Error getting SSL modes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get SSL modes: {str(e)}"
        )
