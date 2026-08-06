"""
Projeto: Projeto Ágil TCC

Camada:
Google Sheets -> Raw

Responsabilidade:
- Conectar ao Google Sheets
- Baixar todas as planilhas definidas em config/sources.yaml
- Salvar uma cópia na camada Raw
"""

from pathlib import Path
import yaml
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# Configurações
# ==========================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

CONFIG_FILE = "config/sources.yaml"
SERVICE_ACCOUNT_FILE = "credentials.json"

RAW_PATH = Path("raw")
RAW_PATH.mkdir(exist_ok=True)

# ==========================================
# Autenticação
# ==========================================

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

# ==========================================
# Ler arquivo de configuração
# ==========================================

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# ==========================================
# Download das planilhas
# ==========================================

for nome, info in config["google_sheets"].items():

    print(f"Baixando: {nome}")

    planilha = client.open_by_key(info["spreadsheet_id"])

    aba = planilha.worksheet(info["worksheet"])

    registros = aba.get_all_records()

    df = pd.DataFrame(registros)

    destino = RAW_PATH / f"{nome}.parquet"

    df.to_parquet(destino, index=False)

    print(f"Arquivo salvo em {destino}")

print("\nExtração concluída.")
