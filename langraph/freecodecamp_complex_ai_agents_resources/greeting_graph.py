import os
from dotenv import load_dotenv
from typing import Dict, TypedDict
from langgraph.graph import StateGraph
import matplotlib.pyplot as plt

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AgentState(TypedDict): # Our state schema
    message : str

def greeting_node(state: AgentState) -> AgentState:
    """
        Node that adds a greeting message to the state.
    """
    state['message'] = f"Hey, {state['message']}. How is your day going?"
    return state

graph = StateGraph(AgentState) 
graph.add_node("greeter", greeting_node)
graph.set_entry_point('greeter')
graph.set_finish_point('greeter')
app = graph.compile()

# png_bytes = app.get_graph().draw_mermaid_png()
# with open("first_graph.png", "wb") as f:
#     f.write(png_bytes)

result = app.invoke({"message": "Bob"})
print(result['message'])