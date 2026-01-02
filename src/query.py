from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Union, List

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

class Predicate(BaseModel):
    pass

ComparisonValue = Union[int, float, str, List[int], List[str], None]

class Comparison(Predicate):
    column: str
    comparator: Comparator
    value: Optional[ComparisonValue] = None


class And(Predicate):
    predicates: List[Predicate] = Field(min_length=1)


class Or(Predicate):
    predicates: List[Predicate] = Field(min_length=1)


class Not(Predicate):
    predicate: Predicate

# Semantic Model

class KpiRef(BaseModel):
    name: str


class FilterRef(Predicate):
    name: str 


# Metrics

class QueryColumn(BaseModel):
    name: str


class MetricExpr(BaseModel):
    pass


class Measure(MetricExpr):
    column: str
    aggregation: Aggregation


class BinaryMetric(MetricExpr):
    left: MetricExpr
    arithmetic: Arithmetic
    right: MetricExpr


class SelectItem(BaseModel):
    alias: Optional[str] = None
    expression: Union[QueryColumn, MetricExpr]


# Query

class GroupBy(BaseModel):
    column: QueryColumn


class OrderBy(BaseModel):
    column: Union[QueryColumn, MetricExpr]
    sorting: Sorting = Sorting.ASC


class Query(BaseModel):
    table_name: str
    columns: List[Union[SelectItem, KpiRef]]
    filters: Optional[Union[Predicate]] = None
    groupby: Optional[List[GroupBy]] = None
    orderby: Optional[List[OrderBy]] = None


class ResolvedQuery(BaseModel):
    table_name: str
    columns: List[SelectItem]
    filters: Optional[Predicate] = None
    groupby: Optional[List[GroupBy]] = None
    orderby: Optional[List[OrderBy]] = None
