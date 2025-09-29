import os
from dotenv import load_dotenv
from typing import TypedDict, Sequence, Annotated, Literal
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages 
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.pydantic_v1 import BaseModel, validator
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode
import sqlite3

db_path = "state_db/example.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)
conn = sqlite3.connect(db_path, check_same_thread=False)
db = SqliteSaver(conn)
# Reducer function, merge new data into the current state, w/o reducer like add_messages, we would
# override data

dotenv_path = os.path.join(os.path.dirname(__file__), "../../..", ".env")
print({"dotenv_path": dotenv_path})
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

document_content = ""

class AgentState(BaseModel):
    name: Literal["Mileidy", "Maria"]
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    @validator('name')
    def validate_name(cls, value):
        if value not in ["Mileidy", "Maria"]:
            raise ValueError("Wrong value")
        return value
    class Config:
        arbitrary_types_allowed = True

@tool
def update(content: str) -> str:
    """This updates the document content

    Args:
        content (str): content that will be updated to document
    """
    
    global document_content
    document_content = content
    return "Document has been updated successfully!"

@tool
def save(filename: str) -> str:
    """Save the current document to a text file (.txt) and finishes the process.

    Args:
        filename (str): Name for the text file.
    """

    global document_content
    if not filename.endswith(".txt"):
        filename = f"{filename}.txt"
    
    try:
        with open(filename, "w") as file:
            file.write(document_content)
        print(f"\n Document has been saved to: {filename}")
        return f"\n Document has been saved to: {filename}"
    except Exception as exception:
        return f"Error saving document: {str(exception)}"

tools = [save, update]
model = ChatOpenAI(model='gpt-3.5-turbo', temperature = 0).bind_tools(tools)

def drafter(state: AgentState) -> AgentState:
    """
        Function capable of saving drafts to file system;
    """
    system = SystemMessage(content=f"""
        You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
        
        - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
        - If the user wants to save and finish, you need to use the 'save' tool.
        - Make sure to always show the current document state after modifications.
        - Also, the user needs to be able to see the current document content during this conversation, so you must sent it back to the user, returning it on content attribute of AIMessageClass.
        
        The current document content is:{document_content}
    """)

    if not state.messages:
        user_input = "I'm ready to help you update a document. Can we start?"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\nWhat would you like to do with the document? \n")
        print(f"\nUSER: {user_input}")
        user_message = HumanMessage(content=user_input)
    
    response = model.invoke([system, *list(state.messages), user_message])
    print(f"\n🤖 AI: {response}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state.messages) + [user_message, response]}

def should_continue(state: AgentState) -> AgentState:
    messages = state.messages
    if not messages:
        return "continue"
    last_message = messages[-1]
    if (isinstance(last_message, ToolMessage) and 
            "saved" in last_message.content.lower() and 
            "document" in last_message.content.lower()):
        return "end"
    return "continue"

def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n🛠️ TOOL RESULT: {message.content}")

graph = StateGraph(AgentState)
graph.add_node("agent", drafter)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END,
    },
)

app = graph.compile(checkpointer = db)

def run_document_agent():
    print("\n ===== DRAFTER =====")
    
    state = {"messages": [], "name": "Mileidy"}
    
    for step in app.stream(state, stream_mode="values", config = {"configurable": {"thread_id": "1"}}):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()
    checkpoints = app.get_state_history({"configurable": {"thread_id": "1"}})