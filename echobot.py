import telebot



from extensions import Converter, APIException
from config import *



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты> \ Чтобы увидеть список доступных валют введите: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные виды валют: '
    for i in currencies.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, quote, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message,'Неверное количество параметров!')
    try:
        new_price = Converter.get_price(base, quote, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {quote} - {new_price}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде: \n{e}")


bot.polling()