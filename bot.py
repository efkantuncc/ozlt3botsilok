import telebot
import requests

API_TOKEN = '7061956025:AAG2frZEKM3Bkk6HtH43PqSKAwn3t1gbJik'
bot = telebot.TeleBot(API_TOKEN)

# Üyelik kontrolü için yetkili kullanıcılar listesi
authorized_users = [6737592159]

# GitHub'dan veri çekmek için kullanılan URL
GITHUB_URL = 'https://raw.githubusercontent.com/efkantuncc/ozlt3botsilok/main/mov.txt'

# Başlangıç menüsü
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    btn1 = telebot.types.KeyboardButton('⚜️ Üyelik Satın Al')
    btn2 = telebot.types.KeyboardButton('💫 Film / Dizi İzle')
    btn3 = telebot.types.KeyboardButton('🤠 Telif - İletişim')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Film ve Dizi İzlemek İçin Üyelik Gereklidir!", reply_markup=markup)

# Buton tıklamaları
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == '⚜️ Üyelik Satın Al':
        bot.send_message(message.chat.id, "Üyelik Satın Almak İçin: t.me/t3rickg")
    elif message.text == '💫 Film / Dizi İzle':
        if message.from_user.id in authorized_users:
            msg = bot.send_message(message.chat.id, "Lütfen içeriğin ismini girin:")
            bot.register_next_step_handler(msg, fetch_movie)
        else:
            bot.send_message(message.chat.id, "📨 Üyeliğiniz Yok Lütfen Üyelik Satın Alın.")
    elif message.text == '🤠 Telif - İletişim':
        bot.send_message(message.chat.id, "Telif ve İletişim İçin: t.me/t3rickg")

# Film/Dizi ismini aldıktan sonra GitHub'dan veri çekme ve yanıt verme
def fetch_movie(message):
    movie_name = message.text.lower()
    response = requests.get(GITHUB_URL)
    if response.status_code == 200:
        data = response.text.splitlines()
        found = False
        for line in data:
            if line.lower().startswith(movie_name):
                movie_url = line.split('=')[1].strip()
                bot.send_message(message.chat.id, f"{movie_name.capitalize()}\n\nSorumluluk Kabul Etmemekteyiz!\n{movie_url}")
                found = True
                break
        if not found:
            bot.send_message(message.chat.id, "Maalesef o içeriğe sahip değiliz.")
    else:
        bot.send_message(message.chat.id, "Veri çekme sırasında bir hata oluştu.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
                         
