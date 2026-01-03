import pandas as pd
from pydantic import BaseModel
from query import Query
from data_connection import BaseDataConnection
from resolver import resolve_query
from compiler import compile_sql

def make_get_data(data_connection: BaseDataConnection):
    def get_data(query: Query) -> dict:
        resolved = resolve_query(query)
        sql = compile_sql(resolved)
        data = data_connection.query(sql)
        return data
    return get_data
