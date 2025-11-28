
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent,AgentExecutor
from pydantic import BaseModel

from tools import search_tool,wiki_tool,save_tool,speak_tool
from send_email_tool import send_email_tools


load_dotenv()  # Load environment variables from .env file

# specify all of the field that you want as output from your LLM call
class ResearchResponse(BaseModel):
    text: str
    topic: str
    summary: str
    sources: list[str]
    tools: list[str]


'''
api_key = os.getenv("API_GEMINAI_KEY")
genai.configure(api_key=api_key)  
model=genai.GenerativeModel("gemini-2.0-flash")  
chat = model.start_chat()
response = chat.send_message("Hello Are you there?")
print("Gemini:",response.text)
'''
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
parser=PydanticOutputParser(pydantic_object=ResearchResponse)

# Define the prompt for the LLM
prompt=ChatPromptTemplate.from_messages(
    [
       (
        "system",
        """
        You are a research assistant that will help generate research papers. 
        Answer the user query thoroughly, providing detailed explanations, examples, and elaboration where relevant. Expand your writing beyond minimal answers to ensure depth and clarity. 
        If the user wants to save the output, include the "save" tool in your response. 
        If the user wants to send the output via email, include the "send_email" tool in your response. 
        Always output in this format and provide no other text: {format_instructions}
        """

       ),
       ("placeholder","{chat_history}"),
       ("human","{query}"),
       ("placeholder","{agent_scratchpad}"),

    ]

).partial(format_instructions=parser.get_format_instructions())

# Define the tools to be used by the agent

tools=[search_tool,wiki_tool,save_tool,speak_tool,send_email_tools]

# Create the agent
agent=create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)
# Function to run the agent with a given query
def run_agent(query: str) -> str:
    raw_response=agent_executor.invoke({"query":query})
    print("Raw response:",raw_response)

    raw_output = raw_response["output"]

    if raw_output.startswith("```json"):
        raw_output = raw_output[len("```json"):].strip()
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3].strip()


    try:
        structured_response=parser.parse(raw_output)
        print(structured_response)
        tools_list=structured_response.tools
        for tool_name in tools_list:
            if tool_name == "save":
                save_tool.invoke({"data": structured_response.text})
            elif tool_name == "speak":
                speak_tool.invoke({"text": structured_response.text})
            elif tool_name == "send_email":
                print("Invoking send email tool")
                save_tool.invoke({"data": structured_response.text})
                send_email_tools.invoke({"file_path": "research_output.txt", "topic": structured_response.topic})
        return structured_response.text
    except Exception as e:
        print("Error parsing response:", e,"Raw response -- ", raw_response)


#response=llm.invoke(prompt)
#print("Gemini:",response.content)
