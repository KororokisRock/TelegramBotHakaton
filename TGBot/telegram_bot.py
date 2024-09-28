from ProjectClass import bot
from ..dataBase.func_db import create_db, exists_db, create_tables_db, user_not_exist


def initial_start_work():
    if not exists_db():
        create_db()
    create_tables_db()


@bot.message_handler(commands=['start'])
def welcome_func_bot(message):
    if user_not_exist():
        bot.send_message(message.chat.id, 'Здравствуйте! Вы не зарегестрированы. Введите логин: ')
        bot.register_next_step_handler(message, set_login_func_bot)
    else:
        bot.send_message()


def set_login_func_bot(message):
    user_login = message.text
    print(user_login)
    bot.send_message(message.chat.id, 'А теперь введите пароль:')
    bot.register_next_step_handler(message, set_password_func_bot)


def set_password_func_bot(message):
    user_password = message.text
    print(user_password)
    bot.send_message(message.chat.id, 'Вы зарегестрированы!')


if __name__ == '__main__':
    print('Bot start!')
    bot.infinity_polling()