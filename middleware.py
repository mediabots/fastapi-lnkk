

class ASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            #print(scope.keys())
            # ------- extracting request host name
            #host = [_[1].decode() for _ in scope['headers'] if _[0]==b'host'][0]
            # OR
            host = ""
            for header in scope['headers']:
                if header[0]==b'host':
                    host = header[1].decode()
                    break
                else:
                    continue
            # ------- fetching subdomain out of host name
            subdomain = host.replace(f".{self.app.config['SERVER_NAME']}","")
            #print("Host: ", host, subdomain)
            # ------- adding custom http header
            scope['headers'].append((b'tenant', subdomain.encode()))
            ##self.subdomain = subdomain
        await self.app(scope, receive, send)

"""
@app.midleware("http")
async def add_process_time_header(request: Request, call_next):
    host = request.headers.get("host")
    subdomain = request.headers.get("tenant")
    print("Host: ", host, subdomain) # PS: tenant info would not be there
    response = await call_next(request)
    return response
"""
