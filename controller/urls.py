from view import Post, Ping, PostCBV#,ping
#from view.posts import ping
from controller.blueprint import blp_user, blp_post

@blp_user.get("/test2")
def test2():
    return "test"


@blp_post.get("/test")
def test():
    return "test"

#blp_post.add_api_route("/ping", endpoint=ping, methods=["GET"])
#blp_post.add_api_route("/ping/<string:username>", endpoint=ping, methods=["GET"])
blp_post.add_api_route("/ping", endpoint=Ping.get, methods=["GET"])
#blp_post.add_api_route("/ping", endpoint=Ping.as_view, methods=["GET"])
#blp_post.add_api_route("/pingnew2", endpoint=Ping.as_view, methods=["GET"])
#blp_post.add_api_route("/ping", endpoint=Ping.as_view(Ping), methods=["GET"])
#blp_post.add_api_route("/ping", endpoint=Ping.get, methods=["GET"])
#blp_post.add_api_route("/ping/{username:str}", endpoint=Ping.get, methods=["GET"])
#blp_post.add_api_route("/ping", endpoint=Ping.post, methods=["POST"])
#blp_post.add_api_route("/{url_key:str}", endpoint=Post.as_view, methods=["GET"])
#blp_post.add_api_route("/{url_key:str}", endpoint=Post.as_view, methods=["GET","PUT","DELETE"])
#blp_post.add_api_route("/{url_key:str}", endpoint=Post.as_view, methods=["GET"])
blp_post.add_api_route("/{url_key:str}", endpoint=PostCBV.get, methods=["GET"])
# blp_post.add_url_rule("/health", view_func=Ping.as_view("health"))
# blp_post.add_url_rule("/<string:url_key>", view_func=Post.as_view("post"))
# blp_post.add_url_rule("/posts", view_func=Posts.as_view("posts"))
# blp_post.add_url_rule("/posts/bulk", view_func=PostsBulk.as_view("posts_bulk"))