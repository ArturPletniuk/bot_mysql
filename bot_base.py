import telebot
import mysql.connector
from mysql.connector import Error
from telebot import types # для указание типов
from re import findall
# Создаем экземпляр бота
bot = telebot.TeleBot('5865980939:AAEyNQIVekiR8x1QYPgO8RFbzF0NwL5quHc') ### переменная 
# бота сюда записываем наш токен который прислал нам телеграм бот BotFather
def nazad():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#,one_time_keyboard = True)  ## спрятать клаву при нажатии
    btn1 = types.KeyboardButton("Назад ➡")
    markup.add(btn1)
    return markup
def starte(messаge):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#,one_time_keyboard = True)  ## спрятать клаву при нажатии
    btn1 = types.KeyboardButton("Показать справочник ☎")
    btn2 = types.KeyboardButton("Добавить контакт ✅ ")
    btn3 = types.KeyboardButton("Поиск контакта ♻")
    btn4 = types.KeyboardButton("Удалить контакт ❌")
    btn5 = types.KeyboardButton("Изменить контакт ✒")
    markup.add(btn1, btn2,btn3,btn4,btn5)
    bot.send_message(messаge.chat.id,"Выбери команду?", reply_markup=markup)
'''def func(reqest):
    conect = sqlite3.connect('C:/Users/admin/Desktop/base_bot/baza.db')
    cursor =  conect.cursor()
    try:
        value = cursor.execute(reqest)
        conect.commit()
    except Error as e:
        return f"Произошла ошибка {e}" 
    return value'''
import mysql.connector
from mysql.connector import Error
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database=db_name)
    except Error as e:
        print(f"Произошла ошибка '{e}'")
    return connection        
connection = create_connection("localhost", "root", "20062014Denis", "bot")
### создание таблицы
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"Произошла ошибка '{e}'")
def func(quest,a = 0):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="20062014Denis",
        database="bot")
    except Error as e:
        print(f"Произошла ошибка '{e}'")
    curso = connection.cursor()
    try:
        curso.execute(quest)
        if a == 0:
            c = curso.fetchone()[0]
        elif a ==2:
             c = curso.fetchone()   
        else:
            c = curso.fetchall()    
        connection.commit()
        return c
    except Error as e:
        return f"Произошла ошибка '{e}'"
def func_name(array,a = 0):
    client_array = []
    if a == 0:
        nomer = f"""SELECT N.nomer FROM client_nomer AS N JOIN client AS C ON
        C.id = N.client_id WHERE N.client_id = (SELECT id FROM client WHERE family =
        '{array[0]}' AND name = '{array[1]}' AND otches = '{array[2]}' )"""
    else:
        nomer = f"""SELECT N.nomer FROM client_nomer AS N JOIN client AS C ON
        C.id = N.client_id WHERE N.client_id = (SELECT id FROM client WHERE family =
        '{array[1]}' AND name = '{array[2]}' AND otches = '{array[3]}' )"""    
    f = func(nomer,1)
    for i in f:
        for j in i:
            client_array.append(str(j))
    return client_array
##### функкия удаления контакта ############## start
def delet_client(message,delet):
        text  = message.text
        for i in delet:
            result = "".join(findall(r'^\w+',i))
            if text == result:
                delet_nomet = f"""DELETE FROM client_nomer WHERE client_id = {int(text)} """
                delet_nomet = execute_query(connection,delet_nomet)
                delete_client = f"""DELETE FROM client WHERE id = {int(text)} """
                delete_client = execute_query(connection,delete_client)
                bot.send_message(message.chat.id,f'Контакт успешно удален!',parse_mode="html")
                return starte(message)
        if text == 'Назад ➡': 
            return starte(message)
        markup = nazad()
        count = bot.send_message(message.chat.id,f"Такой номера нет в выбранном вами списке\nВыберите номер или нажмите 'Назад ➡'!'",parse_mode="html",reply_markup=markup)
        bot.register_next_step_handler(count,delet_client,delet) 
def delete(message,a = 0):
    if a == 0:
        search(message,a=1)
    else:
        search(message,a=1,b = "изменить")
