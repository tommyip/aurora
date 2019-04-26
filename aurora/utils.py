import functools

import yaml


class Dict:
    """ A dictionary wrapped in a class.
    """
    def __init__(self, init=None):
        self.dict = init or {}

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __call__(self):
        return self.dict

    def get(self, key, value=None):
        return self.dict.get(key, value)


def partial_class(class_, *args, **kwds):
    class NewClass(class_):
        __init__ = functools.partialmethod(class_.__init__, *args, **kwds)

    return NewClass


def load_yaml(content):
    """ Return an object instead of None even when the input is empty.
    """
    return yaml.load(content or '') or {}
