import os

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"
task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
timezone = os.getenv("TZ", "Europe/Moscow")  # Или ваш часовой пояс
enable_utc = True
