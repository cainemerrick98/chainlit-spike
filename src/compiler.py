from models.query import (
    ResolvedQuery,
    SelectItem,
    QueryColumn,
    Measure,
    BinaryMetric,
    Comparison,
    And,
    Or,
    Not,
)

def compile_metric(expr) -> str:
    if isinstance(expr, Measure):
        return f"{expr.aggregation.value}({expr.column.name})"

    if isinstance(expr, BinaryMetric):
        left = compile_metric(expr.left)
        right = compile_metric(expr.right)
        return f"({left} {expr.arithmetic.value} {right})"

    if isinstance(expr, QueryColumn):
        return expr.name

    raise ValueError(f"Unsupported metric expression: {expr}")


def compile_predicate(pred) -> str:
    if isinstance(pred, Comparison):
        if pred.value is None:
            return f"{pred.column} {pred.comparator.value}"
        if isinstance(pred.value, str):
            return f"{pred.column} {pred.comparator.value} '{pred.value}'"
        if isinstance(pred.value, list):
            values = ", ".join(
                f"'{v}'" if isinstance(v, str) else str(v)
                for v in pred.value
            )
            return f"{pred.column} {pred.comparator.value} ({values})"
        return f"{pred.column} {pred.comparator.value} {pred.value}"

    if isinstance(pred, And):
        return "(" + " AND ".join(compile_predicate(p) for p in pred.predicates) + ")"

    if isinstance(pred, Or):
        return "(" + " OR ".join(compile_predicate(p) for p in pred.predicates) + ")"

    if isinstance(pred, Not):
        return f"(NOT {compile_predicate(pred.predicate)})"

    raise ValueError(f"Unsupported predicate: {pred}")

# TODO we need to validate the aliases
def compile_sql(query: ResolvedQuery) -> str:
    select_clause = ", ".join(
        f"{compile_metric(col.expression)}"
        + (f" AS {col.alias.replace('" "', "")}" if col.alias else "")
        for col in query.columns
    )

    sql = f"SELECT {select_clause}\nFROM {query.table_name}"

    if query.filters:
        sql += f"\nWHERE {compile_predicate(query.filters)}"

    if query.groupby:
        group_cols = ", ".join(g.column.name for g in query.groupby)
        sql += f"\nGROUP BY {group_cols}"

    if query.orderby:
        order_cols = ", ".join(
            f"{compile_metric(o.column)} {o.sorting.value}"
            for o in query.orderby
        )
        sql += f"\nORDER BY {order_cols}"

    return sql
