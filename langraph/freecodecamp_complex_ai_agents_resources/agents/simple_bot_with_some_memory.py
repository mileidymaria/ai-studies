import os
from dotenv import load_dotenv
from typing import TypedDict, List, Union
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
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
    messages: List[Union[HumanMessage, AIMessage]]

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = chain.invoke(state["messages"])
    print(f"\nAI: {response}")
    state["messages"].append(AIMessage(content=response))
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []
user_input = input("YOU: ")
states = []

while user_input != "exit":
    conversation_history.append(HumanMessage(content = user_input))
    result = agent.invoke({
        "messages": conversation_history
    })
    states.append(result)
    user_input = input("YOU: ")

with open("logging.txt", "w") as file:
    file.write("Your conversation log:\n")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")