# 8 Неделя курса. 

Задачи:
1. Повторить пройденное
2. Понять, как работает Веб и БД

## БД 7-8 неделя.
1. Связь многие-ко-многим
2. Создадим новые модели
3. Создадим список проектов для загрузки
4. Напишем код для загрузки проектов в БД
5. Добавим обработку ошибок
6. Делаем более сложные запросы

### 1. Связь многие-ко-многим.
1-ко-многим -> на каждого сотрудника приходится несолько выплат.
Более сложный случай: 
<p>Есть проекты, прчем над каждым проектом в разное время могут работать разные сотрудники. Это связь <code>many-to-many</code> или Многие-ко-многим.
</p>

<p>Используем файлы <code>db.py, models.py</code> и данные в базе из прошлого урока.</p>

![Схема БД_1_к_многим.png]

Связь многий ко многим, это связь через промежуточную таблицу.

### 2. Создание новой модели.

Добавим модель.

Понадобится 2 новые модели: - `Project`

```python
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey(Company.id), index=Trrue, nullable=False)
    name - Column(String)
    company = relationship("Company", lazy="joined")
    emplooyees = relationship("ProjectEmployee")

    def __repr__(self):
        return f"Project id: {self.id} name: {self.name}"
```

модель - `ProjectEmployee`
```python
class ProjectEmployee(Base):
    __tableame__ = "project_employees"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), index=True, nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id), index=True, nullable=False)
    date_start = Column(Date)
    date_end = Column(Date)
    project = relationship("Project", lazy="joined")
    employee = relationship("Employee", lazy="joined")

    def __repr__(self):
        return f"ProjectEmployee {self.project_id} employee: {self.employee}"
```

### 3. Создание проектов для загрузки

<p>1. Генерация csv, потом загрузка этих данных в бд. Для этого могут быть файлы csv, excel, json или API внешних систем.</p>

`Создадим файл create_data.py`

```python
import csv

def generate_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        writer = csv.write(f, delimiter=";")
        for row in data:
            write.writerow(row)

if __name_ == "__main__":
    generate_data()
```

<p>Создадим функцию, которая будет давать случайное название проекта.</p>

```python
import random

def get_project_name():
    projects = ["Ребрендинг", "Разработка CRM", "Обслуживание 1С", "Разработка сайта", "Опрос покупателей", "Запук коллцентра", "Модернизация wifi-сети", "Проведение исследований", "Дизайн сайта", "Разработка моб. приложения", "Дизайн буклетов", "Аудит информационной безопасности", "Обучение сотрудников"]

    return random.choice(projects)
```

<h1>Создадим список проектов.</h1>
<p>Произведем перебор в цикле компаний и их сотрудников и для каждого сотрудника сгенерируем список проектов.</p>

```python
from models import Company

def fake_project_list() -> list:
    """Фиктивныв Данные"""
    data = []
    companies = Company.query.all()
    for company in companies:
        for employee in company.employees:
            data += projects_for_employee(company.id, employee.id)
    return data
```

```python
def projects_for_employee(company_id, employee_id) -> list:
    projects = []
    for month in range(1, 13):
        date_start = date(2021, month, random.randint(1, 10))
        date_end = date_start + timedelta(days=random.randint(5, 20))
        project = [get_project_name(), company_id, employee_id, date_start, date_end]
        projects.append(project)
    return projects


```
Обший вид файла
```python
import csv
from datetime import date, timedelta
import random
from models import Company


def get_project_name():
    projects = [
        "Ребрендинг",
        "Разработка CRM",
        "Обслуживание 1С",
        "Разработка сайта",
        "Опрос покупателей",
        "Запук коллцентра",
        "Модернизация wifi-сети",
        "Проведение исследований",
        "Дизайн сайта",
        "Разработка моб. приложения",
        "Дизайн буклетов",
        "Аудит информационной безопасности",
        "Обучение сотрудников",
    ]

    return random.choice(projects)


def projects_for_employee(company_id, employee_id) -> list:
    projects = []
    for month in range(1, 13):
        date_start = date(2021, month, random.randint(1, 10))
        date_end = date_start + timedelta(days=random.randint(5, 20))
        project = [get_project_name(), company_id, employee_id, date_start, date_end]
        projects.append(project)
    return projects


def fake_project_list() -> list:
    """Фиктивныв Данные"""
    data = []
    companies = Company.query.all()
    for company in companies:
        for employee in company.employees:
            data += projects_for_employee(company.id, employee.id)
    return data


def generate_data(data, filename) -> "csv":
    with open(filename, "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    generate_data(fake_project_list(), "projects.csv")

```

