
#from functools import wraps

"""
def prefill_args():
    def get(func):
        print(func.__name__)
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(args, kwargs)
            result = func(*args, **kwargs)
            return result
        return wrapper
    return get
"""

class MethodView(object):
     from typing import Optional
     from fastapi import Request

     @classmethod
     #async def as_view(cls):
     async def as_view(cls, request: Request, url_key: Optional[str] = None, kwargs2: Optional[str] = None):
        kwargs = {"url_key":url_key, "kwargs2":kwargs2}
        method = request.method.lower()
        exec(f'from view import {cls.__name__}')
        instance = eval(f"{cls.__name__}()")
        #print("invoking")
        #print(vars())
        #return eval(f"{cls.__name__}.get.__call__()")
        #yield eval(f"instance.{method}(request, **kwargs)")
        #return eval(f"instance.{method}(request, **kwargs)")
        return await eval(f"instance.{method}(request, **kwargs)")
     