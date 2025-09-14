from langgraph.graph import StateGraph
from typing import TypedDict, Dict

class AgentState(TypedDict):
    name : str
    message : str
    
def complimenting_node(state: AgentState) -> AgentState:
    """Simple node that compliments people"""
    state["message"] = f"Hey, {state['name']}! You are doing an amazing job!"
    return state

graph = StateGraph(AgentState)
graph.add_node("complimenter", complimenting_node)
graph.set_entry_point("complimenter")
graph.set_finish_point("complimenter")
app = graph.compile()
result = app.invoke({"name": "Mileidy"})
print(result["message"])