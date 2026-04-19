"""
Файл: config.py
Отвечает за сохранение и загрузку конфигурации приложения.
Содержит функции:
- load_config(): Загружает данные из settings.json.
- save_config(): Сохраняет данные в settings.json.
"""

import json
import os

CONFIG_PATH = "settings.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"tg_enabled": False, "tg_token": "", "tg_chat_id": ""}

def save_config(config_data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4, ensure_ascii=False)
