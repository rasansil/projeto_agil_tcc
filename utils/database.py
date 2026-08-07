from pathlib import Path
import yaml

import pandas as pd
from sqlalchemy import create_engine

CONFIG_FILE = Path("config/database.yaml")

with open(CONFIG_FILE, encoding="utf-8") as f:
    config = yaml.safe_load(f)

engine = create_engine(
    f"mysql+pymysql://{config['user']}:{config['password']}"
    f"@{config['host']}:{config['port']}/{config['database']}"
)

def publish_dataframe(df, tabela):

    df.to_sql(
        tabela,
        engine,
        if_exists="replace",
        index=False
    )
