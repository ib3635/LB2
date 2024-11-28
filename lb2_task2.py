from flask import Flask

app = Flask(__name__)

# Обработка GET-запроса на корневой маршрут
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World!"  # Ответ на запрос

if __name__ == '__main__':
    app.run(port=8000)  # Запуск сервера на порту 8000
