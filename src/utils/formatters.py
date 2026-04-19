"""
Файл: formatters.py
Отвечает за форматирование сырых данных (байт, миллисекунд) в человекочитаемый вид.
Содержит функции:
- format_memory(): Преобразует байты в MB/GB.
- format_uptime(): Преобразует миллисекунды аптайма в строку (дни, часы, минуты, секунды).
"""

def format_memory(bytes_val):
    if bytes_val is None:
        return "0 MB"
    mb = bytes_val / (1024 * 1024)
    if mb > 1024:
        return f"{mb / 1024:.2f} GB"
    return f"{mb:.1f} MB"

def format_uptime(uptime_ms, current_time_ms):
    if uptime_ms is None or uptime_ms == 0 or current_time_ms is None:
        return "0s"
        
    diff_ms = current_time_ms - uptime_ms
    if diff_ms < 0:
        return "0s"
        
    seconds = diff_ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    if days > 0:
        return f"{days}d {hours % 24}h"
    elif hours > 0:
        return f"{hours}h {minutes % 60}m"
    elif minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    else:
        return f"{seconds}s"
