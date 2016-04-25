import pprint
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

    def _get_properties(self):
        properties = []
        for name in dir(self.__class__):
            cls_attribute = getattr(self.__class__, name)
            if isinstance(cls_attribute, property):
                properties.append(name)
        return properties

    def to_dict(self):
        ret = {}
        for attribute in self._get_properties():
            value = getattr(self, attribute)
            if getattr(value, 'to_dict', None) is not None:
                value = value.to_dict()
            if isinstance(value, (dict, int)):
                ret[attribute] = value
            else:
                ret[attribute] = str(value)
        return ret

    def from_dict(self, dict_):
        for attribute, value in dict_.items():
            if attribute not in self._get_properties():
                raise ValueError('{} not found'.format(attribute))
            setattr(self, attribute, value)

    def __str__(self):
        content = pprint.pformat(self.to_dict())
        return '{}: {}'.format(self.__class__.__name__, content)

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
