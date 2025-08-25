from langchain_community.tools import WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
import pyttsx3
from langchain.tools import Tool
from datetime import datetime
import re



def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_data = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_data)
    return f"Data saved to {filename}"   

save_tool= Tool(
    name="save_to_txt",
    description="Saves the provided text data to a text file named research_output.txt. The input should be a string containing the data to be saved.",
    func=save_to_txt
) 
search=DuckDuckGoSearchRun()
search_tool=Tool(
    name="search",
    description="Search the web for information",
    func=search.run
)

# --- Speak text aloud ---
def speak_text(text: str):
    """Reads the given text aloud using system TTS"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return "Text was spoken out loud "

speak_tool = Tool(
    name="speak",
    description="Speaks the provided text aloud",
    func=speak_text
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=100)
wiki_tool=WikipediaQueryRun(api_wrapper=api_wrapper)
