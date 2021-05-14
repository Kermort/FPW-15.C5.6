import telebot
from extensions import Converter, APIException
from config import TOKEN, keys

# кнопки помощи и списка валют
help_btn = telebot.types.KeyboardButton(text="/help")
values_btn = telebot.types.KeyboardButton(text="/валюты")
reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
reply_markup.row(help_btn, values_btn)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help_message(message: telebot.types.Message):
    text = "Чтобы начать работы введите команду в виде:\n\
<имя валюты>\
<в какую валюту перевести>\
<сумма>, например:\n\
евро рубль 100\n\
/валюты - список доступных валют\n\
/help - помощь"
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)

@bot.message_handler(commands=["валюты"])
def values_help(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)

@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        user_message = message.text.split(" ")
        if len(user_message) != 3:
            raise APIException("Передано неверное количество параметров")
        cur, base, amount = user_message
        total = float(Converter.convert(cur, base, amount))
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка ввода\n{e}", reply_markup=reply_markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду\n{e}", reply_markup=reply_markup)
    else:
        
        text = f"Чтобы купить {amount} {cur.lower()} нужно {(total * float(amount)):.2f} {base.lower()}"
        bot.send_message(message.chat.id, text, reply_markup=reply_markup)

bot.polling(none_stop=True)

# почему-то в API не работает комбинация CNY->RUB и RUB->CNY
