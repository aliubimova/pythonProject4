import pandas as pd
import json
import requests
from datetime import datetime, timedelta

# Указать количество дней статистики
N_days = 10

# Session_id из кук, можно взять из консоли разработчика при входе в яндекс как на скрине http://joxi.ru/v29M4Oocpx4Q32
Session_id = '3:1659688090.5.2.1658829212947:kLfgWw:28.1.2:1|402695905.0.2|1669359231.691792.2.2:691792|609849184.858878.2.2:858878|3:10256307.521160.j2YlP-Hgn21prdpoqpfEavOpLb0'

# publisherId это id кабинета в zen, можно взять из урла как на скрине http://joxi.ru/DmBonJqi4GqPj2
publisherId = '62e3dc31a0c6cf0f005c0b95'


def get_zen_stat(Session_id, publisherId, N_days):
    Cookie = {
        'Session_id': Session_id
    }

    yesterday = (datetime.now() - timedelta(days=N_days)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')

    parameters = \
        'publisherId=' + publisherId \
        + '&from=' + yesterday \
        + '&to=' + today \
        + '&filterType=' + 'by-event'

    url = 'https://zen.yandex.ru/editor-api/v2/flights/campaigns/statistics-xls?' + parameters

    r = requests.get(url, cookies=Cookie)

    return r


r = get_zen_stat(Session_id, publisherId, N_days)
pd.ExcelFile(r.content).sheet_names
selected_sheet = 'Статистика\xa0кампаний по дням'
pd.Series(pd.read_excel(r.content, selected_sheet, skiprows=2).columns)
df = pd.read_excel(r.content, selected_sheet, skiprows=2)[['Срез на дату', 'Кампания', 'Расход,\nруб. (без НДС)']].drop(
    index=0)
print()
