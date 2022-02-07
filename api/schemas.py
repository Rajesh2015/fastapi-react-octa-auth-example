from pydantic import BaseModel

"""Create database schemas, see https://fastapi.tiangolo.com/tutorial/sql-databases/"""

class Fruits(BaseModel):
    name: str
    price: str
