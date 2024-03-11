from pydantic import BaseModel, constr, conint, confloat
from typing import Optional, List

class CategoryPayload(BaseModel):
    #category_id: int
    category_name: constr(max_length=25)
    category_description: Optional[constr(max_length=50)] = None


class CategoriesPayload(BaseModel):
    categories: List[CategoryPayload]