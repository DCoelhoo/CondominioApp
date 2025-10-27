import json
import os

CAMINHO_CONFIG = "config/config.json"

def carregar_config():
    """Lê as configurações do ficheiro JSON, ou cria padrão se não existir."""
    if os.path.exists(CAMINHO_CONFIG):
        try:
            with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
                config = json.load(f)
        except:
            config = {}
    else:
        config = {}

    # Valores padrão (incluindo contador de recibos)
    defaults = {
        "nome_condominio": "Condomínio de Massamá",
        "morada": "",
        "codigo_postal": "",
        "localidade": "",
        "nif": "",
        "telefone": "",
        "email": "",
        "logo": "",
        "assinatura": "",
        "numero_recibo": 0  
    }

    # Garante que todas as chaves existem
    for chave, valor in defaults.items():
        config.setdefault(chave, valor)

    # Guarda de volta (caso haja novos campos)
    guardar_config(config)

    return config


def guardar_config(config):
    """Guarda as configurações no ficheiro JSON."""
    os.makedirs(os.path.dirname(CAMINHO_CONFIG), exist_ok=True)
    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)