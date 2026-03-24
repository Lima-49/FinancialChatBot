from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel

def convert_history(history):
    messages = []
    for m in history or []:
        if m.role == "user":
            messages.append(HumanMessage(content=m.content))
        elif m.role == "bot":
            messages.append(AIMessage(content=m.content))
    return messages

class Message(BaseModel):
    role: str
    content: str
