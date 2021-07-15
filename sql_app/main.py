from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
# from main import app
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='')
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(request: Request, skip:int=0, limit:int=100, db: Session = Depends(get_db)):
    # print(request.__dict__)
    # import pdb; pdb.set_trace()

    return crud.get_users(skip=skip, limit=limit, db=db)


from lib.serialiser import CbvSerializer, SerializerMeta, patch

@patch
class UserSerialiser(CbvSerializer):
    class Config:
        orm_mode = True

    class Meta:
        model = models.User
        write_only_fields = {'hashed_password'}
        read_only_fields = {'id'}


@app.get("/a_users/", response_model=List[UserSerialiser.response_model])
def read_users(request: Request, skip:int=0, limit:int=100, db: Session = Depends(get_db)):
    serialser = UserSerialiser
    # import pdb
    # pdb.set_trace()
    s = serialser.sanitize_list([i.__dict__ for i in crud.get_users(skip=skip, limit=limit, db=db)])

    return s

    # return crud.get_users(skip=skip, limit=limit, db=db)


# @app.get("/b_users/", response_model=UserSerialiser.response_model)
# async def read_users(serializer:UserSerialiser=None):
#     model_instance = await serializer.save()
#     return model_instance.dict()

@app.post("/a_users/", response_model=UserSerialiser.response_model)
async def root(serializer: UserSerialiser):
    model_instance = await serializer.save()
    return model_instance


from lib.MyCBV import CustomRouter
from typing import Optional
from pydantic import BaseModel
import inspect

class Paginate:
    def __init__(self, page:int, page_size:int, next:str, prev:str):
        pass

class ApiView:
    serializer_class = UserSerialiser
    pagination_class:Optional[Paginate] = None
    lookup_field: Optional[str] = ''

    class QueryParams:
        email: Optional[str] = None

    def __init__(self):
        self.db = SessionLocal()
        self.model = self.get_serializer().Meta.model

    def get_serializer(self):
        return self.serializer_class

    def get_query_params(self, *args, **kwargs):
        default_query_params = inspect.getmembers(self.QueryParams, lambda a: not (inspect.isroutine(a)))
        default_query_params = [a for a in default_query_params if not (a[0].startswith('__') and a[0].endswith('__'))]
        default_query_params = dict(default_query_params)
        query_params = {}
        for k,v in default_query_params.items():
            query_params[k] = kwargs.get(k)
        return query_params


    def get_queryset(self, *args, **kwargs):
        queryset = self.db.query(self.model).filter_by(**self.get_query_params(*args, **kwargs))
        return queryset


    def get(self, *args, **kwargs):
        return self.get_serializer().sanitize_list([i.__dict__ for i in self.get_queryset(*args,**kwargs)])

    async def post(self,*args,**kwargs):
        serializer = kwargs.get('serializer')
        model_instance = await serializer.save()
        return model_instance

CustomRouter(router=app, url="/test_200/", ViewClass=ApiView, tags=["Custom Router"])