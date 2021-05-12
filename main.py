from fastapi import FastAPI, Query
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from my_routers.admin import my_user
from my_routers.users import abc as old_user

app = FastAPI()
app.include_router(my_user.router, prefix="/user",)
app.include_router(old_user.router, prefix="/admin",)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/abcd")
# async def read_item():
#     return {"item_id": 'all'}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


fake_items_db = [i for i in range(200)]


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 100):
    return fake_items_db[skip: skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None, short: bool = False):
    return {"item_id": item_id, "q": q, "short": short}


class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    tax: Optional[float] = None

    def __repr__(self):
        return f"{self.name} - {self.price}"

    # def __str__(self):
    #     return f" --- {self.name} - {self.price}"


@app.post("/items/")
async def create_item(item: Item):
    print(item.name.capitalize())
    print(item)
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    return{"item_id": item_id, "item": item, "q": q}


@app.get("/items_read/")
async def read_item(
        q: Optional[str] = Query(
            None,
            title='QueryParam-q',
            alias='q-param',
            description='this is a sample query param',
            min_length=3,
            max_length=50,
            regex="^sample",
            deprecated=True

        )
):
    return {"item_id": 'all', "q": q}


# class ApiClass:
#     rounter = app
#
#     def __init__(self, *args, **kwargs):
#         pass
#
#     router.get('/hello/')
#
#     def get(self, request_obj):
#         return {'hi': 123455}


from lib.ClassBased import ClassBasedView
# from main import app
wrapper = ClassBasedView(app)
@wrapper('cbv2')
class CBV2:
    route = "/test_47/"

    def get(self):
        return {"message": "Hello World....."}
