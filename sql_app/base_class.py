from typing import Optional
import inspect

from lib.serialiser import CbvSerializer

from .database import SessionLocal, engine


from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .database import SessionLocal, engine
from lib.serialiser import CbvSerializer, SerializerMeta, patch
from lib.MyCBV import CustomRouter
from typing import Optional
from pydantic import BaseModel
import inspect
from . import new_models
from abc import ABC

# new_models.Base.metadata.create_all(bind=engine)
# from main import app
# app = FastAPI()

import copy

class Paginate:
    pass

class _ApiView(object):
    '''This class will be eventually developed as a base class.
    currently it implements a sample get method

    TODO: add functionality for models - pydentic models
    TODO: add functionality for query & search
    '''

    serializer_class:CbvSerializer = None
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
        'define query params here with type hints and required validations if any'
        pass

    def get(self, *args, **kwargs):
        return self.get_serializer().sanitize_list([i.__dict__ for i in self.get_queryset(*args, **kwargs)])

    async def post(self,*args,**kwargs):
        serializer = kwargs.get('serializer')
        model_instance = await serializer.save()
        return model_instance


def ApiView2():
    return type('ApiView', _ApiView.__bases__, dict(_ApiView.__dict__))
# ApiView = type('ApiView', _ApiView.__bases__, dict(ApiView.__dict__))
# class ApiView:
#     # @property
#     @classmethod
#     def view(cls):
#         return type('ApiView', _ApiView.__bases__, dict(ApiView.__dict__))