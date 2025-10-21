import json
import os

CAMINHO_CONFIG = "config/condominio.json"

def carregar_config():
    if not os.path.exists(CAMINHO_CONFIG):
        return {}
    with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_config(dados):
    os.makedirs(os.path.dirname(CAMINHO_CONFIG), exist_ok=True)
    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)