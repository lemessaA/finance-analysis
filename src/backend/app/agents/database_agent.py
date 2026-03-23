"""
Database Configuration and Management Agent

This agent handles:
- Database connection setup and management
- Schema discovery and mapping
- Connection testing and validation
- Multi-database support
- Security and authentication management
"""

from __future__ import annotations

import asyncio
import json
import ssl
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from sqlalchemy import create_engine, text, inspect, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError, ProgrammingError
from sqlalchemy.pool import StaticPool

from app.agents.base_agent import BaseAgent
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseType(Enum):
    """Supported database types."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    ORACLE = "oracle"
    SQLSERVER = "sqlserver"


class ConnectionStatus(Enum):
    """Database connection status."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    TESTING = "testing"


@dataclass
class DatabaseConfig:
    """Database configuration model."""
    id: str
    name: str
    type: DatabaseType
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    ssl_mode: Optional[str] = None
    connection_string: Optional[str] = None
    is_active: bool = True
    created_at: Optional[str] = None
    last_tested: Optional[str] = None
    status: ConnectionStatus = ConnectionStatus.DISCONNECTED


@dataclass
class SchemaInfo:
    """Database schema information."""
    table_name: str
    columns: List[Dict[str, Any]]
    row_count: Optional[int] = None
    indexes: List[Dict[str, Any]] = None
    foreign_keys: List[Dict[str, Any]] = None
    primary_keys: List[str] = None


@dataclass
class ConnectionTestResult:
    """Connection test result."""
    success: bool
    message: str
    response_time_ms: Optional[float] = None
    error_details: Optional[str] = None
    schema_info: Optional[List[SchemaInfo]] = None


