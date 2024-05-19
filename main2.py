import os

from datetime import datetime as dt
from dotenv import find_dotenv, load_dotenv

import telebot
from telebot import types

# Create file '.env' with your TOKEN=TOKEN
load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')

BALL_PRICE = 400
GUN_PRICE = 500

bot = telebot.TeleBot(TOKEN)

ball_games = []
gun_games = []


def get_sum_games(name, games, price):
    text = ''
    for game in games:
        text += f'{game}\n'

    text += f'{name}: {len(games)}шт - {len(games) * price}р\n\n'
    return text


def get_totalSum():
    result = len(ball_games) * BALL_PRICE + len(gun_games) * GUN_PRICE
    return f'Всего: {result}р'


# Старт
@bot.message_handler(commands=['start'])
def start_bot(message):
    ball_text = f'{get_sum_games('Шарики', ball_games, BALL_PRICE)}'
    gun_text = f'{get_sum_games('Пневматика', gun_games, GUN_PRICE)}'
    text = f'{ball_text}{gun_text}{get_totalSum()}'

    # Кнопки
    markup = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton('Шарики', callback_data='add_ball')
    button_2 = types.InlineKeyboardButton(
        'Пневматика', callback_data='add_gun')
    # button_3 = types.InlineKeyboardButton('Удалить', callback_data='delete')
    markup.row(button_1, button_2)

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_fn(call):
    now = dt.now()
    time_game = f'{now:%H:%M}'
    if call.data == 'add_ball':
        ball_games.append(time_game)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start_bot(call.message)

    elif call.data == 'add_gun':
        gun_games.append(time_game)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start_bot(call.message)

    elif call.data == 'delete':
        bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(commands=['reset'])
def reset_bot(message):
    global ball_games, gun_games
    ball_games = []
    gun_games = []


if __name__ == '__main__':
    print('Bot Online')
    bot.polling(none_stop=True)
