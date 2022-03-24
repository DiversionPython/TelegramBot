import telebot
from config import TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

# При вводе команды /start или /help пользователю выводятся инструкции по применению бота

@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Что бы конвертировать валюту, введите данные через пробел в формате: \n' \
           'Изначальная  валюта -> в какую валюту перевести -> количество переводимой валюты \n'   'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

# При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде.

@bot.message_handler(commands=['values'])
def repeat(message):
    text = 'доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convertor(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException("Не правильно заданы параметры")

        base, quote, amount = values
        total_base = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.send_message(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} : {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)


