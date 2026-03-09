#!/bin/bash

echo "Остановка всех сервисов..."

sudo systemctl stop webhook-handler
echo "Webhook остановлен"

sudo systemctl stop catty-reminders
echo "Приложение остановлено"

sudo systemctl stop frpc
echo "FRP остановлен"

echo
echo "Все сервисы остановлены"
