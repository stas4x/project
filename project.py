import mysql.connector
from tabulate import tabulate  # Добавление импорта tabulate
dbconfig_sakila = {
    'host': 'ich-db.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila'
}
dbconfig_loggs = {
    'host': 'ich-edit.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'ich1_password_ilovedbs',
    'database': '01stas_project'
}
def execute_query(query, params=None):
    sakila_connection = mysql.connector.connect(**dbconfig_sakila)
    sakila_cursor = sakila_connection.cursor()
    try:
        sakila_cursor.execute(query, params)
        result = sakila_cursor.fetchall()
        return result
    except Exception as e:
        print(f'Ошибка выполнения запроса: {str(e)}')
    finally:
        sakila_cursor.close()
        sakila_connection.close()
def log_search_query(log):
    loggs_connection = mysql.connector.connect(**dbconfig_loggs)
    loggs_cursor = loggs_connection.cursor()
    try:
        loggs_cursor.execute("INSERT INTO queries (query) VALUES (%s)", (log,))
        loggs_connection.commit()
    except Exception as e:
        print(f'Ошибка логирования: {str(e)}')
    finally:
        loggs_cursor.close()
        loggs_connection.close()
def log_sql_request(connection, query, command_text):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO proekt (SQL_req_user, commands_text, timestamp) VALUES (%s, %s, NOW())",
        (query, command_text))
    connection.commit()
    print("Запрос записан в историю.")
def get_popular_queries():
    loggs_connection = mysql.connector.connect(**dbconfig_loggs)
    loggs_cursor = loggs_connection.cursor()
    try:
        sql = "SELECT query, COUNT(*) as count FROM Stas_queries GROUP BY query ORDER BY count DESC LIMIT 3"
        loggs_cursor.execute(sql)
        result = loggs_cursor.fetchall()
        if result:
            print('Результаты поиска самых популярных запросов:')
            columns = ['User filter', 'Quantity']
            print(tabulate(result, headers=columns, tablefmt='grid'))
        else:
            print('Ничего не найдено.')
    except Exception as e:
        print(f'Ошибка при выполнении запроса популярности: {str(e)}')
    finally:
        loggs_cursor.close()
        loggs_connection.close()


def search_sakila():
    genre = input('Введите жанр [Action, Adventure, Drama, Comedy ...] (или оставьте поле пустым): ')
    year = input('Введите год (или оставьте поле пустым): ')
    actor = input('Введите актера (или оставьте поле пустым): ')
    rating = input('Введите рейтинг фильма (или оставьте поле пустым): ')
    keyword = input('Введите ключевое слово (или оставьте поле пустым): ')

    # Словарь для описания рейтингов
    rating_descriptions = {
        'G': 'Для всех возрастов',
        'PG': 'Рекомендуется присутствие родителей',
        'PG-13': 'Не подходит для детей до 13 лет',
        'R': 'Лицам до 17 лет обязательно присутствие взрослого',
        'NC-17': 'Только для взрослых (18+)',
    }

    query = '''
        SELECT film.title, film.release_year, film.rating, category.name AS genre, film.length
        FROM film
        JOIN film_category ON film.film_id = film_category.film_id
        JOIN category ON film_category.category_id = category.category_id
        WHERE 1=1
    '''
    query_params = []

    if genre:
        query += " AND category.name LIKE %s"
        query_params.append(f"%{genre}%")
    if year:
        query += " AND film.release_year = %s"
        query_params.append(year)
    if actor:
        query += " AND film.actors LIKE %s"
        query_params.append(f"%{actor}%")
    if rating:
        query += " AND film.rating = %s"
        query_params.append(rating)
    if keyword:
        query += " AND (film.title LIKE %s OR film.description LIKE %s)"
        query_params.append(f"%{keyword}%")
        query_params.append(f"%{keyword}%")
    query += " LIMIT 11"

    log = ' '.join([f'{k}: {v}' for k, v in
                    zip(['genre', 'year', 'actor', 'rating', 'keyword'], [genre, year, actor, rating, keyword]) if v])
    result = execute_query(query, query_params)
    log_search_query(log)

    if result:
        # Замена рейтинга на описание
        result_with_descriptions = [
            (
                row[0],  # Title
                row[1],  # Year
                rating_descriptions.get(row[2], row[2]),  # Описание рейтинга
                row[3],  # Genre
                row[4]  # Length
            )
            for row in result
        ]
        print('Результат поиска:')
        columns = ['Title', 'Year', 'Rating (Description)', 'Genres', 'Length']
        print(tabulate(result_with_descriptions, headers=columns, tablefmt='grid'))
    else:
        print('Ничего не найдено')


s = "y"
while s == "y":
    search_sakila()
    s = input("Продолжить поиск? (Введите y/n): ")

flag_search = input("Хотите вывести статистику самых частых запросов? (Введите y/n): ")
if flag_search == "y":
    get_popular_queries()

