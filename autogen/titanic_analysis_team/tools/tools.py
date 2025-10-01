from autogen_agentchat.messages import ToolCallExecutionEvent, FunctionExecutionResult

def extract_tool_results(agent_response):
    """
    Extract only ToolCallExecutionEvent results from an agent response.
    Returns a list of dictionaries with tool name and result.
    """
    tool_results = []

    for message_event in agent_response.inner_messages:
        if isinstance(message_event, ToolCallExecutionEvent):
            # message_event.content é uma lista de FunctionExecutionResult
            for func_result in message_event.content:
                if isinstance(func_result, FunctionExecutionResult):
                    tool_results.append({
                        "tool_name": func_result.name,
                        "result": func_result.content
                    })

    return tool_results
