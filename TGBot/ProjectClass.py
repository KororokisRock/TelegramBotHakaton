import telebot
from config import TOKEN

class ProjectBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)


bot = ProjectBot(TOKEN)