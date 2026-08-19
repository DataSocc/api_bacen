import json
import calendar
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests


URL = "https://bcb.gov.br"

ARQUIVO = Path("dados.jsonl")


def executar():
    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

    ultimo_dia = calendar.monthrange(
        agora.year,
        agora.month
    )[1]

    data_final = f"{ultimo_dia:02d}/{agora.month:02d}/{agora.year}"

    params = {
        "formato": "json",
        "dataInicial": "01/08/2026",
        "dataFinal": data_final
    }

    print("Chamando API com:")
    print(params)

    response = requests.get(
        URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    try:
        retorno = response.json()
    except ValueError:
        retorno = response.text

    registro = {
        "data_hora": agora.isoformat(),
        "dataInicial": params["dataInicial"],
        "dataFinal": params["dataFinal"],
        "status": response.status_code,
        "retorno": retorno
    }

    with ARQUIVO.open("a", encoding="utf-8") as arquivo:
        arquivo.write(
            json.dumps(registro, ensure_ascii=False) + "\n"
        )

    print("Coleta realizada com sucesso.")


if __name__ == "__main__":
    executar()