import telebot
import os
import random

TOKEN = "799084665:AAGww_oeZLrGxYoxFnTFW0AGyTjWBSALP3E"
bot = telebot.TeleBot(TOKEN)

user = bot.get_me()

def distort(fname):
    boi = "convert "+fname+" -liquid-rescale 320x320 -implode 0.30 result/"+fname
    os.system(boi)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """ку, я могу распидорасить твою медию""")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Отправь мне картинку и ей пиздец")


@bot.message_handler(content_types=['photo'])
def photudl(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    download = bot.download_file(file_info.file_path)
    file_name = str(random.randint(1,101))+".jpg"
    with open(file_name, 'wb') as new_file:
        new_file.write(download)
    distort(file_name)
    photo = open('file_name, 'rb')
    bot.send_photo(message.chat.id, photo)
    os.remove(file_name)
	
   # os.remove(file_name)

while True:
	try:
		bot.polling(none_stop=True)
	except Exception as e:
		from time import sleep
		print('error!!!!!!!!!')
		print(e)
		sleep(50)
