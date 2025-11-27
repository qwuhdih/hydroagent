"""Database query and data manipulation tools."""

from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.tools.base import BaseTool, register_tool
from src.config import settings


class DatabaseQueryTool(BaseTool):
    """Tool for executing database queries."""

    name = "database_query"
    description = "Execute SQL queries on the database. Use with caution and validate queries."

    def __init__(self, database_url: Optional[str] = None):
        """Initialize database query tool.
        
        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url or settings.DATABASE_URL
        self._engine: Optional[Engine] = None

    @property
    def engine(self) -> Engine:
        """Get or create database engine."""
        if self._engine is None:
            self._engine = create_engine(self.database_url)
        return self._engine

    async def execute(self, query: str, limit: int = 100) -> Dict[str, Any]:
        """Execute a SQL query.
        
        Args:
            query: SQL query string
            limit: Maximum number of rows to return
            
        Returns:
            Dictionary containing query results
        """
        try:
            # Add LIMIT if not present (safety measure)
            if "LIMIT" not in query.upper():
                query = f"{query} LIMIT {limit}"

            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                rows = result.fetchall()
                columns = result.keys()

                return {
                    "columns": list(columns),
                    "rows": [dict(zip(columns, row)) for row in rows],
                    "row_count": len(rows),
                }
        except Exception as e:
            return {
                "error": str(e),
            }


# Register tools
# register_tool(DatabaseQueryTool())

