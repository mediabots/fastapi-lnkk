#from sqlalchemy.exc import SQLAlchemyError, StatementError, OperationalError, IntegrityError, DatabaseError, DataError
#from sqlalchemy import Table, Column, String, Integer, Text, MetaData, create_engine, func, \
#    and_, text, schema
#import pdb
import starlette.status as status
from fastapi import Request
from typing import Optional
from controller.blueprint import blp_post
from utils.decorators import get_uow, get_uow_cbv
from view.base import MethodView

"""
def ping():
    return "pong"

@blp_post.get("/ping/{username:str}")
def ping(username):
    print(username)
    return "pong"
"""

@blp_post.get("/ping2")
async def pingnew():
    return "pong 2"

# ------- ClassBasedView
    
class Ping():
    async def get():
        return "pong"
    
    async def post():
        return "post pong"
    
class PostCBV():
    @get_uow_cbv(units=["sql"])
    async def get(request: Request, url_key: str, sql: Optional[str] = None):
        from fastapi.responses import RedirectResponse
        from fastapi import HTTPException
        from service import post_retrievation, post_retrievation_prep_stmt
        #from app import app

        #username = request.headers.get("tenant")
        #sql = app.config[f"sql_uow_{username}"]
        #print("invoked", username)
        code, url = await post_retrievation(sql, url_key)
        #code, url = await post_retrievation_prep_stmt(sql, url_key)
        if not code:
            return url
            return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
        #return {"message": "redirect not found", "code":404}
        raise HTTPException(status_code=404, detail="redirect not found")

    async def delete(*args, **kwargs):
        raise NotImplementedError("delete method is not imeplemented yet!")
    
    async def put(*args, **kwargs):
        raise NotImplementedError("put method is not imeplemented yet!")


# ------- MethodView

# class Ping(MethodView):
#     #@blp_post.get("/ping")
#     async def get(self, *args, **kwargs):
#         return "pong"
    
#     async def post(self, *args, **kwargs):
#         return "post pong"
     
class Post(MethodView):
    @get_uow(units=["sql"])
    async def get(self, request, *args, url_key, **kwargs):
        from fastapi.responses import RedirectResponse
        from fastapi import HTTPException
        from service import post_retrievation
        #from app import app

        #username = request.headers.get("tenant")
        #sql = app.config[f"sql_uow_{username}"]
        #print("invoked", username)
        code, url = await post_retrievation(kwargs['sql'], url_key)
        if not code:
            return url
            return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
        #return {"message": "redirect not found", "code":404}
        raise HTTPException(status_code=404, detail="redirect not found")

    async def delete(self, *args, **kwargs):
        raise NotImplementedError("delete method is not imeplemented yet!")
    
    async def put(self, *args, **kwargs):
        raise NotImplementedError("put method is not imeplemented yet!")


class Posts(MethodView):
    @get_uow(units=['sql'])
    def post(self, username, **kwargs):
        '''
        to test this using curl - command:
        curl -i -X POST "http://tenant1.lnkk.in:8080/posts" --header "Content-Type: application/json" --data '{"redirect_url":"https://www.youtube.com/watch?v=p3ISf5PpGYS_1","url_key":"uycgpXYsje-i-000"}'
        curl -i -X POST "http://tenant1.lnkk.in:8080/posts" --header "Content-Type: application/json" --data '{"redirect_url":"https://www.youtube.com/watch?v=p3ISf5PpGYS_1"}'
        '''
        from service import post_creation
        
        #bulk = True if request.args.get("bulk") else False
        code, message = post_creation(username, kwargs['sql'], request.get_json())
        if not code:
            return message, 201
        return message, 409
    

class PostsBulk(MethodView):
    @get_uow(units=['sql'])
    def post(self, username, **kwargs):
        '''
        to test this using curl - command:
        curl -i -X POST "http://tenant1.lnkk.in:8080/posts/bulk" --header "Content-Type: application/json" --data '[{"redirect_url":"https://www.youtube.com/watch?v=p3ISf5PpGYS_1"},{"redirect_url":"https://www.youtube.com/watch?v=p3ISf5PpGYS_2"}]'
        '''
        from service import post_bulk_creation
        
        code, message = post_bulk_creation(username, kwargs['sql'], request.get_json())
        if not code:
            return message, 201
        return message, 409
    
