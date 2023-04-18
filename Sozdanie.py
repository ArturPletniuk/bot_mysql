import mysql.connector
from mysql.connector import Error
def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password
               )
        print("Подключение к базе данных MySQL прошло успешно")
    except Error as e:
        print(f"Произошла ошибка '{e}'")
    return connection
connection = create_connection("localhost", "root", "XXXXXXX")

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("База данных создана успешно")
    except Error as e:
        print(f"Произошла ошибка '{e}'")

create_database_query = "CREATE DATABASE  bot"
create_database(connection, create_database_query)



