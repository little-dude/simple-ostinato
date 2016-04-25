from ostinato.protocols import arp_pb2, gmp_pb2, ip4over6_pb2, mld_pb2, \
    tcp_pb2, dot2llc_pb2, hexdump_pb2, ip6_pb2, payload_pb2, textproto_pb2, \
    dot2snap_pb2, icmp_pb2, ip6over4_pb2, protocol_pb2, udp_pb2, dot3_pb2, \
    igmp_pb2, ip6over6_pb2, sample_pb2, userscript_pb2, eth2_pb2, ip4_pb2, \
    llc_pb2, snap_pb2, vlan_pb2, fileformat_pb2, ip4over4_pb2, mac_pb2, \
    svlan_pb2, vlanstack_pb2
from . import baseclass
from .. import utils


class _Mac(baseclass.Protocol):

    """
    ['Represent the MAC layer. Since we make a distiction between the MAC layer and', 'the Ethernet layer, this layer defines the source and destination MAC', 'addresses.']
    """

    protocol_id = 100
    _extension = mac_pb2.mac

    def __init__(self, source='FF:FF:FF:FF:FF:FF', destination='00:00:00:00:00:00', **kwargs):
        super(_Mac, self).__init__(source=source, destination=destination, **kwargs)

    @property
    def source(self):
        """
        ['Source MAC address']
        """
        return utils.to_str(self._source)

    @source.setter
    def source(self, value):
        self._source = utils.parse(value)

    def _save_source(self, ext):
        ext.src_mac = self._source

    def _fetch_source(self, ext):
        self._source = ext.src_mac

    @property
    def destination(self):
        """
        ['Destination MAC address']
        """
        return utils.to_str(self._destination)

    @destination.setter
    def destination(self, value):
        self._destination = utils.parse(value)

    def _save_destination(self, ext):
        ext.dst_mac = self._destination

    def _fetch_destination(self, ext):
        self._destination = ext.dst_mac


class _Ethernet(baseclass.Protocol):

    """
    ['Represent the ethernet layer. Since we make a distinction between the MAC layer', 'and the Ethernet layer, this layer only defines the ethernet type']
    """

    protocol_id = 200
    _extension = eth2_pb2.eth2

    def __init__(self, ether_type='0x0800', **kwargs):
        super(_Ethernet, self).__init__(ether_type=ether_type, **kwargs)

    @property
    def ether_type(self):
        """
        ['Ethernet type field. 0x800 is for IPv4 inner packets.']
        """
        return utils.to_str(self._ether_type)

    @ether_type.setter
    def ether_type(self, value):
        self._ether_type = utils.parse(value)

    def _save_ether_type(self, ext):
        ext.type = self._ether_type

    def _fetch_ether_type(self, ext):
        self._ether_type = ext.type


