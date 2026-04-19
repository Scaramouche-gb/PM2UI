"""
Файл: tg_monitor.py
Отвечает за фоновый мониторинг ошибок PM2 и отправку уведомлений в Telegram.
Содержит класс TGMonitorThread (наследник QThread), который асинхронно читает вывод `pm2 logs --err` и отправляет сообщения через aiogram.
"""

import subprocess
import asyncio
import re
from PyQt6.QtCore import QThread
from aiogram import Bot

class TGMonitorThread(QThread):
    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.running = True
        self.process = None

    def run(self):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
        try:
            # Запускаем pm2 logs только для вывода ошибок
            self.process = subprocess.Popen(
                ['pm2', 'logs', '--err', '--raw', '--lines', '0'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
        except FileNotFoundError:
            return

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot = Bot(token=self.bot_token)

        async def send_msg(text):
            try:
                # Ограничиваем длину текста, чтобы не превысить лимит Telegram
                text = text[:4000]
                await bot.send_message(
                    chat_id=self.chat_id, 
                    text=f"⚠️ <b>Ошибка PM2</b>\n<pre>{text}</pre>", 
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Telegram Send Error: {e}")

        while self.running:
            line = self.process.stdout.readline()
            if not line and self.process.poll() is not None:
                break
            
            clean_line = ansi_escape.sub('', line).strip()
            if clean_line and self.running:
                loop.run_until_complete(send_msg(clean_line))

        loop.run_until_complete(bot.session.close())
        loop.close()

    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()
        self.wait()
