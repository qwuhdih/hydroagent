"""External API calling tools."""

from typing import Any, Dict, Optional
import httpx

from src.tools.base import BaseTool, register_tool


class HTTPRequestTool(BaseTool):
    """Tool for making HTTP requests to external APIs."""

    name = "http_request"
    description = "Make HTTP requests to external APIs. Supports GET, POST, PUT, DELETE methods."

    async def execute(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute an HTTP request.
        
        Args:
            url: Target URL
            method: HTTP method (GET, POST, PUT, DELETE)
            headers: Request headers
            params: Query parameters
            json_data: JSON body for POST/PUT requests
            
        Returns:
            Dictionary containing response data
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method=method.upper(),
                    url=url,
                    headers=headers or {},
                    params=params,
                    json=json_data,
                )
                response.raise_for_status()

                return {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                }
        except httpx.HTTPError as e:
            return {
                "error": f"HTTP error: {str(e)}",
            }
        except Exception as e:
            return {
                "error": f"Request failed: {str(e)}",
            }


# Register tools
# register_tool(HTTPRequestTool())

