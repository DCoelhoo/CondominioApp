from pathlib import Path
import os

APP_NAME = "CondominioApp"

def get_data_dir() -> Path:
    flet_data = os.getenv("FLET_APP_STORAGE_DATA")
    if flet_data:
        base = Path(flet_data)
    else:
        base = Path(os.getenv("APPDATA", str(Path.home())))

    data_dir = base / APP_NAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_moradores_path() -> Path:
    return get_data_dir() / "moradores.json"

def get_config_path() -> Path:
    return get_data_dir() / "config.json"

def get_updates_dir() -> Path:
    p = get_data_dir() / "updates"
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_backups_dir() -> Path:
    p = get_data_dir() / "backups"
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_documentos_dir() -> Path:
    return Path.home() / "Documents"

def get_recibos_dir() -> Path:
    p = get_documentos_dir() / APP_NAME / "Recibos"
    p.mkdir(parents=True, exist_ok=True)
    return p