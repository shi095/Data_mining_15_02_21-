from sqlalchemy.ext.declarative import declarative_base # образует связи
from sqlalchemy.orm import relationship # виртуальная связь

from sqlalchemy import Column, Integer, String, ForeingKey, Table

Base = declarative_base()

class IdMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)

class NameMixin:
    name = Column(String, nullable=False)

class UrlMixin:
    url = Column(String, nullable=False, unique=True)


class Post(Base, IdMixin, UrlMixin): # наследуюем все атрибуты Вase
    __tablename__  = 'post' # имя таблицы
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id")) #физическая связь
    author = relationship("Author")

class Author(Base, IdMixin, NameMixin, UrlMixin):
    __tablename__  = 'author' # имя таблицы
    name = Column(String, nullable=False)


class Tag(Base, IdMixin, NameMixin, UrlMixin):
    __tablename__  = 'tag' # имя таблицы
    name = Column(String, nullable=False)

