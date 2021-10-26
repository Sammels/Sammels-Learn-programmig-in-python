import time
from db import db_session
from models import Company, Employee

# Решение задачи по варианту 1
def employees_by_company(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    # Создаем список для сотрудников
    employee_list = []
    if company:
        for employee in Employee.query.filter(Employee.company_id == company.id):
            employee_list.append(f"{company.name} - {employee.name}")
    return employee_list

# Второй 
def employees_by_company_joined(company_name):
    query = db_session.query(Employee, Company).join(
        Company, Employee.company_id == Company.id
        ).filter(Company.name == company_name)
    employee_list = []
    
    for employee, company in query:
        employee_list.append(f"{company.name} - {employee.name}")
    return employee_list

# 3  вариант - relationship
def employees_by_company_relation(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    # Создаем список для сотрудников
    employee_list = []
    if company:
        for employee in company.employees:
            employee_list.append(f"{company.name} - {employee.name}")
    return employee_list


if __name__ == "__main__":
    # start = time.perf_counter()

    # for _ in range(100):
    #     employees_by_company("Россельхозбанк")
    # print(f"employees_by_company: {time.perf_counter() - start}")
    # Вариант 2
    # start = time.perf_counter()

    # for _ in range(100):
    #     employees_by_company_joined("Россельхозбанк")
    # print(f"employees_by_company: {time.perf_counter() - start}")
    
    start = time.perf_counter()
    for _ in range(100):
        employees_by_company_relation("Россельхозбанк")
    print(f"employees_by_company_relation: {time.perf_counter() - start}")
    