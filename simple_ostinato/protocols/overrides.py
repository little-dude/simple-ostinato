import pprint
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

    def from_dict(self, values):
        """
        Get the MAC address configuration from a dictionary.

        >>> mymac = MacAddress()
        >>> mymac.from_dict({'address': '00:11:22:33:44:55', 'mode': \
'INCREMENT', 'count': 255, 'step': 1})
        """
        if 'address' in values:
            self.address = values['address']
        if 'mode' in values:
            self.mode = values['mode']
        if 'count' in values:
            self.count = values['count']
        if 'step' in values:
            self.step = values['step']

    def to_dict(self):
        """
        Return the MAC address configuration as a dictionary
        """
        return {
            'address': self.address,
            'mode': self.mode,
            'count': self.count,
            'step': self.step
        }

    def __str__(self):
        return pprint.pformat(self.to_dict())

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
        Source MAC address. It works exactly as :attr:`destination`.
        """
        return self._source

    @source.setter
    def source(self, value):
        if getattr(self, '_source', None) is None:
            self._source = MacAddress()
        if isinstance(value, dict):
            self._source.from_dict(value)
        elif isinstance(value, MacAddress):
            self._source = value
        else:
            self._source.address = value

    @property
    def destination(self):
        """
        Destination MAC address. Under the hood, it is a :class:`MacAddress`:

            >>> mac = Mac()
            >>> dst = MacAddress()
            >>> dst.address = '00:00:00:aa:bb:cc'
            >>> dst.mode = 'INCREMENT'
            >>> dst.count = 255
            >>> dst.step = 8
            >>> mac.destination = dst

        However, for simple cases, it's cumbersome, so it also accepts a string
        or an in representing the MAC address value as input. Internally, a
        :class:`MacAddress` object is created. Here is an equivalent version of
        the above example:

            >>> mac = Mac()
            >>> mac.destination = '00:00:00:aa:bb:cc'
            >>> mac.destination.mode = 'INCREMENT'
            >>> mac.destination.count = 255
            >>> mac.destination.step = 8

        Note the the MacAddress object is not returned when accessing this
        attribute. Only a string representation of the MAC address value:

            >>> isinstance(mac.destination, MacAddress)
            False
            >>> isinstance(mac.destination, str)
            True
            >>> print mac.destination
            00:00:00:aa:bb:cc
        """
        return self._destination

    @destination.setter
    def destination(self, value):
        if getattr(self, '_destination', None) is None:
            self._destination = MacAddress()
        if isinstance(value, dict):
            self._destination.from_dict(value)
        elif isinstance(value, MacAddress):
            self._destination = value
        else:
            self._destination.address = value

    def _save_destination(self, ext):
        ext.dst_mac = self._destination._address
        ext.dst_mac_mode = self._destination._mode
        ext.dst_mac_count = self._destination.count
        ext.dst_mac_step = self._destination.step

    def _save_source(self, ext):
        ext.src_mac = self._source._address
        ext.src_mac_mode = self._source._mode
        ext.src_mac_count = self._source.count
        ext.src_mac_step = self._source.step

    def _fetch_destination(self, ext):
        self._destination._address = ext.dst_mac
        self._destination._mode = ext.dst_mac_mode
        self._destination.count = ext.dst_mac_count
        self._destination.step = ext.dst_mac_step

    def _fetch_source(self, ext):
        self._source._address = ext.src_mac
        self._source._mode = ext.src_mac_mode
        self._source.count = ext.src_mac_count
        self._source.step = ext.src_mac_step


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

    def from_dict(self, values):
        """
        Configure the IP address from a dictionary.

            >>> ip = IPv4Address()
            >>> ip.from_dict({'address': '1.0.0.1', 'mode': 'RANDOM', 'count':\
 '10', 'mask': '255.0.225.255'})
        """
        if 'address' in values:
            self.address = values['address']
        if 'mode' in values:
            self.mode = values['mode']
        if 'count' in values:
            self.count = values['count']
        if 'mask' in values:
            self.mask = values['mask']

    def to_dict(self):
        """
        Return the IP address configuration as a dictionary
        """
        return {
            'address': self.address,
            'mode': self.mode,
            'count': self.count,
            'mask': self.mask
        }

    def __str__(self):
        return pprint.pformat(self.to_dict())

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
        """
        Source IPv4 address. See :attr:`destination`.
        """
        return self._source

    @source.setter
    def source(self, value):
        if getattr(self, '_source', None) is None:
            self._source = IPv4Address()
        if isinstance(value, dict):
            self._source.from_dict(value)
        elif isinstance(value, IPv4Address):
            self._source = value
        else:
            self._source.address = value

    @property
    def destination(self):
        """
        IPv4 destination address. Under the hood, it is a :class:`IPv4Address`:

            >>> pkt = IPv4()
            >>> dst = IPv4Address()
            >>> dst.address = '1.2.3.4'
            >>> dst.mode = 'INCREMENT'
            >>> dst.mask = '255.0.255.255'
            >>> dst.count = 50
            >>> pkt.destination = dst

        However, for simple cases, it's cumbersome, so it also accepts a string
        or an in representing the IPv4 address value as input. Internally, a
        :class:`IPAddress` object is created. Here is an equivalent version of
        the above example:

            >>> pkt = IPv4()
            >>> pkt.destination = '1.2.3.4'
            >>> pkt.destination.mode = 'INCREMENT'
            >>> pkt.destination.count = 50
            >>> pkt.destination.mask = '255.0.255.255'

        Note the the :class:`Ipv4Address` object is not returned when accessing
        this attribute. Only a string representation of the IP address value:

            >>> isinstance(pkt.destination, IPv4Address)
            False
            >>> isinstance(pkt.destination, str)
            True
            >>> print pkt.destination
            '1.2.3.4'
        """
        return self._destination

    @destination.setter
    def destination(self, value):
        if getattr(self, '_destination', None) is None:
            self._destination = IPv4Address()
        if isinstance(value, dict):
            self._destination.from_dict(value)
        elif isinstance(value, IPv4Address):
            self._destination = value
        else:
            self._destination.address = value

    def _save_destination(self, ext):
        ext.dst_ip = self._destination._address
        ext.dst_ip_mode = self._destination._mode
        ext.dst_ip_count = self._destination.count
        ext.dst_ip_mask = self._destination._mask

    def _save_source(self, ext):
        ext.src_ip = self._source._address
        ext.src_ip_mode = self._source._mode
        ext.src_ip_count = self._source.count
        ext.src_ip_mask = self._source._mask

    def _fetch_destination(self, ext):
        self._destination._address = ext.dst_ip
        self._destination._mode = ext.dst_ip_mode
        self._destination.count = ext.dst_ip_count
        self._destination._mask = ext.dst_ip_mask

    def _fetch_source(self, ext):
        self._source._address = ext.src_ip
        self._source._mode = ext.src_ip_mode
        self._source.count = ext.src_ip_count
        self._source._mask = ext.src_ip_mask

    @property
    def _header_length(self):
        return self._ver_hdrlen

    @property
    def _version(self):
        return self._ver_hdrlen

    @_header_length.setter
    def _header_length(self, value):
        self._ver_hdrlen = value

    @_version.setter
    def _version(self, value):
        self._ver_hdrlen = value

    @property
    def version(self):
        """
        Version of the IP protocol. For IPv4, it is  normally set to ``4``.
        """
        return (self._ver_hdrlen & 0xf0) >> 4

    @version.setter
    def version(self, value):
        value = (value << 4) & 0xf0
        self._ver_hdrlen = getattr(self, '_ver_hdrlen', 0) & 0x0f + value

    @property
    def header_length(self):
        """
        Header length, in words of 5 bytes.
        """
        return self._ver_hdrlen & 0x0f

    @header_length.setter
    def header_length(self, value):
        self._ver_hdrlen = getattr(self, '_ver_hdrlen', 0) & 0xf0 + value


class Payload(autogenerates._Payload):

    __metaclass__ = baseclass.make_protocol_class

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


class Ethernet(autogenerates._Ethernet):

    __metaclass__ = baseclass.make_protocol_class


class Udp(autogenerates._Udp):

    __metaclass__ = baseclass.make_protocol_class


class Tcp(autogenerates._Tcp):

    __metaclass__ = baseclass.make_protocol_class

    @property
    def _header_length(self):
        return (self._hrn & 0b11110000) >> 4

    @property
    def _reserved(self):
        return (self._hrn & 0b00001110) >> 1

    @property
    def _flag_ns(self):
        return self._hrn & 0b00000001

    @_header_length.setter
    def _header_length(self, value):
        hrn = getattr(self, '_hrn', 0)
        self._hrn = (hrn & 0b00001111) + ((value << 4) & 0b11110000)

    @_reserved.setter
    def _reserved(self, value):
        hrn = getattr(self, '_hrn', 0)
        self._hrn = (hrn & 0b11110001) + ((value << 1) & 0b00001110)

    @_flag_ns.setter
    def _flag_ns(self, value):
        hrn = getattr(self, '_hrn', 0)
        self._hrn = (hrn & 0b11110001) + (value & 0b00000001)

    def _save_header_length(self, ext):
        ext.hdrlen_rsvd = self._hrn

    def _save_reserved(self, ext):
        ext.hdrlen_rsvd = self._hrn

    def _save_flag_ns(self, ext):
        ext.hdrlen_rsvd = self._hrn

    def _fetch_header_length(self, ext):
        self._hrn = ext.hdrlen_rsvd

    def _fetch_reserved(self, ext):
        self._hrn = ext.hdrlen_rsvd

    def _fetch_flag_ns(self, ext):
        self._hrn = ext.hdrlen_rsvd

    @property
    def _flag_cwr(self):
        return (self._flags & 0b10000000) >> 7

    @_flag_cwr.setter
    def _flag_cwr(self, value):
        flags = getattr(self, '_flags', 0)
        self._flags = (flags & 0b01111111) + ((value << 7) & 0b10000000)

    def _save_flag_cwr(self, ext):
        ext.flags = self._flags

    def _fetch_flag_cwr(self, ext):
        self._flags = ext.flags

    @property
    def _flag_ece(self):
        return (self._flags & 0b01000000) >> 6

    @_flag_ece.setter
    def _flag_ece(self, value):
        flags = getattr(self, '_flags', 0)
        self._flags = (flags & 0b10111111) + ((value << 6) & 0b01000000)

    def _save_flag_ece(self, ext):
        ext.flags = self._flags

    def _fetch_flag_ece(self, ext):
        self._flags = ext.flags

    @property
    def _flag_urg(self):
        return (self._flags & 0b00100000) >> 5

    @_flag_urg.setter
    def _flag_urg(self, value):
        flags = getattr(self, '_flags', 0)
        self._flags = (flags & 0b11011111) + ((value << 5) & 0b00100000)

    def _save_flag_urg(self, ext):
        ext.flags = self._flags

    def _fetch_flag_urg(self, ext):
        self._flags = ext.flags

    @property
    def _flag_ack(self):
        return (self._flags & 0b00010000) >> 4

    @_flag_ack.setter
    def _flag_ack(self, value):
        flags = getattr(self, '_flags', 0)
        self._flags = (flags & 0b11101111) + ((value << 4) & 0b00010000)

    def _save_flag_ack(self, ext):
        ext.flags = self._flags

    def _fetch_flag_ack(self, ext):
        self._flags = ext.flags

    @property
    def _flag_psh(self):
        return (self._flags & 0b00001000) >> 3

    @_flag_psh.setter
    def _flag_psh(self, value):
        flags = getattr(self, '_flags', 0)
        self._flags = (flags & 0b11110111) + ((value << 3) & 0b00001000)

    def _save_flag_psh(self, ext):
        ext.flags = self._flags

    def _fetch_flag_psh(self, ext):
        self._flags = ext.flags

    @property
    def _flag_rst(self):
        return (self._flags & 0b00000100) >> 2

    @_flag_rst.setter
    def _flag_rst(self, value):
        flags = getattr(self, '_flags', 0)
        self._flags = (flags & 0b11111011) + ((value << 2) & 0b00000100)

    def _save_flag_rst(self, ext):
        ext.flags = self._flags

    def _fetch_flag_rst(self, ext):
        self._flags = ext.flags

    @property
    def _flag_syn(self):
        return (self._flags & 0b00000010) >> 1

    @_flag_syn.setter
    def _flag_syn(self, value):
        flags = getattr(self, '_flags', 0)
        self._flags = (flags & 0b11111101) + ((value << 1) & 0b00000010)

    def _save_flag_syn(self, ext):
        ext.flags = self._flags

    def _fetch_flag_syn(self, ext):
        self._flags = ext.flags

    @property
    def _flag_fin(self):
        return self._flags & 0b00000001

    @_flag_fin.setter
    def _flag_fin(self, value):
        flags = getattr(self, '_flags', 0)
        self._flags = flags & 0b11111110 + value & 0b00000010

    def _save_flag_fin(self, ext):
        ext.flags = self._flags

    def _fetch_flag_fin(self, ext):
        self._flags = ext.flags