class _IPv4(baseclass.Protocol):

    """
    ['Represent the IPv4 layer.']
    """

    protocol_id = 301
    _extension = ip4_pb2.ip4

    def __init__(self, protocol=0, flags=0, dscp=0, ttl=127, header_length=5, fragments_offset=0, tos=0, destination='127.0.0.1', source='127.0.0.1', version=4, identification=0, checksum=0, total_length=0, **kwargs):
        super(_IPv4, self).__init__(protocol=protocol, flags=flags, dscp=dscp, ttl=ttl, header_length=header_length, fragments_offset=fragments_offset, tos=tos, destination=destination, source=source, version=version, identification=identification, checksum=checksum, total_length=total_length, **kwargs)

    @property
    def protocol(self):
        """
        ['Indicates the protocol that is encapsulated in the IP packet.']
        """
        return utils.to_str(self._protocol)

    @protocol.setter
    def protocol(self, value):
        self._protocol = utils.parse(value)

    def _save_protocol(self, ext):
        ext.proto = self._protocol

    def _fetch_protocol(self, ext):
        self._protocol = ext.proto

    @property
    def flags(self):
        """
        ["A three bits field: bit 0 is reserved, bit 1 is the Don't Fragment (DF) flag,", 'and bit 2 is the More Fragments (MF) flags']
        """
        return utils.to_str(self._flags)

    @flags.setter
    def flags(self, value):
        self._flags = utils.parse(value)

    def _save_flags(self, ext):
        ext.flags = self._flags

    def _fetch_flags(self, ext):
        self._flags = ext.flags

    @property
    def dscp(self):
        """
        ['Differentiated Services Code Point (DSCP) field (previously known as Type Of', 'Service (TOS) field']
        """
        return utils.to_str(self._dscp)

    @dscp.setter
    def dscp(self, value):
        self._dscp = utils.parse(value)

    def _save_dscp(self, ext):
        ext.tos = self._dscp

    def _fetch_dscp(self, ext):
        self._dscp = ext.tos

    @property
    def ttl(self):
        """
        ['Time To Live (TTL) field.']
        """
        return utils.to_str(self._ttl)

    @ttl.setter
    def ttl(self, value):
        self._ttl = utils.parse(value)

    def _save_ttl(self, ext):
        ext.ttl = self._ttl

    def _fetch_ttl(self, ext):
        self._ttl = ext.ttl

    @property
    def header_length(self):
        """
        ['Internet Header Length (IHL): number of 4 bytes words in the header. The', 'minimum valid value is 5, and maximum valid value is 15. By default, this', 'attribute is computed automatically.']
        """
        return utils.to_str(self._header_length)

    @header_length.setter
    def header_length(self, value):
        self._header_length = utils.parse(value)

    def _save_header_length(self, ext):
        ext.ver_hdrlen = self._header_length

    def _fetch_header_length(self, ext):
        self._header_length = ext.ver_hdrlen

    @property
    def fragments_offset(self):
        """
        ['The Fragment Offset field indicates the offset of a packet fragment in the', 'original IP packet']
        """
        return utils.to_str(self._fragments_offset)

    @fragments_offset.setter
    def fragments_offset(self, value):
        self._fragments_offset = utils.parse(value)

    def _save_fragments_offset(self, ext):
        ext.frag_ofs = self._fragments_offset

    def _fetch_fragments_offset(self, ext):
        self._fragments_offset = ext.frag_ofs

    @property
    def tos(self):
        """
        ['Type Of Service (TOS) field. This field is now the Differentiated Services Code', 'Point (DSCP) field.']
        """
        return utils.to_str(self._tos)

    @tos.setter
    def tos(self, value):
        self._tos = utils.parse(value)

    def _save_tos(self, ext):
        ext.tos = self._tos

    def _fetch_tos(self, ext):
        self._tos = ext.tos

    @property
    def destination(self):
        """
        ['Destination IP address']
        """
        return utils.to_str(self._destination)

    @destination.setter
    def destination(self, value):
        self._destination = utils.parse(value)

    def _save_destination(self, ext):
        ext.dst_ip = self._destination

    def _fetch_destination(self, ext):
        self._destination = ext.dst_ip

    @property
    def source(self):
        """
        ['Source IP address']
        """
        return utils.to_str(self._source)

    @source.setter
    def source(self, value):
        self._source = utils.parse(value)

    def _save_source(self, ext):
        ext.src_ip = self._source

    def _fetch_source(self, ext):
        self._source = ext.src_ip

    @property
    def version(self):
        """
        ['Version of the protocol (usually 4 or 6)']
        """
        return utils.to_str(self._version)

    @version.setter
    def version(self, value):
        self._version = utils.parse(value)

    def _save_version(self, ext):
        ext.ver_hdrlen = self._version

    def _fetch_version(self, ext):
        self._version = ext.ver_hdrlen

    @property
    def identification(self):
        """
        ['Identification field. This is used to identify packet fragments']
        """
        return utils.to_str(self._identification)

    @identification.setter
    def identification(self, value):
        self._identification = utils.parse(value)

    def _save_identification(self, ext):
        ext.id = self._identification

    def _fetch_identification(self, ext):
        self._identification = ext.id

    @property
    def checksum(self):
        """
        ['Header checksum By default, this attribute is computed automatically.']
        """
        return utils.to_str(self._checksum)

    @checksum.setter
    def checksum(self, value):
        self._checksum = utils.parse(value)

    def _save_checksum(self, ext):
        ext.cksum = self._checksum

    def _fetch_checksum(self, ext):
        self._checksum = ext.cksum

    @property
    def total_length(self):
        """
        ['Total length of the IP packet in bytes. The minimum valid value is 20, and the', 'maxium is 65,535 By default, this attribute is computed automatically.']
        """
        return utils.to_str(self._total_length)

    @total_length.setter
    def total_length(self, value):
        self._total_length = utils.parse(value)

    def _save_total_length(self, ext):
        ext.totlen = self._total_length

    def _fetch_total_length(self, ext):
        self._total_length = ext.totlen


class _Payload(baseclass.Protocol):

    """
    ['Represent the payload. This layer can be encapsulated in any other layer']
    """

    protocol_id = 101
    _extension = payload_pb2.payload

    def __init__(self, pattern='00 00 00 00', mode='FIXED_WORD', **kwargs):
        super(_Payload, self).__init__(pattern=pattern, mode=mode, **kwargs)

    @property
    def pattern(self):
        """
        ['Payload initial word. Depending on the chosen mode, this word will be repeated', 'unchanged, incremented/decremented, or randomized']
        """
        return utils.to_str(self._pattern)

    @pattern.setter
    def pattern(self, value):
        self._pattern = utils.parse(value)

    def _save_pattern(self, ext):
        ext.pattern = self._pattern

    def _fetch_pattern(self, ext):
        self._pattern = ext.pattern

    @property
    def mode(self):
        """
        ['Mode to generate the payload content']
        """
        return utils.to_str(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = utils.parse(value)

    def _save_mode(self, ext):
        ext.pattern_mode = self._mode

    def _fetch_mode(self, ext):
        self._mode = ext.pattern_mode
