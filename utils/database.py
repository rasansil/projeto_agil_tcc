from sqlalchemy import create_engine
import pandas as pd

SERVER = "localhost"
DATABASE = "ProjetoAgilTCC"

CONNECTION_STRING = (
    f"mssql+pyodbc://{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(CONNECTION_STRING)


def publish_dataframe(df: pd.DataFrame,
                      schema: str,
                      table: str):

    df.to_sql(
        name=table,
        con=engine,
        schema=schema,
        if_exists="replace",
        index=False
    )
