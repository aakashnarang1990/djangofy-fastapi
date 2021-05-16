from typing import Optional, Iterable
from abc import ABC
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from enum import Enum
from typing import Type, List

from pydantic import Required, create_model


base = declarative_base()


class SerializerMeta(ABC):
    exclude: set = set()
    write_only_fields: set = set()
    read_only_fields: set = set()
    model: base = None


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
            if hasattr(cls.Meta, "exclude"):
                for e in cls.Meta.exclude:
                    d.pop(e, None)
                return d
            return d

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
            await instance.save(
                include=include, exclude=exclude, rewrite_fields=rewrite_fields
            )
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
        response_model = gen_model(cls, mode=FieldGenerationMode.RESPONSE)

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