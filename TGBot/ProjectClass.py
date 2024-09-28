import telebot
from decouple import config

# берём токен бота
TOKEN = config('TOKEN',default='')


# обёртка бота библиотеки telebot в наш класс
class ProjectBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)


# обёртка меню кнопок под полем для ввода сообщений в наш класс
class ProjectReplyKeyboard(telebot.types.ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard, keyboard, row_width=3):
        # запрашиваем будет ли телеграм менять размер кнопок для лучшего визуала
        super().__init__(resize_keyboard)
        # задаётся кол-во кнопок в поле и список кнопок
        l = []
        for i in range(len(keyboard)):
            l.append(telebot.types.InlineKeyboardButton(text=keyboard[i]))
            if len(l) >= row_width or i == len(keyboard) - 1:
                self.add(*l)
                l.clear()


    # чтобы удалить клавиатуру вызываем эту функцию и результат передаём в reply_markup функции send_message
    def delete_keyboard_markup(self):
        return telebot.types.ReplyKeyboardRemove()


class ProjectInlineKeyboard(telebot.types.InlineKeyboardMarkup):
    def __init__(self, keyboard=None, row_width=3):
        super().__init__()
        # задаётся кол-во кнопок в поле и список кнопок
        l = []
        for i in range(len(keyboard)):
            l.append(telebot.types.InlineKeyboardButton(text=keyboard[i]['text'], callback_data=keyboard[i]['callback_data']))
            if len(l) >= row_width or i == len(keyboard) - 1:
                self.add(*l)
                l.clear()


class MenuPageListQuestion(ProjectInlineKeyboard):
    def __init__(self, list_question=None, row_width=3, current_page=1, ammount_question_in_one_page=20):
        buttons = [{'text': 'Back', 'callback_data': 'back_page_list_question'},
               {'text': 'Next', 'callback_data': 'next_page_list_question'}]
        buttons += [{'text': list_question[i][:7] + '...', 'callback_data': f'{i}_clicked_element_list_question'}
                for i in range(current_page * ammount_question_in_one_page,
                               current_page * ammount_question_in_one_page + ammount_question_in_one_page)
                               if i <= len(list_question) - 1]
        super().__init__(keyboard=buttons, row_width=row_width)
    
    def give_current_page_by_message_text(message_text=''):
        return int(message_text[message_text.index('Страница') + 9 : message_text.index('/')]) - 1
    
    def give_index_question(callback_data_text=''):
        return int(callback_data_text[:callback_data_text.index('_')])
    
    def give_current_page_by_index_question(index_question=0, ammount_question_in_one_page=20):
        return index_question // ammount_question_in_one_page


class QuestionInlineKeyboard(ProjectInlineKeyboard):
    def __init__(self, row_width=3):
        buttons = [{'text': 'Back to list', 'callback_data': 'back_to_list_question'},
                   {'text': '1', 'callback_data': '1'}]
        super().__init__(keyboard=buttons, row_width=row_width)
    
    def give_index_question_by_message_text(message_text=''):
        return int(message_text[message_text.index('№') + 1:message_text.index(':')]) - 1


bot = ProjectBot(TOKEN)
