# This is an agent that has a list of tools available and decide which tool
# should be called or if there is no tool available to be called and when that happens
# it should go to end

import os
from dotenv import load_dotenv
from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages 
# Reducer function, merge new data into the current state, w/o reducer like add_messages, we would
# override data
from langgraph.prebuilt import ToolNode

dotenv_path = os.path.join(os.path.dirname(__file__), "../../..", ".env")
print({"dotenv_path": dotenv_path})
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int) -> int:
    """This is an addition function that adds two numbers together. e.g., a + b

    Args:
        a (int): first number
        b (int): second number

    Returns:
        int: the result of the addition
    """
    return a+b

def subtract(a: int, b:int) -> int:
    """Subtraction of two numbers. eg., a - b

    Args:
        a (int): first number
        b (int): second number

    Returns:
        int: result of the subtraction
    """
    return a - b

def multiply(a: int, b:int) -> int:
    """Multiply two numbers. eg., a * b

    Args:
        a (int): first number
        b (int): second number

    Returns:
        int: result of the multiplication
    """
    return a * b

tools = [add, subtract, multiply]
model = ChatOpenAI(model='gpt-3.5-turbo').bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system = SystemMessage(
        content=(
            "You are my AI assistant, please answer my query to the best of your ability. "
            "Also, show me your steps to get to the final result, including resources/tools calling."
        )
    )
    response = model.invoke([system, *state["messages"]])
    print(response)
    return {"messages": [response]}

def should_continue(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1]
    if getattr(last_message, "tool_calls", None):
        return "continue"
    return "end"

graph = StateGraph(AgentState)
graph.add_node("model_call", model_call)
graph.add_node("tools", ToolNode(tools=tools))
graph.add_edge(START, "model_call")
graph.add_conditional_edges(
    "model_call",
    should_continue,
    {
        "end": END,
        "continue": "tools"
    }
)
graph.add_edge("tools", "model_call")
agent = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [HumanMessage(content="Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
print_stream(agent.stream(inputs, stream_mode="values"))