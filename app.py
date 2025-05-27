from fastapi.responses import HTMLResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from tools import mcp
import uvicorn

## FastAPI app
app = FastAPI(docs_url=None, redoc_url=None)

mcp_app = mcp.http_app(
    path='/mcp',
    transport='sse',
    middleware=[
        Middleware(CORSMiddleware, allow_origins=["*"]),
    ]
)
app.mount("/mcp-server", mcp_app)

## Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>FastMCP Server</title>
        </head>
        <body>
            <p>MCP Server is now running!</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)