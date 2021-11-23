from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db import Base, engine

# Модель, класс Компания
class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    address = Column(String)
    phone = Column(String)
    year_founded = Column(Integer)

    employees = relationship("Employee", lazy="joined")

    def __repr__(self):
        return f"Company id: {self.id}, name: {self.name}"


# Модель, класс Сотрудник
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey(Company.id), index=True, nullable=False)
    name = Column(String)
    job = Column(String)
    phone = Column(String)
    email = Column(String)
    date_of_birth = Column(Date)

    company = relationship("Company")
    payments = relationship("Payment")

    def __repr__(self):
        return f"Employee id: {self.id}, name: {self.name}"


# Модель, класс Платеж
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), index=True, nullable=False)
    payment_date = Column(Date)
    ammount = Column(Integer)
    currency = Column(String, nullable=False)
    employee = relationship("Employee", lazy="joined")

    def __repr__(self):
        return f"Payment id: {self.id}, date: {self.payment_date}"


# Модель, класс Проекты
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey(Company.id), index=True, nullable=False)
    name = Column(String)
    company = relationship("Company", lazy="joined")
    employees = relationship("ProjectEmployee")

    def __repr__(self):
        return f"Project id {self.id} name: {self.name}"


# Модель, класс Работник на проекте
class ProjectEmployee(Base):
    __tablename__ = "projects_employees"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), index=True, nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id), index=True, nullable=False)
    date_start = Column(Date)
    date_end = Column(Date)
    project = relationship("Project", lazy="joined")
    employee = relationship("Employee", lazy="joined")

    def __repr__(self):
        return f"ProjectEmployee project: {self.project_id} employee: {self.employee}"


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
