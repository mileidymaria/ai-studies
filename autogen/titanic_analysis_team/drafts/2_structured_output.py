import os
import sqlite3
import json
import asyncio
from typing import Optional
from dotenv import load_dotenv
from models import math_reasoning
from autogen_agentchat.messages import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

# -----------------------------
# Environment & Database Setup
# -----------------------------
db_path = "state_db/example.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)
conn = sqlite3.connect(db_path, check_same_thread=False)

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
print({"dotenv_path": dotenv_path})
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -----------------------------
# Client Initialization
# -----------------------------
client = OpenAIChatCompletionClient(model="gpt-4o-mini")

# -----------------------------
# Structured Output Function
# -----------------------------
async def ask_math_question(prompt: str):
    """
    Sends a math question to the OpenAI client and returns a validated structured output.

    Args:
        prompt (str): The math question or instruction for the assistant.

    Returns:
        MathReasoning: A Pydantic model instance with the structured output.
    """

    # Define the user message
    messages = [UserMessage(content=prompt, source="user")]

    # Call the client with structured output
    response = await client.create(
        messages=messages,
        extra_create_args={"response_format": math_reasoning.MathReasoning}
    )

    # Extract content as string
    response_content: Optional[str] = response.content if isinstance(response.content, str) else None
    if response_content is None:
        raise ValueError("Response content is not a valid JSON string")
    
    print({'response_content': response_content})

    # Parse JSON and validate using Pydantic
    parsed_content = json.loads(response_content)
    validated_response = math_reasoning.MathReasoning.model_validate(parsed_content)

    return validated_response

# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    prompt_text = "What is 16 + 32?"
    validated_result = asyncio.run(ask_math_question(prompt_text))
    print(validated_result)
