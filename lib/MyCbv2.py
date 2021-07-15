import inspect
from typing import Any, Callable, List, Type, TypeVar, Union, get_type_hints
from fastapi import Depends, Body
import pdb
import copy
ALLOWED_METHODS = (
    'get',
    'post',
    # 'put',
    # 'delete',
    # 'trace',
    # 'head',
    # 'options',
    # 'connect',
    # 'patch',
)


def create_get(ViewClass, method_name):
    new_method = copy.deepcopy(getattr(ViewClass, method_name))
    ViewClass.get = new_method
    new_method = copy.deepcopy(getattr(ViewClass, method_name))
    old_signature = inspect.signature(new_method)
    old_parameters: List[inspect.Parameter] = list(
        i for i in old_signature.parameters.values() if i.name not in ('args', 'kwargs'))
    QueryParams = ViewClass.QueryParams
    query_params_list = []
    default_query_params = inspect.getmembers(
        QueryParams, lambda a: not(inspect.isroutine(a)))
    default_query_params = [a for a in default_query_params if not(
        a[0].startswith('__') and a[0].endswith('__'))]
    default_query_params = dict(default_query_params)

    if ViewClass.get('lookup_field'):
        lookup_field = ViewClass.lookup_field
        query_params_list.append(
            inspect.Parameter(name=lookup_field, kind=inspect.Parameter.KEYWORD_ONLY,
                              annotation=str)
        )

    for param_name, param_type_hint in get_type_hints(QueryParams).items():
        default_val = default_query_params.pop(
            param_name, inspect.Parameter.empty)

        query_params_list.append(
            inspect.Parameter(name=param_name, kind=inspect.Parameter.KEYWORD_ONLY,
                              annotation=param_type_hint, default=default_val)
        )

    for param_name, default_val in default_query_params.items():
        query_params_list.append(
            inspect.Parameter(name=param_name, kind=inspect.Parameter.KEYWORD_ONLY,
                              annotation=inspect.Parameter.empty, default=default_val)
        )

    old_first_parameter = [i for i in old_parameters if i._name == "self"][0]
    new_first_parameter = old_first_parameter.replace(
        default=Depends(ViewClass))
    new_parameters = [new_first_parameter] + [
        parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY) for parameter in query_params_list
    ]
    old_signature = old_signature.replace(parameters=[])
    new_signature = old_signature.replace(parameters=new_parameters)
    setattr(new_method, "__signature__", new_signature)
    return new_method


def create_post(ViewClass, method_name):
    new_method = getattr(ViewClass, method_name)
    old_signature = inspect.signature(new_method)
    old_parameters: List[inspect.Parameter] = list(
        i for i in old_signature.parameters.values() if i.name not in ('args', 'kwargs'))
    serializer = ViewClass.serializer_class
    old_first_parameter = [i for i in old_parameters if i._name == "self"][0]
    new_first_parameter = old_first_parameter.replace(
        kind=inspect.Parameter.KEYWORD_ONLY, default=Depends(ViewClass))
    new_parameters = [inspect.Parameter(name='serializer',
                                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                        default=inspect._empty, annotation=serializer),
                      new_first_parameter]
    old_signature = old_signature.replace(parameters=[])
    new_signature = old_signature.replace(parameters=new_parameters)
    setattr(new_method, "__signature__", new_signature)
    return new_method

METHOD_MAP = {
    'get': create_get,
    'post': create_post
}

# class CustomRouter:
#     @classmethod
def CustomRouter(router, url, ViewClass, *args, **kwargs):

    # panret_methods = copy.deepcopy(ViewClass.__bases__[0].__dict__)
    # for k in panret_methods:
    #     print(k)
    #     if k not in ViewClass.__dict__ and not(
    #     k.startswith('__') and k.endswith('__')):
    #         setattr(ViewClass,k, panret_methods[k])

    for method_name in ALLOWED_METHODS:
        if hasattr(ViewClass, method_name):
            method = getattr(router, method_name, None)
            if method is not None:
                method = method(url, **kwargs)
                compute_method = METHOD_MAP.get(method_name)
                new_method = compute_method(
                    ViewClass=ViewClass, method_name=method_name)
                new_method = method(new_method)
                setattr(ViewClass, method_name, new_method)
                # ViewClass.__dict__[method_name] = new_method
    import pdb
    # return ViewClass
