import telebot
from decouple import config

TOKEN = config('TOKEN',default='')


class ProjectBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)


class ProjectReplyKeyboard(telebot.types.ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard, *args):
        super().__init__(resize_keyboard)
        for buttons in args:
            self.add(*buttons)

    def delete_keyboard_markup(self):
        return telebot.types.ReplyKeyboardRemove()



bot = ProjectBot(TOKEN)