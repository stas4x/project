import mysql.connector
from proj.db_config import dbconfig_sakila, dbconfig_loggs

def get_connection_sakila():
    return mysql.connector.connect(**dbconfig_sakila)

def get_connection_logs():
    return mysql.connector.connect(**dbconfig_loggs)

def execute_query(query, params=None):
    connection = get_connection_sakila()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f'Ошибка выполнения запроса: {str(e)}')
    finally:
        cursor.close()
        connection.close()
