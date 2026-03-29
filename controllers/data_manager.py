import json
import shutil
from pathlib import Path
from utils.storage import get_moradores_path

ARQUIVO_MORADORES = get_moradores_path()
ARQUIVO_ANTIGO = Path("data/moradores.json")

def garantir_arquivo():
    ARQUIVO_MORADORES.parent.mkdir(parents=True, exist_ok=True)

    if ARQUIVO_MORADORES.exists():
        return

    if ARQUIVO_ANTIGO.exists():
        shutil.copy(ARQUIVO_ANTIGO, ARQUIVO_MORADORES)
        return

    ARQUIVO_MORADORES.write_text("[]", encoding="utf-8")

def carregar_moradores():
    garantir_arquivo()

    try:
        with open(ARQUIVO_MORADORES, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_moradores(moradores):
    ARQUIVO_MORADORES.parent.mkdir(parents=True, exist_ok=True)

    with open(ARQUIVO_MORADORES, "w", encoding="utf-8") as f:
        json.dump(moradores, f, ensure_ascii=False, indent=4)