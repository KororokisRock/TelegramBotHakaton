from ProjectClass import bot


@bot.message_handler(commands=['start'])
def welcome_func_bot(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Этот бот сделан для хакатона.')


if __name__ == '__main__':
    print('Bot start!')
    bot.infinity_polling()