from tkinter import Button

import psycopg2 as ps
from pickle import GLOBAL

import telebot
from telebot import types
from telebot.apihelper import send_message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

rezultid = ''
bot = telebot.TeleBot('7698285311:AAEiiHh3NRTuE1-a-xA4INEi3Yw1tR8vZiA')


@bot.message_handler(commands=['start'])
def start (message):
    message1 = message
    Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Meteostancia = types.KeyboardButton('меню')
    Button.add(Meteostancia)
    bot.send_message(message.chat.id, 'добро пожаловать в бота для метео станции "гидра"', reply_markup = Button)


@bot.message_handler(content_types =['text'])
def commands(message):
    if message.text == 'Метеостанция':
        ypr(message)
    elif message.text == 'показатели':
        if rezultid == '':
            eror(message)
        else:
            inform(message)
    elif message.text == 'вернуться':
        menu(message)
    elif message.text == 'меню':
        menu(message)
    elif message.text == 'Поддержка':
        pod(message)
    elif message.text == 'полезности':
        infa(message)
    elif message.text == 'покупка станции':
        pass
    elif message.text == 'подключить':
        reg(message)
    elif message.text == 'о станции':
        infST(message)

def infa(message):
    Button = InlineKeyboardMarkup(row_width= True)
    b1 = InlineKeyboardButton(text = 'ухаживание', url = 'https://flowwow.com/blog/kak-pravilno-uhazhivat-za-komnatnymi-rasteniyami/')
    b2 = InlineKeyboardButton(text = 'пересаживание', url = 'https://ria.ru/20240905/tsvety-1791728879.html?ysclid=m2yw4m9rgy644548269')
    b3 = InlineKeyboardButton(text = 'виды', url = 'https://megacvet24.ru/blog/vidy-komnatnyh-tsvetov.html')
    b4 = InlineKeyboardButton(text = 'факты', url = 'https://poryadok.ru/blog/interesnye-fakty-o-komnatnykh-rasteniyakh-i-ikh-istorii/?ysclid=m2yw33kb2l985362244')
    Button.add(b1,b2,b3,b4)
    bot.send_message(message.chat.id, 'здесь вы можете найти полезную информацию для домашних растений', reply_markup=Button)



def pod(message):
    Button = InlineKeyboardMarkup()
    url_Button = InlineKeyboardButton(text = 'напишите нам', url = 't.me/s1s6a')
    Button.add(url_Button)
    bot.send_message(message.chat.id,'сообщите об ошибке',reply_markup= Button)




def menu(message):
    Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Meteostancia = types.KeyboardButton('Метеостанция')
    potderca = types.KeyboardButton('Поддержка')
    infa = types.KeyboardButton('полезности')
    informate = types.KeyboardButton('о станции')
    #buy = types.KeyboardButton('покупка станции')
    Button.add(Meteostancia,potderca,infa,informate)
    bot.send_message(message.chat.id, 'вы в меню', reply_markup=Button)



def ypr(message):
    Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pocazat = types.KeyboardButton('показатели')
    back = types.KeyboardButton('вернуться')
    new = types.KeyboardButton('подключить')
    Button.add(pocazat,back,new)
    bot.send_message(message.chat.id, 'здесь вы можете управлять станцией и получать данные', reply_markup=Button)

def reg(message):
    bot.send_message(message.chat.id,'введите id вашей станции')
    bot.register_next_step_handler(message,rav)

def rav(message):
    global rezultid
    rezultid = message.text
    if rezultid == 'вернуться':
        menu(message)
        rezultid = ''
    else:
        with ps.connect(dbname='meteostancia', user='postgres', password='Erfgtyhjuiklop', host='127.0.0.1') as con:

            con.autocommit = True
            with con.cursor() as cur:

                cur.execute('''SELECT id FROM dannie WHERE id = (%s)''', (rezultid,))
                if cur.fetchall() == []:
                    bot.send_message(message.chat.id,'неверный id, проверьте и попробуйте еще раз')
                    reg(message)
                else:
                    bot.send_message(message.chat.id,'ваша метео станция подключена')


def inform(message):
    with ps.connect(dbname='meteostancia', user='postgres', password='Erfgtyhjuiklop', host='127.0.0.1') as con:

        con.autocommit = True
        with con.cursor() as cur:
            cur.execute('''SELECT temp FROM dannie WHERE id = (%s)''', (rezultid,))
            result = cur.fetchall()
            for item in result:
                temp = str(item[0])

            cur.execute('''SELECT vlag FROM dannie WHERE id = (%s)''', (rezultid,))
            result2 = cur.fetchall()
            for item2 in result2:
                vlag = str(item2[0])

            cur.execute('''SELECT vlagP FROM dannie WHERE id = (%s)''', (rezultid,))
            result3 = cur.fetchall()
            for item3 in result3:
                vlagP = str(item3[0])

    bot.send_message(message.chat.id,f'температура в помещение: {temp} °C')
    bot.send_message(message.chat.id,f'влажность в помещение:  {vlag} %')
    bot.send_message(message.chat.id,f'влажность почвы растения: {vlagP} %')


def eror(message):
    Button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pocazat = types.KeyboardButton('подключить')
    back = types.KeyboardButton('вернуться')
    Button.add(pocazat, back)
    bot.send_message(message.chat.id, 'Метеостанция еще не подключена, хотите подключить?', reply_markup=Button)


def infST(message):
    Button = InlineKeyboardMarkup(row_width= True)
    idea = InlineKeyboardButton(text='Наша идея', callback_data='идея')
    problems = InlineKeyboardButton(text='проблемы',callback_data='проблемс')
    stancia = InlineKeyboardButton(text='о станции',callback_data='о станции')
    o_nas = InlineKeyboardButton(text='разработчики',callback_data='разраб')
    Button.add(idea,problems,stancia,o_nas)
    bot.send_message(message.chat.id, 'В этом разделе вы найдете всю информацию о нашей метео станции и о нас',reply_markup=Button)


