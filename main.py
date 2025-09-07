# Required imports
import os
from dotenv import load_dotenv
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio


class URLSummarizer:
    def __init__(self, api_key: str = None):
        """Initialize the URL summarizer with API key."""
        # Load environment variables
        load_dotenv()
        
        # Set API key
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
        elif "GROQ_API_KEY" not in os.environ:
            raise ValueError("GROQ_API_KEY must be set either as environment variable or passed as parameter.")
        
        # Setup MCP server and agent
        self.mcp_server = MCPServerStdio(command="python", args=["-m", "mcp_server_fetch"])
        self.agent = Agent(model="groq:llama-3.3-70b-versatile", mcp_servers=[self.mcp_server])

    async def summarize_url(self, url: str) -> str:
        """Fetch content from URL and summarize it."""
        try:
            async with self.agent.run_mcp_servers():
                result = await self.agent.run(
                    f"Please use the fetch tool to get the content from {url} and then provide a comprehensive summary of what you find."
                )
                return result.output
        except Exception as e:
            return f"Error: {str(e)}"

    def summarize_url_sync(self, url: str) -> str:
        """Synchronous wrapper for summarize_url."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.summarize_url(url))
        finally:
            loop.close()


# Standalone script functionality
async def main():
    """Main function for standalone usage."""
    try:
        # Initialize summarizer
        summarizer = URLSummarizer()
        
        # Get URL from user
        url = input("Enter URL to summarize: ")
        
        # Process URL
        print("Processing...")
        summary = await summarizer.summarize_url(url)
        
        # Display results
        print(f"\nSummary:\n{summary}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


# Run the script
if __name__ == "__main__":
    asyncio.run(main())