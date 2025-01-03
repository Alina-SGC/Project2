import telebot
from telebot import types
from decorators import decorate_message
from user import User  # Импортируем класс User
from exceptions import UserException  # Импортируем исключения

API_TOKEN = '8110482192:AAEeQ4HLdn5_Jnl2wNyrHYbXet0ApTKzSX0'
bot = telebot.TeleBot(API_TOKEN)

user_states = {}  # Словарь для хранения состояний пользователей по chat_id


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Обрабатывает команду /start.
    Сбрасывает состояние пользователя и инициализирует нового пользователя.
    Предлагает выбрать место для дальнейшего общения.
    """
    reset_user_state(message.chat.id)
    try:
        user_states[message.chat.id] = User(message.chat.id)  # Создаем объект User для нового пользователя
    except UserException as e:
        bot.send_message(message.chat.id, decorate_message(str(e)))  # Отправляем сообщение об ошибке
        return

    # Создаем клавиатуру с вариантами мест
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton("Кунсткамера")
    btn2 = types.KeyboardButton("Дворец Просковьи Фёдоровны")
    btn3 = types.KeyboardButton("Санкт-Петербургский государственный университет")
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id,
                     decorate_message(
                         "Привет! Я — Ломоносов, и я буду твоим гидом по Санкт-Петербургу. Выбери место, о котором ты хочешь узнать больше:"),
                     reply_markup=markup)
    user_states[message.chat.id].set_state('select_place')  # Устанавливаем состояние


def reset_user_state(chat_id):
    """
    Сбрасывает состояние пользователя, удаляя его из словаря user_states.
    """
    user_states.pop(chat_id, None)


@bot.message_handler(func=lambda message: user_states.get(message.chat.id).get_state() == 'select_place')
def select_place(message):
    """
    Обрабатывает выбор места пользователем.
    В зависимости от выбранного места вызывает соответствующую функцию.
    """
    selected_place = message.text
    if selected_place == "Кунсткамера":
        kunstkamera_response(message.chat.id)
    elif selected_place == "Дворец Просковьи Фёдоровны":
        palace_response(message.chat.id)
    elif selected_place == "Санкт-Петербургский государственный университет":
        university_response(message.chat.id)
    else:
        bot.send_message(message.chat.id, decorate_message("Пожалуйста, выбери одно из предложенных мест."))


def kunstkamera_response(chat_id):
    """
    Отправляет информацию о Кунсткамере пользователю.
    """
    bot.send_message(chat_id,
                     decorate_message(
                         "Кунсткамера — одно из первых музеев в России, основанное Петром I. Здесь я изучал анатомию."))
    continue_prompt(chat_id)


def palace_response(chat_id):
    """
    Отправляет информацию о Дворце Просковьи Фёдоровны пользователю.
    """
    bot.send_message(chat_id,
                     decorate_message(
                         "Дворец Просковьи Фёдоровны — это место, где я выступал с лекциями и обсуждал научные идеи."))
    continue_prompt(chat_id)


def university_response(chat_id):
    """
    Отправляет информацию о Санкт-Петербургском государственном университете пользователю.
    """
    bot.send_message(chat_id,
                     decorate_message(
                         "Санкт-Петербургский государственный университет — моя гордость, место, где я развивал научные традиции."))
    continue_prompt(chat_id)


def continue_prompt(chat_id):
    """
    Запрашивает у пользователя, что он хочет делать дальше после получения информации.
    """
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton("Расскажи еще!")
    btn2 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2)

    bot.send_message(chat_id, decorate_message("Что бы ты хотел сделать дальше?"), reply_markup=markup)
    user_states[chat_id].set_state('after_info')  # Устанавливаем новое состояние


@bot.message_handler(func=lambda message: user_states.get(message.chat.id).get_state() == 'after_info')
def after_info(message):
    """
    Обрабатывает дальнейшие действия пользователя после получения информации.
    """
    if message.text == "Расскажи еще!":
        bot.send_message(message.chat.id, decorate_message(
            "Какой аспект интересует тебя? Могу рассказать подробнее о науке, архитектуре или своих достижениях."))
    elif message.text == "Вернуться в главное меню":
        start_message(message)
    else:
        bot.send_message(message.chat.id, decorate_message("Пожалуйста, выбери один из предложенных вариантов."))


# Запуск бота
bot.polling(none_stop=True)