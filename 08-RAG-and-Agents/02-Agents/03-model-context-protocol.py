# ======================================
# TOPIC: MODEL CONTEXT PROTOCOL (MCP)
# LEVEL: ADVANCED
# ID: rag-agents.agents.mcp
# ======================================

# INTRODUCTION
# Every AI app used to write custom glue code for every tool. The Model Context
# Protocol (MCP) is an open standard that lets any compatible AI application
# connect to any compatible tool/data server - like USB-C for AI integrations.
#
# THEORY
# - MCP SERVERS expose capabilities; MCP CLIENTS (inside AI apps such as
#   Claude Desktop, Claude Code, IDEs or your own agent) connect to them.
# - Capabilities a server can expose:
#   TOOLS (functions the model can call), RESOURCES (readable data like files
#   or records), PROMPTS (reusable prompt templates).
# - Messages use JSON-RPC 2.0 (method, params, id). Key methods: initialize,
#   tools/list, tools/call, resources/list, resources/read.
# - Transports: stdio (local processes) and streamable HTTP (remote servers).
# - Official SDKs exist (Python: the "mcp" package with FastMCP decorators).
# - Security: servers run with your permissions; only install trusted servers,
#   scope credentials, and remember tool results are untrusted input.
#
# REAL-WORLD ANALOGY
# A universal power socket standard: once appliances and sockets agree on one
# shape, any appliance works in any building without custom adapters.
#
# SYNTAX:
#   {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
#    "params": {"name": "get_weather", "arguments": {"city": "Pune"}}}
#
# SMALL WORKING EXAMPLE:
import json

class MiniMCPServer:
    """A toy, in-process imitation of an MCP server's JSON-RPC handling."""

    def __init__(self, name):
        self.name, self.tools = name, {}

    def tool(self, description, schema):
        def register(func):
            self.tools[func.__name__] = {"func": func, "description": description, "inputSchema": schema}
            return func
        return register

    def handle(self, request_json):
        request = json.loads(request_json)
        method, params = request["method"], request.get("params", {})
        try:
            if method == "initialize":
                result = {"serverInfo": {"name": self.name}, "capabilities": {"tools": {}}}
            elif method == "tools/list":
                result = {"tools": [{"name": n, "description": t["description"], "inputSchema": t["inputSchema"]}
                                    for n, t in self.tools.items()]}
            elif method == "tools/call":
                if params["name"] not in self.tools:
                    raise ValueError(f"unknown tool {params['name']}")
                output = self.tools[params["name"]]["func"](**params["arguments"])
                result = {"content": [{"type": "text", "text": json.dumps(output)}]}
            else:
                raise ValueError(f"unknown method {method}")
            return json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result})
        except Exception as error:
            return json.dumps({"jsonrpc": "2.0", "id": request["id"], "error": {"code": -32000, "message": str(error)}})

server = MiniMCPServer("course-notes")

@server.tool("Count words in a note", {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]})
def word_count(text):
    return {"words": len(text.split())}

for request_id, (method, params) in enumerate([
        ("initialize", {}), ("tools/list", {}),
        ("tools/call", {"name": "word_count", "arguments": {"text": "MCP connects tools to models"}}),
        ("tools/call", {"name": "delete_everything", "arguments": {}})], start=1):
    request = json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
    print(f"-> {method}\n<- {server.handle(request)}")

# EXPLANATION (LINE BY LINE):
# MiniMCPServer              -> imitates the JSON-RPC methods of a real MCP server.
# @server.tool(...)          -> registers a function with a description and JSON schema
#                               (like FastMCP's @mcp.tool decorator).
# handle()                   -> dispatches initialize / tools/list / tools/call and returns
#                               JSON-RPC results or errors.
# The client side            -> an AI app calls tools/list, gives the tools to the model,
#                               and forwards the model's tool calls as tools/call.
# Unknown tool               -> a JSON-RPC error, not a crash.
# For real servers use the official "mcp" Python SDK (pip install mcp).
#
# COMMON MISTAKES:
# 1. Installing untrusted MCP servers (they run code with your permissions).
# 2. Exposing broad write tools with no confirmation.
# 3. Vague tool descriptions (the model can't choose correctly).
# 4. Treating server output as trusted instructions.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Register two more tools on the mini server (e.g. search_notes, list_topics)
# and print the tools/list response.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Add resources/list and resources/read methods exposing 3 in-memory notes by
# URI (note://python/lists). Write a client function that lists resources and
# reads one.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Install the official "mcp" package, build a real stdio MCP server exposing a
# tool that reads your course PROGRESS.md, connect it to Claude Code or Claude
# Desktop (claude mcp add ...), and document the setup steps as comments.

# YOUR CODE:

