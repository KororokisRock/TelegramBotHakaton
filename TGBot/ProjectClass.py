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
    def __init__(self, resize_keyboard, *args):
        # запрашиваем будет ли телеграм менять размер кнопок для лучшего визуала
        super().__init__(resize_keyboard)
        # каждый список в поле args - одна строка с кнопками в меню
        # ['1', '2', '3'], ['4', '5', '6'] -> |1| |2| |3|
        #                                     |4| |5| |6|
        for buttons in args:
            self.add(*buttons)

    # чтобы удалить клавиатуру вызываем эту функцию и результат передаём в reply_markup функции send_message
    def delete_keyboard_markup(self):
        return telebot.types.ReplyKeyboardRemove()



bot = ProjectBot(TOKEN)