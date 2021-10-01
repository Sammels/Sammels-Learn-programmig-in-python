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

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)