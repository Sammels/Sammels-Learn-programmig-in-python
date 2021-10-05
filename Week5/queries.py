from sqlalchemy import desc
from sqlalchemy.sql import func

from db import db_session
from model import Salary

# Запрос "Сколько-то зарплат по базе"
def top_salary(num_rows) -> str:
    top_salary = Salary.query.order_by(Salary.salary.desc()).limit(num_rows)

    for s in top_salary:
        print(f"З/п: {s.salary}")


# Запрос зарплат для какого-то города
def salary_by_city(city_name) -> str:
    top_salary = Salary.query.filter(Salary.city == city_name).order_by(
        Salary.salary.desc()
    )

    print(city_name)
    for s in top_salary:
        print(f"ЗП {s.salary}")


# Запрос по электронной помощи
def top_salary_by_domain(domain, num_rows) -> str:
    top_salary = (
        Salary.query.filter(Salary.email.ilike(f"%{domain}"))
        .order_by(Salary.salary.desc())
        .limit(num_rows)
    )

    print(domain)
    for s in top_salary:
        print(f"з.п. {s.salary}")


# Запрос на среднюю зарплату
def average_salary() -> str:
    avg_salary = db_session.query(func.avg(Salary.salary)).scalar()
    print(f"Средняя зарплата {avg_salary:.2f}")


# Запрос на количесво уникальных городов
def count_distinct_cities() -> str:
    count_cities = db_session.query(Salary.city).group_by(Salary.city).count()
    print(f"Кол-во городов {count_cities}")


# топ средних зарплат в городе
def top_avg_salary_by_city(num_rows) -> str:
    top_salary = (
        db_session.query(Salary.city, func.avg(Salary.salary).label("avg_salary"))
        .group_by(Salary.city)
        .order_by(desc("avg_salary"))
        .limit(num_rows)
    )

    for city, salary in top_salary:
        print(f"Город {city} - зарплаты {salary:.2f}")


if __name__ == "__main__":
    # top_salary(10)
    # salary_by_city("Ростов-на-Дону")
    # top_salary_by_domain("@yandex.ru", 5)
    # average_salary()
    # count_distinct_cities()
    top_avg_salary_by_city(5)
