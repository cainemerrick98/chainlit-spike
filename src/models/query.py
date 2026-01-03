from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Union, List, Literal

class Comparator(Enum):
    LESS_THAN = '<'
    GREATER_THAN = '>'
    EQUAL = '='
    NOT_EQUAL = '!='
    IN = 'IN'
    NOT_IN = 'NOT IN'
    IS_NULL = 'IS NULL'
    IS_NOT_NULL = 'IS NOT NULL'
    LIKE = 'LIKE'


class Sorting(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class Aggregation(Enum):
    SUM = 'SUM'
    MAX = 'MAX'
    MIN = 'MIN'
    COUNT = 'COUNT'


class Arithmetic(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


# Predicates
ComparisonValue = Union[int, float, str, List[int], List[str], None]
Predicates = Union["And", "Comparison", "Or", "Not", "FilterRef"]

class Comparison(BaseModel):
    column: str
    comparator: Comparator
    value: Optional[ComparisonValue] = None


class And(BaseModel):
    predicates: List[Predicates] = Field(min_length=1)


class Or(BaseModel):
    predicates: List[Predicates] = Field(min_length=1)


class Not(BaseModel):
    predicate: Predicates

# Semantic Model

class KpiRef(BaseModel):
    name: str


class FilterRef(BaseModel):
    name: str 


# Metrics
MetricExpr = Union["QueryColumn", "Measure", "BinaryMetric"]

class QueryColumn(BaseModel):
    kind: Literal["column"]
    name: str

class Measure(BaseModel):
    kind: Literal["measure"]
    column: QueryColumn
    aggregation: Aggregation


class BinaryMetric(BaseModel):
    kind: Literal["binary"]
    left: MetricExpr
    arithmetic: Arithmetic
    right: MetricExpr


class SelectItem(BaseModel):
    alias: Optional[str] = None
    expression: MetricExpr


# Query

class GroupBy(BaseModel):
    column: QueryColumn


class OrderBy(BaseModel):
    column: Union[QueryColumn, MetricExpr]
    sorting: Sorting = Sorting.ASC


class Query(BaseModel):
    table_name: str
    columns: List[Union[SelectItem, KpiRef]]
    filters: Optional[Predicates] = None
    groupby: Optional[List[GroupBy]] = None
    orderby: Optional[List[OrderBy]] = None


class ResolvedQuery(BaseModel):
    table_name: str
    columns: List[SelectItem]
    filters: Optional[Predicates] = None
    groupby: Optional[List[GroupBy]] = None
    orderby: Optional[List[OrderBy]] = None
