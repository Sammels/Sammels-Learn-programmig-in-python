from datetime import date
from models import Payment, Employee
import time

from sqlalchemy.orm import joinedload


def employees_and_payments():
    employee_list = []
    for payment in Payment.query.filter(Payment.payment_date > date(2020, 6, 1)):
        employee_list.append(
            f"{payment.employee.company.name} - {payment.employee.name} - {payment.ammount}"
            )
    return employee_list

def employees_and_payments_joined():
    employee_list = []
    query = Payment.query.options(
        joinedload(Payment.employee).joinedload(Employee.company)
        ).filter(Payment.payment_date > date(2020, 6, 1))
    for payment in query:
        employee_list.append(
            f"{payment.employee.company.name} - {payment.employee.name} - {payment.ammount}"
            )
    return employee_list


if __name__ == "__main__":
    # start = time.perf_counter()
    # for _ in range(10):
    #     employees_and_payments()
    # print(f"employees_and_payments: {time.perf_counter() - start}")

    start = time.perf_counter()
    for _ in range(10):
        employees_and_payments_joined()
    print(f"employees_and_payments_joined: {time.perf_counter() - start}")