@bot.callback_query_handler(func=lambda call:True)
def callback(call: types.CallbackQuery):
    if call.data == 'идея':
        bot.send_message(call.message.chat.id,'у каждого были ситуации что нужно надолго отъехать,нет времени, ну или просто вылетает из головы про то, что нужно полить цветы\nнаша команда задумалсь, как можно упростить жизнь людей и цветов и поставила перед собой цель - Облегчить заботу о культурных растениях\nспустя многочисленых размышлений мы решили использовать автоматический полив')

    elif call.data == 'проблемс':
        Button = InlineKeyboardMarkup(row_width=True)
        language = InlineKeyboardButton(text='язык ардуино', url='https://all-arduino.ru/programmirovanie-arduino/')
        script = InlineKeyboardButton(text='Что такое скрипт', url='https://blog.skillfactory.ru/glossary/skript/')
        biblia = InlineKeyboardButton(text='что такое библиотеки',
                                      url='https://ru.wikipedia.org/wiki/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA%D0%B0_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)')
        Button.add(language, script, biblia)
        bot.send_message(call.message.chat.id,
                         'Мы столкнулись с несколькими проблемами в ходе разработки станции.\n Из за незнания языка програмирования на котором пишутся скрипты к ардуино, нам пришлось эксперементировать и искать информацию про языкю\nТакже некоторые библиотеки к датчикам станции работали не коректно, из за чего у нас долгое время не получалось подключить датчики и написать код.',
                         reply_markup=Button)

    elif call.data == 'о станции':
        Button = InlineKeyboardMarkup(row_width=True)
        monik = InlineKeyboardButton(text='Монитор', url='https://wiki.amperka.ru/products:display-lcd-text-20x4?ysclid=m3661odmfk695652476')
        temp_vlag = InlineKeyboardButton(text='DHT11', url='https://3d-diy.ru/wiki/arduino-datchiki/datchik-vlazhnosti-i-temperatury-dht11/?ysclid=m3662cvt3k735636021')
        pocva = InlineKeyboardButton(text='FC-28', url='https://3d-diy.ru/wiki/arduino-datchiki/datchik-vlazhnosti-pochvy-arduino/?ysclid=m366301kas377052116')
        plata = InlineKeyboardButton(text='Макетная плата', url='https://3d-diy.ru/wiki/other/maketnye-platy/?ysclid=m3663ogcez772704402')
        kompas = InlineKeyboardButton(text='Компас 3Д', url='https://kompas.ru/kompas-3d/about/?admin__mode')
        printer = InlineKeyboardButton(text='3Д Принтер', url='https://zenit3d.ru/product/3d-printer-zenit/')
        Button.add(monik, temp_vlag, pocva, plata, kompas, printer)
        bot.send_message(call.message.chat.id,
                         'Автоматический полив — оборудование, обеспечивающее равномерный ежедневный '
                         'полив заданной территории \n В теории, мы планировали чтобы наша система могла '
                         'сама определять влажность почвы и включать подачу воды, что на практике у нас получилось, '
                         'так же мы добавили датчик температуры и влажности воздуха. Теперь она может сама поливать цветы, '
                         'практически без участия человека в домашних условиях. Основное назначение удовлетворение потребностей растения, '
                         'получения им воды. \n Такое устройство вполне может сэкономить немного времени на поливе цветов, '
                         'так же не даст им умереть от жажды. Если даже вы или ваши родственники забыли полить их, ничего страшного не произойдет. '
                         'Также встроенный датчик температуры и влажности комнаты поможет следить за состоянием цветов снаружи. '
                         'Основные преимущества заключаются в автоматическом уходе, которое позволяет занятому человеку лишний раз на работе, на отдыхе, не думать за растение, '
                         'ведь многие люди, занимаясь различными делами, могут и совсем забыть про домашнего зелёного друга, вспоминая о нём именно в тот момент, как тот уже '
                         'погибает. \n В станции мы использовали \n Жидкий кристаллический монитор(20х4) - для вывода данных, DHT11 — это цифровой датчик для определения температуры и влажности, '
                         'FC-28 Arduino - это простой датчик влажности почвы, Макетная плата - универсальная печатная плата для сборки системы. \n 2 Для того чтобы наша модель имела хороший вид и не выглядело сборкой , '
                         'нам нужен был корпус, так же выполнявший защитную роль для всех наших комплектующих. Для его создания мы отталкивались от нашей идеи, '
                         'желая воплотить саму суть его функции, передав на внешние данные, мы использовали следующее:',
                         reply_markup=Button)

    elif call.data == 'разраб':
        Button = InlineKeyboardMarkup(row_width=True)
        I = InlineKeyboardButton(text='Александр', url='t.me/s1s6a')
        dima = InlineKeyboardButton(text='Дмитрий', url='t.me/shadowprettyx')
        arina = InlineKeyboardButton(text='Арина', url='t.me/vmolok')
        sergey = InlineKeyboardButton(text='Сергей', url='t.me/s1s6a')
        Button.add(I, dima, arina, sergey)
        bot.send_message(call.message.chat.id,
                         'Над созданием станции участвовало 4 человека \n Курдасов Александр - Главный разработчик \n Золотовский Дмитрий - Генератор Идей, помощник разработчика \n Кудрявцева Арина - Дизайнер, Генератор идей \n Боржемский Сергей - Руководитель',
                         reply_markup=Button)


bot.polling(none_stop = True)