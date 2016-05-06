import re


def hexstr_to_int(string):
    """
    Convert a string representing an hexadecimal sequence to an int. It removes
    all spaces, columns, and hyphens from the string before processing it.

    >>> hexstr_to_int('FF-01-A2')
    4282039056

    >>> hexstr_to_int('ff:01:a2')
    4282039056

    >>> hexstr_to_int('Ff 01 A2')
    4282039056

    >>> hexstr_to_int('fF:01-a2')
    4282039056

    >>> hexstr_to_int('0xfF:01-a2')
    4282039056

    >>> hexstr_to_int('0xff01a2')
    4282039056
    """
    return int(re.sub(r'(^0x)?[\s:-]', '', string), 16)


def to_str(integer, padding=None, sep=':'):
    string = hex(integer).replace('0x', '').upper()
    if padding:
        while len(string) < padding:
            string = '0{}'.format(string)
    return sep.join(re.findall('..?', string))


def parse(value):
    if isinstance(value, int):
        return value
    if isinstance(value, (unicode, str)):
        return hexstr_to_int(value)
    else:
        raise ValueError('Invalid value {}'.format(value))


class Enum(object):

    @classmethod
    def get_key(cls, value):
        for key, val in cls.__dict__.iteritems():
            if val == value:
                return key

    @classmethod
    def get_value(cls, key):
        keys = cls.keys()
        if key in keys:
            return getattr(cls, key)
        enum = cls.__name__
        valid = ','.join([k for k in keys])
        err = '{} not a valid {}. Must be one of: {}.'.format(key, enum, valid)
        raise ValueError(err)

    @classmethod
    def keys(cls):
        for key in cls.__dict__.iterkeys():
            if not key.startswith('_'):
                yield key
