# MCP Servers

MCP servers are programs that expose specific capabilities to AI applications through standardized protocol interfaces.
Examples include file system servers for document access, database servers for queries, and GitHub servers for code and project management.

### Capabilities

* **Tools**
  Executable functions that an LLM can actively invoke based on user requests.
  They can call external APIs, query databases, modify files, or trigger other logic.
  *Control: the model decides when and how to use them.*

* **Resources**
  Passive, read-only data sources that provide contextual information such as file contents, documents, or database schemas.
  *Control: the application manages access to them.*

* **Prompts**
  Predefined instruction templates that guide the model in working with tools and resources.
  *Control: the user selects and applies them.*

---

### Validation and Design

* MCP uses **JSON Schema validation** to ensure well-defined inputs and outputs.
* Each tool should represent a **single, atomic operation** with clearly specified parameters.
* Some operations may require **human-in-the-loop validation** before execution.

---

### Resources

Resources expose contextual data from files, APIs, databases, or other sources that an AI system may need to understand and operate effectively.
Applications can query these resources directly to provide additional context for the LLM.

