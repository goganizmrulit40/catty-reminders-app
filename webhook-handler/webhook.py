#!/usr/bin/env python3
"""
GitHub Webhook Handler - Версия с обработкой push-событий
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
import subprocess
import os

# Конфигурация
APP_DIR = "/opt/catty-reminders-app"  # Директория для размещения приложения
LOG_FILE = "/var/log/webhook.log"      # Файл для записи логов

# Настройка логирования
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WebhookHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Обработка POST-запросов от GitHub"""
        # Получаем длину тела запроса
        content_length = int(self.headers.get('Content-Length', 0))
        # Читаем данные
        post_data = self.rfile.read(content_length)
        
        try:
            # Парсим JSON из тела запроса
            payload = json.loads(post_data)
            # Получаем тип события из заголовка
            event = self.headers.get('X-GitHub-Event', 'unknown')
            logging.info(f"Получено событие: {event}")
            
            # Обрабатываем только push-события
            if event == 'push':
                # Извлекаем название ветки из ref (refs/heads/lab1 -> lab1)
                branch = payload.get('ref', '').replace('refs/heads/', '')
                logging.info(f"Push в ветку: {branch}")
                
                # Получаем информацию о коммитах
                commits = payload.get('commits', [])
                if commits:
                    # Берем последний коммит
                    last_commit = commits[-1]
                    logging.info(f"Последний коммит: {last_commit.get('message')}")
                
                # Отправляем успешный ответ
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "received",
                    "branch": branch
                }).encode())
            else:
                # Для других событий просто отвечаем 200 OK
                self.send_response(200)
                self.end_headers()
                
        except Exception as e:
            # Логируем ошибку
            logging.error(f"Ошибка: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Переопределяем метод для записи логов в файл вместо stdout"""
        logging.info(f"{self.address_string()} - {format % args}")

def run(port=8080):
    """Запуск webhook-сервера"""
    server = HTTPServer(('', port), WebhookHandler)
    print(f"Webhook сервер запущен на порту {port}")
    print(f"Логи записываются в {LOG_FILE}")
    print("Нажмите Ctrl+C для остановки")
    server.serve_forever()

if name == 'main':
    run()
