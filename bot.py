import logging
import config
from database import orm
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, executor
import request
from aiogram.dispatcher import FSMContext

logging.basicConfig(level=logging.INFO)
token = Bot(token=config.bot_token)
storage = MemoryStorage()
bot = Dispatcher(token, storage=storage)

class ChoiceCityWeather(StatesGroup):
    waiting_city = State()

class SetUserCity(StatesGroup):
    waiting_user_city = State()

@bot.message_handler(commands=['start'])
async def start_message(message):
    orm.add_user(message.from_user.id)
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Погода в моём городе')
    btn2 = types.KeyboardButton('Погода в другом месте')
    btn3 = types.KeyboardButton('История')
    btn4 = types.KeyboardButton('Установить свой город')
    markup.add(btn1, btn2, btn3, btn4)
    text = f'Привет {message.from_user.first_name}, я бот, который расскжет тебе о погоде на сегодня'
    await message.answer(text, reply_markup=markup)

@bot.message_handler(regexp='Погода в моём городе')
async def get_user_city_weather(message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')   
    markup.add(btn1)  
    data = request.get_weather()
    text = f' Температура: {data["temp"]} C\n Ощущается как: {data["feels_like"]} C \n Скорость ветра: {data["wind_speed"]}м/с\n Давление: {data["pressure_mm"]}мм'
    await message.answer(text, reply_markup=markup)

@bot.message_handler(regexp='Меню')
async def menu(message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Погода в моём городе')
    btn2 = types.KeyboardButton('Погода в другом месте')
    btn3 = types.KeyboardButton('История')
    markup.add(btn1, btn2, btn3)
    text = f'Привет {message.from_user.first_name}, я бот, который расскжет тебе о погоде на сегодня'
    await message.answer(text, reply_markup=markup)

def register_handlers_city(dp: Dispatcher):
    dp.register_message_handler(city_start, regexp="Погода в другом месте", state="*")
    dp.register_message_handler(city_chosen, state=ChoiceCityWeather.waiting_city)
    dp.register_message_handler(set_user_city_start, regexp="Установить свой город", state="*")
    dp.register_message_handler(user_city_chosen, state=SetUserCity.waiting_user_city)

@bot.message_handler(regexp='Погода в другом месте', state='*')
async def city_start(message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    text = 'Введите название города'
    await message.answer(text, reply_markup=markup)
    await ChoiceCityWeather.waiting_city.set()

@bot.message_handler(state=ChoiceCityWeather.waiting_city)
async def city_chosen(message: types.Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer('Названия городов пишутся с большой буквы)')
        return
    await state.update_data(waiting_city=message.text)
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Погода в моём городе')
    btn2 = types.KeyboardButton('Погода в другом месте')
    btn3 = types.KeyboardButton('История')
    btn4 = types.KeyboardButton('Установить свой город')
    markup.add(btn1, btn2, btn3, btn4)
    user_data = await state.get_data()
    data = request.get_weather_by_city(user_data.get('waiting_city'))
    text = f' Погода в {data[1]+"е"}\n Температура: {data[0]["temp"]} C\n Ощущается как: {data[0]["feels_like"]} C \n Скорость ветра: {data[0]["wind_speed"]}м/с\n Давление: {data[0]["pressure_mm"]}мм'
    await message.answer(text, reply_markup=markup)
    await state.finish()

@bot.message_handler(regexp='Установить свой город', state='*')
async def set_user_city_start(message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    text = 'В каком городе проживаете?'
    await message.answer(text, reply_markup=markup)
    await SetUserCity.waiting_user_city.set()

@bot.message_handler(state=SetUserCity.waiting_user_city)
async def user_city_chosen(message: types.Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer('Названия городов пишутся с большой буквы)')
        return
    await state.update_data(waiting_user_city=message.text)
    user_data = await state.get_data()
    orm.set_user_city(message.from_user.id, user_data.get('waiting_user_city'))
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Погода в моём городе')
    btn2 = types.KeyboardButton('Погода в другом месте')
    btn3 = types.KeyboardButton('История')
    btn4 = types.KeyboardButton('Установить свой город')
    markup.add(btn1, btn2, btn3, btn4)
    text = f'Запомнил, {user_data.get("waiting_user_city")} ваш город'
    await message.answer(text, reply_markup=markup)
    await state.finish()
    

if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)