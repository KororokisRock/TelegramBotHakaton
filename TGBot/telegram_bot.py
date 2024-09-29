from ProjectClass import bot, ProjectReplyKeyboard, MenuQuestionKeyboard, ListUserQuestionKeyboard, ShowAnswersOnQuestionKeyboard, SetRateAnswerKeyboard
from db import user_in_db, user_to_db, get_object, get_count_questions, answer_to_db, get_question_user_by_user_id, get_all_answer_by_question_id, user_rate
import math
AMMOUNT_QUESTION_IN_ONE_PAGE = 20


# python TGBot\telegram_bot.py


# если введена комманда start
@bot.message_handler(commands=['start'])
def welcome_func_bot(message):
    print(message.chat.id)
    print(message.from_user.id)
    if not user_in_db('tg_id', message.from_user.id):# смотрим существует ли такой пользователь
        # если не существует, то запрашиваем логин
        
        bot.send_message(message.chat.id, 'Здравствуйте! Вы не зарегестрированы. Введите логин: ')
        bot.register_next_step_handler(message, set_login_func_bot)
    else:
        # если существует, то присылаем ему меню кнопок (каждый список обозначает одну строку)
        keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', 'Список моих вопросов', '/start', 'Мой рейтинг'], row_width=2)
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

    user_to_db(user_login,user_password,message.from_user.id, message.chat.id)

    keyboard = ProjectReplyKeyboard(True, ['Задать вопрос', 'Список вопросов', 'Список моих вопросов', '/start', 'Мой рейтинг'], row_width=2)
    bot.send_message(message.chat.id, 'Вы зарегестрированы!', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Список моих вопросов')
def show_question_user_func_bot(message):
    questions = get_question_user_by_user_id(message.from_user.id)
    keyboard = ListUserQuestionKeyboard(list_question=questions, row_width=2)

    bot.send_message(message.chat.id, 'Список ваших вопросов:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.endswith('_clicked_item_list_user_question'))
def show_all_answers_on_user_question_func_bot(call):
    id_question = ListUserQuestionKeyboard.get_id_question_by_call_text(call.data)
    question = get_object(table='quest', column='q_id', cell=f'{id_question}')
    answers = get_all_answer_by_question_id(id_question)
    new_text = f'Вопрос:\n{question['q_text']}\n\n' + '\n\n'.join([f'Ответ {i+1}:\n{answers[i][3]}' for i in range(len(answers))])

    keyboard = ShowAnswersOnQuestionKeyboard(row_width=1)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_list_user_question')
def back_to_list_user_question_func_bot(call):
    questions = get_question_user_by_user_id(call.from_user.id)
    keyboard = ListUserQuestionKeyboard(list_question=questions, row_width=2)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Список ваших вопросов:', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Мой рейтинг')
def show_user_rate_func_bot(message):
    user = get_object('users', 'tg_id', str(message.from_user.id))
    bot.send_message(chat_id=message.chat.id, text=f'Ваш рейтинг: {user['rating']}')


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
    index_quest = str(MenuQuestionKeyboard.get_index_quest_by_message_text(call.message.text))
    bot.set_state(call.from_user.id, index_quest)
    
    bot.send_message(call.from_user.id, text='Введите ответ на вопрос:')
    bot.register_next_step_handler(call.message, get_answer_from_user_func_bot)


def get_answer_from_user_func_bot(message):
    index_quest = bot.get_state(message.from_user.id)

    answer_to_db(message.from_user.id, index_quest, message.text)

    question = get_object('quest', 'q_id', index_quest)
    user_id_question = question['user_id']
    user_tg_id_question = get_object('users', 'id', str(user_id_question))['tg_id']
    chat_id = user_tg_id_question
    new_text = f'На ваш вопрос пришёл ещё один ответ.\nВопрос:\n{question['q_text']}\nОтвет:\n{message.text}'

    bot.set_state(user_id=int(user_tg_id_question), state=str(message.from_user.id))

    keyboard = SetRateAnswerKeyboard(row_width=2)
    bot.send_message(chat_id=chat_id, text=new_text, reply_markup=keyboard)

    bot.send_message(message.chat.id, text='Ответ записан. Спасибо!')


@bot.callback_query_handler(func=lambda call: call.data == 'add_rate_to_user')
def add_rate_to_user_func_bot(call):
    user_id_answer = int(bot.get_state(call.from_user.id))
    user_rate(user_id_answer, '+')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id, text='Спасибо за оценку!')


@bot.callback_query_handler(func=lambda call: call.data == 'remove_rate_to_user')
def add_rate_to_user_func_bot(call):
    user_id_answer = int(bot.get_state(call.from_user.id))
    user_rate(user_id_answer, '-')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id, text='Спасибо за оценку!')


if __name__ == '__main__':
    print('Bot start!')
    bot.infinity_polling()
