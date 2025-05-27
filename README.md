# SQL MCP Server
A FastAPI-based, read-only server for managing and querying SQL databases using the Model Context Protocol (MCP). This is a simple template for an MCP server designed to interact with SQL databases in a read-only mode.

## Installation
Install UV package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
or pipx
```bash
pip install uv
```

## Install Dependencies
```bash
uv sync
```

## Usage
Run MCP Server Inspector:
```bash
make mcp-dev
```
Run the FastAPI application:
```bash
make dev
```
## Project Structure

```
├── app.py            # FastAPI application entry point
├── Dockerfile        # Containerization support
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # uv dependency lock file
├── config.json      # Configuration file for MCP server
├── tools/
│   ├── server.py     # Server logic for FastMCP
│   ├── model.py      # Response models for FastMCP
│   ├── helpers.py    # Helper functions for FastMCP
│   └── __init__.py
└── README.md          # Project documentation
```

## Features
- `get_all_tables`: Retrieve a list of tables in the database.
- `get_table_info`: Get information about a specific table.
- `get_table_description`: Retrieves the description of a specific table from the config file (useful if tables or columns have short names).
- `get_all_table_descriptions`: Retrieves descriptions of all tables from the config file (useful if tables or columns have short names).
- `execute_query`: Execute a SQL query and return the results.

## Deployment
### Docker
Build the Docker image:
```bash
docker build -t mcp-server .
```
Run the Docker container:
```bash
docker run -d -p 8000:8000 mcp-server
```
- MCP server url: `http://localhost:8000/mcp-server/mcp`