from functools import partial
from lib.cbv import cbv
from typing import Any, Callable, List, Type, TypeVar, Union, get_type_hints, Optional
from lib.cbv import _cbv
from lib.MyCBV import CustomRouter
from lib.ClassBased import ClassBasedView
from fastapi import APIRouter, Query, Depends
from typing import Optional

router = APIRouter()


@router.get("/test_1/", tags=["users"])
async def route_test1():
    return {"message": "Hello World"}


class Hello:
    route = "/test_45/"

    @router.get(route, tags=["users"])
    def get():
        return {"message": "Hello World....."}


@cbv(router)
class CBV1:
    route = "/test_46/"

    @router.get(route, tags=["users"])
    def get(self):
        return {"message": "Hello World....."}


# # from main import app
wrapper = ClassBasedView(router)


@wrapper('/cbv100/', tags=['New Cbv 2'])
class ApiViewClass:
    def get(self):
        return {"message": "Hello World....."}


class ApiViewClass2:

    lookup_field = 'item_id'

    class QueryParams:
        q: Optional[str] = None
        limit: int = 10
        a = 10
        skip: int = 0
        req: str
        q2: Optional[str] = Query(
            None,
            title='QueryParam-q',
            alias='q-param',
            description='this is a sample query param',
            min_length=3,
            max_length=50,
            regex="^sample",
            deprecated=True

        )

    def get(self, *args, **kwargs):
        for (k, v) in kwargs.items():
            setattr(self, k, v)
        return {"message": "Hello World....."}


CustomRouter(router=router, url="/test_200/{item_id}",
             ViewClass=ApiViewClass2, tags=["Custom Router"])
# def UserClass(ApiViewClass):


'router: APIRouter, cls: Type[T]'


# def custom_router(route:APIRouter, class_view:Any)->Callable:


# class myClass:

# def as_view(self):
#     return _cbv
