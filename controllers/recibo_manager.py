import json
import os

CAMINHO_CONTADOR = "config/condominio.json"

def carregar_numero_recibo():
    """Lê o último número de recibo do ficheiro (ou começa em 0)."""
    if os.path.exists(CAMINHO_CONTADOR):
        try:
            with open(CAMINHO_CONTADOR, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("ultimo_numero", 0)
        except:
            return 0
    return 0

def incrementar_numero_recibo():
    """Incrementa o número do recibo e guarda-o."""
    numero_atual = carregar_numero_recibo() + 1
    with open(CAMINHO_CONTADOR, "w", encoding="utf-8") as f:
        json.dump({"ultimo_numero": numero_atual}, f, indent=4, ensure_ascii=False)
    return numero_atual