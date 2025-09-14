[Hashtag treinamentos course](https://www.youtube.com/watch?v=7L0MnVu1KEo)

# LangChain

LangChain works similarly to the *Chain of Responsibility* pattern in software development. Each element in a LangChain implements the `invoke` method, and the output of one step is used as the input for the next.

It offers several features, including:

* **Choice of LLM (Large Language Model)**

  * OpenAI
  * Anthropic
  * Grok
  * Others

* **Chat functionalities**

  * Allows defining roles like *SystemMessage* (instructions for the LLM) and *HumanMessage* (user input).
  * Provides numerous functions to parse and connect workflow steps.

**Limitation:** The data flow is restricted—you can only move forward or backward, without full control over the execution path.
