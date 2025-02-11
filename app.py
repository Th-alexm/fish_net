"""* @file app.py
* @brief Flask-приложение для проверки ссылок на фишинг.
*
* Этот файл содержит минимальное Flask-приложение, которое обрабатывает POST-запросы с URL-адресом,
* передаёт их в функцию `check_phishing` (из модуля main.py) и возвращает результат проверки
* на веб-странице index.html.
"""
from flask import Flask, render_template, request
from main import check_phishing  # Импортируем функцию для проверки ссылок

"""
* @var app
* @brief Экземпляр Flask-приложения.
*
* Создаём объект Flask, который будет обрабатывать входящие HTTP-запросы и маршруты.
"""
app = Flask(__name__)

"""
* @brief Обрабатывает корневой маршрут '/' для методов GET и POST.
*
* - При методе GET просто рендерит страницу index.html с начальными значениями.
* - При методе POST извлекает URL из формы, передаёт его в функцию `check_phishing`,
*   получает результат и отображает на той же странице.
*
* @return Возвращает сгенерированный шаблон HTML с результатами проверки или без них.
"""

@app.route('/', methods=['GET', 'POST'])

def index():
    """
    * @brief Проверка метода запроса и дальнейшая логика обработки.
    *
    * Если метод POST, получаем введённый пользователем URL из формы,
    * передаём его в `check_phishing`, получаем результат (is_safe, message)
    * и затем рендерим шаблон с результатами. Если метод GET, отображаем шаблон
    * с пустыми значениями.
    *
    * @param None
    * @return HTML-страница с результатами проверки.
    """
    if request.method == 'POST':
        url = request.form['url']
        is_safe, message = check_phishing(url)
        return render_template('index.html', is_safe=is_safe, message=message, url=url)
    
    # Метод GET или другие случаи
    return render_template('index.html', is_safe=None, message=None, url=None)

"""
* @brief Точка входа в приложение.
*
* Запускает Flask-сервер в режиме отладки.  
"""

if __name__ == '__main__':
    app.run(debug=True)
