#!/bin/bash

echo "========================================="
echo "ЗАПУСК И ПРОВЕРКА ВСЕХ СЕРВИСОВ"
echo "========================================="
echo

# 1. Запуск FRP
echo "[1] Запуск FRP..."
sudo systemctl start frpc
sudo systemctl status frpc --no-pager | head -3
echo

# 2. Запуск приложения
echo "[2] Запуск приложения catty-reminders..."
sudo systemctl start catty-reminders
sudo systemctl status catty-reminders --no-pager | head -3
echo

# 3. Проверка порта 8181
echo "[3] Проверка порта 8181..."
sudo ss -tlnp | grep 8181 || echo "Порт 8181 не слушается"
echo

# 4. Проверка локального доступа к приложению
echo "[4] Проверка локального доступа к приложению..."
curl -I http://localhost:8181/login 2>/dev/null | head -1
echo

# 5. Запуск webhook
echo "[5] Запуск webhook-handler..."
sudo systemctl start webhook-handler
sudo systemctl status webhook-handler --no-pager | head -3
echo

# 6. Проверка порта 8080
echo "[6] Проверка порта 8080..."
sudo ss -tlnp | grep 8080 || echo "Порт 8080 не слушается"
echo

# 7. Проверка webhook (тестовый POST)
echo "[7] Проверка webhook (тестовый ping)..."
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -d '{"zen": "test"}' -I 2>/dev/null | head -1
echo

# 8. Внешние адреса
echo "[8] Внешние адреса:"
echo "   Приложение: http://app.yaroslavtsev.course.prafdin.ru"
echo "   Webhook: http://webhook.yaroslavtsev.course.prafdin.ru"
echo

# 9. Статус всех сервисов
echo "[9] Статус всех сервисов:"
sudo systemctl status frpc catty-reminders webhook-handler --no-pager | grep "Active:" | sed 's/^/   /'
echo

# 10. Проверка портов
echo "[10] Слушаемые порты:"
sudo ss -tlnp | grep -E "8080|8181" || echo "   Ни один порт не слушается"
echo

# 11. Логи (последние 5 строк)
echo "[11] Последние записи в логах:"
echo "   Лог webhook (последние 5 строк):"
tail -5 /var/log/webhook/webhook.log 2>/dev/null | sed 's/^/      /' || echo "      Лог не найден"
echo
echo "   Лог приложения (последние 5 строк):"
sudo journalctl -u catty-reminders -n 5 --no-pager 2>/dev/null | sed 's/^/      /' || echo "      Нет записей"

echo
echo "========================================="
echo "ПРОВЕРКА ЗАВЕРШЕНА"
echo "========================================="
