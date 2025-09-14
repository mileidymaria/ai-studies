from langserve import RemoteRunnable

remote_chain_endpoint = "http://localhost:8000/find"
remote_chain = RemoteRunnable(remote_chain_endpoint)
response = remote_chain.invoke({"text": "Noite feliz."})
print(response)