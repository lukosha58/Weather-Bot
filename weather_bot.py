from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from time import strftime
import requests
from weather_api import Weather

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
start_keyboard = [['Текущий день'], ['Прогноз на 5 дней']]


def start(bot, update):
    update.message.reply_text('Привет!\nЯ Weather-Bot, я могу показать прогноз погоды.')
    update.message.reply_text('Введите координаты, название города, IP-адресс или ZIP-code.')
    return 1


def close_keyboard(bot, update):
    update.message.reply_text("Ok", reply_markup=ReplyKeyboardRemove())


def stop(bot, update):
    update.message.reply_text('Увимидимся.')


def coords_response(bot, update, user_data):
    markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text('Выберите действие', reply_markup=markup)
    place = update.message.text
    user_data['place'] = place
    return 2


def choose(bot, update):
    if bot.update.text != 'Текущая погода':
        bot.update.reply_text('Попробуйте ещё раз')
    return 3


def forecast_weather(bot, update, user_data):
    print('Forecast')
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
        for i in weather.data['weather']:
            date = weather.data['weather'][i]['date']
            bot.update.reply_text(
                'Погода: {}\nМестоположение: {}\nДата: {}\nМинимальная температура: {}\nМаксимальная температура'.format(
                    emoji[i[0]['hourly'][0]['weatherCode']], weather.get_place(), date, i['mintempC'], i['maxtempC']))
    except:
        print('Error')


def current_weather(bot, update, args, user_data):
    print('Running')
    url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?'
    try:
        response = requests.get(url, params={
            'key': '0286dd85214445fbad7112041180304',
            'q': user_data['place'],
            'num_of_days': '1',
            'format': 'json',
            'tp': '1'
        })
        weather = Weather(response)
        update.message.reply_text(
            'Погода: {}\nМестоположение: {}\nТемпература: {}°C\nВремя: {}\nСкорость ветра: {}м/c'.format(
                emoji[weather.current_condition['weatherCode']], weather.get_place(),
                weather.get_temp_in_celsius(), weather.get_time(), weather.wind_speed))
    except Exception as arr:
        print('Error%s' % arr)


def main():
    updater = Updater('589513313:AAGCseMBKhTGFvVSc1h_M_7H5z07m2zR7sk')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('weather', current_weather, pass_args=True, pass_user_data=True))
    conv_handler = ConversationHandler \
            (
            entry_points=[CommandHandler('start', start)],
            states=
            {
                1: [MessageHandler(Filters.text, coords_response, pass_user_data=True)],
                2: [MessageHandler(Filters.text, choose)],
                3: [CommandHandler('weather', current_weather, pass_user_data=True)]
            },
            fallbacks=[CommandHandler('stop', stop)]
        )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler('forecast', forecast_weather))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
