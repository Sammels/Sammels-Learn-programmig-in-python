# Базы данных: Связь один-ко-многим

## Для чего использовать несколько таблиц.

Данные нужно хранить разделяя на сущности

## Данные будут хранится в разных таблицах.

В наших данных можно выделить 3 типа объектов наших данных.
У нас есть `Компании`, в каждой из которых могут работать один или несколько`Сотрудников`. И каждый сотрудник получил за год несколько `Выплат`. Для простоты будем хранить географич инф. (города, адреса) вместе с компаниями и предположим что все сотрудники фрилансеры и получают вылаты 1 раз в месяц и сумма каждый раз разраная.

## Нарисуем схему данных
Для рисования исп `LucidChart`
Схема БД в `Схема БД.png`

## Установим Зависимости

Нужно установить несколько библиотек, создадим файл `requirements.txt`

```python
Faker
psycopg2-binary
sqlalchemy
```
и выполним `pip3 install -r requirements.txt`


## Переработаем генерацию данных
Нужно сгенерировать несколько компаний, для каждой компании -несколько сотрудников и для каждого сотрудника платежи за несколько месяцев.

Пример:
10 компаний, в каждой по 10 сотрудников и для каждого сотрудника платежи за 1 год: `10*10*12 = 1200`


## Функция для создания фиктивной компании


```python
# Функция Фиктивная компания
def fake_companies(num_rows=10) -> list:
    companies = []
    for _ in range(num_rows):
        companies.append(
            [fake.large_company(), fake.city_name(),
            fake.street_address(), fake.phone_number()]
            )
    return companies
```

## Функция, создаюшая сотрудников
При сложении двух списков мы объединяем их содержимое в общий список.
Т.е. в результате работы этого кода мы получим список со 100 списками внутри, в каждом из которых будет информация о компании и сотруднике:

```python
def fake_employees(companies, num_rows=10):
    employees = []
    for company in companies:
        for _ in range(num_rows):
            employee = [fake.name(), fake.job(), fake.phone_number(),
                        fake.free_email(), fake.date_of_birth(minimum_age=18, maximum_age=70)]
            employees.append(company + employee)
    return employees
```

## Функция генерации фиктивного платежа
```python
...
from datetime import date
...

# Функция фиктивных выплат
def fake_payment(employees) -> list:
    payments = []
    for employee in employees:
        for month in range(1,13):
            payment_date = date(2020, month, random.randint(10, 28))
            ammount = random.randint(20000, 200000)
            payment = [payment_date, ammount]
            payments.append(employee + payment)
    return payments
...

if __name__ == "__main__":
    companies = fake_companies()
    employees = fake_employees(companies)
    payments = fake_payment(employees)
    print(len(payments))
    #generate_data()

```

## Генерация данных
```python
...

def generate_data(payments) -> "csv file":
    with open("salary.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        for payment in payments:
            writer.writerow(payment)
```

## Создадим модели
Создадим модель для каждой сущности: `Company`, `Employee`, `Payment`.
Для связи между моделями мы будем использовать поле специального типа - `ForeignKey`

`ForeignKey` при добавлении данных проверяет, что число, которое мы в него вставляем, действительно есть в связанной таблице.


### Модель Company

Создадим файл `models.py`

```python
from sqlalchemy import Column, Integer, String, Date



from db import Base, engine

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    address = Column(String)
    phome = Column(String)

    def __repr__ (self):
        return f'Company id: {self.id}, name: {self.name}'
```

### Модель Employee

```python
from sqlalchemy import Column, Integer, String, Date, ForeignKey

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey(Company.id), index=True, nullable=True)
    name = Column(String)
    job = Column(String)
    phone = Column(String)
    email = Column(String)
    date_of_birth = Column(Date)

    def __repr__(self):
        return f'Employee id: {self.id}, Name: {self.name}'
```

### Модель Payment
Создадим модель платежей

```python
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer(), primary_key=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), index=True, nullable=True)
    payment_date = Column(Date)
    ammount = Column(Integer)

    def __repr__(self):
        return f'Payment id: {self.id}, date: {self.payment_date}'
```

После всего ран
```python
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
```

# Загрузка данных

Более сложный вариант загрузки:
1. Прочитаем все строки из csv-файла в список словарей
2. Выберем все уникальные компании, загрузим их в базу и получим `id` для каждой компании.
3. Выберем всех уникальных сотрудников и загрузим их в базу, подставляя в поле `company_id` иденификатор соответствующей коспании и получим `id` для каждого сотрудника.
4. Загрузим все данные платежей, подставляя в поле `employee_id` идентификатор сотрудника.


## Чтение CSV

```python
import csv


from db import db_session
from models import Company, Employee, Payment

# Читаем csv
def read_csv(filename):
    with open(filenamem 'r', encoding='utf-8') as f:
        fields = ['company', 'city', 'address', 'phone_company', 'name', 'job',
                  'phone_person', 'email', 'date_of_birth', 'payment_date', 'ammount']
        reader = csv.DictReader(f, fields, delimeter=';')
        payment_data = []
        for row in reader:
            payment_data.append(row)
        return payment_data

```

