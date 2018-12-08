from functools import wraps
from inspect import isclass
from trio import run

import pycord.config
from pycord.exceptions import NoContextAvailable

from combomethod import combomethod

def _get_property(context_data, property_path: list):
    if not context_data:
        raise NoContextAvailable
    for prop in property_path:
        context_data = getattr(context_data, prop, None)
        if not context_data:
            raise NoContextAvailable
    return context_data


def insert_context(**contexts):
    """
    If values are not supplied along and the instance can't help, try to get into from context.

    The order in which information is overwritten is like this. If accessing the model as a class, Contexts will be
    used, overwritten by provided kwargs. If accessing the model as an instance, The instance properties will be used
    for requirements that use it's class for information. Then it will take information from context for other classes,
    and for information that couldn't be supplied by the instance. While all of this is overwritten by provided kwargs.

    :param kwargs: The name of the method's kwarg that will have data provided. This is to a tuple of strings, working
    as a path to a properties's attribute. Ex `channel_id=['Channel', 'id']`
    :type kwargs: Dict[str, Tuple[str]]
    :return: A wrapped version of the function
    """
    def func_wrapper(func):  # I want to refactor this later
        @wraps
        @combomethod
        async def wrapper(*args, **kwargs):
            if isclass(args[0]):
                for key, value in kwargs.items():
                    if value is None and key in contexts:
                        try:
                            obj = getattr(pycord.models, contexts[key][0], None)
                            if obj is None:
                                raise NoContextAvailable
                            data = _get_property(obj, contexts[key][1:])
                        except NoContextAvailable:
                            continue
                        kwargs[key] = data
            else:
                for key, value in kwargs.items():
                    if value is None and contexts[key][0] == args[0].__class__.__name__:
                            try:
                                inst_data = _get_property(args[0], contexts[key][1:])
                            except NoContextAvailable:
                                continue
                            kwargs[key] = inst_data
                for key, value in kwargs.items():
                    if value is None and key in contexts:
                        try:
                            obj = getattr(pycord.models, contexts[key][0], None)
                            if obj is None:
                                raise NoContextAvailable
                            data = _get_property(obj, contexts[key][1:])
                        except NoContextAvailable:
                            continue
                        kwargs[key] = data
            return func(*args, **kwargs)
        return wrapper
    return func_wrapper


class ModelMagic(type):
    """
    A metaclass to make contexts work, like magic

    This will be the meta class for the Model class. Keep in mind, this class is not a template, you can do whatever
    you want with your plugins. There is not option to change this, because you can't really change a class's meta
    class at run time, and the same with parent classes. At least not without great pain.
    """

    def __getattr__(cls, item):
        if item in dir(cls):
            return super().__getattribute__(item)

        try:
            info = pycord.config.event.get().get(cls.__name__)
        except LookupError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(cls.__name__, item))
        if info:
            if info['complete'] and info['data'] is not None:
                return getattr(info['data'], item)
            elif not info['complete']:
                if not hasattr(cls, 'get'):
                    raise AttributeError("'{0}' object has no attribute '{1}' (Model doesn't support contexts in this"
                                         "event)".format(cls.__name__, item))
                if all(info['data']):
                    info['complete'] = True
                    info['data'] = run(cls.get(*info['data']))
                    return getattr(cls, item)


        raise AttributeError("'{0}' object has no attribute '{1}' (Model doesn't support contexts in this"
                             "event)".format(cls.__name__, item))
