"""Search-related tools (e.g., Google Search, web scraping)."""

from typing import Any, Optional
import httpx

from src.tools.base import BaseTool, register_tool


class GoogleSearchTool(BaseTool):
    """Tool for performing Google searches."""

    name = "google_search"
    description = "Search the web using Google. Useful for finding current information."

    def __init__(self, api_key: Optional[str] = None, search_engine_id: Optional[str] = None):
        """Initialize Google Search tool.
        
        Args:
            api_key: Google Custom Search API key
            search_engine_id: Custom Search Engine ID
        """
        self.api_key = api_key
        self.search_engine_id = search_engine_id

    async def execute(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Execute a Google search.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Dictionary containing search results
        """
        if not self.api_key or not self.search_engine_id:
            return {
                "error": "Google Search API key and Search Engine ID must be configured"
            }

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num_results,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        return {
            "query": query,
            "results": [
                {
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                }
                for item in data.get("items", [])
            ],
        }


# Register tools
# register_tool(GoogleSearchTool())

