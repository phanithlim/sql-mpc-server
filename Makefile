# CLI for Uvicorn
dev:
	uvicorn app:app --reload

run:
	uvicorn app:app

# CLI for FatMCP
mcp-dev:
	fastmcp dev tools/server.py
mcp:
	fastmcp run tools/server.py --transport sse --host 0.0.0.0 --port 8080