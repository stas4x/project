from proj.db_utils import get_connection_logs

def log_search_query(log):
    connection = get_connection_logs()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Stas_queries (query) VALUES (%s)", (log,))
        connection.commit()
    except Exception as e:
        print(f'Ошибка логирования: {str(e)}')
    finally:
        cursor.close()
        connection.close()
