# Model Context Protocol (MCP)

[Documentation Reference](https://modelcontextprotocol.io/docs/learn/architecture)

## Overview

The **Model Context Protocol (MCP)** is a **stateful protocol** that follows a **client-server architecture**. It can be used as an API, where an MCP host is responsible for running the client that communicates with the server.

* **MCP Host**: An AI application that manages one or more MCP clients.
* **MCP Client**: A component that maintains a connection to an MCP server and retrieves context for the MCP host to use.
* **MCP Server**: A program that provides context and capabilities to MCP clients.

---

## Architecture

MCP consists of two main layers:

1. **Data Layer**

   * Defines a JSON-RPC–based protocol for client-server communication.
   * Includes lifecycle management and core primitives (tools, resources, prompts, notifications).
   * Authentication is typically handled via OAuth for token exchange.
   * Lifecycle defines what capabilities are supported by both client and server, since MCP is a stateful protocol.

   In practice, the data layer defines interfaces so clients and servers can interact much like APIs.

---

## Core Primitives

Primitives define what clients and servers can offer each other.

### Servers

* **Tools**: Executable functions that AI applications can invoke (e.g., file operations, API calls, database queries).
* **Resources**: Data sources that provide contextual information (e.g., file contents, database records, API responses).
* **Prompts**: Reusable templates that structure interactions with LLMs (including few-shot examples).

Server methods include:

* `/list` → discover available primitives
* `/get` → retrieve specific resources
* `/tools/call` → execute a tool

### Clients

* **Sampling**: Servers can request LLM completions from the client’s AI application. This allows servers to remain model-agnostic and avoid embedding model SDKs directly.
* **Elicitation**: Servers can request additional input or confirmation from users (human-in-the-loop interactions).
* **Logging**: Servers can send log messages to clients for debugging and monitoring.

---

## Notifications

MCP supports **real-time notifications** via JSON-RPC.

* Notifications are **one-way messages** (no response expected).
* Example: `notifications/tools/list_changed` lets servers notify clients when available tools have been updated.
* Typically implemented via **Server-Sent Events (SSE)**.

---

## Client–Server Interaction

1. **Initialization (Handshake)**
   Similar to WebSocket handshakes, the client sends an `initialize` request to establish a connection and negotiate supported features.

   * `protocolVersion`: Ensures client and server use compatible versions.
   * `capabilities`: Declares supported primitives and features (e.g., notifications, elicitation).
   * `clientInfo` and `serverInfo`: Provide versioning and identification for compatibility and debugging.

   **Example request:**

   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "initialize",
     "params": {
       "protocolVersion": "2025-06-18",
       "capabilities": {
         "elicitation": {}
       },
       "clientInfo": {
         "name": "example-client",
         "version": "1.0.0"
       }
     }
   }
   ```

   **Example response:**

   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "protocolVersion": "2025-06-18",
       "capabilities": {
         "tools": { "listChanged": true },
         "resources": {}
       },
       "serverInfo": {
         "name": "example-server",
         "version": "1.0.0"
       }
     }
   }
   ```

---

## Discovery and Tool Execution

Once connected, the MCP client can discover available tools using `tools/list`.
This discovery mechanism is crucial: clients must know what capabilities are available on a server before invoking them.

Each tool description includes:

* `name`: Unique identifier within the server namespace (primary key for execution).
* `title`: Human-readable display name.
* `description`: Explanation of what the tool does.
* `inputSchema`: JSON Schema defining input parameters (with type validation and documentation).

AI applications typically fetch all available tools from connected MCP servers and consolidate them into a unified **tool registry**. LLMs can then dynamically select and call tools during conversations.

**Example tool execution request:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "weather_current",
    "arguments": {
      "location": "San Francisco",
      "units": "imperial"
    }
  }
}
```

**Example response:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Current weather in San Francisco: 68°F, partly cloudy with light winds from the west at 8 mph. Humidity: 65%"
      }
    ]
  }
}
```

---

## Real-Time Updates

Servers that support change notifications (e.g., `listChanged: true`) can push updates to clients via notifications:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

* No response is required.
* The client then issues a new `tools/list` request to refresh its registry.
* This mechanism applies to all MCP primitives, ensuring LLMs always have an up-to-date view of available capabilities.
