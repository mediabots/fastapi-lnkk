#import asyncio
#import psycopg

class SqlUoW(object):
    '''
    A "Driver" for handling SQL statements. Supports ORM too.  
    methods:
        __init__(self, tenant)
        __enter__(self)
        __exit__(self, *args)
    eg, sql = Sql(); with sql:sql.session.execute(".....");

    '''
    def __init__(self, tenant):
        from app import app

        #self.tenant = tenant
        self.session = None
        self.asession = None
        self.session_factory = app.config[f'sql_session_{tenant}']
        self.async_session_factory = app.config[f'async_sql_session_{tenant}']
        #self.session_factory = app.config.get(f'sql_session_{tenant}', app.config['db_session_global'])
    
    
    # async def __call__(self, scope, receive, send):
    #     await self.app(scope, receive, send)
    

    def __enter__(self):
        from sqlalchemy.orm import scoped_session

        self.session  = scoped_session(self.session_factory)
    
    def __exit__(self, *args):
        ##super().__exit__(*args)
        self.session.close()
        self.session.remove()

    async def __aenter__(self):
        import asyncio
        from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession

        try:
            self.asession  = async_scoped_session(self.async_session_factory, asyncio.current_task)
            #self.asession  = self.async_session_factory()
        except:
            pass
            #await self.asession.close()
            #await self.asession.rollback()
            #await self.asession.close_all()
            await self.asession.remove()
            #self.asession.close()
            #self.asession.remove()
            #asyncio.shield(self.asession.close())
            #psycopg.AsyncConnection.close(self.asession)

    #async def __aexit__(self, exc_type, exc, tb):
    async def __aexit__(self, *args):
        ##super().__exit__(*args)
        #await self.asession.close()
        #await self.asession.rollback()
        #await self.asession.close_all()
        await self.asession.remove()
        #self.asession.close()
        #self.asession.remove()
        #asyncio.shield(self.asession.close())
        #psycopg.AsyncConnection.close(self.asession)

#from contextlib import contextmanager

# @contextmanager
# def session_scope() -> Session:
#     """Provide a transactional scope around a series of operations."""
#     session = session_maker()  # create session from SQLAlchemy sessionmaker
#     try:
#         yield session
#         session.commit()
#     except:
#         session.rollback()
#         raise