##### функкия удаления контакта ############## finish
##### функкия изменения контакта ############## start
def update_family(message,id,a = 0):
    family = f"""SELECT family FROM client WHERE id = {int(id)}"""
    family = func(family)
    name = f"""SELECT name FROM client WHERE id = {int(id)}"""
    name = func(name)
    otches = f"""SELECT otches FROM client WHERE id = {int(id)}"""
    otches = func(otches)
    if a == 0:
        family = message.text.title()
        fio = 'family'
    elif a == 1:
        name = message.text.title()
        fio = 'name'
    elif a == 2:
        otches = message.text.title() 
        fio = 'otches'      
    prov = f"""SELECT COUNT(id) FROM client WHERE family = '{family}' AND 
    name = '{name}' AND otches = '{otches}' """
    prov = func(prov)
    if int(prov) == 0:
        update = f"""UPDATE client SET {fio} = '{message.text.title() }' WHERE id = {id}"""
        update = execute_query(connection, update)
        bot.send_message(message.chat.id,'Данные успешно обновлены!',parse_mode="html")
        return starte(message)
    else:
        count = bot.send_message(message.chat.id,'Такой контакт с такими данными уже есть в справочнике.\nВыберите другие данные.',parse_mode="html")  
        text = f'Изменить:\nф - фамилию\nи - имя\nо - отчество\nт - телефон'
        count = bot.send_message(message.chat.id,text,parse_mode="html")
        bot.register_next_step_handler(count,update_client_text,id)
def update_nomer_text(message,resulte,a = 0):
    if a == 0:
        result = int("".join((findall(r'\w+$',resulte))))
    else: 
        results = int("".join((findall(r'^\w+',resulte[0]))))
    prov = f"""SELECT COUNT(nomer) FROM client_nomer WHERE nomer = {int(message.text)}"""
    prov = func(prov)
    if prov > 0:
        bot.send_message(message.chat.id,"Такой номер уже есть в справочнике",parse_mode="html")
        count = bot.send_message(message.chat.id,"Введите новый номер:",parse_mode="html")
        if a == 0:           
            bot.register_next_step_handler(count,update_nomer_text,resulte)
        else:
            bot.register_next_step_handler(count,update_nomer_text,resulte,1)   
    else:
        if a == 0:
            update = f"""UPDATE client_nomer SET nomer = {int(message.text)} WHERE nomer  = {result}""" 
        else:
            client_id = f"""SELECT client_id FROM client_nomer WHERE id == {results}"""
            client_id = func(client_id)
            update = f"""INSERT INTO client_nomer ('nomer','client_id') VALUES ({int(message.text)},{int(client_id)})"""           
        update = execute_query(connection, update)
        bot.send_message(message.chat.id,"Номер успешно обновлён!",parse_mode="html") 
        return starte(message)
def update_nomer(message,array,a = 0):
    for i in array:
        result = "".join(findall(r'^\w+',i))
        if message.text == result:
            if a == 0:
                count = bot.send_message(message.chat.id,"Введите новый номер:",parse_mode="html")           
                return bot.register_next_step_handler(count,update_nomer_text,i)
            else:
                return update_nomer_delet(message,i)
    bot.send_message(message.chat.id,"Такой цифры нет в списке",parse_mode="html")
    if a == 0:
        count = bot.send_message(message.chat.id,"Выберите цифру номера который хотите изменить:",parse_mode="html")           
        bot.register_next_step_handler(count,update_nomer,array) 
    else:
        count = bot.send_message(message.chat.id,"Выберите цифру номера который хотите удалить:",parse_mode="html")
        bot.register_next_step_handler(count,update_nomer,array,1) 
def update_nomer_delet(message,nomer):    ### сюда попадает номер для удаления
    result = int("".join((findall(r'\w+$',nomer))))
    delet = f"""DELETE FROM client_nomer WHERE nomer = {result}"""
    delet =  execute_query(connection, delet)
    bot.send_message(message.chat.id,"Номер успешно удалён!",parse_mode="html")
    return starte(message)
def update_delet_nomer(message,array):
    if message.text == 'Изменить ✏':
        count  = bot.send_message(message.chat.id,"Выберите цифру номера который хотите изменить:",parse_mode="html")        
        bot.register_next_step_handler(count,update_nomer,array)
    elif message.text == 'Удалить ❎':
        count  = bot.send_message(message.chat.id,"Выберите цифру номера который хотите удалить:",parse_mode="html")        
        bot.register_next_step_handler(count,update_nomer,array,1)
    elif message.text == 'Добавить ✅':
        count  = bot.send_message(message.chat.id,"Введите номер который хотите добавить:",parse_mode="html")           
        bot.register_next_step_handler(count,update_nomer_text,array,1)
    else:
        count  = bot.send_message(message.chat.id,"Вы можете выбрать только 'Удалить ❎' или 'Изменить ✏'!!",parse_mode="html")        
        bot.register_next_step_handler(count,update_delet_nomer,array)
