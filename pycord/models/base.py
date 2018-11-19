from inspect import isclass, getmro
from typing import List, Dict, _Union, Any

from pycord.exceptions import InvalidModel


class Model:
    """
    The model object is used to represent objects returned by the API.

    This class should be inherited by all objects that wish represent discord objects. If you'd like to create your own
    Model for your plugin, don't overwrite this class in a child. Make your own classes to represent discord objects and
    set each individual one in the config. Keep in mind when using a discord object, PyCharm or other editors may not
    auto-suggest attribute names because they're generated dynamically. As a side note, all models that have an ID
    attribute can be used in `==` operations with other objects with an ID. Also, if it has an ID, the hash is equal to
    that ID.

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
            if isinstance(value, _Union):
                api_val = data.get(name)
                if not api_val:
                    setattr(self, name, None)
                    continue
                value = value.__args__[0]
            setattr(self, name, self._load(value))

    def _get_val(self, name):
        api_value = self.d_data.get(name)
        if api_value is None:
            raise InvalidModel("Data received didn't fulfill object requirements.")
        return api_value

    def _load(self, value):
        if isclass(value):
            return value
        else:
            if isinstance(value, List.__class__):
                return lambda x: [self._load(value.__args__[0])(v) for v in x]
            elif isinstance(value, Dict.__class__):
                return lambda x: {self._load(value.__args__[0])(i): self._load(value.__args__[1])(m)
                                  for i, m in x.items()}

    def __eq__(self, other):
        if not hasattr(self, 'id'):
            raise NotImplementedError("This object doesn't have an ID, therefor can't be compared.")
        if not hasattr(other, 'id'):
            return False
        return self.id == other.id

    def __hash__(self):
        if not hasattr(self, 'id'):
            return super().__hash__()
        return self.id
