import os
from dotenv import load_dotenv
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

dotenv_path = os.path.join(os.path.dirname(__file__), "../../..", ".env")
print({"dotenv_path": dotenv_path})
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model='gpt-3.5-turbo')
str_output_parser = StrOutputParser()
chain = model | str_output_parser

class AgentState(TypedDict):
    messages: List[HumanMessage]

def process(state: AgentState) -> AgentState:
    response = chain.invoke(state["messages"])
    print(f"\nAI: {response}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

user_input = input("")
while user_input != "exit":
    agent.invoke({
        "messages": [
            HumanMessage(content = user_input)
        ]
    })
    user_input = input("")