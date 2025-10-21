import json, os

CAMINHO = "data/moradores.json"

def carregar_dados():
    if not os.path.exists(CAMINHO):
        salvar_dados([])
    with open(CAMINHO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(dados):
    os.makedirs(os.path.dirname(CAMINHO), exist_ok=True)
    with open(CAMINHO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)