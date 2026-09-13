# Инструкция по настройке локальной разработки

## Архитектура разработки

- **В Docker контейнерах**: nginx, MySQL
- **На хосте (для отладки)**: backend, frontend, admin

## Быстрый старт

### 1. Подготовка окружения

```bash
# Скопируйте пример конфигурации
cp .env.dev.example .env

# Отредактируйте .env под свои нужды
nano .env
```

### 2. Запуск Docker сервисов (nginx + DB)

```bash
# Запустить nginx и базу данных
docker-compose -f docker-compose.dev.yaml up -d

# Проверить статус
docker-compose -f docker-compose.dev.yaml ps

# Посмотреть логи
docker-compose -f docker-compose.dev.yaml logs -f
```

### 3. Запуск Backend (на хосте)

```bash
# Установите зависимости (если нужно)
pip install -r requirements.txt

# Запустите backend на порту 5000
python main.py
# или
flask run --host=0.0.0.0 --port=5000
```

### 4. Запуск Admin Backend (на хосте)

```bash
cd admin_bot_path  # путь к admin приложению

# Установите зависимости
pip install -r requirements.txt

# Примените миграции
python manage.py migrate

# Запустите dev server на порту 5001
python manage.py runserver 0.0.0.0:5001
```

### 5. Запуск Frontend (на хосте)

```bash
cd frontend/foodmap_front

# Установите зависимости (если нужно)
npm install

# Запустите dev server (по умолчанию порт 5173)
npm run dev
```

### 6. Доступ к приложению

- Frontend: http://localhost (через nginx) или http://localhost:5173 (напрямую)
- Backend API: http://localhost/api
- Admin Panel: http://localhost/admin_page
- MySQL: localhost:3306

## Отладка

### Проверка подключения к БД

```bash
# Из хоста
mysql -h 127.0.0.1 -P 3306 -u egor_user -p

# Внутри контейнера
docker exec -it db_mysql_egor_dev mysql -u root -p
```

### Логи nginx

```bash
docker exec -it nginx_dev tail -f /var/log/nginx/error.log
docker exec -it nginx_dev tail -f /var/log/nginx/access.log
```

### Health check

```bash
curl http://localhost/health
```

## Переход к Production

### Параметры для учета:

1. **Переменные окружения**
   - Создайте отдельный `.env.production`
   - Используйте сильные пароли и секретные ключи
   - Отключите DEBUG режим (`DEBUG=False`, `DJANGO_DEBUG=False`)

2. **База данных**
   - Используйте volumes для персистентности данных
   - Настройте бэкапы
   - Измените дефолтные пароли

3. **Nginx**
   - Используйте конфиг с HTTPS (см. `Deploy/nginx.confd/nginx-https.conf`)
   - Настройте SSL сертификаты
   - Включите gzip компрессию
   - Настройте rate limiting
   - Добавьте security headers

4. **Backend/Frontend**
   - Соберите production билд frontend: `npm run build`
   - Используйте gunicorn/uwsgi вместо dev серверов
   - Настройте процессы мониторинга (systemd, supervisor)
   - Соберите Docker образы для всех сервисов

5. **Секреты и безопасность**
   - Используйте Docker secrets или vault для секретов
   - Не коммитьте `.env` файлы
   - Ограничьте доступ к портам БД (не expose наружу)
   - Используйте файрвол

6. **Мониторинг**
   - Добавьте health checks для всех сервисов
   - Настройте логирование (ELK, Loki)
   - Добавьте метрики (Prometheus, Grafana)

## Docker Compose профили

### Development (текущая конфигурация)
```bash
docker-compose -f docker-compose.dev.yaml up -d
```

### Production (полная сборка)
```bash
docker-compose -f docker-compose.local.yaml up -d
```

## Полезные команды

### Остановка dev окружения
```bash
docker-compose -f docker-compose.dev.yaml down
```

### Остановка с удалением volumes
```bash
docker-compose -f docker-compose.dev.yaml down -v
```

### Пересборка после изменений в nginx конфиге
```bash
docker-compose -f docker-compose.dev.yaml restart nginx
```

### Выполнение миграций в контейнере DB
```bash
docker exec -it db_mysql_egor_dev mysql -u root -p < ./migrations/migration.sql
```

## Структура файлов

```
.
├── docker-compose.dev.yaml          # Dev композ (nginx + DB)
├── docker-compose.local.yaml        # Production композ (все сервисы)
├── .env                             # Переменные окружения
├── .env.dev.example                 # Пример dev конфига
├── local_test/
│   └── nginx.confd/
│       └── nginx-local-dev.conf     # Nginx конфиг для dev
├── Deploy/
│   └── nginx.confd/
│       ├── nginx.conf               # Production конфиг
│       └── nginx-https.conf         # HTTPS конфиг
└── DEV_SETUP.md                     # Эта инструкция
```

## Troubleshooting

### Backend не подключается к БД
- Проверьте, что контейнер DB запущен: `docker ps`
- Проверьте MYSQL_HOST в .env (должен быть `localhost` для хоста)
- Проверьте порт 3306: `netstat -tlnp | grep 3306`

### Nginx не видит сервисы на хосте
- Убедитесь, что используется `host.docker.internal` в nginx конфиге
- Проверьте, что сервисы слушают 0.0.0.0, а не только 127.0.0.1

### Frontend HMR не работает через nginx
- Проверьте WebSocket соединения в browser dev tools
- Убедитесь, что proxy headers настроены правильно в nginx

### Порт уже занят
```bash
# Найти процесс на порту
sudo lsof -i :5000
sudo lsof -i :5173

# Убить процесс
kill -9 <PID>
```
