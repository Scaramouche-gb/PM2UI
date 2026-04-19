"""
Файл: logs_window.py
Отвечает за отображение логов выбранного процесса.
Содержит класс LogsWindow (наследник QDialog) с методами для загрузки логов через PM2Manager и их очистки от ANSI-кодов.
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PyQt6.QtGui import QFont
import re
from src.core.pm2_manager import PM2Manager

class LogsWindow(QDialog):
    def __init__(self, process_id, process_name, parent=None):
        super().__init__(parent)
        self.process_id = process_id
        self.setWindowTitle(f"Логи - {process_name} (ID: {process_id})")
        self.resize(750, 550)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        button_style = """
            QPushButton {
                background-color: #21262d;
                color: #c9d1d9;
                padding: 8px 16px;
                border: 1px solid #30363d;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #30363d; }
            QPushButton:pressed { background-color: #282e33; }
        """
        
        self.btn_refresh = QPushButton("Обновить логи")
        self.btn_refresh.setStyleSheet(button_style)
        self.btn_refresh.clicked.connect(self.load_logs)
        btn_layout.addWidget(self.btn_refresh)
        
        self.btn_close = QPushButton("Закрыть")
        self.btn_close.setStyleSheet(button_style)
        self.btn_close.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_close)
        
        layout.addLayout(btn_layout)
        
        self.setStyleSheet("QDialog { background-color: #161b22; }")
        self.load_logs()
        
    def load_logs(self):
        self.text_edit.setPlainText("Загрузка логов...")
        success, logs = PM2Manager.get_logs(self.process_id)
        if success:
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            clean_logs = ansi_escape.sub('', logs)
            self.text_edit.setPlainText(clean_logs)
            
            scrollbar = self.text_edit.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        else:
            self.text_edit.setPlainText(f"Не удалось загрузить логи:\n{logs}")
