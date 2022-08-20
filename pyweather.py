import requests
import datetime
from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

tg_token = "5606873888:AAG_qnezY9NETRBNasBrJN5lwmnt5eEEGsw"

bot = Bot(tg_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Пришли мне название города, и я пришлю тебе сводку погоды!")

@dp.message_handler()
async def get_weather(message: types.Message):

    token = "5e762c92a2c7db83992d01579c8a4c95"

    try:
        r_Geo = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={token}"
        )
        dataGeo = r_Geo.json()
        dataGeoDict = dataGeo[0]
        lon = dataGeoDict['lon']
        lat = dataGeoDict['lat']

        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&units=metric"
        )
        data = r.json()

        city = message.text
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        windSpeed = data["wind"]["speed"]

        result = f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\nПогода в городе {city}:\n\nТемпература: {temp} C\nВлажность: {humidity}\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {windSpeed} м/с\nШирота: {lat}\nДолгота: {lon}\n\n***Хорошего дня!***"
        await message.reply(result)

    except Exception as e:
        await message.reply('\U00002620 Ошибка \U00002620\nКод ошибки: ' + str(e) + '\nПроверьте данные!')

if (__name__ == '__main__'):
    executor.start_polling(dp)