#!/usr/bin/env python3
"""Regenerate tools.json and operations.json from a Pixtorium MCP binary.

    python3 scripts/update_reference.py /path/to/pixtorium-mcp
"""
import json, subprocess, sys

binary = sys.argv[1] if len(sys.argv) > 1 else "pixtorium-mcp"
requests = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize",
     "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                "clientInfo": {"name": "docs", "version": "0"}}},
    {"jsonrpc": "2.0", "method": "notifications/initialized"},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
     "params": {"name": "list_operations", "arguments": {}}},
]
out = subprocess.run([binary], input="\n".join(map(json.dumps, requests)) + "\n",
                     capture_output=True, text=True, timeout=60, check=True).stdout
answers = {m["id"]: m["result"] for m in map(json.loads, out.splitlines()) if "id" in m}
init, tools = answers[1], answers[2]["tools"]
json.dump({"serverInfo": init["serverInfo"], "instructions": init["instructions"],
           "tools": tools}, open("tools.json", "w"), indent=1, ensure_ascii=False)
ops = json.loads(answers[3]["content"][0]["text"])
json.dump(ops, open("operations.json", "w"), indent=1, ensure_ascii=False)
print(f'{init["serverInfo"]["version"]}: {len(tools)} tools, {len(ops)} operations')
