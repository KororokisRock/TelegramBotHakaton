import telebot
from decouple import config
TOKEN = config('TOKEN',default='')
class ProjectBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)


bot = ProjectBot(TOKEN)