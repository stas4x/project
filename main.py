from search import search_sakila
from stats import get_popular_queries

s = "y"
while s.lower() == "y":
    search_sakila()
    s = input("Продолжить поиск? (Введите y/n): ")

flag_search = input("Хотите вывести статистику самых частых запросов? (Введите y/n): ")
if flag_search.lower() == "y":
    get_popular_queries()

