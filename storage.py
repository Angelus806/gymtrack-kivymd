# -*- coding: utf-8 -*-
"""
Capa de persistencia. Reemplaza localStorage del HTML original por un
archivo JSON guardado en el almacenamiento privado de la app
(equivalente offline, no requiere permisos especiales en Android).
"""
import json
import os
from datetime import datetime

LOGS_FILENAME = "gymtrack_pro_logs.json"


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def get_app_dir():
    """Directorio de datos de la app (persistente entre sesiones)."""
    try:
        from kivy.app import App
        app = App.get_running_app()
        if app is not None:
            path = app.user_data_dir
            os.makedirs(path, exist_ok=True)
            return path
    except Exception:
        pass
    # Fallback para ejecucion fuera del ciclo de vida de la app (tests)
    path = os.path.join(os.path.expanduser("~"), ".gymtrack_pro")
    os.makedirs(path, exist_ok=True)
    return path


def get_exports_dir():
    path = os.path.join(get_app_dir(), "exports")
    os.makedirs(path, exist_ok=True)
    return path


def logs_path():
    return os.path.join(get_app_dir(), LOGS_FILENAME)


def load_logs():
    path = logs_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_logs(logs):
    path = logs_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def default_exercise_entry(n_sets=3):
    return {"sets": [{} for _ in range(n_sets)], "completed": False}
