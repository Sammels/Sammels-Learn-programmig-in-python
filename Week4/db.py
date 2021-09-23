# Импортим необходимое для работы SQLAlchemy
# Для безопасности выводим от сюда пассворды и прочее
from settings import login, passwd, host, port, DN_name

from sqlalchemy import create_engine

# Для исп SQLAlch в декларат. форм. с моделями.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

connect = f"postgresql://{login}:{passwd}@{host}:{port}/{DN_name}"

engine = create_engine(connect, pool_pre_ping=True)
db_session = scoped_session(sessionmaker(bind=engine))

# Все модели будут наследоваться от Base
Base = declarative_base()
# Это для того, чтобы использовать на пряму модель
Base.query = db_session.query_property()
