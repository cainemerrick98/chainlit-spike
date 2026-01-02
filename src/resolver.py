from query import ResolvedQuery, Query, KpiRef, FilterRef, BinaryMetric, SelectItem, MetricExpr, Not, And, Or
from semantic import SemanticModel

def resolve_metric(expr: KpiRef | MetricExpr, semantic: SemanticModel) -> MetricExpr:
    if isinstance(expr, KpiRef):
        return semantic.get_kpi(expr.name).expression

    if isinstance(expr, BinaryMetric):
        return BinaryMetric(
            left=resolve_metric(expr.left, semantic),
            arithmetic=expr.arithmetic,
            right=resolve_metric(expr.right, semantic),
        )

    return expr

def resolve_filter(predicate, semantic: SemanticModel):
    if predicate is None:
        return None

    if isinstance(predicate, FilterRef):
        return semantic.get_filter(predicate.name).predicate

    if isinstance(predicate, And):
        return And(
            predicates=[resolve_filter(p, semantic) for p in predicate.predicates]
        )

    if isinstance(predicate, Or):
        return Or(
            predicates=[resolve_filter(p, semantic) for p in predicate.predicates]
        )

    if isinstance(predicate, Not):
        return Not(
            predicate=resolve_filter(predicate.predicate, semantic)
        )

    return predicate


def resolve_query(query: Query, semantic: SemanticModel) -> ResolvedQuery:
    return ResolvedQuery(
        table_name=query.table_name,
        columns=[
            SelectItem(
                alias=col.alias,
                expression=resolve_metric(col, semantic)
            )
            if isinstance(col, SelectItem)
            # else it is a kpi ref
            else SelectItem(
                alias=col.name,
                expression=resolve_metric(col, semantic)
            )
            for col in query.columns
        ],
        filters=resolve_filter(query.filters, semantic),
        groupby=query.groupby,
        orderby=query.orderby
    )


