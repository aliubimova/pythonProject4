# Импортируем библиотеку requests
import json
from datetime import datetime
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

# Загружаем параметры из json
config_variables = json.load(open('params.json'))

# Устанавливаем переменные
locals().update(config_variables)

# Вычисляем дату начала и дату окончания
DayStart = datetime.today() + relativedelta(years=-1)
DayStart = DayStart.strftime('%Y-%m-%d')
DayEnd = datetime.today().strftime('%Y-%m-%d')

# Адрес api метода для запроса get
url_param = "https://api-metrika.yandex.net/stat/v1/data"


def get_data_to_excel(api_param, header_params, file_name):
    # Отправляем get request (запрос GET)
    response = requests.get(
        url_param,
        params=api_param,
        headers=header_params
    )

    # Преобразуем response с помощью json()
    result = response.json()
    result = result['data']

    # Создаем пустой dict (словать данных)
    dict_data = {}

    # Парсим исходный list формата Json в dictionary (словарь данных)
    for i in range(0, len(result) - 1):
        dict_data[i] = {
            'date': result[i]["dimensions"][0]["name"],
            'traffic-source': result[i]["dimensions"][1]["name"],
            'traffic-details': result[i]["dimensions"][2]["name"],
            'users': result[i]["metrics"][0],
            'visits': result[i]["metrics"][1],
            'pageviews': result[i]["metrics"][2],
            'bounceRate': result[i]["metrics"][3],
            'pageDepth': result[i]["metrics"][4],
            'avgVisitDurationSeconds': result[i]["metrics"][5]
        }

    # Создаем DataFrame из dict (словаря данных или массива данных)
    dict_keys = dict_data[0].keys()
    df = pd.DataFrame.from_dict(dict_data, orient='index', columns=dict_keys)

    # Выгрузка данных из DataFrame в Excel
    df.to_excel(file_name, sheet_name='data', index=False)


for (site_name, metric_id) in METRIC_IDS.items():
    print("site_name: " + site_name)

    # Задаем параметры для API
    api_param = {
        "ids": metric_id,
        "metrics": "ym:s:users,ym:s:visits,ym:s:pageviews,ym:s:bounceRate,ym:s:pageDepth,ym:s:avgVisitDurationSeconds",
        "dimensions": "ym:s:date,ym:s:<attribution>TrafficSource,ym:s:<attribution>SourceEngine",
        "date1": DayStart,
        "date2": DayEnd,
        "sort": "ym:s:date",
        "accuracy": "full",
        "limit": 100000
    }

    # Задаем параметры header_params
    header_params = {
        'GET': '/management/v1/counters HTTP/1.1',
        'Host': 'api-metrika.yandex.net',
        'Authorization': 'OAuth ' + ACCESS_TOKEN,
        'Content-Type': 'application/x-yametrika+json'
    }

    # Название файла Excel
    file_name = PATH + metric_id + "_Трафик.xlsx"

    # Вызываем функцию
    get_data_to_excel(api_param, header_params, file_name)