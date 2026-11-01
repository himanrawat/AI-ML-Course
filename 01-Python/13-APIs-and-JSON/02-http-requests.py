# ======================================
# TOPIC: MAKING HTTP REQUESTS
# LEVEL: INTERMEDIATE
# ID: python.apis.http-requests
# ======================================

# INTRODUCTION
# Every LLM, vector database and data source you use is reached over HTTP.
# Understanding requests and responses lets you use any API - and debug SDKs.
#
# THEORY
# - A request has a METHOD (GET read, POST create/send, PUT/PATCH update,
#   DELETE), a URL, HEADERS (auth, content type) and an optional BODY (JSON).
# - A response has a STATUS CODE (2xx success, 4xx your mistake - 400 bad
#   request, 401 unauthenticated, 404 not found, 429 rate limited;
#   5xx server problem), headers and a body.
# - Query parameters go in the URL: ?q=python&page=2 (use urlencode).
# - Never hard-code API keys: read them from environment variables (os.environ).
# - The standard library offers urllib.request. In real projects you will
#   usually use the third-party httpx or requests libraries, or a vendor SDK.
# - This example starts a tiny local server so it works offline.
#
# REAL-WORLD ANALOGY
# Ordering at a restaurant counter: you state what you want (method + URL),
# show your membership card (auth header), hand over a written order (body),
# and get back food plus a receipt code (status).
#
# SYNTAX:
#   req = urllib.request.Request(url, data=json_bytes, headers={...}, method="POST")
#   with urllib.request.urlopen(req, timeout=10) as resp: body = resp.read()
#
# SMALL WORKING EXAMPLE:
import json
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode

class DemoAPI(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get("Authorization") != "Bearer secret":
            self.send_response(401)
            self.end_headers()
            return
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        reply = json.dumps({"echo": body["prompt"].upper(), "path": self.path}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(reply)

    def log_message(self, *args):
        pass

server = HTTPServer(("127.0.0.1", 0), DemoAPI)
threading.Thread(target=server.serve_forever, daemon=True).start()
base_url = f"http://127.0.0.1:{server.server_port}"

def post_json(path, payload, api_key):
    request = urllib.request.Request(
        f"{base_url}{path}?{urlencode({'version': 2})}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return response.status, json.loads(response.read())

print(post_json("/v1/echo", {"prompt": "hello api"}, "secret"))
try:
    post_json("/v1/echo", {"prompt": "hi"}, "wrong-key")
except urllib.error.HTTPError as error:
    print("HTTP error:", error.code)
server.shutdown()

# EXPLANATION (LINE BY LINE):
# class DemoAPI(...)            -> a fake API: checks the auth header, echoes JSON.
# HTTPServer(("127.0.0.1", 0))  -> port 0 means "pick any free port".
# threading.Thread(...serve_forever) -> run the server in the background.
# urllib.request.Request(url, data, headers, method="POST") -> build the request.
# urlencode({'version': 2})     -> safe query string "version=2".
# urlopen(request, timeout=5)   -> send it; ALWAYS set a timeout.
# json.loads(response.read())   -> parse the JSON body.
# HTTPError with code 401       -> the server rejected the wrong key.
#
# COMMON MISTAKES:
# 1. Hard-coding secrets in code or committing them to Git.
# 2. No timeout -> a hung request blocks forever.
# 3. Ignoring status codes and parsing error pages as data.
# 4. Building query strings by hand without encoding special characters.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Read an environment variable DEMO_API_KEY with os.environ.get and a default.
# Print whether a key is configured without printing the key itself
# (show only its last 4 characters).

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Extend the DemoAPI with a do_GET that returns a list of items filtered by a
# ?category= query parameter (use urllib.parse.parse_qs). Call it with
# different categories and print the results.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a small reusable APIClient class (base_url, api_key, timeout) with
# get(path, params) and post(path, json) methods, consistent error handling
# (raise a custom APIError with status and body), and a context-manager
# interface. Test it against the local demo server, including 401 and 404.

# YOUR CODE:

