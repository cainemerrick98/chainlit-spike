from pydantic import BaseModel
from enum import Enum
from typing import Optional
from query import MetricExpr, Predicate


class DataTypes(Enum):
    DATE = "DATE"
    STRING = "STRING"
    NUMERIC = "NUMERIC"
    BOOLEAN = "BOOLEAN"


class Column(BaseModel):
    name: str
    data_type: DataTypes
    description: str


class Table(BaseModel):
    name: str
    columns: list[Column]
    description: str


class KPI(BaseModel):
    name: str
    expression: MetricExpr
    description: str
    return_type: DataTypes


class Filter(BaseModel):
    name: str
    predicate: Predicate 
    description: str


class SemanticModel(BaseModel):
    tables: list[Table]
    kpis: Optional[list[KPI]] = None
    filters: Optional[list[Filter]] = None