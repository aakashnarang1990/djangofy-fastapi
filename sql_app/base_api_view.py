from typing import Optional
import inspect

from lib.serialiser import CbvSerializer

from .database import SessionLocal, engine


from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request, APIRouter
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .database import SessionLocal, engine
from lib.serialiser import CbvSerializer, SerializerMeta, patch
from lib.MyCBV import CustomRouter
from typing import Optional
from pydantic import BaseModel
import inspect
from . import new_models
from .base_class import ApiView2
from abc import ABC

new_models.Base.metadata.create_all(bind=engine)
# from main import app
# app = FastAPI()

router = APIRouter(prefix='/items')
# app.include_router(router)
@router.get('/abc/')
def test_api():
    return{"hi":1}

class Paginate:
    pass

# class ApiView(ABC):
#     '''This class will be eventually developed as a base class.
#     currently it implements a sample get method
#
#     TODO: add functionality for models - pydentic models
#     TODO: add functionality for query & search
#     '''
#
#     serializer_class:CbvSerializer = None
#     pagination_class: Optional[Paginate] = None
#     lookup_field: Optional[str] = ''
#
#     def __init__(self):
#         self.db = SessionLocal()
#         self.model = self.get_model()
#
#     def get_serializer(self):
#         return self.serializer_class
#
#     def get_model(self):
#         return self.get_serializer().Meta.model
#
#     def get_query_params(self, *args, **kwargs):
#         _query_params = self.QueryParams.__annotations__
#         default_query_params = inspect.getmembers(self.QueryParams, lambda a: not (inspect.isroutine(a)))
#         default_query_params = [a for a in default_query_params if not (a[0].startswith('__') and a[0].endswith('__'))]
#         default_query_params = dict(default_query_params)
#         query_params = {}
#         for k, v in default_query_params.items():
#             if k in kwargs:
#                 query_params[k] = kwargs.get(k)
#             else:
#                 query_params[k] = v
#         for key in _query_params:
#             if key in kwargs:
#                 query_params[key] = kwargs.get(key)
#         return query_params
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = self.db.query(self.model).filter_by(**self.get_query_params(*args, **kwargs))
#         return queryset
#
#     def get_response_model(self, request):
#         pass
#
#     class QueryParams:
#         'define query params here with type hints and required validations if any'
#         pass
#
#     def get(self, *args, **kwargs):
#         return self.get_serializer().sanitize_list([i.__dict__ for i in self.get_queryset(*args, **kwargs)])
#
#     async def post(self,*args,**kwargs):
#         serializer = kwargs.get('serializer')
#         model_instance = await serializer.save()
#         return model_instance


@patch
class ClientSerialiser(CbvSerializer):
    class Config:
        orm_mode = True

    class Meta:
        model = new_models.Client
        read_only_fields = {'client_id'}


@patch
class ClusterTypeSerialiser(CbvSerializer):
    class Config:
        orm_mode = True

    class Meta:
        model = new_models.ClusterType
        read_only_fields = {'cluster_type_id'}

#
# @patch
# class ClusterSerialiser(CbvSerializer):
#     class Config:
#         orm_mode = True
#
#     class Meta:
#         model = new_models.Cluster
#         read_only_fields = {'cluster_id'}
#
#
# @patch
# class TestSuiteSerialiser(CbvSerializer):
#     class Config:
#         orm_mode = True
#
#     class Meta:
#         model = new_models.TestSuite
#         read_only_fields = {'test_suite_id'}
#
#
# @patch
# class TestCaseSerialiser(CbvSerializer):
#     class Config:
#         orm_mode = True
#
#     class Meta:
#         model = new_models.TestCase
#         read_only_fields = {'test_case_id'}


class ClientApiView(ApiView2()):
    serializer_class = ClientSerialiser

    class QueryParams:
        name: Optional[str] = None

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    async def post(self, *args, **kwargs):
        return await super().post(*args, **kwargs)


class ClusterTypeApiView(ApiView2()):
    serializer_class = ClusterTypeSerialiser

    class QueryParams:
        name22: str

    def get(self, *args, **kwargs):
        return super(self.get(*args, **kwargs))

    async def post(self, *args, **kwargs):
        return await super().post(*args, **kwargs)


class ApiViewNew:
    '''This class will be eventually developed as a base class.
    currently it implements a sample get method

    TODO: add functionality for models - pydentic models
    TODO: add functionality for query & search
    '''

    serializer_class = ClientSerialiser
    pagination_class: Optional[Paginate] = None
    lookup_field: Optional[str] = ''

    def __init__(self):
        self.db = SessionLocal()
        self.model = self.get_model()

    def get_serializer(self):
        return self.serializer_class

    def get_model(self):
        return self.get_serializer().Meta.model

    def get_query_params(self, *args, **kwargs):
        _query_params = self.QueryParams.__annotations__
        default_query_params = inspect.getmembers(self.QueryParams, lambda a: not (inspect.isroutine(a)))
        default_query_params = [a for a in default_query_params if not (a[0].startswith('__') and a[0].endswith('__'))]
        default_query_params = dict(default_query_params)
        query_params = {}
        for k, v in default_query_params.items():
            if k in kwargs:
                query_params[k] = kwargs.get(k)
            else:
                query_params[k] = v
        for key in _query_params:
            if key in kwargs:
                query_params[key] = kwargs.get(key)
        return query_params

    def get_queryset(self, *args, **kwargs):
        queryset = self.db.query(self.model).filter_by(**self.get_query_params(*args, **kwargs))
        return queryset

    def get_response_model(self, request):
        pass

    class QueryParams:
        name: Optional[str] = None

    def get(self, *args, **kwargs):
        return self.get_serializer().sanitize_list([i.__dict__ for i in self.get_queryset(*args, **kwargs)])

    async def post(self,*args,**kwargs):
        serializer = kwargs.get('serializer')
        model_instance = await serializer.save()
        return model_instance


#
# class ClusterApiView(ApiView):
#     serializer_class = ClusterSerialiser
#
#     class QueryParams:
#         name: str
#
#
# class TestSuiteApiView(ApiView):
#     serializer_class = TestSuiteSerialiser
#
#     class QueryParams:
#         name: str
#
#
# class TestCaseApiView(ApiView):
#     serializer_class = TestCaseSerialiser
#
#     class QueryParams:
#         name: str


CustomRouter(router=router, url="/client/", ViewClass=ClientApiView, tags=["Custom Router"])
CustomRouter(router=router, url="/cluster-type/", ViewClass=ClusterTypeApiView, tags=["Custom Router"])
# CustomRouter(router=app, url="/cluster/", ViewClass=ClusterApiView, tags=["Custom Router"])
# CustomRouter(router=app, url="/test-suite/", ViewClass=TestSuiteApiView, tags=["Custom Router"])
# CustomRouter.router(router=app, url="/test-case/", ViewClass=TestCaseApiView, tags=["Custom Router"])
# CustomRouter(router=app, url="/client/", ViewClass=UserApiView, tags=["Custom Router"])
