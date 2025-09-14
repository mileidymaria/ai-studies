from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    prices: List[int]
    name: str
    result: str

def apply_discount(state: AgentState) -> AgentState:
    """Node that is responsible to apply discount on a list of prices"""
    
    print(state)
    prices_with_discount = list(map(lambda price: price * 0.5, state["prices"]))
    state["result"] = f"""
        The discount that will be applied to client {state['name']} will be:
            Prices without discount = {state["prices"]}
            Prices with discount = {prices_with_discount}
    """
    print(state)
    return state

graph = StateGraph(AgentState)
graph.add_node("discounter", apply_discount)
graph.set_entry_point("discounter")
graph.set_finish_point("discounter")
app = graph.compile()
result = app.invoke({
    "name": "Mileidy",
    "prices": [1,2,3,4,8,9]
})
print(result["result"])