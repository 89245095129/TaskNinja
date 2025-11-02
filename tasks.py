from celery_app import celery
import time
from datetime import datetime

# Простая задача для отправки "email"
@celery.task(bind=True)
def send_email(self, recipient, subject, message):
    """
    Имитация отправки email - долгая операция
    """
    total_steps = 5
    
    # Имитируем процесс отправки с прогрессом
    for i in range(total_steps):
        time.sleep(2)  # Имитируем задержку
        progress = (i + 1) * 100 // total_steps
        
        # Обновляем прогресс задачи
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i + 1,
                'total': total_steps,
                'progress': progress,
                'status': f'Отправка email... Шаг {i + 1}/{total_steps}'
            }
        )
    
    # Имитируем результат отправки
    result = {
        'status': 'Email отправлен успешно!',
        'recipient': recipient,
        'subject': subject,
        'message': message[:50] + '...' if len(message) > 50 else message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'task_id': self.request.id
    }
    
    return result

# Быстрая задача для вычислений
@celery.task
def calculate_sum(numbers):
    """
    Вычисление суммы чисел - быстрая операция
    """
    time.sleep(1)  # Небольшая задержка для наглядности
    result = sum(numbers)
    
    return {
        'numbers': numbers,
        'sum': result,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# Долгая задача для тяжелых вычислений
@celery.task(bind=True)
def long_running_task(self, duration=10):
    """
    Долгая задача для демонстрации
    """
    total_seconds = duration
    
    for i in range(total_seconds):
        time.sleep(1)
        progress = (i + 1) * 100 // total_seconds
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i + 1,
                'total': total_seconds,
                'progress': progress,
                'status': f'Выполняется долгая задача... {i + 1}/{total_seconds} сек.'
            }
        )
    
    return {
        'status': 'Долгая задача завершена!',
        'duration': f'{duration} секунд',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
