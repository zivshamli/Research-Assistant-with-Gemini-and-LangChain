# Research Assistant with Gemini and LangChain

This project is a research assistant that leverages **Google Gemini AI** and **LangChain** to generate research content, summarize information, and fetch sources from the web and Wikipedia. It also allows saving the research output to a text file.

---

## Features

- Chat with **Gemini AI** (`gemini-2.0-flash`) to answer research queries.
- Use **tools** for:
  - Searching the web (via DuckDuckGo)
  - Querying Wikipedia
  - Saving research output to a text file
- Structured output parsing using **Pydantic**.
- Easy integration with **LangChain agents**.

---

## Installation

1. Clone this repository :

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Create a virtual environment and activate it :

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. Install the required dependencies :
```bash 
pip install -r requirements.txt
```
4. Add your Google Gemini API key to a `.env` file :

```ini
API_GEMINAI_KEY=your_api_key_here
```
---
## Tools

- **Search Tool** – Searches the web using DuckDuckGo.

- **Wikipedia Tool** – Fetches relevant information from Wikipedia.

- **Save Tool** – Saves research output to a timestamped text file.
---

## Dependencies

- `google-generativeai`  
- `wikipedia`  
- `python-dotenv`  
- `pydantic`  
- `langchain`  
- `langchain-google-genai`  
- `langchain-community`  
- `duckduckgo-search`  
