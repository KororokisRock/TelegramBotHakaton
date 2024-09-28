from ProjectClass import bot
from ..dataBase.func_db import create_db, exists_db


def initial_start_work():
    if not exists_db:
        create_db()
    


@bot.message_handler(commands=['start'])
def welcome_func_bot(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Вы не зарегестрированы. Введите логин: ')
    bot.register_next_step_handler(message, set_login_func_bot)


def set_login_func_bot(message):
    user_login = message.text
    bot.send_message(message.chat.id, 'А теперь введите пароль:')
    bot.register_next_step_handler(message, set_password_func_bot)


def set_password_func_bot(message):
    user_password = message.text
    bot.send_message(message.chat.id, 'Вы зарешестрированы!')


if __name__ == '__main__':
    print('Bot start!')
    bot.infinity_polling()