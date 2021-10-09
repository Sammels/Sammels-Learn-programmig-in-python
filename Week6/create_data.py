import csv
import random
from datetime import date

# Импортируем фейкер
from faker import Faker

fake = Faker("ru_RU")

# Функция Фиктивная компания
def fake_companies(num_rows=10) -> list:
    companies = []
    for _ in range(num_rows):
        companies.append(
            [
                fake.large_company(),
                fake.city_name(),
                fake.street_address(),
                fake.phone_number(),
            ]
        )
    return companies


# Функция Фиктивный работник
def fake_employees(companies, num_rows=10) -> list:
    employees = []
    # Делаем цикл по компаниям, и в цикле перебираем 10 списков
    for company in companies:
        # Для каждого цикла делаем еще несколько циклов
        for _ in range(num_rows):
            employee = [
                fake.name(),
                fake.job(),
                fake.phone_number(),
                fake.free_email(),
                fake.date_of_birth(minimum_age=18, maximum_age=70),
            ]
            employees.append(company + employee)
    return employees


# Функция фиктивных выплат
def fake_payment(employees) -> list:
    payments = []
    for employee in employees:
        for month in range(1, 13):
            payment_date = date(2020, month, random.randint(10, 28))
            ammount = random.randint(20000, 200000)
            payment = [payment_date, ammount]
            payments.append(employee + payment)
    return payments


# Функция для записи csv файла
def generate_data(payments) -> "csv file":
    with open("salary.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        for payment in payments:
            writer.writerow(payment)


if __name__ == "__main__":
    companies = fake_companies()
    employees = fake_employees(companies)
    payments = fake_payment(employees)
    generate_data(payments)
