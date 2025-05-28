from pydantic import BaseModel, Field
from typing import Optional, List

class ColumnModel(BaseModel):
    type: str = Field(..., description="The data type of the column")
    name: str = Field(..., description="The name of the column")
    primary_key: bool = Field(False, description="Indicates if the column is a primary key")
    
class TableModel(BaseModel):
    name: str = Field(..., description="The name of the table")
    columns: List[ColumnModel] = Field(..., description="List of columns in the table")

class TablesModel(BaseModel):
    tables: list[str] = Field(..., description="List of table names in the database")
    
class QueryResultModel(BaseModel):
    columns: List[str] = Field(..., description="List of column names in the result set")
    rows: List[List[Optional[str]]] = Field(..., description="List of rows, each row is a list of values")
    
    def __str__(self):
        return f"QueryResultModel(columns={self.columns}, rows={self.rows})"
