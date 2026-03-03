#!/usr/bin/env python3
"""
Обработчик вебхуков GitHub - Версия с обновлением кода
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
import subprocess
import os
import threading

# Конфигурация
REPO_URL = "https://github.com/goganizmrulit40/catty-reminders-app.git"
APP_DIR = "/opt/catty-reminders-app"
LOG_FILE = "/var/log/webhook.log"
BRANCH = "lab1"

# Настройка логирования
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def update_code():
    """Клонирование или обновление репозитория"""
    try:
        if not os.path.exists(APP_DIR):
            logging.info("Клонирование репозитория...")
            subprocess.run([
                "git", "clone", "-b", BRANCH, "--single-branch", REPO_URL, APP_DIR
            ], check=True)
            logging.info("Репозиторий успешно склонирован")
        else:
            logging.info("Обновление репозитория...")
            os.chdir(APP_DIR)
            subprocess.run(["git", "fetch", "origin"], check=True)
            subprocess.run(["git", "reset", "--hard", f"origin/{BRANCH}"], check=True)
            logging.info("Репозиторий успешно обновлен")
        
        # Получаем текущий коммит
        os.chdir(APP_DIR)
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True
        )
        commit_hash = result.stdout.strip()
        logging.info(f"Текущий коммит: {commit_hash}")
        
        return True, commit_hash
    except Exception as e:
        logging.error(f"Не удалось обновить код: {e}")
        return False, None

class WebhookHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Обработка POST запросов"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data)
            event = self.headers.get('X-GitHub-Event', 'неизвестно')
            logging.info(f"Получено событие {event}")
            
            if event == 'push':
                branch = payload.get('ref', '').replace('refs/heads/', '')
                logging.info(f"Push в ветку: {branch}")
                
                if branch == BRANCH:
                    # Запускаем обновление в фоне
                    thread = threading.Thread(target=update_code)
                    thread.start()
                    
                    self.send_response(202)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "принято",
                        "branch": branch,
                        "message": "Обновление запущено"
                    }, ensure_ascii=False).encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "игнорируется",
                        "branch": branch,
                        "message": f"Отслеживается только ветка {BRANCH}"
                    }, ensure_ascii=False).encode())
            else:
                self.send_response(200)
                self.end_headers()
                
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        logging.info(f"{self.address_string()} - {format % args}")

def run(port=8080):
    server = HTTPServer(('', port), WebhookHandler)
    print(f"Сервер вебхуков запущен на порту {port}")
    server.serve_forever()

if __name__ == '__main__':
    run()
