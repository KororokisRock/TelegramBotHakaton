from ProjectClass import bot, ProjectReplyKeyboard, MenuPageListQuestion, QuestionInlineKeyboard
from db import user_in_db, user_to_db
import math
AMMOUNT_QUESTION_IN_ONE_PAGE = 20


# python TGBot\telegram_bot.py


# если введена комманда start
@bot.message_handler(commands=['start'])
def welcome_func_bot(message):
    if not user_in_db('tg_id', message.from_user.id):# смотрим существует ли такой пользователь
        # если не существует, то запрашиваем логин
        
        bot.send_message(message.chat.id, 'Здравствуйте! Вы не зарегестрированы. Введите логин: ')
        bot.register_next_step_handler(message, set_login_func_bot)
    else:
        # если существует, то присылаем ему меню кнопок (каждый список обозначает одну строку)
        keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', 'Список моих вопросов', '/start'], row_width=2)
        bot.send_message(message.chat.id, 'Здравствуйте!', reply_markup=keyboard)


# записываем логин, запрашиваем пароль
def set_login_func_bot(message):
    user_login = message.text
    bot.set_state(message.from_user.id, user_login)

    bot.send_message(message.chat.id, 'А теперь введите пароль:')
    bot.register_next_step_handler(message, set_password_func_bot)


# записываем пароль, присылаем меню кнопок (каждый список обозначает одну строку)
def set_password_func_bot(message):
    user_password = message.text

    user_login = bot.get_state(message.from_user.id)

    user_to_db(user_login,user_password,message.from_user.id)

    keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', 'Список моих вопросов', '/start'], row_width=2)
    bot.send_message(message.chat.id, 'Вы зарегестрированы!', reply_markup=keyboard)


# Тут начинается цепочка функций бота для вопросов
@bot.message_handler(func=lambda message: message.text == 'Задать вопрос')
def ask_question_func_bot(message):
    pass


# Тут начинается цепочка функций бота для ответа на вопросы
@bot.message_handler(func=lambda message: message.text == 'Список вопросов')
def list_question_func_bot(message):
    list_question = [f'{i} - question in  bot lalalalal' for i in range(57)]
    
    keyboard = MenuPageListQuestion(list_question=list_question, row_width=2,
                                    current_page=0, ammount_question_in_one_page=AMMOUNT_QUESTION_IN_ONE_PAGE)
    bot.send_message(chat_id=message.chat.id, text=f'Список текущих вопросов. Страница 1/{math.ceil(len(list_question) / AMMOUNT_QUESTION_IN_ONE_PAGE)}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'back_page_list_question')
def list_question_back_page_func_bot(call):
    list_question = [f'{i} - question in  bot lalalalal' for i in range(57)]
    current_page = MenuPageListQuestion.give_current_page_by_message_text(message_text=call.message.text)

    if current_page > 0:
        current_page -= 1

        keyboard = MenuPageListQuestion(list_question=list_question, row_width=2,
                                        current_page=current_page, ammount_question_in_one_page=AMMOUNT_QUESTION_IN_ONE_PAGE)

        bot.edit_message_text(text=f'Список текущих вопросов. Страница {current_page + 1}/{math.ceil(len(list_question) / AMMOUNT_QUESTION_IN_ONE_PAGE)}',
                              chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'next_page_list_question')
def list_question_next_page_func_bot(call):
    list_question = [f'{i} - question in  bot lalalalal' for i in range(57)]
    current_page = MenuPageListQuestion.give_current_page_by_message_text(message_text=call.message.text)

    if current_page < math.ceil(len(list_question) / AMMOUNT_QUESTION_IN_ONE_PAGE) - 1:
        current_page += 1

        keyboard = MenuPageListQuestion(list_question=list_question, row_width=2,
                                        current_page=current_page, ammount_question_in_one_page=AMMOUNT_QUESTION_IN_ONE_PAGE)

        bot.edit_message_text(text=f'Список текущих вопросов. Страница {current_page + 1}/{math.ceil(len(list_question) / AMMOUNT_QUESTION_IN_ONE_PAGE)}',
                              chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.endswith('_clicked_element_list_question'))
def show_question_in_list_question_func_bot(call):
    list_question = [f'{i} - question in  bot lalalalal' for i in range(57)]
    index_question = MenuPageListQuestion.give_index_question(call.data)

    keyboard = QuestionInlineKeyboard(row_width=2)
    bot.edit_message_text(text=f'Вопрос №{index_question + 1}:\n{list_question[index_question]}', chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_list_question')
def list_question_func_bot(call):
    list_question = [f'{i} - question in bot lalalalal' for i in range(57)]
    index_question = QuestionInlineKeyboard.give_index_question_by_message_text(message_text=call.message.text)
    current_page = MenuPageListQuestion.give_current_page_by_index_question(index_question=index_question, ammount_question_in_one_page=AMMOUNT_QUESTION_IN_ONE_PAGE)

    keyboard = MenuPageListQuestion(list_question=list_question, row_width=2, current_page=current_page, ammount_question_in_one_page=AMMOUNT_QUESTION_IN_ONE_PAGE)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'Список текущих вопросов. Страница {current_page + 1}/{math.ceil(len(list_question) / AMMOUNT_QUESTION_IN_ONE_PAGE)}', reply_markup=keyboard)


if __name__ == '__main__':
    print('Bot start!')
    bot.infinity_polling()
