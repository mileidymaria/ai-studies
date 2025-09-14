from typing import TypedDict, Union, Optional, Any, Annotated

# Normal Dictionary: Does not check if the data is the correct type or structure
movie = {
    "name": "string",
    "year": 2015
}

# Typed Dictionary: Type safety
def typed_dict_example():
    class Movie(TypedDict):
        name : str
        year : int
    
    typed_movie = Movie(name="name", year="Name")
    print(typed_movie)
typed_dict_example()

# Union: One of another type
def square(x: Union[int, float]) -> float:
    return x * x

# Optional: The parameter should be of the given type or it should be none
def nice_message(name: Optional[str]) -> None:
    if name is None:
        print("Hey random person!")
    else:
        print(f"Hey there, {name}!")

# Any: Any type is allowed
def print_value(value: Any):
    print(value)

# Lambda Function: shortcut to write small functions
square = lambda x: x*x
squares = list(map(lambda num: num * num, [1,2,3,6,5,4]))

# Annotated = Provides additional context without affecting the type itself, metadata
class Person(TypedDict):
    email : Annotated[str, "This has to be a valid email format!"]

# Sequence - To automatically handle the state updates for sequences such as by adding new
# messages to a chat history, ordered collection.