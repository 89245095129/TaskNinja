from celery import Celery

# Создаем экземпляр Celery
def make_celery():
    celery = Celery(
        'tasks',
        broker='redis://localhost:6379/0',  # Брокер задач
        backend='redis://localhost:6379/0'  # Хранилище результатов
    )
    
    # Настройки
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Europe/Moscow',
        enable_utc=True,
    )
    
    return celery

# Инициализируем Celery
celery = make_celery()
