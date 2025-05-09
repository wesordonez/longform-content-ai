from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests
from typing import Dict


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

# Create a custom SerperDevTool implementation
class CustomSerperDevTool(BaseTool):
    name: str = "CustomSerperDevTool"
    description: str = "A tool that performs web searches using Serper API to find information on the internet."

    def __init__(self, api_key=None):
        super().__init__()
        # Get API key from environment variable if not provided
        self.api_key = api_key or os.environ.get("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError("Serper API key is required. Set the SERPER_API_KEY environment variable or pass it to the tool.")

    def _run(self, query: str) -> str:
        """
        Run a search query using the Serper API.
        """
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # Prepare the request payload
        payload = {
            "q": query,
            "gl": "us",  # Geographic location - US by default
            "hl": "en",  # Language - English by default
            "num": 10    # Number of results to return
        }
        
        try:
            response = requests.post(
                'https://google.serper.dev/search',
                headers=headers,
                json=payload
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse the JSON response
            search_results = response.json()
            
            # Format the results in a readable way
            formatted_results = self._format_results(search_results)
            return formatted_results
            
        except requests.exceptions.RequestException as e:
            return f"Error performing search: {str(e)}"
    
    def _format_results(self, results: Dict) -> str:
        """
        Format the search results in a readable way.
        """
        formatted_text = "### Search Results\n\n"
        
        # Add organic results if available
        if "organic" in results:
            formatted_text += "#### Organic Results\n\n"
            for i, result in enumerate(results["organic"], 1):
                title = result.get("title", "No Title")
                link = result.get("link", "No Link")
                snippet = result.get("snippet", "No Snippet")
                
                formatted_text += f"{i}. **{title}**\n"
                formatted_text += f"   - URL: {link}\n"
                formatted_text += f"   - Summary: {snippet}\n\n"
        
        # Add knowledge graph if available
        if "knowledgeGraph" in results:
            kg = results["knowledgeGraph"]
            formatted_text += "#### Knowledge Graph\n\n"
            title = kg.get("title", "No Title")
            formatted_text += f"**{title}**\n"
            
            if "description" in kg:
                formatted_text += f"Description: {kg['description']}\n\n"
            
            # Add attributes if available
            if "attributes" in kg:
                formatted_text += "Attributes:\n"
                for key, value in kg["attributes"].items():
                    formatted_text += f"- {key}: {value}\n"
                formatted_text += "\n"
        
        # Add answer box if available
        if "answerBox" in results:
            answer = results["answerBox"]
            formatted_text += "#### Featured Answer\n\n"
            
            if "answer" in answer:
                formatted_text += f"Answer: {answer['answer']}\n\n"
            elif "snippet" in answer:
                formatted_text += f"Snippet: {answer['snippet']}\n\n"
            
            if "title" in answer and "link" in answer:
                formatted_text += f"Source: [{answer['title']}]({answer['link']})\n\n"
        
        return formatted_text