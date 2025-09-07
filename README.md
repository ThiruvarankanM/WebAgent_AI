# WebAgent AI - URL Content Summarizer

## Overview
WebAgent AI is a modern web application that summarizes the content of any public web page using advanced language models. Built with Streamlit and the pydantic-ai framework, it provides a simple interface for users to extract concise summaries from articles, blogs, documentation, and more.

## Features
- Summarize content from any public URL
- Utilizes state-of-the-art LLMs via the pydantic-ai framework
- Asynchronous processing for fast and responsive summaries
- Easy-to-use web interface built with Streamlit
- Environment-based configuration for secure API key management

## Tech Stack
- **Python 3.10+**
- **Streamlit**: For the web application interface
- **pydantic-ai**: LLM orchestration and agent management
- **MCP Server**: Model Context Protocol server for LLM tool use
- **python-dotenv**: Environment variable management

## Supported Websites
WebAgent AI is designed to work best with publicly accessible, text-based web pages, including:
- News articles
- Blog posts
- Wikipedia pages
- Technical documentation
- Most static HTML content

### Limitations
- Content behind paywalls, logins, or dynamically loaded via JavaScript may not be accessible or summarized accurately.
- Some websites with aggressive anti-bot measures may block content fetching.
- The summarizer does not support PDF, DOCX, or other non-HTML formats.

## Getting Started
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your environment**
   - Create a `.env` file in the project root:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```
4. **Run the application**
   ```bash
   streamlit run app.py
   ```
5. **Open your browser** to the local URL provided by Streamlit.

## Configuration
- The application requires a valid `GROQ_API_KEY` for LLM access. This should be set in the `.env` file.
- Model and agent settings can be adjusted in `app.py` and `main.py`.

## Frameworks and Libraries Used
- [Streamlit](https://streamlit.io/)
- [pydantic-ai](https://github.com/pydantic/pydantic-ai)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Contributing
Contributions are welcome. Please open an issue or submit a pull request for improvements or bug fixes.

## License
This project is licensed under the MIT License.
