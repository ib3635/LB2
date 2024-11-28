import requests
from flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Базовый URL для API НБУ
API_URL = "https://bank.gov.ua/NBU_Exchange/exchange_site"

# Функция для получения данных с НБУ
def get_currency_data(date: str, currency_code: str = 'usd'):
    params = {
        "start": date,
        "end": date,
        "valcode": currency_code,
        "sort": "exchangedate",
        "order": "desc",
        "json": "",  # Указание JSON-формата
    }
    response = requests.get(API_URL, params=params)
    return response

# Обработка запроса для курса USD
@app.route("/currency", methods=["GET"])
def currency():
    param = request.args.get("param")
    content_type = request.headers.get("Content-Type")

    # Получаем текущую дату в формате YYYYMMDD
    today = datetime.today().strftime('%Y%m%d')

    if param == 'today':
        date = today
    elif param == 'yesterday':
        # Получаем дату вчерашнего дня в формате YYYYMMDD
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
        date = yesterday
    else:
        return "Параметр 'param' должен быть 'today' или 'yesterday'."

    # Запрос данных от НБУ
    response = get_currency_data(date)

    if response.status_code != 200:
        return "Ошибка получения данных с НБУ."

    # Обработка формата ответа
    if content_type == "application/json":
        # Если запрашивается JSON
        data = response.json()
        usd_data = [item for item in data if item['cc'] == 'USD']
        if usd_data:
            return jsonify(usd_data[0])
        else:
            return jsonify({"error": "USD data not found"}), 404
    elif content_type == "application/xml":
        # Если запрашивается XML
        data = response.text
        root = ET.fromstring(data)
        usd_data = [item for item in root.findall(".//currency") if item.find("cc").text == "USD"]
        if usd_data:
            # Формируем новый XML только с курсом USD
            usd_rate = usd_data[0].find("rate").text
            usd_xml = f"""
            <currencies>
                <currency>
                    <cc>USD</cc>
                    <rate>{usd_rate}</rate>
                </currency>
            </currencies>
            """
            return Response(usd_xml, mimetype='application/xml')
        else:
            return "<error>USD data not found</error>", 404
    else:
        # Если Content-Type не указан или не поддерживается, возвращаем текстовое сообщение
        return f"Курс USD на {date}: 41.5"

if __name__ == "__main__":
    app.run(port=8000)
