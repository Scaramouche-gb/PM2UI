"""
Файл: main.py
Отвечает за инициализацию и запуск приложения.
Содержит функцию main(), которая создает экземпляр QApplication, применяет стиль и отображает главное окно.
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Использование стиля Fusion для кроссплатформенного современного вида
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
