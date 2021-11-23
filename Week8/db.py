# Файл скопирован из week4
from settings import login, passwd, host, port, DN_name
from sqlalchemy.engine import Engine

from sqlalchemy import create_engine, event

# Декларатифная форма работы с моделями
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

connect = f"postgresql://{login}:{passwd}@{host}:{port}/{DN_name}"

engine = create_engine(connect, pool_pre_ping=True)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


SQL_DEBUG = True

if SQL_DEBUG:

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", []).append(time.perf_counter())
        print(f"Делаем запрос: {statement}")

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):

        total = time.perf_counter() - conn.info["query_start_time"].pop(-1)
        print(f"Время выполнения: {total}")
