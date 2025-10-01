from pydantic import BaseModel
from typing import List

class MathReasoning(BaseModel):
    class Step(BaseModel):
        explanation: str
        output: str

    steps: List[Step]
    final_answer: str
