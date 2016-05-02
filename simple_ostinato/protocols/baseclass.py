import inspect
"""
"""


# FIXME: inherit docstrings for properties
# def fix_docs(cls):
#     for name, func in vars(cls).items():
#         if not func.__doc__:
#             for parent in cls.__bases__:
#                 try:
#                     parent_func = getattr(parent, name)
#                 except AttributeError:
#                     continue
#                 if parent_func and getattr(parent_func, '__doc__', None):
#                     func.__doc__ = parent_func.__doc__
#                     break
#     return cls


def make_protocol_class(name, bases, attributes):
    # http://stackoverflow.com/a/13937525/1836144
    if '__doc__' not in attributes:
        # create a temporary 'parent' to simplify the MRO search
        temp = type('temporaryclass', bases, {})
        for cls in inspect.getmro(temp):
            if cls.__doc__ is not None:
                attributes['__doc__'] = cls.__doc__
                break
    return type(name, bases, attributes)
    # return fix_docs(my_cls)


class Protocol(object):

    """
    Base class for the actual protocols
    """

    def __init__(self, **kwargs):
        for attribute, value in kwargs.iteritems():
            setattr(self, attribute, value)

    # def _get_properties(self):
    #     properties = []
    #     for name in dir(self.__class__):
    #         cls_attribute = getattr(self.__class__, name)
    #         if isinstance(cls_attribute, property):
    #             properties.append(name)
    #     return properties

    def _save(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for method in dir(self):
            if method.startswith('_save_'):
                getattr(self, method)(ext)

    def _fetch(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for method in dir(self):
            if method.startswith('_fetch_'):
                getattr(self, method)(ext)
