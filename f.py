import math


def finder(response):  # масштаб для 1 параметра поиска
    x, y = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"][
                       "Envelope"]["lowerCorner"], response["response"]["GeoObjectCollection"]["featureMember"][0][
                       "GeoObject"]["boundedBy"]["Envelope"]["upperCorner"]
    x, y = x.split(), y.split()
    return str(abs(float(x[0]) - float(y[0])) / 2), str(abs(float(x[1]) - float(y[1])) / 2)


def finder2(a, b):  # расстояние до приюта
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def finder3(response):  # масштаб для 3 параметра поиска
    x, y = response["properties"]['ResponseMetaData']["SearchRequest"]["boundedBy"][0],\
           response["properties"]['ResponseMetaData']["SearchRequest"]["boundedBy"][1]
    return str(abs(float(x[0]) - float(y[0])) / 70), str(abs(float(x[1]) - float(y[1])) / 70)

