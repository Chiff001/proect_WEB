from f import finder, finder2, finder3
from io import BytesIO
import requests
from PIL import Image


def search1(toponym_to_find):  # Поиск приютов рядом с адресом
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    json_response = requests.get(geocoder_api_server, params=geocoder_params).json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    x, y = toponym["Point"]["pos"].split()
    point1 = ','.join([x, y]) + ',pm2rdl'
    search_params = {
        "apikey": "55158855-ae53-4c29-9123-e8e8795497b9",
        "text": "приют",
        "lang": "ru_RU",
        "ll": ','.join([x, y]),
        "type": "biz",
        "results": 10
    }
    json_response_2 = requests.get("https://search-maps.yandex.ru/v1/", params=search_params).json()
    print(json_response_2)
    n1 = -100
    n2 = 100
    m1 = -100
    m2 = 100
    res = ''
    for i in range(len(json_response_2["features"])):
        x1, y1 = str(json_response_2["features"][i]["geometry"]["coordinates"][0]), str(json_response_2["features"][i]["geometry"]["coordinates"][1])
        if float(x1) > n1:
            n1 = float(x1)
        if float(x1) < n2:
            n2 = float(x1)
        if float(y1) > m1:
            m1 = float(y1)
        if float(y1) < m2:
            m2 = float(y1)
        if json_response_2["features"][i]["properties"]["CompanyMetaData"]["Hours"]["text"] == 'ежедневно, круглосуточно':
            res += ','.join([x1, y1]) + ',pm2gnm' + str(i + 1) + "~"
        elif 'круглосуточно' not in json_response_2["features"][i]["properties"]["CompanyMetaData"]["Hours"]["text"]:
            res += ','.join([x1, y1]) + ',pm2gnm' + str(i + 1) + "~"
        else:
            res += ','.join([x1, y1]) + ',pm2gnm' + str(i + 1) + "~"
    res = res[:-1]
    map_params = {
        "bbox": ','.join([str(n1), str(m1)]) + '~' + ','.join([str(n2), str(m2)]),
        "l": "map",
        "pt": point1 + "~" + res
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    res = requests.get(map_api_server, params=map_params)
    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(res.content)
    return json_response_2


def search2(toponym_to_find):  # Поиск приюта по адреса (находит ближайший к адресу)
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    json_response = requests.get(geocoder_api_server, params=geocoder_params).json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    x, y = toponym["Point"]["pos"].split()
    point1 = ','.join([x, y]) + ',pm2rdm'
    search_params = {
        "apikey": "55158855-ae53-4c29-9123-e8e8795497b9",
        "text": "приют",
        "lang": "ru_RU",
        "ll": ','.join([x, y]),
        "type": "biz"
    }
    json_response_2 = requests.get("https://search-maps.yandex.ru/v1/", params=search_params).json()
    x1, y1 = str(json_response_2["features"][0]["geometry"]["coordinates"][0]), str(
        json_response_2["features"][0]["geometry"]["coordinates"][1])
    point2 = ','.join([x1, y1]) + ',pm2gnm'
    map_params = {
        "bbox": ','.join([x, y]) + '~' + ','.join([x1, y1]),
        "l": "map",
        "pt": point1 + "~" + point2
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    res = requests.get(map_api_server, params=map_params)
    S = finder2([float(x), float(y)], [float(x1), float(y1)])
    print(json_response_2["features"][0]["properties"])
    print("Расстояние:", round(S, 2))
    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(res.content)
    return json_response_2, S


def search3(toponym_to_find):  # Поиск по названию
    search_params = {
        "apikey": "55158855-ae53-4c29-9123-e8e8795497b9",
        "text": toponym_to_find,
        "lang": "ru_RU",
        "type": "biz"
    }
    json_response_2 = requests.get("https://search-maps.yandex.ru/v1/", params=search_params).json()
    x1, y1 = str(json_response_2["features"][0]["geometry"]["coordinates"][0]), str(
        json_response_2["features"][0]["geometry"]["coordinates"][1])
    point2 = ','.join([x1, y1]) + ',pm2gnm'
    print(json_response_2)
    spn = finder3(json_response_2)
    map_params = {
        "ll": ",".join([x1, y1]),
        "spn": ",".join(spn),
        "l": "map",
        "pt": point2
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    res = requests.get(map_api_server, params=map_params)
    print(json_response_2["features"][0]["properties"])
    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(res.content)
    return json_response_2
