from database import SQLClass
from sqlalchemy.orm import declarative_base

sql = SQLClass()
Base = declarative_base()
Base.metadata.reflect(sql._engine)

class Categories(Base):
    __table__ = Base.metadata.tables['categories']
    def __repr__(self):
        return self.category_name