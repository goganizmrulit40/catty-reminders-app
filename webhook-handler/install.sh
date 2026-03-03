#!/bin/bash
# Скрипт установки обработчика вебхуков

set -e

echo "Установка обработчика вебхуков GitHub..."

# Создаем директории
sudo mkdir -p /opt/webhook-handler
sudo mkdir -p /var/log/webhook

# Копируем файлы
sudo cp webhook.py /opt/webhook-handler/
sudo cp requirements.txt /opt/webhook-handler/
sudo chmod +x /opt/webhook-handler/webhook.py

# Создаем systemd сервис
sudo tee /etc/systemd/system/webhook-handler.service > /dev/null <<SERVICE
[Unit]
Description=Обработчик вебхуков GitHub
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/webhook-handler
ExecStart=/usr/bin/python3 /opt/webhook-handler/webhook.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Перезагружаем и запускаем
sudo systemctl daemon-reload
sudo systemctl enable webhook-handler
sudo systemctl start webhook-handler

echo "✅ Установка завершена!"
echo "Проверьте статус: sudo systemctl status webhook-handler"
