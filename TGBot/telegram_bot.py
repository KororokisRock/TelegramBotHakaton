from ProjectClass import bot, ProjectReplyKeyboard, MenuQuestionKeyboard
from db import user_in_db, user_to_db, get_object, get_count_questions, answer_to_db
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
    bot.delete_state(message.from_user.id)

    user_to_db(user_login,user_password,message.from_user.id)

    keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', 'Список моих вопросов', '/start'], row_width=2)
    bot.send_message(message.chat.id, 'Вы зарегестрированы!', reply_markup=keyboard)


# Тут начинается цепочка функций бота для вопросов
@bot.message_handler(func=lambda message: message.text == 'Задать вопрос')
def ask_question_func_bot(message):
    pass


# Тут начинается цепочка функций бота для ответа на вопросы
@bot.message_handler(func=lambda message: message.text == 'Список вопросов')
def show_question_func_bot(message):
    keyboard = MenuQuestionKeyboard(row_width=2)
    question = get_object('quest', 'q_id', '1')

    bot.send_message(chat_id=message.chat.id, text=f'Вопрос №{question['q_id']}:\n{question['q_text']}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'prev_quest')
def go_to_prev_quest_func_bot(call):
    keyboard = MenuQuestionKeyboard(row_width=2)
    index_quest = MenuQuestionKeyboard.get_index_quest_by_message_text(call.message.text)
    index_quest -= 1

    if index_quest >= 1:
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=f'...')
        question = get_object('quest', 'q_id', str(index_quest))
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=f'Вопрос №{question['q_id']}:\n{question['q_text']}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'next_quest')
def list_question_next_page_func_bot(call):
    keyboard = MenuQuestionKeyboard(row_width=2)
    index_quest = MenuQuestionKeyboard.get_index_quest_by_message_text(call.message.text)
    index_quest += 1

    if index_quest <= get_count_questions():
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=f'...')
        question = get_object('quest', 'q_id', str(index_quest))
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=f'Вопрос №{question['q_id']}:\n{question['q_text']}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'answer_quest')
def list_question_func_bot(call):
    print('zsfs')
    index_quest = str(MenuQuestionKeyboard.get_index_quest_by_message_text(call.message.text))
    bot.delete_state(call.message.from_user.id)
    bot.set_state(call.message.from_user.id, index_quest)

    
    bot.send_message(call.message.chat.id, text='Введите ответ на вопрос:')
    bot.register_next_step_handler(call.message, get_answer_from_user)


def get_answer_from_user(message):
    print(324134)
    index_quest = bot.get_state(message.from_user.id)
    print(index_quest)

    answer_to_db(message.from_user.id, index_quest, message.text)

    bot.send_message(message.chat.id, text='Ответ записан. Спасибо!')


if __name__ == '__main__':
    print('Bot start!')
    bot.infinity_polling()
