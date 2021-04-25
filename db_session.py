import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

# Пытался добавить в проект базу данных, чтобы в ней хранились оценки сайта. Но SQLstudio перестал работать.
# Не открывал базы данных и не создавал их. Я переустанавливал его но не помогло. Я создал бд, но не могу открыть и посмотреть ее
Base = dec.declarative_base()
engine = sqlalchemy.create_engine('sqlite:///review.db')
Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'review'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)