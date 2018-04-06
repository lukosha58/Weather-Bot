from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from weather_api import Weather
from geocoder import geocoder
import requests, os

SUNNY = '☀'
PARTLY_CLOUDY = '⛅'
CLOUDY = '☁'
OVERCAST = '☔'
MIST = '🌁'
SNOW = '❄'
STORM = '⛈'
emoji = {'113': SUNNY, '116': PARTLY_CLOUDY, '119': CLOUDY, '122': OVERCAST, '143': MIST, '176': OVERCAST,
         '179': SNOW,
         '182': SNOW + OVERCAST, '185': SNOW, '200': STORM, '227': SNOW, '230': SNOW * 3, '248': MIST, '260': MIST,
         '263': SNOW, '266': SNOW, '281': SNOW, '284': SNOW, '293': OVERCAST, '296': OVERCAST, '299': OVERCAST,
         '302': OVERCAST,
         '305': OVERCAST * 2, '308': OVERCAST * 3, '311': OVERCAST}
start_keyboard = [['Текущий день'], ['Прогноз на 5 дней'], ['Новое место']]


def start(bot, update):
    update.message.reply_text('Введите координаты, название города, IP-адрес или ZIP-code.')
    return 1


def help(bot, update):
    update.message.reply_text('Привет!\nЯ Weather-Bot, я могу показать прогноз погоды.')


def stop(bot, update):
    update.message.reply_text('Увимидимся.')


def coords_response(bot, update, user_data):
    markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False, resize_keyboard=True)
    place = update.message.text
    url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?'
    user_data['place'] = place
    try:
        response = requests.get(url, params={
            'key': '0286dd85214445fbad7112041180304',
            'q': user_data['place'],
            'num_of_days': '5',
            'format': 'json',
            'tp': '12'
        })
        update.message.reply_text('Выберите действие', reply_markup=markup)
    except:
        start(bot, update)
        update.message.reply_text('Введите корректные данные.')
    return 2


def choose(bot, update, user_data):
    choice = update.message.text
    if choice == 'Текущий день':
        current_weather(bot, update, user_data)
    elif choice == 'Прогноз на 5 дней':
        forecast_weather(bot, update, user_data)
    elif choice == 'Новое место':
        start(bot, update)
    else:
        return 1


def forecast_weather(bot, update, user_data):
    url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?'
    try:
        response = requests.get(url, params={
            'key': '0286dd85214445fbad7112041180304',
            'q': user_data['place'],
            'num_of_days': '5',
            'format': 'json',
            'tp': '12'
        })
        weather = Weather(response)
        index = weather.data['weather']
        for i in range(5):
            date = weather.data['weather'][i]['date']
            update.message.reply_text(
                'Погода: {}\nМестоположение: {}\nДата: {}\nМинимальная температура: {}°C\nМаксимальная температура: {}°C'.format(
                    emoji[index[i]['hourly'][0]['weatherCode']], weather.get_place(), date, index[i]['mintempC'], index[i]['maxtempC']))
    except:
        return 1


def current_weather(bot, update, user_data):
    url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?'
    try:
        response = requests.get(url, params={
            'key': '0286dd85214445fbad7112041180304',
            'q': user_data['place'],
            'num_of_days': '1',
            'format': 'json',
            'tp': '1'
        })
        geocoder(update, bot, user_data['place'])
        weather = Weather(response)
        bot.send_photo(chat_id=update.message.chat.id,
                       photo=open('map.png', 'rb'),
                       caption='Погода: {}\nМестоположение: {}\nТемпература: {}°C\nВремя: {} по Москве\nСкорость ветра: {}м/c'.format(
                                emoji[weather.current_condition['weatherCode']], weather.get_place(),
                                weather.get_temp_in_celsius(), weather.get_time(), weather.wind_speed))
        os.remove('map.png')
    except:
        return 1


def main():
    updater = Updater('589513313:AAGCseMBKhTGFvVSc1h_M_7H5z07m2zR7sk')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('weather', current_weather, pass_user_data=True))
    dp.add_handler(CommandHandler('forecast', forecast_weather, pass_user_data=True))
    conv_handler = ConversationHandler \
            (
            entry_points=[CommandHandler('start', start)],
            states=
            {
                1: [MessageHandler(Filters.text, coords_response, pass_user_data=True)],
                2: [MessageHandler(Filters.text, choose, pass_user_data=True)]
            },
            fallbacks=[CommandHandler('stop', stop)]
        )
    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

