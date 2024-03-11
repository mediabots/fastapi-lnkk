from sqlalchemy import create_engine, func, or_, and_, MetaData, Table, text, schema
from sqlalchemy.orm import scoped_session, sessionmaker, Session, declarative_base, registry, relationship
from sqlalchemy.sql import text as txt # same as from sqlalchemy import text
import os
import numpy as np
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, \
async_scoped_session
import asyncio
from sqlalchemy.pool import NullPool

# engine = create_engine('', echo=True)
# mapper_registry = registry()
# Base = mapper_registry.generate_base()

class SQLClass(object):
    def __init__(self) -> None:
        self._dbuser = os.environ.get('DB_USERNAME','root')
        self._dbpswd = os.environ.get('DB_PASSWORD')
        self._dbhost = os.environ.get('DB_HOST','localhost')
        self._dbport = os.environ.get('DB_PORT','3306')
        self._dbanme = os.environ.get('DB_NAME','mysql')
        self._url = f"postgresql+psycopg://{self._dbuser}:{self._dbpswd}@{self._dbhost}:{self._dbport}/{self._dbanme}"
        self._engine = create_engine(f"mysql+mysqlconnector://{self._dbuser}:{self._dbpswd}@{self._dbhost}:{self._dbport}/{self._dbanme}")
        self.async_engine = create_async_engine(self._url, poolclass=NullPool)
        self._meta = MetaData() 
        self._meta.reflect(self._engine)

    def insert_into_table(self, table_name, *args, **kwargs):
        #values = list(*args)
        TargetedTable = Table(table_name, self._meta) 
        # IMP: for parsing
        # [column for column in TargetedTable.columns]
        # column.key, column.type, column.nullable, column.primary_key, column.table.key
        # 
        insert_statement = TargetedTable.insert()
        with self._engine.connect() as conn:
            #conn.execute(insert_statement, values) #  Execute many (or Bulk insert)
            conn.execute(insert_statement, args) #  Execute many (or Bulk insert)
            #conn.commit() # Note: .commit() is N.A.
        # async way
        #async with self.async_engine.begin() as conn:
            #await conn.execute(text(f'insert into {table_name} values(args)'))
            # OR
            #await conn.execute(insert_statement, args)
        # verify
        with self._engine.connect() as conn:
            print(conn.execute(text(f'select * from {table_name}')).all())
        # verify async way
        #async with self.async_engine.connect() as conn:
        #    result = await conn.execute(text(f'select * from {table_name}'))
        #    print(result.fetchall())

    def insert_into_table_using_session(self, ModelClass, *args, **kwargs):
        #print("**********\n\t",type(args),args)
        #import pdb
        #pdb.set_trace()
        Async_session = async_scoped_session(async_sessionmaker(bind=self.async_engine), asyncio.current_task)
        Session = scoped_session(sessionmaker(bind=self._engine))
        with Session.connection() as conn:
            # - single record insert
            #new_record = ModelClass(**kwargs)
            #Session.add(new_record)
            #Session.commit()
            ##new_record = ModelClass(category_name=kwargs['category_name'],category_description=kwargs['category_description'])
            # - multiple record insert
            #[Session.add(ModelClass(**arg)) for arg in args]
            # OR 
            # np array implementation (vectorization)
            arr = np.array(args)
            np.apply_along_axis(lambda l: list(map(lambda idx: Session.add(ModelClass(**l[idx])), range(len(l)))), axis=0, arr=arr)
            Session.commit()
        # commit async way
        #async with Async_session() as session:
        #    await session.execute(text(f'insert into test(num) values({list(args)})'))
        #    await session.commit()
        # verify
        Session = scoped_session(sessionmaker(bind=self._engine))
        with Session.connection() as conn:
             #id(Session)
             print(Session.query(ModelClass).all())
        # verify async way
        #Async_session = async_scoped_session(async_sessionmaker(bind=self.async_engine), asyncio.current_task)
        #async with Async_session() as session:
        #    result = await session.execute(text('select * from test'))
        #    print(result.fetchall())


if __name__ == '__main__':
    from models import Categories
    sql = SQLClass()
    # Note: don't forget to set local env variables through below command(for linux)
    # export DB_NAME="testdb" DB_PORT="3307" DB_PASSWORD="12345678"
    # - single record insert (through session)
    #sql.insert_into_table_using_session(Categories,**{"category_name":"cat_12", "category_description":"..."})
    # - bulk record insert (through session)
    sql.insert_into_table_using_session(Categories,*[{"category_name":"cat_29", "category_description":""}, {"category_name":"cat_30", "category_description":None}])
    # - bulk record insert 
    #sql.insert_into_table("categories",*[{"category_name":"cat_17", "category_description":"..."}, {"category_name":"cat_18", "category_description":"..."}]) # insert mutiple values
