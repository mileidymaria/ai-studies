#!/usr/bin/env python3
"""
Wikipedia Agent - Uses MCP to access Wikipedia information
"""
import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient


class WikipediaMCPClient:
    """Client to interact with Wikipedia MCP server"""
    
    def __init__(self):
        self.server_process = None
        self.request_id = 0
    
    async def start_server(self):
        """Start the Wikipedia MCP server"""
        try:
            self.server_process = subprocess.Popen(
                ["wikipedia-mcp"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True
        except Exception as e:
            print(f"Error starting Wikipedia MCP server: {e}")
            return False
    
    async def stop_server(self):
        """Stop the Wikipedia MCP server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
    
    async def search_wikipedia(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search Wikipedia for articles"""
        if not self.server_process:
            await self.start_server()
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": "search_wikipedia",
                "arguments": {
                    "query": query,
                    "limit": limit
                }
            }
        }
        
        self.request_id += 1
        
        try:
            self.server_process.stdin.write(json.dumps(request) + "\n")
            self.server_process.stdin.flush()
            
            response_line = self.server_process.stdout.readline()
            response = json.loads(response_line.strip())
            
            if "result" in response:
                return response["result"]
            else:
                return {"error": response.get("error", "Unknown error")}
                
        except Exception as e:
            return {"error": f"Request failed: {e}"}
    
    async def get_article_summary(self, title: str, max_length: int = 500) -> Dict[str, Any]:
        """Get a summary of a Wikipedia article"""
        if not self.server_process:
            await self.start_server()
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": "get_article_summary",
                "arguments": {
                    "title": title,
                    "max_length": max_length
                }
            }
        }
        
        self.request_id += 1
        
        try:
            self.server_process.stdin.write(json.dumps(request) + "\n")
            self.server_process.stdin.flush()
            
            response_line = self.server_process.stdout.readline()
            response = json.loads(response_line.strip())
            
            if "result" in response:
                return response["result"]
            else:
                return {"error": response.get("error", "Unknown error")}
                
        except Exception as e:
            return {"error": f"Request failed: {e}"}
    
    async def get_article_content(self, title: str) -> Dict[str, Any]:
        """Get full content of a Wikipedia article"""
        if not self.server_process:
            await self.start_server()
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": "get_article_content",
                "arguments": {
                    "title": title
                }
            }
        }
        
        self.request_id += 1
        
        try:
            self.server_process.stdin.write(json.dumps(request) + "\n")
            self.server_process.stdin.flush()
            
            response_line = self.server_process.stdout.readline()
            response = json.loads(response_line.strip())
            
            if "result" in response:
                return response["result"]
            else:
                return {"error": response.get("error", "Unknown error")}
                
        except Exception as e:
            return {"error": f"Request failed: {e}"}


# Global MCP client instance
wikipedia_client = WikipediaMCPClient()


async def search_wikipedia_tool(query: str, limit: int = 10) -> str:
    """Tool function for searching Wikipedia"""
    try:
        result = await wikipedia_client.search_wikipedia(query, limit)
        
        if "error" in result:
            return f"Error searching Wikipedia: {result['error']}"
        
        if "results" in result and result["results"]:
            articles = result["results"]
            response = f"Found {len(articles)} Wikipedia articles for '{query}':\n\n"
            
            for i, article in enumerate(articles[:5], 1):  # Show top 5
                response += f"{i}. {article.get('title', 'Unknown Title')}\n"
                response += f"   {article.get('snippet', 'No description available')}\n\n"
            
            return response
        else:
            return f"No Wikipedia articles found for '{query}'"
            
    except Exception as e:
        return f"Error searching Wikipedia: {e}"


async def get_wikipedia_summary_tool(title: str, max_length: int = 500) -> str:
    """Tool function for getting Wikipedia article summary"""
    try:
        result = await wikipedia_client.get_article_summary(title, max_length)
        
        if "error" in result:
            return f"Error getting Wikipedia summary: {result['error']}"
        
        if "summary" in result:
            return f"Wikipedia Summary for '{title}':\n\n{result['summary']}"
        else:
            return f"No summary available for '{title}'"
            
    except Exception as e:
        return f"Error getting Wikipedia summary: {e}"


async def get_wikipedia_content_tool(title: str) -> str:
    """Tool function for getting Wikipedia article content"""
    try:
        result = await wikipedia_client.get_article_content(title)
        
        if "error" in result:
            return f"Error getting Wikipedia content: {result['error']}"
        
        if "content" in result:
            content = result["content"]
            # Truncate if too long
            if len(content) > 2000:
                content = content[:2000] + "..."
            return f"Wikipedia Content for '{title}':\n\n{content}"
        else:
            return f"No content available for '{title}'"
            
    except Exception as e:
        return f"Error getting Wikipedia content: {e}"


def create_wikipedia_agent(openai_client) -> AssistantAgent:
    """Create the Wikipedia agent"""
    return AssistantAgent(
        "wikipedia_agent",
        openai_client,
        system_message="""
        You are Wikipedia Agent, a specialized research assistant that provides contextual information from Wikipedia.
        You work with the Titanic analysis team to provide historical context, background information, and additional insights.
        
        Your role:
        1. Search Wikipedia for relevant information related to Titanic analysis topics
        2. Provide summaries and detailed information from Wikipedia articles
        3. Offer historical context and background information
        4. Help the team understand broader historical and social contexts
        
        Available tools:
        - search_wikipedia_tool: Search for Wikipedia articles on any topic
        - get_wikipedia_summary_tool: Get concise summaries of specific articles
        - get_wikipedia_content_tool: Get detailed content from specific articles
        
        Always provide relevant, well-structured information that enhances the team's analysis.
        Focus on historical context, social factors, and background information that could be relevant to Titanic data analysis.
        """,
        tools=[
            search_wikipedia_tool,
            get_wikipedia_summary_tool,
            get_wikipedia_content_tool
        ]
    )
