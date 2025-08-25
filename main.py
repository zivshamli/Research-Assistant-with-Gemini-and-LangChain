
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


load_dotenv()  # Load environment variables from .env file

# specify all of the field that you want as output from your LLM call
class ResearchResponse(BaseModel):
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
         You are a research assistant that will help generate research paper.
         Answer the user query and use necessary tools.
         If the user wants to save the output, include the "save" tool in your response. 
         the output in this format and provide no other text{format_instructions}
         """
       ),
       ("placeholder","{chat_history}"),
       ("human","{query}"),
       ("placeholder","{agent_scratchpad}"),

    ]

).partial(format_instructions=parser.get_format_instructions())

# Define the tools to be used by the agent

tools=[search_tool,wiki_tool,save_tool]

# Create the agent
agent=create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)
query= input("What can a help u with?")
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
    structured_response_Json = json.loads(raw_output)
    tools_list=structured_response_Json.get("tools", [])
    if "save" in tools_list:
        save_tool.invoke({"data": structured_response_Json.get("summary", "")})
except Exception as e:
    print("Error parsing response:", e,"Raw response -- ", raw_response)


#response=llm.invoke(prompt)
#print("Gemini:",response.content)
