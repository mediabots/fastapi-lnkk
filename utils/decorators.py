from fastapi  import Request
from functools import wraps
from app import app

def get_uow(units):
    def get(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = args[1]
            tenant = request.headers.get("tenant")
            all_kwargs = dict()
            for unit in units:
                all_kwargs[unit] = app.config[f"{unit}_uow_{tenant}"]
                # OR
                #unt_name = unit.title()+"UoW"
                #exec(f'from utils import {unt_name}')
                #all_kwargs[unit] = eval(unt_name+f"('{tenant}')")
            all_kwargs.update(kwargs)
            result = func(*args, **all_kwargs)
            return await result
        return wrapper
    return get

def get_uow_cbv(units):
    def get(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs['request']
            tenant = request.headers.get("tenant")
            #all_kwargs = dict()
            for unit in units:
                kwargs[unit] = app.config[f"{unit}_uow_{tenant}"]
            #all_kwargs.update(kwargs)
            #result = func(*args, **all_kwargs)
            # ------- <OR>
            result = func(*args, **kwargs)
            return await result
        return wrapper
    return get

