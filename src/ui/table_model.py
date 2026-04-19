"""
Файл: table_model.py
Отвечает за модель данных для таблицы процессов.
Содержит класс ProcessTableModel (наследник QAbstractTableModel), который связывает сырые данные процессов PM2 с QTableView и настраивает их отображение.
"""

from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt6.QtGui import QColor, QBrush, QFont
from src.utils.formatters import format_memory, format_uptime
import time

class ProcessTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []
        self._headers = ["ID", "Name", "Status", "CPU", "Memory", "Uptime", "Restarts"]

    def update_data(self, new_data):
        # Если количество строк не изменилось, обновляем без сброса выделения
        if len(self._data) == len(new_data):
            self._data = new_data
            if len(self._data) > 0:
                top_left = self.index(0, 0)
                bottom_right = self.index(len(self._data) - 1, len(self._headers) - 1)
                self.dataChanged.emit(top_left, bottom_right)
        else:
            self.beginResetModel()
            self._data = new_data
            self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headers[section]
        return None

    def get_process_at(self, row):
        if 0 <= row < len(self._data):
            return self._data[row]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        row = index.row()
        col = index.column()
        proc = self._data[row]
        
        pm2_env = proc.get('pm2_env', {})
        monit = proc.get('monit', {})
        
        p_id = proc.get('pm_id', 'N/A')
        p_name = proc.get('name', 'N/A')
        p_status = pm2_env.get('status', 'N/A')
        restarts = pm2_env.get('restart_time', 0)
        
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0: return str(p_id)
            if col == 1: return p_name
            if col == 2: return p_status.upper()
            if col == 3: 
                cpu_val = monit.get('cpu', 0) if monit else 0
                return f"{cpu_val}%"
            if col == 4:
                mem_val = monit.get('memory', 0) if monit else 0
                return format_memory(mem_val)
            if col == 5:
                uptime_ms = pm2_env.get('pm_uptime', 0)
                current_time = int(time.time() * 1000)
                return format_uptime(uptime_ms, current_time) if p_status == 'online' else "0s"
            if col == 6: return str(restarts)
            
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
            
        elif role == Qt.ItemDataRole.ForegroundRole:
            if col == 2:
                if p_status == 'online':
                    return QBrush(QColor('#3fb950')) # GitHub Green
                elif p_status in ['stopped', 'errored']:
                    return QBrush(QColor('#f85149')) # GitHub Red
                else:
                    return QBrush(QColor('#d29922')) # GitHub Yellow
                    
        elif role == Qt.ItemDataRole.FontRole:
            if col == 2:
                font = QFont()
                font.setBold(True)
                return font
                
        return None
