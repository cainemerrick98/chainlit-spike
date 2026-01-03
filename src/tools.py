import pandas as pd
import json
from pydantic import BaseModel
from models.query import Query
from data_connection import BaseDataConnection
from models.semantic import SemanticModel
from resolver import resolve_query
from compiler import compile_sql
import inspect

TOOL_REGISTRY = {}

class ToolRegistration(BaseModel):
    type: str
    name: str
    description: str
    parameters: object
    required: list[str]

MAX_PREVIEW_ROWS = 30

def make_get_data(data_connection: BaseDataConnection, semantic_model: SemanticModel):
    def get_data(*, query: Query) -> dict:
        query = Query.model_validate(query)
        resolved = resolve_query(query, semantic_model)
        sql = compile_sql(resolved)
        print(sql)
        data = data_connection.query(sql)
        # TODO: store query result somewhere.
        preview_rows = data.get("rows", [])[:MAX_PREVIEW_ROWS]
        return {
            **data,
            "rows": preview_rows,
            "truncated": len(data.get("rows", [])) > MAX_PREVIEW_ROWS,
        }
    return get_data


def register_tool(name: str):
    def decorator(fn):
        TOOL_REGISTRY[name] = fn
        return fn
    return decorator

def run_tool(name: str, parameters: str):
    fn = TOOL_REGISTRY.get(name)
    if fn is None:
        raise KeyError()
    
    if isinstance(parameters, str):
        parameters = json.loads(parameters)

    sig = inspect.signature(fn)

    parameters = {k:v for k,v in parameters.items() if k in sig.parameters}

    result = fn(**parameters)

    return result
