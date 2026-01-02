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
    predicates: Predicate


class Column(BaseModel):
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
    expression: Union[Column, MetricExpr]


class GroupBy(BaseModel):
    column: str


class OrderBy(BaseModel):
    column: str


class Query(BaseModel):
    table_name: str
    columns: List[SelectItem]
    filters: Optional[Predicate] = None
    groupby: Optional[List[GroupBy]] = None
    orderby: Optional[List[OrderBy]] = None