## Выберем все уникальные компании

```python
def save_companies(data):
    processed = []
    unique_companies = []
    for row in data:
        if row['company'] not in processed:
            company = {"name": row["company"], "city": row["city"], "address": row["address"],
                       "phone": row['phone_company']}
            unique_companies.append(company)
            processed.append(company["name"])
    db_session.bulk_insert_mappings(Company, unique_companies, return_defaults=True)
    db_session.commit()
    return unique_companies
...

if __name__ =="__main__":
    all_data = read_csv('salary.csv')
    companies = save_companies(all_data)
    print(companies)
```

## Выбираем всех уникальрных сотруднков.

```python
def get_company_by_id(companies, company_name):
    for company in companies:
        if company["name"] == company_name:
            return company["id"]


# Сохранение сотрудников
def save_employees(data, companies):
    processed = []
    unique_employees = []
    for row in data:
        if row["phone_person"] not in processed:
            employee = {
                "name": row["name"],
                "job": row["job"],
                "phone": row["phone_person"],
                "email": row["email"],
                "date_of_birth": row["date_of_birth"],
                "company_id": get_company_by_id(companies, row["company"]),
            }
            unique_employees.append(employee)
            processed.append(employee["phone"])
    db_session.bulk_insert_mappings(Employee, unique_employees, return_defaults=True)
    db_session.commit()
    return unique_employees

...
# upgrade
if __name__ == "__main__":
    all_data = read_csv("salary.csv")
    companies = save_companies(all_data)
    employees = save_employees(all_data, companies)
    print(employees)

```

## Выбираем из всех них зарплаты

```python
# Получаем Сотрудника по id
def get_employee_by_id(employees, phone):
    for employee in employees:
        if employee["phone"] == phone:
            return employee["id"]

# Сохраняем зарплаты
def save_payments(data, employees):
    payments = []
    for row in data:
        payment = {"payment_date": row["payment_date"], "ammount": row["ammount"], "employee_id": get_employee_by_id(employees, row["phone_person"])}
        payments.append(payment)
    db_session.bulk_insert_mappings(Payment, payments)
    db_session.commit()

```

## Как получить данные?

Задача: Найти компанию по названию и вывести для неё всех сотрундников.

Решается задача несколькими способами.
1. Найти `Company`, затем получить всех `Employee` по `company_id`
2. Если вы раньше работали с БД, очевидный вариант сделать `join`
3. Использовать `relationship`  удобный механизм, который предоставляет SQLAlchemy для получения данных из связанных таблиц.

<b>Решение 1:</b>
Создадим `queries.py`

```python
from db import db_session
from models import Company, Employee


def employees_by_company(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    # Создаем список для сотрудников
    employee_list = []
    if company:
        for employee in Employee.query.filter(Employee.company_id == company.id):
            employee_list.append(f"{company.name} - {employee.name}")
    return employee_list


if __name__ == "__main__":
    print(employees_by_company("Россельхозбанк"))
```

Произведем замер данного подхода

```python
import time

...

if __name__ == "__main__":
    start = time.perf_counter()
    for _ im range (100):
        employees_by_company("Россельхозбанк")
    print(f"employees_by_company: {time.perf_counter() - start}")
```
<b>Решение 2:</b>

```python
...
# Второй 
def employees_by_company_joined(company_name):
    query = db_session.query(Employee, Company).join(
        Company, Employee.company_id == Company.id
        ).filter(Company.name == company_name)
    employee_list = []

    for employee, company in query:
        employee_list.append(f"{company.name} - {employee.name}")
    return employee_list

...
if __name__ == '__main__':
    start = time.perf_counter()

    for _ in range(100):
        employees_by_company_joined("Россельхозбанк")
    print(f"employees_by_company: {time.perf_counter() - start}")
```
## 3 Вариант решения исп Relations

Relation - Удобный механизм, который SQLAlche,y предоставляет для запросов из связанных таблиц. Специальные поля которы делают за нас эти запросы.

Модифицируем `models.py`

```python
from sqlalchemy.orm import relationship

class Company(Base):
    ...
    employees = relationship("Employee")

class Employee(Base):
    ...
    company = relationship("Company")
```

Вносим изменения в `queries.py`

```python

# 3  вариант - relationship
def employees_by_company_relation(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    # Создаем список для сотрудников
    employee_list = []
    if company:
        for employee in company.employees:
            employee_list.append(f"{company.name} - {employee.name}")
    return employee_list


```
Результат выполнения не оч.
Добавим в `models.py`

```python
...

class Company(Base):
    ...
    employees = relationship("Employee", lazy="joined")

class Employee(Base):
    ...
    company = relationship("Company")

```

## Почему это важно.
Одна из ошибок - 1+N запросы, когда мы в цикле обращаемся к relationship'ам, не задумываяь, что это бомбардирует базу дополнительными запросами.

Возмем пример - нужно получить из базы платежи за определенный период, и для каждого платежа вывести сотрудника и компанию.

Создадим файл `bad_query.py`