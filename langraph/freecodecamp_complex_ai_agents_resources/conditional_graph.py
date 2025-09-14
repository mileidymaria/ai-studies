from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    first_number: int
    second_number: int
    operation: str
    result: int

def adder(state: AgentState) -> AgentState:
    """Add two numbers"""
    state["result"] = state["first_number"] + state["second_number"]
    return state

def multiplier(state: AgentState) -> AgentState:
    """Multiply two numbers"""
    state["result"] = state["first_number"] * state["second_number"]
    return state

def operation_router(state: AgentState) -> AgentState:
    """Decide the next step based on state operation"""
    
    if state["operation"] == '+':
        return "adder"
    else:
        return "multiplier"

graph = StateGraph(AgentState)
graph.add_node("adder", adder)
graph.add_node("multiplier", multiplier)
graph.add_node("operation_router", lambda state:state) #Like pass state of step function
graph.add_edge(START, "operation_router")
graph.add_conditional_edges(
    "operation_router", # Source
    operation_router,
    { # Path Map. Key: Edge, Value: Node
        "adder": "adder",
        "multiplier": "multiplier"
    }
)
graph.add_edge("adder", END)
graph.add_edge("multiplier", END)
app = graph.compile()

png_bytes = app.get_graph().draw_mermaid_png()
with open("conditional.png", "wb") as f:
    f.write(png_bytes)

result = app.invoke({
    "first_number": 1,
    "second_number": 2,
    "operation": "+"
})

print(result["result"])

result = app.invoke({
    "first_number": 2,
    "second_number": 2,
    "operation": "*"
})

print(result["result"])