from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from tools import mcp

if __name__ == "__main__":
    mcp.run()