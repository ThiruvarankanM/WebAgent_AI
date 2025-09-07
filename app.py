import os
from dotenv import load_dotenv
import asyncio
import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

# --- Page Configuration ---
st.set_page_config(
    page_title="URL Summarizer",
    page_icon="📄",
    layout="centered"
)

# --- Configuration ---
@st.cache_resource
def setup_agent():
    """Initialize the agent with MCP server."""
    load_dotenv()
    if "GROQ_API_KEY" not in os.environ:
        st.error("GROQ_API_KEY not found in environment. Please set it in your .env file.")
        return None
    
    try:
        mcp_server = MCPServerStdio(command="python", args=["-m", "mcp_server_fetch"])
        agent = Agent(model="groq:llama-3.3-70b-versatile", mcp_servers=[mcp_server])
        return agent
    except Exception as e:
        st.error(f"Error setting up agent: {str(e)}")
        return None

# --- Functions ---
async def summarize_url(agent, url: str) -> str:
    """Fetch content from URL and summarize it."""
    try:
        async with agent.run_mcp_servers():
            result = await agent.run(
                f"Please use the fetch tool to get the content from {url} and then provide a comprehensive summary of what you find. Make sure to actually fetch the content and summarize it, don't just show the function call."
            )
            return result.output
    except Exception as e:
        return f"Error: {str(e)}"

def run_async_summarization(agent, url):
    """Wrapper to run async function in Streamlit."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(summarize_url(agent, url))
    finally:
        loop.close()

# --- Streamlit App ---
def main():
    st.title("URL Content Summarizer")
    st.write("Enter a URL to generate an AI-powered summary of its content.")
    
    # Initialize agent
    agent = setup_agent()
    if agent is None:
        st.stop()
    
    # URL input
    url_input = st.text_input(
        "URL:",
        placeholder="https://example.com/article"
    )
    
    # Summarize button
    if st.button("Summarize", type="primary"):
        if not url_input:
            st.warning("Please enter a URL.")
            return
        
        if not url_input.startswith(('http://', 'https://')):
            st.error("Please enter a valid URL starting with http:// or https://")
            return
        
        # Show loading and process
        with st.spinner("Processing..."):
            try:
                summary = run_async_summarization(agent, url_input)
                
                if "<function=" in summary and "</function>" in summary:
                    st.error("Failed to process URL. Please try again.")
                else:
                    st.success("Summary completed")
                    st.write("**Summary:**")
                    st.write(summary)
                    st.write(f"**Source:** {url_input}")
                    
            except Exception as e:
                st.error("An error occurred while processing the URL.")

if __name__ == "__main__":
    main()