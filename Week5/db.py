# Файл скопирован из week4
from settings import login, passwd, host, port, DN_name

from sqlalchemy import create_engine

# Декларатифная форма работы с моделями
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

connect = f"postgresql://{login}:{passwd}@{host}:{port}/{DN_name}"

engine = create_engine(connect, pool_pre_ping=True)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property() 