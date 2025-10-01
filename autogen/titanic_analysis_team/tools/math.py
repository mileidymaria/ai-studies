from typing import Union, Annotated
Number = Union[int, float]

def add_operation(
    a: Annotated[Number, "First number"], 
    b: Annotated[Number, "Second number"]) -> Number:
    """Perform addition between two numbers."""
    return a + b


def subtract_operation(
    a: Annotated[Number, "First number"], 
    b: Annotated[Number, "Second number"]) -> Number:
    """Perform subtraction between two numbers."""
    return a - b


def multiply_operation(
    a: Annotated[Number, "First number"], 
    b: Annotated[Number, "Second number"]) -> Number:
    """Perform multiplication between two numbers."""
    return a * b


def divide_operation(
    a: Annotated[Number, "Numerator"], 
    b: Annotated[Number, "Denominator (must not be zero)"]) -> float:
    """Perform division between two numbers."""
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed")
    return a / b
