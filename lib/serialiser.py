from typing import Optional, Iterable
from abc import ABC
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from enum import Enum
from typing import Type, List

from pydantic import Required, create_model
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
def get_db():
    db = SessionLocal()
    return db
    # try:
    #     yield db
    # finally:
    #     db.close()


class SerializerMeta(ABC):
    exclude: set = set()
    write_only_fields: set = set()
    read_only_fields: set = set()
    model: base = None
    db: Session = get_db


class FieldGenerationMode(int, Enum):
    REQUEST = 1
    RESPONSE = 2


class CbvSerializer(BaseModel):
    """
        Base Class Based View Serializer class.
    """

    @classmethod
    def sanitize_list(cls, iterable: Iterable) -> List[dict]:
        def clean_d(d):
            print(d)
            if hasattr(cls.Meta, "exclude"):
                for e in cls.Meta.exclude:
                    d.pop(e, None)
                # return d
            col_names = [i.name for i in cls.Meta.model.__table__._columns]
            print(col_names)
            # import pdb;
            # pdb.set_trace()
            output = {}
            for i in col_names:
                output[i] = d.get(i)
            # output = {k:v for k,v in d.items if k in col_names}
            # for i in d:
            #     if i in col_names:
            #
            return output

        return list(map(lambda x: clean_d(x), iterable))

    async def save(
            self,
            include: set = None,
            exclude: set = None,
            rewrite_fields: dict = None,
    ) -> base:
        if (
                hasattr(self, "Meta")
                and getattr(self.Meta, "model", None) is not None
        ):
            instance = self.Meta.model(**self.__dict__)
            db =  self.Meta.db()
            db.add(instance)
            db.commit()
            db.refresh(instance)
            # hash_pwd = user.password + 'abcd'
            # db_user = models.User(email=user.email, hashed_password=hash_pwd)
            # db.add(db_user)
            # db.commit()
            # db.refresh(db_user)
            # return db_user
            # await instance.save(
            #     include=include, exclude=exclude, rewrite_fields=rewrite_fields
            # )
            return instance

    def dict(self, *args, **kwargs) -> dict:
        exclude = kwargs.get("exclude")
        if not exclude:
            exclude = set()

        exclude.update({"_id"})

        if hasattr(self.Meta, "exclude") and self.Meta.exclude:
            exclude.update(self.Meta.exclude)

        if (
                hasattr(self.Meta, "write_only_fields")
                and self.Meta.write_only_fields
        ):
            exclude.update(self.Meta.write_only_fields)

        kwargs.update({"exclude": exclude})
        original = super().dict(*args, **kwargs)
        return original

    class Meta(SerializerMeta):
        ...



def model_generator(cls: Type, mode: FieldGenerationMode):
    _fields = {}

    _Meta = getattr(cls, "Meta", type("Meta"))
    Meta = type("Meta", (_Meta, SerializerMeta), {})

    Config = getattr(cls, "Config", getattr(CbvSerializer, "Config"))

    if mode == FieldGenerationMode.RESPONSE:
        excluded = Meta.exclude | Meta.write_only_fields
    else:
        excluded = Meta.exclude | Meta.read_only_fields

    if hasattr(Meta, "model") and Meta.model is not None:
        for each_col in Meta.model.__table__._columns:
            if each_col.name not in excluded:
                if each_col.default:
                    f_def = each_col.default.arg
                else:
                    f_def = Required
                _type = each_col.type.python_type
                _fields.update({each_col.name: (_type, f_def)})
    # import pdb; pdb.set_trace()
    for f, t in cls.__fields__.items():
    # for f, t in all_fileds:
        if f not in excluded:
            f_def = t.default
            if t.required:
                f_def = Required
            _fields.update({f: (t.type_, f_def)})

    if mode == FieldGenerationMode.REQUEST:
        response_model = model_generator(cls, mode=FieldGenerationMode.RESPONSE)

        CbvSerializer.Config = Config
        model = create_model(cls.__name__, __base__=CbvSerializer, **_fields)
        setattr(model, "response_model", response_model)
        setattr(model, "Meta", Meta)
        setattr(model, "Config", Config)

        reserved_attrs = ["Meta", "response_model", "Config"]
        for attr, value in cls.__dict__.items():
            if not attr.startswith("_") and attr not in reserved_attrs:
                setattr(model, attr, value)

        return model

    return create_model(
        f"{cls.__name__}Response", __config__=Config, **_fields
    )


def patch(cls: Type) -> Type:
    # import pdb; pdb.set_trace()
    return model_generator(cls, mode=FieldGenerationMode.REQUEST)