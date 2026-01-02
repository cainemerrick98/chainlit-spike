import pandas as pd
import operator
from pydantic import BaseModel
from enum import Enum
from typing import Any

ops = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}


class ResultTypes(Enum):
    QUERY = "QUERY"
    TABLE = "TABLE"
    CHART = "CHART"
    KPI = "KPI"


class ToolResult(BaseModel):
    result_type: ResultTypes
    data: Any
    renderable: bool


def get_data(filters: list[tuple[str, int|float, str]], data: pd.DataFrame) -> ToolResult:
    for col, val, com in filters:
        data = data[ops[com](data[col], val)]

    return ToolResult(
        result_type=ResultTypes.QUERY,
        data=data,
        renderable=False
    )

def display_table(data: pd.DataFrame) -> ToolResult:
    return ToolResult(
        result_type=ResultTypes.TABLE,
        data=data,
        renderable=True
    )


