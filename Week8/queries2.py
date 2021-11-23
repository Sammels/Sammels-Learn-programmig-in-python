import time

from models import Employee


if __name__ == "__main__":
    start = time.perf_counter()
    for _ in range(10):
        Employee.query.filter(Employee.job == "Дипломат").all()
    print(f"{time.perf_counter() - start}")
