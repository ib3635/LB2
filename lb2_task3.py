from flask import Flask, request

app = Flask(__name__)

@app.route("/currency", methods=["GET"])
def currency():
    # Получаем параметр 'today' из запроса
    today = request.args.get('today')

    # Если параметр 'today' передан, возвращаем курс валют
    if today:
        return "USD - 41.5"  # Статичное значение курса валют

    # Если параметр 'today' не передан, возвращаем курс валют по умолчанию
    return "Параметр 'today' не передан"

if __name__ == '__main__':
    app.run(port=8000)
