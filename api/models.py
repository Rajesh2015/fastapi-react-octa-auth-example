from sqlalchemy import Column, Integer, String
from .database import Base

"""Create models, see https://fastapi.tiangolo.com/tutorial/sql-databases/"""


class FruitsModel(Base):
    __tablename__ = 'fruits'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(String())

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Fruit {self.name}>"
