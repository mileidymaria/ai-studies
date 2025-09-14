from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import random

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    """Greet the user"""
    print("greeting_node")
    state["name"] = f"Hi there, {state['name']}"
    state["counter"] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    """Returns a random number from zero to ten"""
    print("random_node")
    state["number"].append(random.randint(0,10))
    state["counter"] += 1
    return state

def should_continue(state: AgentState) -> AgentState:
    """Function to decide what to do next"""
    if state["counter"] < 5:
        print("Continue loop...")
        return "loop"
    else:
        return "exit"

graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")
graph.add_conditional_edges(
    "random",
    should_continue,
    {
        "loop": "random",
        "exit": END
    }
)
graph.set_entry_point("greeting")
app = graph.compile()

png_bytes = app.get_graph().draw_mermaid_png()
with open("looping.png", "wb") as f:
    f.write(png_bytes)

result = app.invoke({
    "name": "Mileidy",
    "counter": -1,
    "number": []
})
print(result)