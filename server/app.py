from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class AgentRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(request: AgentRequest):
    query=request.query
    try:
        reply_text=run_agent(query)
    except Exception as e:
        print("Error running agent:", e)
        reply_text="Sorry, there was an error processing your request."    
    
    return {"response": reply_text}
