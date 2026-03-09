#!/bin/bash

echo "===== ПРОВЕРКА СИСТЕМЫ ====="
echo

# FRP
if systemctl is-active --quiet frpc; then
    echo "FRP: работает"
else
    echo "FRP: НЕ работает"
fi

# Приложение
if systemctl is-active --quiet catty-reminders; then
    echo "Приложение: работает"
else
    echo "Приложение: НЕ работает"
fi

# Webhook
if systemctl is-active --quiet webhook-handler; then
    echo "Webhook: работает"
else
    echo "Webhook: НЕ работает"
fi

# Порты
echo
if ss -tlnp | grep -q ":8181"; then
    echo "Порт 8181: слушается"
else
    echo "Порт 8181: НЕ слушается"
fi

if ss -tlnp | grep -q ":8080"; then
    echo "Порт 8080: слушается"
else
    echo "Порт 8080: НЕ слушается"
fi

# Локальный доступ
echo
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8181/login 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo "Приложение локально: отвечает (200)"
elif [ -n "$HTTP_CODE" ]; then
    echo "Приложение локально: отвечает с кодом $HTTP_CODE"
else
    echo "Приложение локально: НЕ отвечает"
fi

WEBHOOK_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -d '{"zen": "test"}' 2>/dev/null)

if [ "$WEBHOOK_CODE" = "200" ] || [ "$WEBHOOK_CODE" = "202" ]; then
    echo "Webhook локально: отвечает ($WEBHOOK_CODE)"
else
    echo "Webhook локально: НЕ отвечает (код $WEBHOOK_CODE)"
fi

# Внешние адреса
echo
ID="yaroslavtsev"
PROXY="course.prafdin.ru"

APP_EXT=$(curl -s -o /dev/null -w "%{http_code}" -I "http://app.$ID.$PROXY" 2>/dev/null | head -1)
if [ -n "$APP_EXT" ]; then
    echo "app.$ID.$PROXY: доступен (код $APP_EXT)"
else
    echo "app.$ID.$PROXY: НЕ доступен"
fi

WEBHOOK_EXT=$(curl -s -o /dev/null -w "%{http_code}" -I "http://webhook.$ID.$PROXY" 2>/dev/null | head -1)
if [ -n "$WEBHOOK_EXT" ]; then
    echo "webhook.$ID.$PROXY: доступен (код $WEBHOOK_EXT)"
else
    echo "webhook.$ID.$PROXY: НЕ доступен"
fi

# Логи
echo
if [ -f /var/log/webhook/webhook.log ]; then
    echo "Лог webhook: существует"
else
    echo "Лог webhook: НЕ найден"
fi

# Последний коммит
echo
cd /opt/catty-reminders 2>/dev/null
if [ $? -eq 0 ]; then
    LAST_COMMIT=$(git log -1 --oneline 2>/dev/null)
    if [ -n "$LAST_COMMIT" ]; then
        echo "Последний коммит: $LAST_COMMIT"
    else
        echo "Не удалось получить коммит"
    fi
else
    echo "Папка приложения не найдена"
fi

echo
echo "===== ПРОВЕРКА ЗАВЕРШЕНА ====="
