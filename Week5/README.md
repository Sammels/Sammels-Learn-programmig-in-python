# add 5 неделя
Продолжение учебы

1. Добавление и фильтрация
2. Загрузка данных в БД
3. Оптимизация загрузки
4. Делаем запросы ч 1
5. Делаем запросы ч.2 

## 1. Добавление и фильтрация
- Создание таблицу и загрузим в неё данные csv файла
- Загрузка запросов, и исп. сортировку и фильтрацию

### Взять данные
Для генерации данных исп. `Faker` - Библиотека для генерации фейковых данных
```python
pip3 install faker
```
Установка библиотеки

### Первичное создание простого файла.
```python
# Импорт
from faker import Faker
# Присваииваем имя классу
fake = Faker()
# Вывод
print(fake.name(), fake.city_name(), fake.large_company())
```

### Какими данными будем оперировать.
Созд. csv файл с данными по зарплата сотрудников разлиных компаний.
Для кажд сотрудника будем генерирвать следующий набор полей:

`ФИО, Город, Адрес, Компания, Должность, Телефон, E-mail, Дата рождения, Размер зп`

<b>Создание текстовых данных.</b>
Напишем функцию, которая возвращает строку таблицы:

```python
import csv
import random
from faker import Faker

fake = Faker()


def get_fake_row() -> list:
    return [fake.name(), fake.city_name(), fake.street_address(),
            fake.large_company(),
            fake.job(), fake.phone_number(), fake.free_email(),
            fake.date_of_birth(minimum_age=18, maximum_age=70),
            random.randint(20000, 200000)]
```

## 2. Загрузка данных в базу
Сделаем простую реализацию загрузки данных

1. Скобируем `db.py` 
2. Создадим файл с моделью и создадим таблицу в БД
3. Создадим файл `loader.py`, который построчно читает csv-файл и сохраняет прочитанное в БД.

### 1. Создание файла с моделью
Создаем файл `model.py`

```python
from sqlalchemy import Column, Integer, String, Date

from db import Base, engine

# Модель называют в ед.ч а табл. в мн.ч
class Salary(Base):
    __tablename__ = 'salary'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    address = Column(String)
    company = Column(String)
    job = Column(String)
    phone_number = Column(String)
    email = Column(String)
    date_of_birth = Column(Date)
    salary = Column(Integer)


    def __repr__(self):
        return f"Salary {self.id}, {self.name}, {self.company}"
```
### Создание файла `loader.py`
Создаем загрузчик файлов
```python
import csv

from db import db_session
from model import Salary

# Функция чтения csv
def read_csv(filename):
    with open(filename, "r", encoding="utf-8") as f:
        fields = [
            "name",
            "city_name",
            "street_address",
            "large_company",
            "job",
            "phone_number",
            "free_email",
            "date_of_birth",
            "salary",
        ]
        reader = csv.DictReader(f, fields, delimiter=";")
        for row in reader:
            save_salary_data(row)


# Функция Сохранения цсв
def save_salary_data(row):
    salary = Salary(
        name=row["name"],
        city=row["city_name"],
        address=row["street_address"],
        company=row["large_company"],
        job=row["job"],
        phone_number=row["phone_number"],
        email=row["free_email"],
        date_of_birth=row["date_of_birth"],
        salary=row["salary"],
    )
    db_session.add(salary)
    db_session.commit()

if __name__=="__main__":
    read_csv('salary.csv')

```

## 3. Оптимизация загрузки
1. Замер времени загрузки таблицы
```python
import time

...

if __name__=='__main__':
    start = time.time()
    read_csv('salary.csv')
    print('Данные загружены за ', time.time() - start)
```

2. Запустем процесс загрузки.
Очистим таблицу через Valentuna studio - `Удалить все записи`

Мы реализовали "наивную" загрузку данных

```python

# Функция чтения оптимизация
def read_csv2(filename):
    with open(filename, "r", encoding="utf-8") as f:
        fields = [
            "name",
            "city",
            "address",
            "company",
            "job",
            "phone_number",
            "email",
            "date_of_birth",
            "salary",
        ]
        reader = csv.DictReader(f, fields, delimiter=";")
        # Создание списка
        salary_data = []
        for row in reader:
            salary_data.append(row)
        save_salary_data2(salary_data)


# Функция сохр оптимизация
def save_salary_data2(data):
    db_session.bulk_insert_mappings(Salary, data)
    db_session.commit()
```
## 4. Запросы к БД ч. 1
Положить данные в БД, это малая часть задачи.
1. Создадим файл `queries.py`
2. Написать код запроса топ 10 больших зарплат
```python
from model import Salary

# Запрос "Сколько-то зарплат по базе"
def top_salary(num_rows):
    top_salary = Salary.query.order_by(Salary.salary.desc()).limit(num_rows)

    for s in top_salary:
        print(f'З/п: {s.salary}')


if __name__ == "__main__":
    top_salary(10)
```
3. Получение топ зарплат по городу
```python
# Запрос зарплат для какого-то города
def salary_by_city(city_name):
    top_salary = Salary.query.filter(Salary.city == city_name).order_by(
        Salary.salary.desc()
    )

    print(city_name)
    for s in top_salary:
        print(f"ЗП {s.salary}")


if __name__ == "__main__":
    #top_salary(10)
    salary_by_city("Москва")
```

4. Топ зарплат по эл. почте
```python
# Запрос по электронной помощи
def top_salary_by_domain(domain, num_rows):
    top_salary = (
        Salary.query.filter(Salary.email.ilike(f"%{domain}"))
        .order_by(Salary.salary.desc())
        .limit(num_rows)
    )

    print(domain)
    for s in top_salary:
        print(f"з.п. {s.salary}")
...

if __name__ == "__main__":
    top_salary_by_domain("@yandex.ru", 5)
```

## 5. Запросы к БД ч. 2
1. Получение средней зарплаты
`avg_salary:.2f` -  округление запроса до 2-х знаков после запятой

```python
from sqlalchemy.sql import func
...

def average_salary():
    avg_salary = db_session.query(func.avg(Salary.salary)).scalar()
    print(f'Средняя зарплата {avg_salary:.2f}')

...
if __name__=="__main__":
    average_salary()
```

2. Посчитаем количество уникальных городов
```python
from db import db_session
...

# Запрос на количесво уникальных городов
def count_distinct_cities() -> str:
    count_cities = db_session.query(Salary.city).group_by(Salary.city).count()
    print(f"Кол-во городов {count_cities}")
...
if __name__ == "__main__":
    ...
    count_distinct_cities()

```
3. новый сложный запрос "топ средних зарплат в городе"
```python
from sqlalchemy import desc
...

# топ средних зарплат в городе
def top_avg_salary_by_city(num_rows)-> str:
    top_salary = db_session.query(
        Salary.city,
        func.avg(Salary.salary).label('avg_salary')
        ).group_by(Salary.city).order_by(desc('avg_salary')).limit(num_rows)

    for city, salary in top_salary:
        print(f"Город {city} - зарплаты {salary:.2f}")

...
if __name__ == "__main__":
    top_avg_salary_by_city(5)

```
print
```
Город Гремячинск (Бурят.) - зарплаты 198849.00
Город Холмск - зарплаты 190608.00
Город Усть-Илимск - зарплаты 190397.00
Город Елабуга - зарплаты 187935.00
Город Рыбинск - зарплаты 186369.00

```
