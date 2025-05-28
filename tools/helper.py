import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from datetime import datetime, date

load_dotenv()

async def get_engine() -> AsyncEngine:
    return create_async_engine(os.getenv('DATABASE_URL', 'sqlite:///default.db'))

async def get_db_info():
    engine = await get_engine()
    async with engine.connect() as conn:
        url = conn.engine.url
        result = {
            "dialect": engine.dialect.name,
            "version": list(engine.dialect.server_version_info), # type: ignore
            "database": url.database,
            "host": url.host,
            "user": url.username
        }
    return result

def format_value(val):
    """Format a value for display, handling None and datetime types"""
    if val is None:
        return "NULL"
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    return str(val)
           

