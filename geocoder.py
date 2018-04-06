import requests


def geocoder(update, bot, place):
    try:
        geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_uri, params={
            "format": "json",
            "geocode": place
        })
        if not response:
            update.message.reply_text("Ошибка выполнения запроса:")
            update.message.reply_text("Http статус:", response.status_code, "(", response.reason, ")")
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        lon, lat = toponym['Point']["pos"].split()
        spn = found_spn(json_response)
        static_api_request = "http://static-maps.yandex.ru/1.x/?"
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([str(spn[0]), str(spn[1])]),
            "l": "map",
            "pt": "{},pm2rdm".format(",".join([lon, lat]))
        }
        with open('map.png', 'wb') as file:
            file.write(requests.get(static_api_request, params=params).content)
    except:
        update.message.reply_text('Не удалось найти объект.\nПроверьте правильность адресса или название места.')


def found_spn(response):
    lowerCorner = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"][
        "Envelope"]["lowerCorner"].split(" ")
    upperCorner = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"][
        "Envelope"]["upperCorner"].split(" ")
    return (float(upperCorner[0]) - float(lowerCorner[0])) / 2, (float(upperCorner[1]) - float(lowerCorner[1])) / 2
