import functools


class Dict:
    """ A dictionary wrapped in a class.
    """
    def __init__(self):
        self.dict = {}

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __call__(self):
        return self.dict


def partial_class(class_, *args, **kwds):
    class NewClass(class_):
        __init__ = functools.partialmethod(class_.__init__, *args, **kwds)

    return NewClass