### 4. Напишем код для загрузки проектов в базу данных.
----------------------------------------------------

<h1>Загрузка данных:</h1>
1. Прочитаем все строоки из csv-файла в список словарей
2. Для каждой строки создадим проект и связь проект-сотрудник.

`loader.py` 

```python
import csv
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from db import db_session
from models import Project, ProjectEmployee


def prepare_date(row):
    row["company_id"] = int(row["company_id"])
    row["employee_id"] = int(row["employee_id"])
    row["date_start"] = datetime.strptime(row["date_start"], "%Y-%m-%d")
    row["date_end"] = datetime.strptime(row["date_end"], "%Y-%m-%d")
    return row


def get_or_create_project(project_name, company_id):
    project = Project.query.filter(
        Project.name == project_name, Project.company_id == company_id
    ).first()
    if not project:
        project = Project(name=project_name, company_id=company_id)
        db_session.add(project)
        try:
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise
    return project


def create_project_employee(row, project):
    project_employee = ProjectEmployee(
        employee_id=row["employee_id"],
        project_id=project.id,
        date_start=row["date_start"],
        date_end=row["date_end"],
    )
    db_session.add(project_employee)
    try:
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        raise

def process_row(row):
    row = prepare_date(row)
    project = get_or_create_project(row["project_name"], row["company_id"])
    create_project_employee(row, project)

def print_error(row_num, error_text, exception):
    print(f"Ошибка на строке {row_num}")
    print(error_text.format(exception))
    print('-' * 100)



def read_csv(filename):
    with open(filename, "r", encoding="utf-8") as f:
        fields = ["project_name", "company_id", "employee_id", "date_start", "date_end"]
        reader = csv.DictReader(f, fields, delimiter=";")
        for row_num, row in enumerate(reader, start=1):
            try:
                process_row(row)
            except(TypeError, ValueError) as e:
                print_error(row_num,"Неправильный формат данных на строке {}", e)
            except SQLAlchemyError as e:
                print_error(row_num, "Ошибка целостности данных данных {}", e)



if __name__ == "__main__":
    read_csv("projects.csv")

```

### 5. Добавим Обработку ошибок
----------------------------------------------------
<h1>Подходы к обработке ошибок.</h1>

* Подход `все-или-ничего` - либо успешно загружаем все данные, либо отменяем загрузку полностью. Реализуется через `транзакцию`
* Подход `грузим-все-что-можем` - встретив ошибку, пропускается строка и сообщаем об этои пользователю.

Обработку ошибок смотреть выше.


### 6. Более сложные запросы к БД
----------------------------------------------------
<p>Получим список сотрудников по проектам компании и узнаем, сколько дней каждый из сотрудников работал над проектом:</p>

`queries.py`

```python
from models import Project, Company


def company_projects_employees(company_name):
    query = Project.query.join(Project.company, Project.employees).filter(
        Company.name == company_name
    )

    for project in query:
        print("-" * 20)
        print(project.name)
        for project_employee in project.employees:
            delta = (project_employee.date_end - project_employee.date_start).days
            print(f"{project_employee.employee.name} -- {delta} день")


if __name__ == "__main__":
    company_projects_employees("Трансмашхолдинг")
```

<p>Посчитаем суммарное время работы над каждым проектом. И сколько всего над ним работали сотрудники за все время.</p>

```python
from sqlalchemy import func
from db import db_session
from models import ..., ProjectEmployee
...
def project_time_total(company_name):
    query = db_session.query(
        Project.name,
        func.sum(ProjectEmployee.date_end - ProjectEmployee.date_start)
    ).join(
        Project.company, Project.employees
        ).filter(Company.name == company_name).group_by(Project.name)

    for row in query:
        print(f"{row[0]} -- {row[1]}")


...
```
<p>Итоговый подсчет сколко всего сотруник проработал в сумме над проектом.</p>

```python
from models import Project, Company, ProjectEmployee, Employee


def project_employees_time_total(company_name):
    query = (
        db_session.query(
            Project.name,
            Employee.name,
            func.sum(ProjectEmployee.date_end - ProjectEmployee.date_start),
        )
        .join(Project.company, Project.employees, ProjectEmployee.employee)
        .filter(Company.name == company_name)
        .group_by(Project.name, Employee.name)
    )

    for project_name, employee_name, delta in query:
        print(f"{project_name} -- {employee_name} -- {delta}")

```

