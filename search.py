from db_utils import execute_query
from log_utils import log_search_query
from tabulate import tabulate

def search_sakila():
    genre = input('Введите жанр [Action, Adventure, Drama, Comedy ...] (или оставьте поле пустым): ')
    year = input('Введите год (или оставьте поле пустым): ')
    rating = input('Введите рейтинг фильма (или оставьте поле пустым): ')
    keyword = input('Введите ключевое слово (или оставьте поле пустым): ')

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
    if rating:
        query += " AND film.rating = %s"
        query_params.append(rating)
    if keyword:
        query += " AND (film.title LIKE %s OR film.description LIKE %s)"
        query_params.append(f"%{keyword}%")
        query_params.append(f"%{keyword}%")
    query += " LIMIT 11"

    log = ' '.join([f'{k}: {v}' for k, v in zip(['genre', 'year', 'rating', 'keyword'], [genre, year, rating, keyword]) if v])
    result = execute_query(query, query_params)
    log_search_query(log)

    if result:
        print('Результат поиска:')
        columns = ['Title', 'Year', 'Rating', 'Genres', 'Length']
        print(tabulate(result, headers=columns, tablefmt='grid'))
    else:
        print('Ничего не найдено')
