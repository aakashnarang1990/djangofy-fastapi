import pdb
from typing import Any, Callable, List, Type, TypeVar, Union, get_type_hints, Optional


class Cbv3:
    model: str = ''

    class QueryParams:
        q: Optional[str]
        limit: int = 10
        skip: int = 0

    def get_query_params(self):
        return self.QueryParams.__annotations__

    def build():
        pass

    def get_queryset(self):
        pass


pdb.set_trace()
