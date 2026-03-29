import json
from utils.storage import get_config_path

CAMINHO_CONFIG = get_config_path()

def carregar_config():
    """Lê as configurações do ficheiro JSON, ou cria padrão se não existir."""
    if CAMINHO_CONFIG.exists():
        try:
            with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            config = {}
    else:
        config = {}

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
        "numero_recibo": 0,
        "quota_base": 30.0,
        "extra_garagem": 0.0,
    }

    for chave, valor in defaults.items():
        config.setdefault(chave, valor)

    guardar_config(config)
    return config


def guardar_config(config):
    """Guarda as configurações no ficheiro JSON."""
    CAMINHO_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)