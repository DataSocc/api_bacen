import json
import calendar
from datetime import datetime
from pathlib import Path

import requests

ARQUIVO = Path("dados.jsonl")

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados"


def executar():

    hoje = datetime.now()

    ultimo_dia = calendar.monthrange(
        hoje.year,
        hoje.month
    )[1]

    params = {
        "formato": "json",
        "dataInicial": "01/08/2026",
        "dataFinal": f"{ultimo_dia:02d}/{hoje.month:02d}/{hoje.year}"
    }

    response = requests.get(
        URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    registro = {
        "executado_em": hoje.isoformat(),
        "url": response.url,
        "status": response.status_code,
        "retorno": response.json()
    }

    with open(ARQUIVO, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False))
        f.write("\n")

    print("Sucesso!")
    print(response.url)


if __name__ == "__main__":
    executar()