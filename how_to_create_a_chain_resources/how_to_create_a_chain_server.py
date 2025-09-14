from how_to_create_a_chain import chain
from fastapi import FastAPI
from langserve import add_routes

server = FastAPI(
    title='Synonimer',
    description="Find synonyms for the words in your sentence"
)

add_routes(
    server,
    chain,
    path = '/find'
)

if __name__ == "__main__": # Executing this file directly, if this is running inside another code, we will nto execute it
    import uvicorn
    uvicorn.run(server, host="localhost", port=8000)