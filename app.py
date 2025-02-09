from flask import Flask, render_template, request
from main import check_phishing  # Импортируем функцию для проверки ссылок

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        is_safe, message = check_phishing(url)
        return render_template('index.html', is_safe=is_safe, message=message, url=url)
    return render_template('index.html', is_safe=None, message=None, url=None)

if __name__ == '__main__':
    app.run(debug=True)
