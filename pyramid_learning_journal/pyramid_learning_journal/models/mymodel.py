from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    DateTime
)

from .meta import Base


class Journal(Base):
    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    posted_date = Column(DateTime)
    body = Column(Unicode)


Index('my_index', Journal.id, unique=True, mysql_length=255)
