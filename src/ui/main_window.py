"""
Файл: main_window.py
Отвечает за главное окно приложения и общую логику интерфейса.
Содержит класс MainWindow (наследник QMainWindow):
- setup_ui(), apply_styles(): Настройка интерфейса и стилей.
- refresh_data(): Обновление таблицы процессов.
- manage_process(): Обработка действий с процессами.
- show_logs(), show_info(), show_settings(): Открытие дочерних окон.
- apply_tg_settings(): Управление фоновым потоком Telegram-мониторинга.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QHeaderView, QMessageBox, QLabel, 
                             QGroupBox, QTableView, QAbstractItemView, QDialog)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from src.core.pm2_manager import PM2Manager
from src.ui.logs_window import LogsWindow
from src.ui.info_window import InfoWindow
from src.ui.settings_window import SettingsWindow
from src.ui.table_model import ProcessTableModel
from src.utils.config import load_config
from src.core.tg_monitor import TGMonitorThread
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PM2 Dashboard")
        self.resize(1050, 700)
        
        # Telegram мониторинг
        self.tg_thread = None
        self.apply_tg_settings()
        
        self.setup_ui()
        
        # Таймер для автообновления данных каждые 2 секунды
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(2000)
        
        self.refresh_data()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        header_label = QLabel("Управление процессами PM2")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        header_label.setFont(font)
        header_label.setStyleSheet("color: #c9d1d9; margin-bottom: 5px;")
        layout.addWidget(header_label)

        # Панель управления (кнопки)
        top_controls = QHBoxLayout()
        top_controls.setSpacing(15)
        
        # Группа: Управление процессом
        process_group = QGroupBox("Действия с процессом")
        process_layout = QHBoxLayout()
        process_layout.setSpacing(8)
        
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_restart = QPushButton("Restart")
        self.btn_reload = QPushButton("Reload")
        self.btn_reset = QPushButton("Reset Meta")
        self.btn_info = QPushButton("Info")
        self.btn_logs = QPushButton("Logs")
        self.btn_delete = QPushButton("Delete")
        
        process_layout.addWidget(self.btn_start)
        process_layout.addWidget(self.btn_stop)
        process_layout.addWidget(self.btn_restart)
        process_layout.addWidget(self.btn_reload)
        process_layout.addWidget(self.btn_reset)
        process_layout.addWidget(self.btn_info)
        process_layout.addWidget(self.btn_logs)
        process_layout.addWidget(self.btn_delete)
        process_group.setLayout(process_layout)
        
        top_controls.addWidget(process_group)
        
        # Группа: Глобальные действия
        global_group = QGroupBox("Общие")
        global_layout = QHBoxLayout()
        global_layout.setSpacing(8)
        
        self.btn_flush = QPushButton("Flush Logs")
        self.btn_save = QPushButton("Save Config")
        self.btn_settings = QPushButton("Settings")
        self.btn_refresh = QPushButton("Refresh")
        
        global_layout.addWidget(self.btn_flush)
        global_layout.addWidget(self.btn_save)
        global_layout.addWidget(self.btn_settings)
        global_layout.addWidget(self.btn_refresh)
        global_group.setLayout(global_layout)
        
        top_controls.addWidget(global_group)
        top_controls.addStretch()

        layout.addLayout(top_controls)

        # Таблица процессов с использованием QTableView и модели
        self.table = QTableView()
        self.model = ProcessTableModel()
        self.table.setModel(self.model)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)

        # Подключение сигналов
        self.btn_start.clicked.connect(lambda: self.manage_process('start'))
        self.btn_stop.clicked.connect(lambda: self.manage_process('stop'))
        self.btn_restart.clicked.connect(lambda: self.manage_process('restart'))
        self.btn_reload.clicked.connect(lambda: self.manage_process('reload'))
        self.btn_reset.clicked.connect(lambda: self.manage_process('reset'))
        self.btn_delete.clicked.connect(lambda: self.manage_process('delete'))
        self.btn_logs.clicked.connect(self.show_logs)
        self.btn_info.clicked.connect(self.show_info)
        
        self.btn_flush.clicked.connect(self.flush_logs)
        self.btn_save.clicked.connect(self.save_pm2)
        self.btn_settings.clicked.connect(self.show_settings)
        self.btn_refresh.clicked.connect(self.refresh_data)
        
        self.apply_styles()

    def apply_styles(self):
        # Строгая профессиональная тёмная тема (а-ля GitHub Dark/VS Code)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1117;
            }
            QWidget {
                color: #c9d1d9;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
                font-size: 13px;
            }
            QGroupBox {
                border: 1px solid #30363d;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                padding-bottom: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #8b949e;
                font-weight: bold;
            }
            QPushButton {
                padding: 6px 12px;
                background-color: #21262d;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #30363d;
                border-color: #8b949e;
            }
            QPushButton:pressed {
                background-color: #282e33;
            }
            
            /* Специфичные цвета для важных кнопок */
            QPushButton#btn_primary {
                background-color: #238636;
                color: #ffffff;
                border-color: #2ea043;
            }
            QPushButton#btn_primary:hover { background-color: #2ea043; }
            
            QPushButton#btn_danger {
                background-color: #da3633;
                color: #ffffff;
                border-color: #f85149;
            }
            QPushButton#btn_danger:hover { background-color: #f85149; }
            
            QTableView {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                outline: none;
                alternate-background-color: #161b22;
            }
            QTableView::item {
                padding: 8px;
                border-bottom: 1px solid #21262d;
            }
            QTableView::item:selected {
                background-color: #1f6feb;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #161b22;
                color: #8b949e;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #30363d;
                font-weight: bold;
                font-size: 13px;
            }
            QScrollBar:vertical {
                border: none;
                background: #0d1117;
                width: 14px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #30363d;
                min-height: 20px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #484f58;
            }
            QMessageBox {
                background-color: #161b22;
                color: #c9d1d9;
            }
            QMessageBox QLabel {
                color: #c9d1d9;
            }
            QMessageBox QPushButton {
                min-width: 80px;
            }
        """)
        self.btn_delete.setObjectName("btn_danger")
        self.btn_save.setObjectName("btn_primary")
        self.btn_start.setObjectName("btn_primary")

    def apply_tg_settings(self):
        if hasattr(self, 'tg_thread') and self.tg_thread:
            self.tg_thread.stop()
            self.tg_thread = None
            
        config = load_config()
        if config.get("tg_enabled") and config.get("tg_token") and config.get("tg_chat_id"):
            self.tg_thread = TGMonitorThread(config["tg_token"], config["tg_chat_id"])
            self.tg_thread.start()

    def show_settings(self):
        dialog = SettingsWindow(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.apply_tg_settings()

    def refresh_data(self):
        processes = PM2Manager.get_processes()
        
        selected_id = self.get_selected_process_id(show_warning=False)
        self.model.update_data(processes)
        
        if selected_id is not None:
            self.select_process_by_id(selected_id)

    def get_selected_process(self, show_warning=True):
        selection_model = self.table.selectionModel()
        if not selection_model.hasSelection():
            if show_warning:
                QMessageBox.warning(self, "Внимание", "Пожалуйста, сначала выберите процесс из списка.")
            return None
            
        row = selection_model.selectedRows()[0].row()
        return self.model.get_process_at(row)

    def get_selected_process_id(self, show_warning=True):
        proc = self.get_selected_process(show_warning)
        return str(proc.get('pm_id')) if proc else None

    def select_process_by_id(self, p_id):
        for row in range(self.model.rowCount()):
            proc = self.model.get_process_at(row)
            if str(proc.get('pm_id')) == p_id:
                self.table.selectRow(row)
                break

    def manage_process(self, action):
        proc = self.get_selected_process()
        if not proc:
            return
            
        p_id = str(proc.get('pm_id'))
        p_name = proc.get('name', 'Unknown')
        
        success = False
        msg = ""
        
        if action == 'start':
            success, msg = PM2Manager.start(p_id)
        elif action == 'stop':
            success, msg = PM2Manager.stop(p_id)
        elif action == 'restart':
            success, msg = PM2Manager.restart(p_id)
        elif action == 'reload':
            success, msg = PM2Manager.reload(p_id)
        elif action == 'reset':
            success, msg = PM2Manager.reset(p_id)
        elif action == 'delete':
            reply = QMessageBox.question(self, 'Подтверждение', 
                                         f"Удалить процесс '{p_name}' (ID: {p_id})?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                success, msg = PM2Manager.delete(p_id)
            else:
                return

        if not success:
            QMessageBox.critical(self, "Ошибка", msg)
        else:
            self.refresh_data()
            
    def show_logs(self):
        proc = self.get_selected_process()
        if not proc:
            return
            
        p_id = str(proc.get('pm_id'))
        p_name = proc.get('name', 'Unknown')
        self.logs_dialog = LogsWindow(p_id, p_name, self)
        self.logs_dialog.show()

    def show_info(self):
        proc = self.get_selected_process()
        if not proc:
            return
            
        self.info_dialog = InfoWindow(proc, self)
        self.info_dialog.show()

    def flush_logs(self):
        reply = QMessageBox.question(self, 'Подтверждение', 
                                     "Вы уверены, что хотите очистить логи всех процессов?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = PM2Manager.flush()
            if success:
                QMessageBox.information(self, "Успех", msg)
            else:
                QMessageBox.critical(self, "Ошибка", msg)

    def save_pm2(self):
        success, msg = PM2Manager.save()
        if success:
            QMessageBox.information(self, "Успех", msg)
        else:
            QMessageBox.critical(self, "Ошибка", msg)

    def closeEvent(self, event):
        # Останавливаем поток Telegram при закрытии приложения
        if hasattr(self, 'tg_thread') and self.tg_thread:
            self.tg_thread.stop()
        super().closeEvent(event)
