import pprint
import netaddr
from ostinato.protocols import mac_pb2, ip4_pb2, payload_pb2
from . import autogenerates
from . import baseclass
from .. import utils


class MacAddress(object):

    class _Mode(utils.Enum):
        INCREMENT = mac_pb2.Mac.e_mm_dec
        FIXED = mac_pb2.Mac.e_mm_fixed
        DECREMENT = mac_pb2.Mac.e_mm_inc

    def __init__(self, address='00:00:00:00:00:00', mode='FIXED', count=16, step=1):
        self.address = address
        self.mode = mode
        self.count = count
        self.step = step

    def from_dict(self, values):
        if 'address' in values:
            self.address = values['address']
        if 'mode' in values:
            self.mode = values['mode']
        if 'count' in values:
            self.count = values['count']
        if 'step' in values:
            self.step = values['step']

    def to_dict(self):
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
        return str(netaddr.EUI(self._address))

    @address.setter
    def address(self, value):
        self._address = netaddr.EUI(value).value

    @property
    def mode(self):
        return self._Mode.get_key(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = self._Mode.get_value(value)


class Mac(autogenerates._Mac):

    __metaclass__ = baseclass.make_protocol_class

    @property
    def source(self):
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

    class _Mode(utils.Enum):
        DECREMENT = ip4_pb2.Ip4.e_im_dec_host
        FIXED = ip4_pb2.Ip4.e_im_fixed
        INCREMENT = ip4_pb2.Ip4.e_im_inc_host
        RANDOM = ip4_pb2.Ip4.e_im_random_host

    def __init__(self, address='0.0.0.0', mode='FIXED', count=16, mask='255.255.255.0'):
        self.address = address
        self.mode = mode
        self.count = count
        self.mask = mask

    def from_dict(self, values):
        if 'address' in values:
            self.address = values['address']
        if 'mode' in values:
            self.mode = values['mode']
        if 'count' in values:
            self.count = values['count']
        if 'mask' in values:
            self.mask = values['mask']

    def to_dict(self):
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
        return str(netaddr.IPAddress(self._mask))

    @mask.setter
    def mask(self, value):
        self._mask = netaddr.IPAddress(value).value

    @property
    def address(self):
        return str(netaddr.IPAddress(self._address))

    @address.setter
    def address(self, value):
        self._address = netaddr.IPAddress(value).value

    @property
    def mode(self):
        return self._Mode.get_key(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = self._Mode.get_value(value)


class IPv4(autogenerates._IPv4):

    __metaclass__ = baseclass.make_protocol_class

    @property
    def source(self):
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
        return (self._ver_hdrlen & 0xf0) >> 4

    @version.setter
    def version(self, value):
        value = (value << 4) & 0xf0
        self._ver_hdrlen = getattr(self, '_ver_hdrlen', 0) & 0x0f + value

    @property
    def header_length(self):
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
        return self._Mode.get_key(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = self._Mode.get_value(value)


class Ethernet(autogenerates._Ethernet):

    __metaclass__ = baseclass.make_protocol_class
