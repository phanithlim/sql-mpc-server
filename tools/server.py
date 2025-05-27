from fastmcp import FastMCP
from sqlalchemy import inspect, text
from helper import get_engine, format_value
from sqlalchemy.ext.asyncio import AsyncEngine
from model import TableModel, ColumnModel, TablesModel, QueryResultModel
import json
import os
from dotenv import load_dotenv

load_dotenv()  


mcp = FastMCP(
    name="Expert SQL",
    instructions='''
    You are an expert in SQL and database management. Your task is to assist users with SQL queries, database schema understanding, and data manipulation. You will provide accurate and efficient SQL code snippets based on user requests.
    You will also help users understand their database schema, including tables and columns.
    '''
)

@mcp.tool(name="get_all_tables", description="Retrieve all tables in the database")
async def all_get_tables():
    """
    Retrieve all tables in the database.
    Returns:
        TablesModel: A model containing a list of TableModel objects.
        dict: An error dictionary if an exception occurs.
    """
    engine: AsyncEngine = await get_engine()
    try:
        async with engine.connect() as conn:
            table_names = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )
            return TablesModel(tables=table_names)
        
    except Exception as e:
        print(f"Error retrieving table names: {e}") # Log the error
        return {"error": f"Error retrieving table names: {e}"}

@mcp.tool(name="get_table_info", description="Retrieve information about a specific table")
async def get_table_info(table_name: str):
    """
    Retrieve information about a specific table.
    Args:
        table_name (str): The name of the table to retrieve information for.
    Returns:
        TableModel: A model containing the table name and its columns.
        dict: An error dictionary if an exception occurs.
    """
    engine: AsyncEngine = await get_engine() # Await the async get_engine()

    try:
        async with engine.connect() as conn:
            columns = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_columns(table_name)
            )
            column_models = [
                ColumnModel(
                    type=col['type'].__class__.__name__,
                    name=col['name'],
                    primary_key=bool(col.get('primary_key', False)) # Ensure boolean conversion
                ) for col in columns
            ]
            return TableModel(
                name=table_name,
                columns=column_models
            )
    except Exception as e:
        raise Exception(f"Error retrieving table info for {table_name}: {e}")
    
@mcp.tool(name="get_table_description", description="Retrieve the description of predefined in specific configuration file")
async def get_table_description(table_name: str):
    config = await json.loads(open(os.getenv('CONFIG_PATH', './config.json')).read())
    tables = config.get("tables", [])
    for table in tables:
        if table.get("name") == table_name:
            return table
    return {"error": "Table not found."}

@mcp.tool(name="get_all_table_descriptions", description="Retrieve descriptions of all predefined tables in the configuration file")
async def get_all_table_descriptions():
    config = await json.loads(open(os.getenv('CONFIG_PATH', './config.json')).read())
    tables = config.get("tables", [])
    return {"tables": tables} if tables else {"error": "No tables found."}

@mcp.tool(name="execute_query", description="Execute a SQL query and return the results")
async def execute_query(query: str):
    """
    Execute a raw SQL query and return the results.
    Args:
        query (str): The SQL query string to execute.
    Returns:
        dict: A dictionary containing 'columns' (list of column names) and 'rows' (list of lists representing data rows).
              Returns an error dictionary if an exception occurs.
    """
    engine: AsyncEngine = await get_engine()
    if not query.strip().lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed."}

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text(query))
            columns = result.keys()
            rows = []
            for row in result:
                rows.append([format_value(val) for val in row])

            return QueryResultModel(
                columns=list(columns),
                rows=rows
            )
    except Exception as e:
        print(f"Error executing query: {query}\nError: {e}") # Log the error
        return {"error": f"Error executing query: {e}"}