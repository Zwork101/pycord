from inspect import isclass, getmro
from typing import Optional, List, Dict, _Union, Any

from pycord.exceptions import InvalidModel


class Model:
    """
    The model object is used to represent objects returned by the API.

    This class should be inherited by all objects that wish represent discord objects. If you'd like to create your own
    Model for your plugin, don't overwrite this class in a child. Make your own classes to represent discord objects and
    set each individual one in the config. Keep in mind when using a discord object, PyCharm or other editors may not
    auto-suggest attribute names because they're generated dynamically.

    :ivar d_data: The original information passed in.
    :type d_data: Dict[str, Any]
    :ivar d_client: The client the object belongs too.
    :type d_client: :py:class:`~pycord.client.client.Client`
    """

    def __init__(self, client, data: Dict[str, Any]):
        """
        Constructor for Model, very rare should this be called manually.

        Most of the time, this class will always be handled by pycord. I don't really see any other reason for it to be
        made by hand.

        :param client: The client object the class was created for.
        :type client: :py:class:`~pycord.client.client.Client`
        :param data: A dict returned by the discord API
        :type data: Dict[str, Any]
        """
        if not hasattr(self.__class__, "__annotations__"):
            raise InvalidModel("Model doesn't contain any annotations")

        self.d_data = data
        self.d_client = client

        annotations = {}
        for obj in getmro(self.__class__)[1::-1]:
            annotations.update(obj.__annotations__)

        for name, value in annotations.items():
            if isclass(value):
                setattr(self, name, value(self._get_val(name)))
            else:
                if isinstance(value, List.__class__):
                    setattr(self, name, [value.__args__[0](v) for v in self._get_val(name)])
                elif isinstance(value, Dict.__class__):
                    setattr(self, name, {})
                    for key, val in self._get_val(name).items():
                        getattr(self, name)[value.__args__[0](key)] = value.__args__[1](val)
                elif isinstance(value, _Union):
                    api_value = data.get(name)
                    if api_value:
                        setattr(self, name, value.__args__[0](api_value))
                    else:
                        setattr(self, name, None)

    def _get_val(self, name):
        api_value = self.d_data.get(name)
        if api_value is None:
            raise InvalidModel("Data received didn't fulfill object requirements.")
        return api_value
