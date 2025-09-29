from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int
    final: str

class OutputState(TypedDict):
    final: str
class PrivateAgentState(TypedDict):
    messages: str

def say_hi(state: AgentState) -> OutputState:
    """This node says hi to the user."""
    state["final"] = f"Hi, {state['name']}!"
    return {"final": "Hey, that's final"}

def say_age(state: AgentState) -> PrivateAgentState:
    """This says user age"""
    state["message"] = "Private test!"
    print(state)
    return state

graph = StateGraph(AgentState, input=AgentState, output=OutputState)
graph.add_node("say_hi", say_hi)
graph.add_node("say_age", say_age)
graph.set_entry_point("say_hi")
graph.add_edge("say_hi", "say_age")
graph.set_finish_point("say_age")
app = graph.compile()

png_bytes = app.get_graph().draw_mermaid_png()
with open("sequential.png", "wb") as f:
    f.write(png_bytes)
    
result = app.invoke({
    "name": "Mileidy",
    "age": 25
})
print(result)
print(type(result))