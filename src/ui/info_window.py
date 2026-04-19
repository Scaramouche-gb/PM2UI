"""
Файл: info_window.py
Отвечает за отображение детальной информации (JSON) о выбранном процессе.
Содержит класс InfoWindow (наследник QDialog), который выводит форматированный JSON в текстовое поле.
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PyQt6.QtGui import QFont
import json

class InfoWindow(QDialog):
    def __init__(self, process_data, parent=None):
        super().__init__(parent)
        name = process_data.get('name', 'Unknown')
        pid = process_data.get('pm_id', 'Unknown')
        self.setWindowTitle(f"Информация о процессе - {name} (ID: {pid})")
        self.resize(600, 600)
        
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
        
        formatted_json = json.dumps(process_data, indent=4, ensure_ascii=False)
        self.text_edit.setPlainText(formatted_json)
        
        layout.addWidget(self.text_edit)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_close = QPushButton("Закрыть")
        self.btn_close.setStyleSheet("""
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
        """)
        self.btn_close.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_close)
        
        layout.addLayout(btn_layout)
        
        self.setStyleSheet("QDialog { background-color: #161b22; }")
