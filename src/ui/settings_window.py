"""
Файл: settings_window.py
Отвечает за окно настроек приложения, в частности конфигурации Telegram-бота.
Содержит класс SettingsWindow (наследник QDialog), который загружает текущие настройки и сохраняет их при подтверждении.
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox
from src.utils.config import load_config, save_config

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.resize(450, 250)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        self.config = load_config()
        
        self.chk_enabled = QCheckBox("Включить отправку логов ошибок в Telegram")
        self.chk_enabled.setChecked(self.config.get("tg_enabled", False))
        layout.addWidget(self.chk_enabled)
        
        layout.addWidget(QLabel("Telegram Bot Token:"))
        self.inp_token = QLineEdit()
        self.inp_token.setText(self.config.get("tg_token", ""))
        self.inp_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.inp_token.setPlaceholderText("123456789:ABCdefGHIjklmNOPqrst...")
        layout.addWidget(self.inp_token)
        
        layout.addWidget(QLabel("Telegram User/Chat ID:"))
        self.inp_chat_id = QLineEdit()
        self.inp_chat_id.setText(self.config.get("tg_chat_id", ""))
        self.inp_chat_id.setPlaceholderText("Например: 123456789")
        layout.addWidget(self.inp_chat_id)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        button_style = """
            QPushButton {
                background-color: #21262d;
                color: #c9d1d9;
                padding: 6px 12px;
                border: 1px solid #30363d;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #30363d; }
        """
        
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.setStyleSheet(button_style)
        self.btn_save.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.btn_save)
        
        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setStyleSheet(button_style)
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)
        
        layout.addLayout(btn_layout)
        
        self.setStyleSheet("""
            QDialog { background-color: #161b22; color: #c9d1d9; }
            QLabel { color: #c9d1d9; }
            QLineEdit {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 8px;
            }
            QCheckBox { color: #c9d1d9; }
        """)
        
    def save_settings(self):
        self.config["tg_enabled"] = self.chk_enabled.isChecked()
        self.config["tg_token"] = self.inp_token.text().strip()
        self.config["tg_chat_id"] = self.inp_chat_id.text().strip()
        
        if self.config["tg_enabled"]:
            if not self.config["tg_token"] or not self.config["tg_chat_id"]:
                QMessageBox.warning(self, "Ошибка", "Для включения Telegram-бота необходимо заполнить Token и Chat ID.")
                return
                
        save_config(self.config)
        self.accept()
