import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model='gpt-3.5-turbo')
str_output_parser = StrOutputParser()


template_message = ChatPromptTemplate.from_messages([
    (
        "system",        
        """
            In your response, for each word of the sentence that you will receive, you should return two synonyms. The output should be in the following json format:
            {{
                "Word of the sentence": ["synonym1", "synonym2"]
            }}
            You should only return the json in your response. Let's think step by step. 
        """
        
    ),
    (
        "user",
        "{text}"
    )
])

chain = template_message | model | str_output_parser