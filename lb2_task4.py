from flask import Flask, request, jsonify
from dicttoxml import dicttoxml  # Для генерации XML

app = Flask(__name__)

@app.route("/currency", methods=["GET"])
def currency():
    # Получаем значение заголовка 'Content-Type'
    content_type = request.headers.get('Content-Type')

    # Статичный курс валют
    currency_data = {"USD": "41.5"}

    # Если заголовок 'Content-Type' - application/json
    if content_type == 'application/json':
        return jsonify(currency_data)

    # Если заголовок 'Content-Type' - application/xml
    elif content_type == 'application/xml':
        # Конвертируем данные в XML формат
        xml_data = dicttoxml(currency_data)
        return xml_data, 200, {'Content-Type': 'application/xml'}

    # Если заголовок отсутствует или другой
    return "USD - 41.5"  # Ответ в виде обычного текста

if __name__ == '__main__':
    app.run(port=8000)
