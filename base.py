import mysql.connector
from mysql.connector import Error
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database=db_name
        )
        print("Подключение к базе данных MySQL прошло успешно")
    except Error as e:
        print(f"Произошла ошибка '{e}'")
    return connection        
connection = create_connection("localhost", "root", "XXXXXX", "bot")
### создание таблицы
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Запрос  на создание таблицы выполнен успешно")
    except Error as e:
        print(f"Произошла ошибка '{e}'")
tabl = """CREATE TABLE IF NOT EXISTS client 
        (id INT PRIMARY KEY AUTO_INCREMENT,
        family VARCHAR(20) DEFAULT  'family',
        name VARCHAR(20) DEFAULT 'name',
        otches VARCHAR(20) DEFAULT 'otches')"""
tabl2 = """CREATE TABLE IF NOT EXISTS client_nomer 
        (id INT PRIMARY KEY AUTO_INCREMENT,
        nomer INT  DEFAULT  0,
        client_id INT,
        FOREIGN KEY (client_id)  REFERENCES client (id) )"""
drop_table = """DROP TABLE price_month"""
add = """INSERT INTO client ('family','name','otches') VALUES ('Бабич','Артём',
'Тимофеевич')
"""
dele = """DELETE FROM client WHERE id  = 20"""
add1 = """INSERT INTO client_nomer ('nomer','client_id') VALUES (444444,2)
"""
update = """UPDATE client_nomer SET nomer = 333 WHERE id = 40
"""
a = """ALTER TABLE client DROP COLUMN number_of_lession11 """
'''f = func(update)
exit()'''
array_drop = ['DROP TABLE price_month','DROP TABLE client_day','DROP TABLE  client_month']
array_add_table = [tabl,tabl2]
def array_tabl_up(array):
    for i in array:
        execute_query(connection,i)
#array_tabl_up(conect,array_drop)
#array_tabl_up(array_add_table) 

add = """INSERT INTO client_nomer (nomer, client_id) VALUES 
(1029809451,1)""" 
add1 = """INSERT INTO client (family, name, otches) VALUES 
('Плетнюк','Артур','Русланович'),
('Плетнюк','Ольга','Валерьевна'),
('Иванов','Иван','Иванович')"""     
execute_query(connection,add)
