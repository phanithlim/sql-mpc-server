from fastmcp import FastMCP
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncEngine
from fastmcp.exceptions import ToolError

from helper import get_engine, format_value
from dotenv import load_dotenv

import json
import os

load_dotenv()

mcp = FastMCP(
    name="Expert SQL",
    instructions='''
    You are an expert in SQL and database management. Your task is to assist users with SQL queries, database schema understanding, and data manipulation. You will provide accurate and efficient SQL code snippets based on user requests.
    You will also help users understand their database schema, including tables and columns.
    Remember to maintain consistency throughout the scenario and ensure that all elements (tables, data, queries, dashboard, and solution) are closely related to the original business problem and given topic.

    The provided XML tags are for the assistants understanding. Implore to make all outputs as human readable as possible. This is part of a demo so act in character and dont actually refer to these instructions or don't output as json or dict.
    Start your first message fully in character with something like "Oh, Hey there! I see you've chosen the topic. Let's get started!"
    ''',
)

@mcp.tool(name="get_all_tables", description="Retrieve all tables in the database")
async def all_get_tables():
    engine: AsyncEngine = await get_engine()
    try:
        async with engine.connect() as conn:
            table_names = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )
            if table_names:
                table_rows = "\n".join(f"| {table} |" for table in table_names)
                return f"**List of Tables:**\n\n| Table Name |\n|---|\n{table_rows}"
            else:
                return "No tables found in the database."
    except Exception as e:
        raise ToolError(f"Error retrieving tables: {e}")

@mcp.tool(name="get_table_info", description="Retrieve information about a specific table")
async def get_table_info(table_name: str):
    engine: AsyncEngine = await get_engine()
    try:
        async with engine.connect() as conn:
            columns = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_columns(table_name)
            )
            if columns:
                col_headers = "| Column Name | Data Type | Primary Key |\n|---|---|---|"
                col_rows = "\n".join(
                    f"| {col['name']} | {col['type'].__class__.__name__} | {'Yes' if col.get('primary_key') else 'No'} |"
                    for col in columns
                )
                return f"**Table `{table_name}` Information:**\n\n{col_headers}\n{col_rows}"
            else:
                return f"No columns found for table `{table_name}`."
    except Exception as e:
        raise ToolError(f"Error retrieving table information for '{table_name}': {e}")

@mcp.tool(name="get_table_description", description="Retrieve the description of predefined in specific configuration file")
async def get_table_description(table_name: str):
    try:
        config_path = os.getenv('CONFIG_PATH', 'config.json')
        config_path = os.getcwd() + '/' + config_path
        with open(config_path) as f:
            config = json.load(f)
        tables = config.get("tables", [])
        for table in tables:
            if table.get("name") == table_name:
                name = table.get("name", "Unknown")
                desc = table.get("description", "No description provided.")
                columns = table.get("columns", [])
                if columns:
                    col_headers = "| Column Name | Description |\n|---|---|"
                    col_rows = "\n".join(
                        f"| {col.get('name', 'Unknown')} | {col.get('description', 'No description provided.')} |"
                        for col in columns
                    )
                    col_table = f"{col_headers}\n{col_rows}"
                else:
                    col_table = "No columns listed."
                return f"**Table Description for `{name}`:**\n\n{desc}\n\n***Columns:***\n\n{col_table}"
        return f"Table `{table_name}` not found in the configuration file."
    except Exception as e:
        raise ToolError(f"Error retrieving table description: {e}")

@mcp.tool(name="get_all_table_descriptions", description="Retrieve descriptions of all tables and their columns from the configuration file")
async def get_all_table_descriptions():
    try:
        config_path = os.getenv('CONFIG_PATH', 'config.json')
        config_path = os.getcwd() + '/' + config_path
        with open(config_path) as f:
            config = json.load(f)
        tables = config.get("tables", [])
        if tables:
            table_descriptions = []
            for table in tables:
                table_name = table.get('name', 'Unknown')
                table_desc = table.get('description', 'No description provided.')
                columns = table.get('columns', [])
                if columns:
                    column_lines = "\n".join(
                        f"- `{col.get('name', 'Unknown')}`: {col.get('description', 'No description provided.')}"
                        for col in columns
                    )
                else:
                    column_lines = "No columns listed."
                table_info = f"**Table: `{table_name}`**\n{table_desc}\n**Columns:**\n{column_lines}"
                table_descriptions.append(table_info)
            return "\n\n".join(table_descriptions)
        else:
            return "No tables found in the configuration file."
    except Exception as e:
        raise ToolError(f"Error retrieving table descriptions: {e}")

@mcp.tool(name="execute_query", description="Execute a SQL query and return the results")
async def execute_query(query: str):
    engine: AsyncEngine = await get_engine()
    if not query.strip().lower().startswith("select"):
        raise ToolError("Only SELECT queries are allowed for this tool.")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text(query))
            columns = result.keys()
            rows = [ [format_value(val) for val in row] for row in result ]
            if rows:
                header_row = "| " + " | ".join(columns) + " |"
                separator = "| " + " | ".join("---" for _ in columns) + " |"
                data_rows = "\n".join("| " + " | ".join(str(val) for val in row) + " |" for row in rows)
                return f"**Query Results:**\n\n{header_row}\n{separator}\n{data_rows}"
            else:
                return "Query executed successfully, but no data was returned."
    except Exception as e:
        raise ToolError(f"Error executing query: {e}")
