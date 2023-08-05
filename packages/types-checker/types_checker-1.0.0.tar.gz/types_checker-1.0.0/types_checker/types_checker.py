# -*- coding: utf-8 -*-
from typing import Coroutine


def check_type(func):
    annotation = func.__annotations__
    defaults = func.__defaults__
    if defaults:
        defaults = list(defaults)

    it = tuple(annotation.items())
    ret_type = annotation.get('return')

    async def ret(coro):
        res = await coro
        if not ret_type is None and not isinstance(res, ret_type):
            raise TypeError(f'func return type = `{type(res)}` need type = `{ret_type}`')
        return res

    def wrapper(*args, **kwargs):
        if defaults and len(args) < len(annotation) - 1:
            arg = list(args)
            arg.extend(defaults)
            args = tuple(arg)

        if kwargs:
            for k, v in kwargs.items():
                t = annotation.get(k)
                if not isinstance(v, t):
                    raise TypeError(f'name = `{k}` got type = `{type(v)}` need type = `{t}`')

        if args:
            for i, v in enumerate(args):
                k, t = it[i]
                if not isinstance(v, t):
                    raise TypeError(f'name = `{k}` got type = `{type(v)}` need type = `{t}`')

        result = func(*args, **kwargs)

        if not ret_type is None:
            if isinstance(result, Coroutine):
                return ret(result)

            if not isinstance(result, ret_type):
                raise TypeError(f'func return type = `{type(result)}` need type = `{ret_type}`')

        return result
    return wrapper
