from flask import Flask, render_template, request, jsonify, session
import uuid
from tasks import send_email, calculate_sum, long_running_task

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.before_request
def make_session_permanent():
    # Создаем уникальный ID сессии для каждого пользователя
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email_route():
    """Эндпоинт для отправки email в фоне"""
    data = request.json
    recipient = data.get('recipient', 'test@example.com')
    subject = data.get('subject', 'Тестовое письмо')
    message = data.get('message', 'Привет от Celery!')
    
    # Запускаем задачу в фоне
    task = send_email.delay(recipient, subject, message)
    
    return jsonify({
        'message': 'Email поставлен в очередь на отправку!',
        'task_id': task.id,
        'status_url': f'/task_status/{task.id}'
    }), 202

@app.route('/calculate', methods=['POST'])
def calculate_route():
    """Эндпоинт для вычислений в фоне"""
    data = request.json
    numbers = data.get('numbers', [1, 2, 3, 4, 5])
    
    # Запускаем задачу вычисления
    task = calculate_sum.delay(numbers)
    
    return jsonify({
        'message': 'Вычисление запущено!',
        'task_id': task.id,
        'status_url': f'/task_status/{task.id}'
    }), 202

@app.route('/long_task', methods=['POST'])
def long_task_route():
    """Эндпоинт для долгой задачи"""
    data = request.json
    duration = data.get('duration', 10)
    
    task = long_running_task.delay(duration)
    
    return jsonify({
        'message': 'Долгая задача запущена!',
        'task_id': task.id,
        'status_url': f'/task_status/{task.id}'
    }), 202

@app.route('/task_status/<task_id>')
def task_status(task_id):
    """Проверка статуса задачи"""
    from celery_app import celery
    
    # Получаем результат задачи
    task_result = celery.AsyncResult(task_id)
    
    response = {
        'task_id': task_id,
        'state': task_result.state,
        'status': 'В ожидании...'
    }
    
    if task_result.state == 'PENDING':
        response.update({
            'status': 'Задача в очереди...'
        })
    elif task_result.state == 'PROGRESS':
        response.update({
            'status': 'Выполняется...',
            'progress': task_result.info.get('progress', 0),
            'details': task_result.info
        })
    elif task_result.state == 'SUCCESS':
        response.update({
            'status': 'Завершено успешно!',
            'result': task_result.result,
            'progress': 100
        })
    elif task_result.state == 'FAILURE':
        response.update({
            'status': 'Ошибка!',
            'result': str(task_result.info)
        })
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
