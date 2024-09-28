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
        for i in range(len(keyboard) // row_width):
            if i == len(keyboard) // row_width - 1:
                self.add(*keyboard[i*row_width :])
            else:
                self.add(*keyboard[i*row_width : i*row_width+row_width])


    # чтобы удалить клавиатуру вызываем эту функцию и результат передаём в reply_markup функции send_message
    def delete_keyboard_markup(self):
        return telebot.types.ReplyKeyboardRemove()


class ProjectInlineKeyboard(telebot.types.InlineKeyboardMarkup):
    def __init__(self, keyboard=None, row_width=3):
        super().__init__(keyboard=keyboard, row_width=row_width)



bot = ProjectBot(TOKEN)