import netaddr
from ostinato.protocols import mac_pb2, ip4_pb2, payload_pb2
from . import autogenerates
from . import baseclass
from .. import utils


class MacAddress(object):

    """
    Represent a MAC address
    """

    class _Mode(utils.Enum):
        INCREMENT = mac_pb2.Mac.e_mm_dec
        FIXED = mac_pb2.Mac.e_mm_fixed
        DECREMENT = mac_pb2.Mac.e_mm_inc

    def __init__(self, address='00:00:00:00:00:00', mode='FIXED',
                 count=16, step=1):
        self.address = address
        self.mode = mode
        self.count = count
        self.step = step

    @property
    def address(self):
        """
        The MAC address value. If :attr:`mode` is set to ``INCREMENT``,
        ``DECREMENT`` or ``RANDOM``, it is the address of the inital frame, the
        next being calculated from this one.
        """
        return str(netaddr.EUI(self._address))

    @address.setter
    def address(self, value):
        self._address = netaddr.EUI(value).value

    @property
    def mode(self):
        """
        If there are several frames in the stream, the mode determine how the
        MAC address of the frames are calculated.

        - ``FIXED``: all the frames will have the MAC address :attr:`address`
        - ``INCREMENT``: the MAC addresses are incremented by :attr:`step` \
            for each frame, starting from :attr:`address`. After the \
            :attr:`count` th frame, it restarts from :attr:`address`.
        - ``DECREMENT``: the MAC addresses are decremented by :attr:`step` \
            for each frame, starting from :attr:`address`. After the \
            :attr:`count` th frame, it restarts from :attr:`address`.
        - ``RANDOM``: the MAC addresses are random
        """
        return self._Mode.get_key(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = self._Mode.get_value(value)


class Mac(autogenerates._Mac):

    __metaclass__ = baseclass.make_protocol_class

    @property
    def source(self):
        """
        Source MAC address
        """
        return str(netaddr.EUI(self._src_mac))

    @source.setter
    def source(self, value):
        self._src_mac = netaddr.EUI(value).value

    @property
    def destination(self):
        """
        destination MAC address
        """
        return str(netaddr.EUI(self._dst_mac))

    @destination.setter
    def destination(self, value):
        self._dst_mac = netaddr.EUI(value).value


class IPv4Address(object):

    """
    Represent an IPv4 address.
    """

    class _Mode(utils.Enum):
        DECREMENT = ip4_pb2.Ip4.e_im_dec_host
        FIXED = ip4_pb2.Ip4.e_im_fixed
        INCREMENT = ip4_pb2.Ip4.e_im_inc_host
        RANDOM = ip4_pb2.Ip4.e_im_random_host

    def __init__(self, address='0.0.0.0', mode='FIXED', count=16,
                 mask='255.255.255.0'):
        self.address = address
        self.mode = mode
        self.count = count
        self.mask = mask

    @property
    def mask(self):
        """
        Control which bytes are affected when :attr:`mode` is not set to
        ``FIXED``.
        """
        return str(netaddr.IPAddress(self._mask))

    @mask.setter
    def mask(self, value):
        self._mask = netaddr.IPAddress(value).value

    @property
    def address(self):
        """
        Actual value of the IPv4 address. If :attr:`mode` is one of
        ``INCREMENT``, ``DECREMENT`` or ``RANDOM``, it is the address of the
        initial packet, the next being calculated from this one.
        """
        return str(netaddr.IPAddress(self._address))

    @address.setter
    def address(self, value):
        self._address = netaddr.IPAddress(value).value

    @property
    def mode(self):
        """
        If there are several packets in the stream, the mode determines how the
        IPv4 address of the packets are calculated.

        - ``FIXED``: all the packets will have the IPv4 address :attr:`address`
        - ``INCREMENT``: the IPv4 addresses are incremented by :attr:`step` \
            for each frame, starting from :attr:`address`. After the \
            :attr:`count` th pakcet, it restarts from :attr:`address`. \
            :attr:`mask` controls which bytes are incremented.
        - ``DECREMENT``: the IPv4 addresses are decremented by :attr:`step` \
            for each packet, starting from :attr:`address`. After the \
            :attr:`count` th packet, it restarts from :attr:`address`. \
            :attr:`mask` controls which bytes are incremented.
        - ``RANDOM``: bytes specified by :attr:`mask` are random
        """
        return self._Mode.get_key(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = self._Mode.get_value(value)


class IPv4(autogenerates._IPv4):

    __metaclass__ = baseclass.make_protocol_class

    @property
    def source(self):
        return str(netaddr.IPAddress(self._src_ip))

    @source.setter
    def source(self, value):
        self._src_ip = netaddr.IPAddress(value).value

    @property
    def destination(self):
        return str(netaddr.IPAddress(self._dst_ip))

    @destination.setter
    def destination(self, value):
        self._dst_ip = netaddr.IPAddress(value).value


class Payload(baseclass.Protocol):

    __metaclass__ = baseclass.make_protocol_class

    _protocol_id = 101
    _extension = payload_pb2.payload

    def __init__(self, pattern='00 00 00 00', mode='FIXED_WORD', **kwargs):
        super(Payload, self).__init__(pattern=pattern, mode=mode, **kwargs)
        self.mode = mode
        self.pattern = pattern

    class _Mode(utils.Enum):
        DECREMENT_BYTE = payload_pb2.Payload.e_dp_dec_byte
        FIXED_WORD = payload_pb2.Payload.e_dp_fixed_word
        INCREMENT_BYTE = payload_pb2.Payload.e_dp_inc_byte
        RANDOM = payload_pb2.Payload.e_dp_random

    @property
    def mode(self):
        """
        The mode can be one of:
        - ``DECREMENT_BYTE``
        - ``FIXED_WORD``
        - ``INCREMENT_BYTE``
        - ``RANDOM``
        """
        return self._Mode.get_key(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = self._Mode.get_value(value)

    @property
    def pattern(self):
        """
        Payload initial word. Depending on the chosen mode, this word will be repeated unchanged, incremented/decremented, or randomized
        """
        return utils.to_str(self._pattern)

    @pattern.setter
    def pattern(self, value):
        self._pattern = utils.parse(value)

    def from_dict(self, values):
        for key, value in values.iteritems():
            setattr(self, key, value)

    def to_dict(self):
        return {'pattern': self.pattern,
                'mode': self.mode}

    def _save_pattern(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.pattern = self._pattern

    def _fetch_pattern(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self._pattern = ext.pattern

    def _save_mode(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.pattern_mode = self._mode

    def _fetch_mode(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self._mode = ext.pattern_mode


class Ethernet(autogenerates._Ethernet):

    __metaclass__ = baseclass.make_protocol_class


class Udp(autogenerates._Udp):

    __metaclass__ = baseclass.make_protocol_class


class Tcp(autogenerates._Tcp):

    __metaclass__ = baseclass.make_protocol_class