----------------------------------------------

## БД 8 неделя
1. Что такое миграции
2. Настраиваем Alembic и делаем первую миграцию
3. Меняем тип существующего поля
4. Добавляем обязательное поле
5. Знакомимся с индексами
6. Профилируем запросы

### 1. Что такое миграции.
----------------------------------------------------

<p>Базы данных: миграции и индексы</p>

Добавление данных в полуавтомотическом режиме  в БД

Установим библиотеку `Alembic`

и выполним `pip3 install -r requirements.txt`

### 2. Настраиваем Alembic и делаем первую миграцию
----------------------------------------------------


1. Для инициализации необходимо выполнить `alembic init migrations`
и в автоматически появится папка `migrations` и несколько новых файлов.

2. Далее ищем в файле `alembic.ini` строку `sqlalchemy.url`, которая показывает как alembic-у соединятся к нашей базе.

3. В папке `migrations` найдем `env.py`
и добавляем
```python
import os, sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
```

4. Далее нужно добавить модели в этот же файл.
```python
from models import Base

# Найти и заменить
target_metadata = Base.metadata
```
`Base.metadata` - Это данные о том как будут работать наши модели.

5. Пробуем сделать миграцию.

Добавляем в `models.py` новое поле `year_founded=Column(String)`

Для запуска миграции необходимо:

`alembic revision --autogenerate -m "Added year_founded"`

Применить upgrade 
`alembic upgrade head`

### 3. Меняем тип существующего поля
--------------------------------------

Меняем в models.py -> Company -> year_founded = Column(Integer)

Прописываем в консоли 
`alembic revision --autogenerate -m "Changed Company.year_founded type"`

Добавим возможность смены колонки в alembic 
в `alembic.ini` найдем `context_configure`  и добавим `compare_type = True,`
Дважды.

Далее в файл последнеей версии миграции добавить
```python
def upgrade():
    ...
    postgresql_using="year_founded::integer")
```

и потом 
`alembic upgrade head`

### 4. Добавляем обязательное поле

в `models.py`
в class Payment добавим `currency = Column(String, nullable=False)`

Создадим новую миграцию.
`alembic revision --autogenerate -m "add Payment.currency type"`

Делаем изменения в  версии миграции
```python
    op.add_column('payments', sa.Column('currency', sa.String(), nullable=True))
    op.execute("UPDATE payments SET currency='RUB'")
    op.alter_column('payments', 'currency', nullable=False)
```

Отмена миграции
Копируем 46c7f516ecae

и печатаемм 
`alembic downgrade 46c7f516ecae`

### 5. Знакомимся с индексами

Данных становится больше.

Выполним запрос `Employee.query.filter(Employee.job == "Сварщик").all()`

```python
import time

from models import Employee


if __name__ == "__main__":
    start = time.perf_counter()
    for _ in range(10):
        Employee.query.filter(Employee.job == "Дипломат").all()
    print(f"{time.perf_counter() - start}")

```

Индексы добавляют базе данных работы при добавлении данных.
Есть книга <b>Use The Index, Luke</b>

### 6. Профилируем SQL-запросы.
Чем чаще мы будем работать с базой данных, тем чаще нужно будет смотреть, что за sql-запрос сгенерировал наш ORM.

Чтобы посмотреть запрос
`query= Employee.query.filter(Employee.job == "Дипломат")`

В sqlalchemy есть возможность подписаться на события.

В `db.py`  внесем изменения

```python
import time
from sqlalchemy.engine import Engine
...

SQL_DEBUG = True

if SQL_DEBUG:
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement,
                              parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.perf_counter())
        print(f"Делаем запрос: {statement}")

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement,
                             parameters, context, executemany):

        total = time.perf_counter() - conn.info['query_start_time'].pop(-1)
        print(f"Время выполнения: {total}")
```

- в `queries2.py`
Добавим
```python
from models import Employee


if __name__ == "__main__":
    Employee.query.filter(Employee.job == "Дипломат")
    print(query.first())

```

Улучшенная версия
```python
...

if __name__ == "__main__":
    employee = Employee.query.first
    print(employee.company.name)
```

Изменения в models
```pythom
class Employee(Base):

...

company = relationship("Company", lazy="joined")
```