def update_client_text(message,id):
    if message.text == 'Фамилия 🍒' or message.text == 'Имя 🍉' or message.text == 'Отчество 🍇':
        if message.text == 'Фамилия 🍒':
            count = bot.send_message(message.chat.id,'Введите новую фамилию:',parse_mode="html")
            bot.register_next_step_handler(count,update_family,id)
        elif message.text == 'Имя 🍉':
            count = bot.send_message(message.chat.id,'Введите новое имя:',parse_mode="html")
            bot.register_next_step_handler(count,update_family,id,1) 
        elif message.text == 'Отчество 🍇':
            count = bot.send_message(message.chat.id,'Введите новое отчество:',parse_mode="html")
            bot.register_next_step_handler(count,update_family,id,2)      
    elif message.text == 'Телефон 📞':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#,one_time_keyboard = True)  ## спрятать клаву при нажатии 
        btn1 = types.KeyboardButton("Удалить ❎")
        btn2 = types.KeyboardButton("Изменить ✏")
        btn3 = types.KeyboardButton("Добавить ✅")
        markup.add(btn1,btn2,btn3)
        nomer_array = []
        nomer = f"""SELECT id,nomer FROM client_nomer WHERE client_id = {id}"""
        nomer = func(nomer,1)
        a = ''
        score = 0
        for i in nomer:
            for j in i:
                score+= 1
                if score == 1:
                    a += str(j) + '.  '
                else:
                     a += str(j)   
            nomer_array.append(a) 
            a = ''
            score = 0 
        bot.send_message(message.chat.id,"\n".join(nomer_array),parse_mode="html")    
        count = bot.send_message(message.chat.id,"Выберите",parse_mode="html",reply_markup=markup) 
        bot.register_next_step_handler(count,update_delet_nomer,nomer_array)
    else:
        bot.send_message(message.chat.id,f'Такой команды нет',parse_mode="html")
        text = f'Выберите что хотите изменить'
        count = bot.send_message(message.chat.id,text,parse_mode="html")
        bot.register_next_step_handler(count,update_client_text,id)
