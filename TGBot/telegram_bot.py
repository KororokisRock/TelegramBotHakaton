
from ProjectClass import bot, ProjectReplyKeyboard



# python TGBot\telegram_bot.py
def user_exist():
    return False


# если введена комманда start
@bot.message_handler(commands=['start'])
def welcome_func_bot(message):
    if not user_exist():# смотрим существует ли такой пользователь
        # если не существует, то запрашиваем логин
        bot.send_message(message.chat.id, 'Здравствуйте! Вы не зарегестрированы. Введите логин: ')
        bot.register_next_step_handler(message, set_login_func_bot)
    else:
        # если существует, то присылаем ему меню кнопок (каждый список обозначает одну строку)
        keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', '/my_login', '/my_password', '/start'], row_width=2)
        bot.send_message(message.chat.id, 'Здравствуйте!', reply_markup=keyboard)


# записываем логин, запрашиваем пароль
def set_login_func_bot(message):
    user_login = message.text
    print(user_login)
    bot.send_message(message.chat.id, 'А теперь введите пароль:')
    bot.register_next_step_handler(message, set_password_func_bot)


# записываем пароль, присылаем меню кнопок (каждый список обозначает одну строку)
def set_password_func_bot(message):
    user_password = message.text
    print(user_password)
    keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', '/my_login', '/my_password', '/start'], row_width=2)
    bot.send_message(message.chat.id, 'Вы зарегестрированы!', reply_markup=keyboard)


# Тут начинается цепочка функций бота для вопросов
@bot.message_handler(func=lambda message: message.text == 'Задать вопрос')
def ask_question_func_bot(message):
    pass


# Тут начинается цепочка функций бота для ответа на вопросы
@bot.message_handler(func=lambda message: message.text == 'Список вопросов')
def list_question_func_bot(message):
    list_question = [f'{i} - question in  bot lalalalal' for i in range(57)]
    bot.send_message(message.chat.id, 'Список текущих вопросов:')
    


if __name__ == '__main__':
    print('Bot start!')
    bot.infinity_polling()