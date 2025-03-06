from db_utils import get_connection_logs
from tabulate import tabulate

def get_popular_queries(limit=10):
    connection = get_connection_logs()
    cursor = connection.cursor()
    try:
        sql = f"SELECT query, COUNT(*) as count FROM Stas_queries GROUP BY query ORDER BY count DESC LIMIT {limit}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            print(f'Top {limit} Most Popular Searches:')
            columns = ['Query', 'Count']
            print(tabulate(result, headers=columns, tablefmt='grid'))
        else:
            print('No searches found.')
    except Exception as e:
        print(f'Ошибка при выполнении запроса популярности: {str(e)}')
    finally:
        cursor.close()
        connection.close()