class DatabaseAgent(BaseAgent):
    """Database Configuration and Management Agent."""
    
    def __init__(self):
        super().__init__(name="DatabaseAgent", temperature=0.0)
        self.connections: Dict[str, Engine] = {}
        self.configs: Dict[str, DatabaseConfig] = {}
        self.default_ports = {
            DatabaseType.POSTGRESQL: 5432,
            DatabaseType.MYSQL: 3306,
            DatabaseType.SQLSERVER: 1433,
            DatabaseType.ORACLE: 1521
        }
    
    async def run(self, input_text: str, filename: str = "") -> Dict[str, Any]:
        """
        Run the database agent - required abstract method implementation.
        
        For the DatabaseAgent, this method provides a simple interface for database operations.
        """
        try:
            # Parse the input to determine the operation
            input_lower = input_text.lower()
            
            if "list" in input_lower or "show" in input_lower:
                # List database configurations
                configs = await self.get_database_configs()
                return {
                    "success": True,
                    "operation": "list_configurations",
                    "configurations": [asdict(config) for config in configs],
                    "count": len(configs)
                }
            
            elif "test" in input_lower:
                # Test all connections
                results = {}
                for config_id, config in self.configs.items():
                    result = await self.test_connection(config)
                    results[config_id] = {
                        "success": result.success,
                        "message": result.message,
                        "response_time_ms": result.response_time_ms
                    }
                
                return {
                    "success": True,
                    "operation": "test_connections",
                    "results": results
                }
            
            elif "stats" in input_lower:
                # Get statistics for all databases
                stats = {}
                for config_id in self.configs:
                    try:
                        stat = await self.get_database_stats(config_id)
                        stats[config_id] = stat
                    except Exception as e:
                        stats[config_id] = {"error": str(e)}
                
                return {
                    "success": True,
                    "operation": "database_statistics",
                    "statistics": stats
                }
            
            else:
                # Default operation - return available databases
                configs = await self.get_database_configs()
                return {
                    "success": True,
                    "operation": "default",
                    "message": "DatabaseAgent is ready. Available operations: list, test, stats",
                    "available_databases": len(configs)
                }
                
        except Exception as e:
            logger.error(f"Error in DatabaseAgent.run: {e}")
            return {
                "success": False,
                "error": str(e),
                "operation": "error"
            }
    
    def _build_connection_string(self, config: DatabaseConfig) -> str:
        """Build database connection string."""
        if config.connection_string:
            return config.connection_string
        
        if config.type == DatabaseType.SQLITE:
            return f"sqlite:///{config.database}"
        
        # Build connection string for SQL databases
        driver = {
            DatabaseType.POSTGRESQL: "postgresql+psycopg2",
            DatabaseType.MYSQL: "mysql+pymysql",
            DatabaseType.SQLSERVER: "mssql+pyodbc",
            DatabaseType.ORACLE: "oracle+cx_oracle"
        }.get(config.type.value, f"{config.type.value}+psycopg2")
        
        port = config.port or self.default_ports.get(config.type, 5432)
        
        connection_string = f"{driver}://{config.username}:{config.password}@{config.host}:{port}/{config.database}"
        
        # Add SSL configuration if specified
        if config.ssl_mode:
            connection_string += f"?sslmode={config.ssl_mode}"
        
        return connection_string
    
    def _create_engine(self, config: DatabaseConfig) -> Engine:
        """Create SQLAlchemy engine with appropriate settings."""
        connection_string = self._build_connection_string(config)
        
        engine_kwargs = {
            "echo": False,  # Set to True for SQL logging
            "pool_pre_ping": True,  # Test connections on checkout
        }
        
        # SQLite-specific settings
        if config.type == DatabaseType.SQLITE:
            engine_kwargs.update({
                "poolclass": StaticPool,
                "connect_args": {
                    "check_same_thread": False,
                    "timeout": 20
                }
            })
        else:
            # SSL and connection settings for other databases
            connect_args = {}
            if config.ssl_mode and config.ssl_mode != "disable":
                connect_args["ssl"] = {
                    "sslmode": config.ssl_mode,
                    "sslcert": None,  # Can be configured for client certificates
                    "sslkey": None,
                    "sslrootcert": None
                }
            
            if connect_args:
                engine_kwargs["connect_args"] = connect_args
            
            # Connection pool settings
            engine_kwargs.update({
                "pool_size": 5,
                "max_overflow": 10,
                "pool_timeout": 30,
                "pool_recycle": 3600  # Recycle connections every hour
            })
        
        return create_engine(connection_string, **engine_kwargs)
    
    async def test_connection(self, config: DatabaseConfig) -> ConnectionTestResult:
        """Test database connection and return detailed results."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Update status to testing
            config.status = ConnectionStatus.TESTING
            
            # Create engine
            engine = self._create_engine(config)
            
            # Test connection with timeout
            async with asyncio.timeout(30):  # 30 second timeout
                with engine.connect() as connection:
                    # Test basic query
                    result = connection.execute(text("SELECT 1"))
                    result.fetchone()
            
            response_time = (asyncio.get_event_loop().time() - start_time) * 1000
            
            # Discover schema
            schema_info = await self._discover_schema(engine)
            
            # Update config
            config.status = ConnectionStatus.CONNECTED
            config.last_tested = asyncio.get_event_loop().time()
            
            # Store connection
            self.connections[config.id] = engine
            self.configs[config.id] = config
            
            logger.info(f"Successfully connected to database {config.name}")
            
            return ConnectionTestResult(
                success=True,
                message=f"Connected successfully to {config.name}",
                response_time_ms=response_time,
                schema_info=schema_info
            )
            
        except OperationalError as e:
            error_msg = f"Connection failed: {str(e)}"
            config.status = ConnectionStatus.ERROR
            
            logger.error(f"Database connection failed for {config.name}: {e}")
            
            return ConnectionTestResult(
                success=False,
                message=error_msg,
                error_details=str(e)
            )
            
        except asyncio.TimeoutError:
            error_msg = "Connection timeout after 30 seconds"
            config.status = ConnectionStatus.ERROR
            
            logger.error(f"Database connection timeout for {config.name}")
            
            return ConnectionTestResult(
                success=False,
                message=error_msg,
                error_details="Connection timeout"
            )
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            config.status = ConnectionStatus.ERROR
            
            logger.error(f"Unexpected error connecting to {config.name}: {e}")
            
            return ConnectionTestResult(
                success=False,
                message=error_msg,
                error_details=str(e)
            )
    
    async def _discover_schema(self, engine: Engine) -> List[SchemaInfo]:
        """Discover database schema information."""
        try:
            inspector = inspect(engine)
            schema_info = []
            
            # Get all table names
            table_names = inspector.get_table_names()
            
            for table_name in table_names:
                try:
                    # Get column information
                    columns = []
                    for column in inspector.get_columns(table_name):
                        columns.append({
                            "name": column["name"],
                            "type": str(column["type"]),
                            "nullable": column.get("nullable", False),
                            "default": str(column.get("default", "")),
                            "auto_increment": column.get("autoincrement", False)
                        })
                    
                    # Get primary keys
                    primary_keys = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
                    
                    # Get indexes
                    indexes = []
                    for index in inspector.get_indexes(table_name):
                        indexes.append({
                            "name": index["name"],
                            "columns": index["column_names"],
                            "unique": index.get("unique", False)
                        })
                    
                    # Get foreign keys
                    foreign_keys = []
                    for fk in inspector.get_foreign_keys(table_name):
                        foreign_keys.append({
                            "constrained_columns": fk["constrained_columns"],
                            "referred_table": fk["referred_table"],
                            "referred_columns": fk["referred_columns"]
                        })
                    
                    # Get row count (sample query)
                    row_count = None
                    try:
                        with engine.connect() as conn:
                            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                            row_count = result.scalar()
                    except Exception:
                        # Skip row count if table is not accessible
                        pass
                    
                    schema_info.append(SchemaInfo(
                        table_name=table_name,
                        columns=columns,
                        row_count=row_count,
                        indexes=indexes,
                        foreign_keys=foreign_keys,
                        primary_keys=primary_keys
                    ))
                    
                except Exception as e:
                    logger.warning(f"Error discovering schema for table {table_name}: {e}")
                    continue
            
            return schema_info
            
        except Exception as e:
            logger.error(f"Error discovering schema: {e}")
            return []
    
    async def add_database_config(self, config_data: Dict[str, Any]) -> DatabaseConfig:
        """Add new database configuration."""
        try:
            # Validate required fields
            if not config_data.get("name") or not config_data.get("type"):
                raise ValueError("Name and database type are required")
            
            # Create config object
            config = DatabaseConfig(
                id=config_data.get("id", f"db_{len(self.configs) + 1}"),
                name=config_data["name"],
                type=DatabaseType(config_data["type"]),
                host=config_data.get("host"),
                port=config_data.get("port"),
                database=config_data.get("database"),
                username=config_data.get("username"),
                password=config_data.get("password"),
                ssl_mode=config_data.get("ssl_mode"),
                connection_string=config_data.get("connection_string"),
                is_active=config_data.get("is_active", True)
            )
            
            # Test connection
            test_result = await self.test_connection(config)
            
            if not test_result.success:
                raise ValueError(f"Connection test failed: {test_result.message}")
            
            logger.info(f"Added database configuration: {config.name}")
            return config
            
        except Exception as e:
            logger.error(f"Error adding database configuration: {e}")
            raise
    
    async def update_database_config(self, config_id: str, updates: Dict[str, Any]) -> DatabaseConfig:
        """Update existing database configuration."""
        try:
            if config_id not in self.configs:
                raise ValueError(f"Database configuration {config_id} not found")
            
            config = self.configs[config_id]
            
            # Update fields
            for key, value in updates.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            
            # Rebuild connection if connection parameters changed
            connection_fields = ["host", "port", "database", "username", "password", "ssl_mode", "connection_string"]
            if any(field in updates for field in connection_fields):
                # Close existing connection
                if config_id in self.connections:
                    self.connections[config_id].dispose()
                    del self.connections[config_id]
                
                # Test new connection
                test_result = await self.test_connection(config)
                
                if not test_result.success:
                    raise ValueError(f"Connection test failed: {test_result.message}")
            
            logger.info(f"Updated database configuration: {config.name}")
            return config
            
        except Exception as e:
            logger.error(f"Error updating database configuration: {e}")
            raise
    
    async def remove_database_config(self, config_id: str) -> bool:
        """Remove database configuration."""
        try:
            if config_id not in self.configs:
                raise ValueError(f"Database configuration {config_id} not found")
            
            # Close connection
            if config_id in self.connections:
                self.connections[config_id].dispose()
                del self.connections[config_id]
            
            # Remove config
            config_name = self.configs[config_id].name
            del self.configs[config_id]
            
            logger.info(f"Removed database configuration: {config_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing database configuration: {e}")
            raise
    
    async def get_database_configs(self) -> List[DatabaseConfig]:
        """Get all database configurations."""
        return list(self.configs.values())
    
    async def get_database_config(self, config_id: str) -> Optional[DatabaseConfig]:
        """Get specific database configuration."""
        return self.configs.get(config_id)
    
    async def switch_database(self, config_id: str) -> DatabaseConfig:
        """Switch to a different database configuration."""
        try:
            if config_id not in self.configs:
                raise ValueError(f"Database configuration {config_id} not found")
            
            config = self.configs[config_id]
            
            # Test connection to ensure it's still valid
            test_result = await self.test_connection(config)
            
            if not test_result.success:
                raise ValueError(f"Cannot switch to {config.name}: {test_result.message}")
            
            logger.info(f"Switched to database: {config.name}")
            return config
            
        except Exception as e:
            logger.error(f"Error switching database: {e}")
            raise
    
    async def execute_query(self, config_id: str, query: str) -> Dict[str, Any]:
        """Execute a query on the specified database."""
        try:
            if config_id not in self.connections:
                raise ValueError(f"Database configuration {config_id} not found")
            
            engine = self.connections[config_id]
            config = self.configs[config_id]
            
            with engine.connect() as connection:
                # Execute query
                result = connection.execute(text(query))
                
                # Handle different query types
                if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN')):
                    # SELECT query - return results
                    rows = result.fetchall()
                    columns = list(result.keys()) if result.keys() else []
                    
                    return {
                        "success": True,
                        "query_type": "select",
                        "columns": columns,
                        "rows": [dict(row._mapping) for row in rows],
                        "row_count": len(rows),
                        "database": config.name
                    }
                else:
                    # INSERT, UPDATE, DELETE - return affected rows
                    affected_rows = result.rowcount
                    
                    return {
                        "success": True,
                        "query_type": "modification",
                        "affected_rows": affected_rows,
                        "database": config.name
                    }
                    
        except Exception as e:
            logger.error(f"Error executing query on {config_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "database": self.configs.get(config_id, {}).name if config_id in self.configs else "Unknown"
            }
    
    async def get_database_stats(self, config_id: str) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            if config_id not in self.connections:
                raise ValueError(f"Database configuration {config_id} not found")
            
            engine = self.connections[config_id]
            config = self.configs[config_id]
            
            stats = {
                "database_name": config.name,
                "database_type": config.type.value,
                "connection_status": config.status.value,
                "last_tested": config.last_tested,
                "tables": [],
                "total_size_mb": 0
            }
            
            # Get table information
            schema_info = await self._discover_schema(engine)
            
            for table in schema_info:
                table_info = {
                    "name": table.table_name,
                    "columns": len(table.columns),
                    "row_count": table.row_count,
                    "indexes": len(table.indexes) if table.indexes else 0,
                    "foreign_keys": len(table.foreign_keys) if table.foreign_keys else 0
                }
                stats["tables"].append(table_info)
            
            # Get database size (if supported)
            try:
                with engine.connect() as conn:
                    if config.type == DatabaseType.POSTGRESQL:
                        result = conn.execute(text("""
                            SELECT pg_database_size(current_database()) / 1024 / 1024 as size_mb
                        """))
                        stats["total_size_mb"] = result.scalar()
                    elif config.type == DatabaseType.MYSQL:
                        result = conn.execute(text("""
                            SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
                            FROM information_schema.tables
                            WHERE table_schema = DATABASE()
                        """))
                        stats["total_size_mb"] = result.scalar() or 0
            except Exception as e:
                logger.warning(f"Could not get database size: {e}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            raise
    
    async def validate_connection_parameters(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate connection parameters before testing."""
        validation_errors = []
        warnings = []
        
        # Check required fields based on database type
        db_type = config_data.get("type")
        
        if not config_data.get("name"):
            validation_errors.append("Database name is required")
        
        if not db_type:
            validation_errors.append("Database type is required")
        else:
            try:
                DatabaseType(db_type)
            except ValueError:
                validation_errors.append(f"Invalid database type: {db_type}")
        
        # Check connection string or individual parameters
        if config_data.get("connection_string"):
            # Connection string provided - validate format
            conn_str = config_data["connection_string"]
            if not any(prefix in conn_str.lower() for prefix in ["postgresql://", "mysql://", "sqlite://", "mongodb://"]):
                validation_errors.append("Invalid connection string format")
        else:
            # Individual parameters - check based on database type
            if db_type != DatabaseType.SQLITE.value:
                if not config_data.get("host"):
                    validation_errors.append("Host is required for non-SQLite databases")
                if not config_data.get("username"):
                    validation_errors.append("Username is required for non-SQLite databases")
                if not config_data.get("password"):
                    warnings.append("Password not provided - connection may fail")
                if not config_data.get("database"):
                    validation_errors.append("Database name is required")
            else:
                if not config_data.get("database"):
                    validation_errors.append("Database file path is required for SQLite")
        
        # Validate port
        port = config_data.get("port")
        if port and (not isinstance(port, int) or port < 1 or port > 65535):
            validation_errors.append("Port must be an integer between 1 and 65535")
        
        # Validate SSL mode
        ssl_mode = config_data.get("ssl_mode")
        if ssl_mode:
            valid_ssl_modes = ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"]
            if ssl_mode not in valid_ssl_modes:
                validation_errors.append(f"Invalid SSL mode. Valid options: {', '.join(valid_ssl_modes)}")
        
        return {
            "valid": len(validation_errors) == 0,
            "errors": validation_errors,
            "warnings": warnings
        }


# Global database agent instance
database_agent = DatabaseAgent()
