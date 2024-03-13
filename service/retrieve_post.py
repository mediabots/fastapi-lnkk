import string, random, datetime
#import logging
from sqlalchemy import text
#import asyncio

HOLDER = string.ascii_letters+string.digits
HOLDER_DICT = dict((idx,letter) for idx,letter in enumerate(HOLDER))
HOLDER_LENGTH = len(HOLDER)
#FORMAT = "%Y%m%d%H%M%S%f" # 4 letter year
FORMAT = "%y%m%d%H%M%S%f" # 2 letter year
CACHE_MOD = dict((_+HOLDER_LENGTH,_) for _ in range(99-HOLDER_LENGTH+1))


async def post_retrievation_prep_stmt(sql, url_key):
    res = None
    query_str = text("""
                     PREPARE get_post_redirect_url(varchar(20)) AS 
                     SELECT redirect_url 
                     FROM posts 
                     WHERE url_key = $1;""")
    async with sql:
        async with sql.asession() as sess:
            await sess.execute(query_str)
            result = await sess.execute(text(f"EXECUTE get_post_redirect_url('{url_key}')"))
            res = result.first()    
    # ------- <OR> Sync way   
    # with sql:
    #     with sql.session() as sess:
    #         sess.execute(query_str)
    #         result = sess.execute(text(f"EXECUTE get_post_redirect_url('{url_key}')"))
    #         res = result.first()    
    if res:
        return 0, res.redirect_url
    return 1, res

async def post_retrievation(sql, url_key):
    #pending = asyncio.all_tasks()  
    #print(len(pending))
    res = None
    query_str = text("""
                     SELECT redirect_url 
                     FROM posts 
                     WHERE url_key = :url_key""").\
                bindparams(url_key=url_key)
    async with sql:
        async with sql.asession() as sess:
            result = await sess.execute(query_str)
            res = result.first()   
        # ------- Note: below will not close the session properly, so avoid at any cost
        #result = await sql.asession.execute(query_str) 
        #res = result.first()       
    # ------- <OR> Sync way
    # with sql:
    #     with sql.session() as sess:
    #         result = sess.execute(query_str)
    #         res = result.first()
    #     # <OR>
    #     #result = sql.session.execute(query_str)
    #     #res = result.first()   
    if res:
        return 0, res.redirect_url
    return 1, res
    
def decode(s):
     time_str = ""
     d = dict()
     pos = list()
     if len(s) < 9:
         print("not a date time")
         return 0
     if "_" in s:
         print("not a date time!")
         return 0
     if "-" in s:
         tmp = s.split("-")
         s = tmp[0]
         for char in tmp[1]:
             pos.append(HOLDER.index(char))
             d[s[HOLDER.index(char)]]=str(HOLDER.index(s[HOLDER.index(char)]) + HOLDER_LENGTH)
     for i,char in enumerate(s):
         if ((char in d.keys()) and (i in pos)):
             time_str+= d[char]
         else:
             time_str+= str(HOLDER.index(char)).zfill(2)
     try:
         datetime.datetime.strptime(time_str, FORMAT)
     except:
         print("not a date time!!!")
         return 0
     return time_str