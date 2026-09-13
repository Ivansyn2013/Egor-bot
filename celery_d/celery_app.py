from celery import Celery

app = Celery("bot_broadcast")
app.config_from_object("celery_config")

# Автоматический импорт задач из файла tasks.py
app.autodiscover_tasks()
