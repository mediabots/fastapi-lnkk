#import os
#import psycopg
#import asyncpg
#import aiomysql
#import asyncmy
#import mysql.connector

#import sqlalchemy
from sqlalchemy import Table, Column, String, Integer, Text, MetaData, create_engine, func, \
    and_, text, schema
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
##from sqlalchemy.ext.declarative import declarative_base # to be depricated
from sqlalchemy.pool import NullPool
from types import SimpleNamespace
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

def init_sql(app, config, engine_name):
    #from app import app

    tenants = eval(config['active']['tenants'])
    for tenant in tenants:
        sql_connection_pattern_url = config['sql'][f'{engine_name}_url']
        tenant_settings = SimpleNamespace(**config[tenant])
        args = [_ for _ in dir(tenant_settings) if not _.startswith("_") ]
        for arg in args:
            sql_connection_pattern_url = sql_connection_pattern_url.replace(arg, eval(f'tenant_settings.{arg}'))
        sql_connection_url = sql_connection_pattern_url
        #del sql_connection_pattern_url # @NR
        # ------- establishing sql connection
        engine = create_engine(sql_connection_url, poolclass=NullPool)
        async_engine = create_async_engine(sql_connection_url, poolclass=NullPool)
        app.config[f'sql_session_{tenant}'] = sessionmaker(bind=engine)
        app.config[f'async_sql_session_{tenant}'] = async_sessionmaker(bind=async_engine)
        # ------- fetching data models
        vars()[f"Base{tenant.title()}"] = declarative_base()
        #vars()[f"Base{tenant.title()}"].metadata.reflect(engine)
        # OR
        #vars()[f"Base{tenant.title()}"].metadata.bind = engine
        vars()[f"Base{tenant.title()}"].metadata.bind = async_engine
        vars()[f"meta_{tenant.title()}"] = MetaData() 
        #vars()[f"meta_{tenant.title()}"].reflect(engine)
        # OR
        #vars()[f"meta_{tenant.title()}"].bind = engine
        vars()[f"meta_{tenant.title()}"].bind = async_engine
        app.config[f"Base{tenant.title()}"] = vars()[f"Base{tenant.title()}"]
        app.config[f"meta_{tenant.title()}"] = vars()[f"meta_{tenant.title()}"]
        # ------- configuring sqluow
        unt_name = "SqlUoW"
        exec(f'from utils import {unt_name}')
        app.config[f"sql_uow_{tenant}"] = eval(unt_name+f"('{tenant}')") 
    #return app

# '''Insert data into Table by insert operation'''
# UsersTable = Table('users', meta) # ,autoload_with=engine
# insert_statement_with_values = UsersTable.insert().values(email='abcde@email.com', password='12345678')
# # OR tuple obj
# #insert_statement_with_values = UsersTable.insert().values(('abcde@email.com','12345678'))
# # multiple insert with dict obj
# #insert_statement_with_values = UsersTable.insert().values([{'email':'abcdef@email.com','password':'12345678'},{'email':'abcdef@mail.com','password':'12345678'}])
# # Execute many
# insert_statement = UsersTable.insert()
# values = [{'email':'abc@gmail.com','password':'123456'},{'email':'abc@ymail.com','password':'123456'}]
# with engine.connect() as conn:
#     conn.execute(insert_statement_with_values)
#     # OR
#     #conn.execute(insert_statement, values) 
#     conn.commit()
# with engine.connect() as conn:
#     conn.execute(text("SELECT * from users")).fetchall()
# # create all tables
# # meta.create_all(engine)


# '''Query data and Insert data into Table by Session'''
# class Users(Base):
#     __table__ = Base.metadata.tables['users']
#     def __repr__(self):
#         return self.email
    
# # Session  = sessionmaker(bind=engine)
# # session = Session()
# session  = scoped_session(sessionmaker(bind=engine))
# #Session  = scoped_session(sessionmaker(bind=engine))
# ##session = Session()
# #with Session.connection() as conn:
# #  id(Session)
# #  Session.query(Users).all()
# # OR
# #conn = Session.connection() 
# #Session.query(Users).all()
# #conn.close()

# # session.expire_on_commit
# session.query(Users).all()
# new_user = Users(email="abc@noemail.com",password='1234')
# session.add(new_user)
# session.commit()
# session.query(Users).all()
