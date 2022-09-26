import requests
site = 66237895
startDate = '2022-09-15'
endDate = '2022-09-18'


API_URL = 'https://api-metrika.yandex.ru/stat/v1/data?'
params = {
        'date1': startDate,
        'date2': endDate,
        'id': site,
        'metrics': 'ym:s:visits',
        'dimensions': 'ym:s:startURL',  # ,ym:s:month
        'accuracy': 'full'
}

r = requests.get(API_URL, params=params, headers={'Authorization': 'OAuth y0_AgAAAABbFME2AAhudQAAAADPeyxyp0s1GEEpSKGLGx6rrIAPCs27Z9Y', 'Content-Type': 'application/x-yametrika+json',
'Content-Length': '123'}, timeout=40)
#r = requests.get("https://api-metrika.yandex.net/stat/v1/data?ids=66237895&metrics=ym%3As%3Apageviews")
r = r.json()
r = r['data']
print (r)

# Создаем пустой dict (словать данных)
dict_data = {}
for i in range(0, len(result) - 1):
    dict_data[i] = {
        'page': result[i]["dimensions"][0]["name"],
        'visits': result[i]["metrics"][0],

    }

# Создаем DataFrame из dict (словаря данных или массива данных)
dict_keys = dict_data[0].keys()
df = pd.DataFrame.from_dict(dict_data, orient='index', columns=dict_keys)

# Выгрузка данных из DataFrame в Excel
print(df)
