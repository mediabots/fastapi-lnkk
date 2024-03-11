from fastapi import APIRouter as Blueprint

responses={404: {"description": "Not found"}}

blp_user = Blueprint(prefix="/users", responses=responses)

blp_post = Blueprint(responses=responses)
