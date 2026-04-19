"""
Файл: pm2_manager.py
Отвечает за взаимодействие с процессами PM2 через системную консоль.
Содержит класс PM2Manager со статическими методами:
- get_processes(): Получает список процессов в формате JSON.
- start(), stop(), restart(), reload(), reset(), delete(): Выполняют соответствующие команды управления процессом.
- flush(), save(): Выполняют глобальные команды PM2.
- get_logs(): Возвращает последние строки логов процесса.
"""

import subprocess
import json

class PM2Manager:
    
    @staticmethod
    def get_processes():
        try:
            result = subprocess.run(['pm2', 'jlist'], capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def _run_command(command, process_id_or_name):
        try:
            subprocess.run(['pm2', command, str(process_id_or_name)], capture_output=True, text=True, check=True)
            return True, f"Команда '{command}' успешно выполнена для '{process_id_or_name}'"
        except subprocess.CalledProcessError as e:
            return False, f"Ошибка при выполнении '{command}': {e.stderr}"
        except FileNotFoundError:
            return False, "PM2 не установлен или не находится в PATH."

    @classmethod
    def start(cls, process_id_or_name):
        return cls._run_command('start', process_id_or_name)

    @classmethod
    def stop(cls, process_id_or_name):
        return cls._run_command('stop', process_id_or_name)

    @classmethod
    def restart(cls, process_id_or_name):
        return cls._run_command('restart', process_id_or_name)

    @classmethod
    def reload(cls, process_id_or_name):
        return cls._run_command('reload', process_id_or_name)
        
    @classmethod
    def reset(cls, process_id_or_name):
        return cls._run_command('reset', process_id_or_name)

    @classmethod
    def delete(cls, process_id_or_name):
        return cls._run_command('delete', process_id_or_name)
        
    @classmethod
    def flush(cls):
        try:
            subprocess.run(['pm2', 'flush'], capture_output=True, text=True, check=True)
            return True, "Логи PM2 успешно очищены."
        except subprocess.CalledProcessError as e:
            return False, f"Ошибка при очистке логов: {e.stderr}"
        except FileNotFoundError:
            return False, "PM2 не установлен."
            
    @classmethod
    def save(cls):
        try:
            subprocess.run(['pm2', 'save'], capture_output=True, text=True, check=True)
            return True, "Конфигурация процессов PM2 успешно сохранена."
        except subprocess.CalledProcessError as e:
            return False, f"Ошибка при сохранении: {e.stderr}"
        except FileNotFoundError:
            return False, "PM2 не установлен."

    @staticmethod
    def get_logs(process_id_or_name, lines=100):
        try:
            result = subprocess.run(
                ['pm2', 'logs', str(process_id_or_name), '--lines', str(lines), '--nostream'], 
                capture_output=True, text=True, check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, f"Ошибка при получении логов: {e.stderr}"
        except FileNotFoundError:
            return False, "PM2 не установлен."
