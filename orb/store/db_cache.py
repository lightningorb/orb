import functools


def aliases_cache(func):
    from orb.store import model

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        pk = args[1]
        alias = model.Alias().select().where(model.Alias.pk == pk)
        if alias:
            return alias.get().alias
        alias = func(*args, **kwargs)
        model.Alias(pk=pk, alias=alias).save()
        return alias

    return wrapper_decorator
