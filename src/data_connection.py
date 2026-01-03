import pandas as pd
import duckdb

class BaseDataConnection():
    def __init__():
        pass

    def query(self, query: str) -> dict:
        raise NotImplementedError()


class DuckDBDataConnection(BaseDataConnection):
    def __init__(self, tables: dict[str, pd.DataFrame]):
        self.con = duckdb.connect(':memory:')
        for name, df in tables.items():
            self.con.register(name, df)

    def query(self, sql: str) -> dict:
        df = self.con.execute(sql).df()
        return {
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records"),
            "row_count": len(df),
        }