def update_client(message,id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#,one_time_keyboard = True)  ## спрятать клаву при нажатии 
    if message.text == 'Назад ➡':
        return starte(message)
    text = message.text
    for i in id:
        result = "".join(findall(r'^\w+',i))
        if text == result:
            btn1 = types.KeyboardButton("Фамилия 🍒")
            btn2 = types.KeyboardButton("Имя 🍉")
            btn3 = types.KeyboardButton("Отчество 🍇")
            btn4 = types.KeyboardButton("Телефон 📞")
            markup.add(btn1,btn2,btn3,btn4)
            texte ='Выберите что хотите изменить?' 
            count = bot.send_message(message.chat.id,texte,parse_mode="html",reply_markup=markup)
            return bot.register_next_step_handler(count,update_client_text,text)
    bot.send_message(message.chat.id,f'Такой цифры нет в выбранном вами списке!',parse_mode="html")
    count = bot.send_message(message.chat.id,"Введите данные которые надо изменить или нажмите 'Назад ➡' для выхода: ",parse_mode="html",reply_markup=markup)
    bot.register_next_step_handler(count,update_client,id)    
##### функкия изменения контакта ############## finish
##### функкия добавления контакта ############## start
def family(message):
        list_fio = []
        list_fio.append(message.text.title())
        msg = bot.send_message(message.chat.id, 'Введите имя: ')
        bot.register_next_step_handler(msg,name,list_fio)
def name(message,list_fio):
    list_fio.append(message.text.title())
    msg = bot.send_message(message.chat.id, 'Введите отчество: ')   
    bot.register_next_step_handler(msg,otches,list_fio)
def otches(message,list_fio,):
    list_fio.append(message.text.title())
    msg = bot.send_message(message.chat.id, 'Введите номер: ')   
    bot.register_next_step_handler(msg,nomer,list_fio)
def nomer(message,list_fio):
    list_fio.append(message.text.title())
    prov = f"""SELECT EXISTS(SELECT id FROM client WHERE family = '{list_fio[0]}'
    AND name = '{list_fio[1]}' AND otches = '{list_fio[2]}')"""
    #prov = func(prov).fetchone()[0]
    prov = func(prov)
    prov_nomer = f"""SELECT EXISTS(SELECT nomer FROM client_nomer WHERE nomer = {int(list_fio[3])})"""
    #prov_nomer = func(prov_nomer).fetchone()[0]
    prov_nomer = func(prov_nomer)
    if int(prov) == 0 and int(prov_nomer == 0):
        insert_foi = f"""INSERT INTO client (family,name,otches) 
    VALUES  ('{list_fio[0]}','{list_fio[1]}','{list_fio[2]}')"""
        #f = func(insert_foi)
        execute_query(connection,insert_foi)
        sel_id = f"""SELECT id FROM client WHERE family = '{list_fio[0]}'AND name = '{list_fio[1]}'
        AND otches = '{list_fio[2]}'"""
        sel_id  = func(sel_id)
        insert_nomer = f"""INSERT INTO client_nomer (nomer,client_id) 
    VALUES  ({int(list_fio[3])},{sel_id})"""
        execute_query(connection,insert_nomer)
        bot.send_message(message.chat.id,"Данные успешно добавлены!",parse_mode="html")
        return starte(message)
    else:
        bot.send_message(message.chat.id,"Такой контакт уже существует!",parse_mode="html")
        return starte(message)
##### функкия добавления контакта ############## finish
##### функкия поиска контакта ############## start
def search(message,a = 0,b = 'удалить'):
    nomer_client = []
    nomer_array_delet = []
    message_text = message.text.title()
    nomer = None
    fio = ''
    try:
        nomer = int(message_text)
    except ValueError:
        fio = message_text    
    if nomer != None:
        markup = nazad()
        try:
            nomer = f"""SELECT C.family,C.name,C.otches FROM client AS C JOIN client_nomer AS N ON
            C.id = N.client_id WHERE N.nomer = {nomer}"""
            fio = func(nomer,2)
            nomer = f"""SELECT N.nomer FROM client_nomer AS N JOIN client AS C ON
            C.id = N.client_id WHERE N.client_id = (SELECT id FROM client WHERE family =
            '{fio[0]}' AND name = '{fio[1]}' AND otches = '{fio[2]}' )"""
            f = func(nomer,1)
            for i in f:
                for j in i:
                    nomer_client.append(str(j))
            client = fio[0] + ' ' +fio[1]+' '+fio[2] + ' - ' + "  ".join(nomer_client)
            if a != 0:
                nomer = f"""SELECT DISTINCT(N.client_id) FROM client_nomer AS N JOIN client AS C ON
            C.id = N.client_id WHERE N.nomer = {int(message_text)}"""
                id = func(nomer)
                delet = str(id) + '. '+ client
                bot.send_message(message.chat.id,delet ,parse_mode="html")
                count = bot.send_message(message.chat.id,f"Выберите цифру контакта который хотите {b} или нажмите 'Назад ➡' для выхода в главное меню",reply_markup=markup)
                nomer_array_delet.append(delet)
                if b == 'удалить':   
                    bot.register_next_step_handler(count,delet_client,nomer_array_delet)
                else:
                    bot.register_next_step_handler(count,update_client,nomer_array_delet)
            else:           
                bot.send_message(message.chat.id,client,parse_mode="html")
                return starte(message) 
        except Exception:
            bot.send_message(message.chat.id,"Такого контакта нет в справочнике!",parse_mode="html")        
            return starte(message)
    else:
        markup = nazad()
        fio = fio.split()
        client_array = []
        if len(fio) == 1:
            prov = f"""SELECT EXISTS(SELECT id FROM client WHERE family = '{fio[0]}' OR 
                name = '{fio[0]}' OR otches = '{fio[0]}')"""
            prov = func(prov)
            if int(prov) > 0:
                if a == 0:
                    a = 0
                    fio_1 = f"""SELECT family,name,otches FROM client WHERE family = '{fio[0]}' OR 
                    name = '{fio[0]}' OR otches = '{fio[0]}'"""
                else:
                    a = 1
                    fio_1 = f"""SELECT * FROM client WHERE family = '{fio[0]}' OR 
                name = '{fio[0]}' OR otches = '{fio[0]}'"""    
                fio_1 = func(fio_1,1)
                for i in fio_1:
                    for j in i:
                        nomer_client.append(str(j))  
                    nomer_array = func_name(nomer_client,a)
                    client = " ".join(nomer_client) +' - '+ " ".join(nomer_array)
                    client_array.append(client)
                    nomer_client = []
                if a != 0:
                    bot.send_message(message.chat.id,"\n".join(client_array),parse_mode="html")
                    count = bot.send_message(message.chat.id,f"Выберите номер контакта который хотите {b}?",parse_mode="html",reply_markup=markup)
                    if b == 'удалить':    
                        bot.register_next_step_handler(count,delet_client,client_array)
                    else:
                        bot.register_next_step_handler(count,update_client,client_array) 
                else:                                 
                    bot.send_message(message.chat.id,"\n".join(client_array),parse_mode="html")
                    return starte(message)
            else:
                bot.send_message(message.chat.id,"Такого контакта нет в справочнике!",parse_mode="html")        
                return starte(message)
        elif len(fio) == 2:
            markup = nazad()
            prov = f"""SELECT EXISTS(SELECT family,name,otches FROM client WHERE (family = '{fio[0]}' OR 
                    name = '{fio[0]}' OR otches = '{fio[0]}') AND(family = '{fio[1]}' OR 
                    name = '{fio[1]}' OR otches = '{fio[1]}'))"""
            prov = func(prov)
            if int(prov) > 0:
                if a == 0:
                    a = 0
                    fio_1 = f"""SELECT family,name,otches FROM client WHERE (family = '{fio[0]}' OR 
                    name = '{fio[0]}' OR otches = '{fio[0]}') AND(family = '{fio[1]}' OR 
                    name = '{fio[1]}' OR otches = '{fio[1]}')"""
                else:
                    a = 1 
                    fio_1 = f"""SELECT * FROM client WHERE (family = '{fio[0]}' OR 
                    name = '{fio[0]}' OR otches = '{fio[0]}') AND(family = '{fio[1]}' OR 
                    name = '{fio[1]}' OR otches = '{fio[1]}')"""   
                fio_1 = func(fio_1,1)
                for i in fio_1:
                    for j in i:
                        nomer_client.append(str(j))
                    nomer_array = func_name(nomer_client,a)
                    client = " ".join(nomer_client) +' - '+ " ".join(nomer_array)
                    client_array.append(client)
                    nomer_client = []              
                if a != 0:
                    bot.send_message(message.chat.id,"\n".join(client_array),parse_mode="html")
                    count = bot.send_message(message.chat.id,f"Выберите номер контакта который хотите {b}?",parse_mode="html",reply_markup=markup)
                    if b == 'удалить':    
                        bot.register_next_step_handler(count,delet_client,client_array)
                    else:
                        bot.register_next_step_handler(count,update_client,client_array) 
                else:                                 
                    bot.send_message(message.chat.id,"\n".join(client_array),parse_mode="html")
                    return starte(message)
            else:
                bot.send_message(message.chat.id,"Такого контакта нет в справочнике!",parse_mode="html")        
                return starte(message)
        elif len(fio) == 3:
            markup = nazad()
            prov = f"""SELECT EXISTS(SELECT family,name,otches FROM client WHERE (family = '{fio[0]}' OR 
                    name = '{fio[0]}' OR otches = '{fio[0]}') AND (family = '{fio[1]}' OR 
                    name = '{fio[1]}' OR otches = '{fio[1]}') AND (family = '{fio[2]}' OR 
                    name = '{fio[2]}' OR otches = '{fio[2]}'))"""
            prov = func(prov)
            if int(prov) > 0:
                if a == 0:
                    a = 0
                    fio_1 = f"""SELECT family,name,otches FROM client WHERE (family = '{fio[0]}' OR 
                    name = '{fio[0]}' OR otches = '{fio[0]}') AND (family = '{fio[1]}' OR 
                    name = '{fio[1]}' OR otches = '{fio[1]}') AND (family = '{fio[2]}' OR 
                    name = '{fio[2]}' OR otches = '{fio[2]}') """
                else:
                    a = 1
                    fio_1 = f"""SELECT * FROM client WHERE (family = '{fio[0]}' OR 
                    name = '{fio[0]}' OR otches = '{fio[0]}') AND (family = '{fio[1]}' OR 
                    name = '{fio[1]}' OR otches = '{fio[1]}') AND (family = '{fio[2]}' OR 
                    name = '{fio[2]}' OR otches = '{fio[2]}') """    
                fio_1 = func(fio_1,1)
                for i in fio_1:
                    for j in i:
                        nomer_client.append(str(j))
                    nomer_array = func_name(nomer_client,a)
                    client = " ".join(nomer_client) +' - '+ " ".join(nomer_array)
                    client_array.append(client)
                    nomer_client = []              
                if a != 0:
                    bot.send_message(message.chat.id,"\n".join(client_array),parse_mode="html")
                    count = bot.send_message(message.chat.id,f"Выберите номер контакта который хотите {b}?",parse_mode="html",reply_markup=markup)
                    if b == 'удалить':    
                        bot.register_next_step_handler(count,delet_client,client_array)
                    else:
                        bot.register_next_step_handler(count,update_client,client_array) 
                else:                                 
                    bot.send_message(message.chat.id,"\n".join(client_array),parse_mode="html")
                    return starte(message)
            else:
                bot.send_message(message.chat.id,"Такого контакта нет в справочнике!",parse_mode="html")        
                return starte(message)
        else:
            bot.send_message(message.chat.id,"Такого контакта нет в справочнике!",parse_mode="html")
##### функкия поиска контакта ############## finish
############### НАЧАЛО БОТА ##################################
### Отслеживание команд
@bot.message_handler(commands = ["start"])
def start(messаge):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#,one_time_keyboard = True)  ## спрятать клаву при нажатии
    btn1 = types.KeyboardButton("Показать справочник ☎")
    btn2 = types.KeyboardButton("Добавить контакт ✅ ")
    btn3 = types.KeyboardButton("Поиск контакта ♻")
    btn4 = types.KeyboardButton("Удалить контакт ❌")
    btn5 = types.KeyboardButton("Изменить контакт ✒")
    markup.add(btn1, btn2,btn3,btn4,btn5)
    bot.send_message(messаge.chat.id,f"Привет!Здесь находится телефонный справочник и я помогу тебе с ним разобраться.", reply_markup=markup)  
### Отслеживание текста
@bot.message_handler()
def get_user_text(message):
    if message.text == "Показать справочник ☎":
        #a = telebot.types.ReplyKeyboardRemove()                ### удаления кнопок
        select ="""SELECT family,name,otches FROM client """
        f = func(select,1)
        fio = []
        nomer_array = []
        fio_nomer = []
        for i in f:
            for j in i:
                fio.append(j)
            nomer=  f"""SELECT N.nomer FROM client_nomer AS N JOIN client AS C ON 
            C.id = N.client_id WHERE C.family = '{fio[0]}' AND
            C.name = '{fio[1]}' AND C.otches = '{fio[2]}' """
            nomer = func(nomer,1)
            for i in nomer:
                for j in i:
                    nomer_array.append(str(j)) 
            fio_nomer.append(" ".join(fio) + ' - ' +"   ".join(nomer_array))            
            fio = []
            nomer_array = []
        bot.send_message(message.chat.id,"\n".join(fio_nomer),parse_mode="html")    
    elif message.text == "Добавить контакт ✅":     
            msg = bot.send_message(message.chat.id, 'Введите Фамилию: ')
            bot.register_next_step_handler(msg,family)
    elif message.text == "Поиск контакта ♻":  
            msg = bot.send_message(message.chat.id, 'Введите данные для поиска: ')
            bot.register_next_step_handler(msg,search)
    elif message.text == "Удалить контакт ❌":
            msg = bot.send_message(message.chat.id,f"Введите данные которые надо удалить: ")
            bot.register_next_step_handler(msg,delete)
    elif message.text == "Изменить контакт ✒":    
            msg = bot.send_message(message.chat.id,"Введите данные которые надо изменить: ")
            bot.register_next_step_handler(msg,delete,1)                                 
    else:
        bot.send_message(message.chat.id, 'Такой команды нет в списке!')    
### запустить бот на постоянную обработку
bot.polling(non_stop=True)   ## non_stop=True - наш бот должен работать постоянно 