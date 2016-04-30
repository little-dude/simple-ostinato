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
    Represent the MAC layer. Since we make a distiction between the MAC layer and the Ethernet layer, this layer defines the source and destination MAC addresses.
    """

    _protocol_id = 100
    _extension = mac_pb2.mac

    def __init__(self, source='00:00:00:00:00:00', destination='FF:FF:FF:FF:FF:FF', **kwargs):
        super(_Mac, self).__init__(source=source, destination=destination, **kwargs)

    @property
    def source(self):
        """
        Source MAC address
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
        Destination MAC address
        """
        return utils.to_str(self._destination)

    @destination.setter
    def destination(self, value):
        self._destination = utils.parse(value)

    def _save_destination(self, ext):
        ext.dst_mac = self._destination

    def _fetch_destination(self, ext):
        self._destination = ext.dst_mac

    def __str__(self):
        return 'Mac(source={},destination={},)'.format(self.source,self.destination,)

    def to_dict(self):
        """
        Return the Mac layer configuration as a
        dictionnary.
        """
        return { 
            'source': self.source,
            'destination': self.destination,
        }

    def from_dict(self):
        """
        Set the Mac layer configuration from a
        dictionary. Keys must be the same as the attributes names, and values
        but by valid values for these attributes.
        """
        for attribute, value in dict_.items():
            setattr(self, attribute, value)


class _Ethernet(baseclass.Protocol):

    """
    Represent the ethernet layer. Since we make a distinction between the MAC layer and the Ethernet layer, this layer only defines the ethernet type
    """

    _protocol_id = 200
    _extension = eth2_pb2.eth2

    def __init__(self, ether_type='0x0800', **kwargs):
        super(_Ethernet, self).__init__(ether_type=ether_type, **kwargs)

    @property
    def ether_type(self):
        """
        Ethernet type field. 0x800 is for IPv4 inner packets.
        """
        return utils.to_str(self._ether_type)

    @ether_type.setter
    def ether_type(self, value):
        self._ether_type = utils.parse(value)

    def _save_ether_type(self, ext):
        ext.type = self._ether_type

    def _fetch_ether_type(self, ext):
        self._ether_type = ext.type

    def __str__(self):
        return 'Ethernet(ether_type={},)'.format(self.ether_type,)

    def to_dict(self):
        """
        Return the Ethernet layer configuration as a
        dictionnary.
        """
        return { 
            'ether_type': self.ether_type,
        }

    def from_dict(self):
        """
        Set the Ethernet layer configuration from a
        dictionary. Keys must be the same as the attributes names, and values
        but by valid values for these attributes.
        """
        for attribute, value in dict_.items():
            setattr(self, attribute, value)


class _IPv4(baseclass.Protocol):

    """
    Represent the IPv4 layer.
    """

    _protocol_id = 301
    _extension = ip4_pb2.ip4

    def __init__(self, protocol=0, flags=0, dscp=0, ttl=127, header_length=5, fragments_offset=0, tos=0, destination='127.0.0.1', source='127.0.0.1', version=4, identification=0, checksum=0, total_length=0, **kwargs):
        super(_IPv4, self).__init__(protocol=protocol, flags=flags, dscp=dscp, ttl=ttl, header_length=header_length, fragments_offset=fragments_offset, tos=tos, destination=destination, source=source, version=version, identification=identification, checksum=checksum, total_length=total_length, **kwargs)

    @property
    def protocol(self):
        """
        Indicates the protocol that is encapsulated in the IP packet.
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
        A three bits field: bit 0 is reserved, bit 1 is the Don't Fragment (DF) flag, and bit 2 is the More Fragments (MF) flags
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
        Differentiated Services Code Point (DSCP) field (previously known as Type Of Service (TOS) field
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
        Time To Live (TTL) field.
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
        Internet Header Length (IHL): number of 4 bytes words in the header. The minimum valid value is 5, and maximum valid value is 15.. By default, this attribute is computed automatically.
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
        The Fragment Offset field indicates the offset of a packet fragment in the original IP packet
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
        Type Of Service (TOS) field. This field is now the Differentiated Services Code Point (DSCP) field.
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
        Destination IP address
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
        Source IP address
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
        Version of the protocol (usually 4 or 6)
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
        Identification field. This is used to identify packet fragments
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
        Header checksum. By default, this attribute is computed automatically.
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
        Total length of the IP packet in bytes. The minimum valid value is 20, and the maxium is 65,535. By default, this attribute is computed automatically.
        """
        return utils.to_str(self._total_length)

    @total_length.setter
    def total_length(self, value):
        self._total_length = utils.parse(value)

    def _save_total_length(self, ext):
        ext.totlen = self._total_length

    def _fetch_total_length(self, ext):
        self._total_length = ext.totlen

    def __str__(self):
        return 'IPv4(protocol={},flags={},dscp={},ttl={},header_length={},fragments_offset={},tos={},destination={},source={},version={},identification={},checksum={},total_length={},)'.format(self.protocol,self.flags,self.dscp,self.ttl,self.header_length,self.fragments_offset,self.tos,self.destination,self.source,self.version,self.identification,self.checksum,self.total_length,)

    def to_dict(self):
        """
        Return the IPv4 layer configuration as a
        dictionnary.
        """
        return { 
            'protocol': self.protocol,
            'flags': self.flags,
            'dscp': self.dscp,
            'ttl': self.ttl,
            'header_length': self.header_length,
            'fragments_offset': self.fragments_offset,
            'tos': self.tos,
            'destination': self.destination,
            'source': self.source,
            'version': self.version,
            'identification': self.identification,
            'checksum': self.checksum,
            'total_length': self.total_length,
        }

    def from_dict(self):
        """
        Set the IPv4 layer configuration from a
        dictionary. Keys must be the same as the attributes names, and values
        but by valid values for these attributes.
        """
        for attribute, value in dict_.items():
            setattr(self, attribute, value)


class _Udp(baseclass.Protocol):

    """
    Represent an UDP datagram
    """

    _protocol_id = 401
    _extension = udp_pb2.udp

    def __init__(self, source=49152, length=0, destination=49153, checksum=0, **kwargs):
        super(_Udp, self).__init__(source=source, length=length, destination=destination, checksum=checksum, **kwargs)

    @property
    def source(self):
        """
        Source port number
        """
        return utils.to_str(self._source)

    @source.setter
    def source(self, value):
        self._source = utils.parse(value)

    def _save_source(self, ext):
        ext.src_port = self._source

    def _fetch_source(self, ext):
        self._source = ext.src_port

    @property
    def length(self):
        """
        Length of the UDP datagram (header and payload).. By default, this attribute is computed automatically.
        """
        return utils.to_str(self._length)

    @length.setter
    def length(self, value):
        self._length = utils.parse(value)

    def _save_length(self, ext):
        ext.totlen = self._length

    def _fetch_length(self, ext):
        self._length = ext.totlen

    @property
    def destination(self):
        """
        Destination port number
        """
        return utils.to_str(self._destination)

    @destination.setter
    def destination(self, value):
        self._destination = utils.parse(value)

    def _save_destination(self, ext):
        ext.dst_port = self._destination

    def _fetch_destination(self, ext):
        self._destination = ext.dst_port

    @property
    def checksum(self):
        """
        Checksum of the datagram, calculated based on the IP pseudo-header.. By default, this attribute is computed automatically.
        """
        return utils.to_str(self._checksum)

    @checksum.setter
    def checksum(self, value):
        self._checksum = utils.parse(value)

    def _save_checksum(self, ext):
        ext.cksum = self._checksum

    def _fetch_checksum(self, ext):
        self._checksum = ext.cksum

    def __str__(self):
        return 'Udp(source={},length={},destination={},checksum={},)'.format(self.source,self.length,self.destination,self.checksum,)

    def to_dict(self):
        """
        Return the Udp layer configuration as a
        dictionnary.
        """
        return { 
            'source': self.source,
            'length': self.length,
            'destination': self.destination,
            'checksum': self.checksum,
        }

    def from_dict(self):
        """
        Set the Udp layer configuration from a
        dictionary. Keys must be the same as the attributes names, and values
        but by valid values for these attributes.
        """
        for attribute, value in dict_.items():
            setattr(self, attribute, value)


class _Tcp(baseclass.Protocol):

    """
    Represent an TCP datagram
    """

    _protocol_id = 400
    _extension = tcp_pb2.tcp

    def __init__(self, flag_ack=0, header_length=0, reserved=0, ack_num=0, flag_rst=0, window_size=0, destination=49153, flag_psh=0, urgent_pointer=0, source=49152, flag_ece=0, flag_urg=0, sequence_num=0, checksum=0, flag_syn=0, flag_cwr=0, flag_fin=0, flag_ns=0, **kwargs):
        super(_Tcp, self).__init__(flag_ack=flag_ack, header_length=header_length, reserved=reserved, ack_num=ack_num, flag_rst=flag_rst, window_size=window_size, destination=destination, flag_psh=flag_psh, urgent_pointer=urgent_pointer, source=source, flag_ece=flag_ece, flag_urg=flag_urg, sequence_num=sequence_num, checksum=checksum, flag_syn=flag_syn, flag_cwr=flag_cwr, flag_fin=flag_fin, flag_ns=flag_ns, **kwargs)

    @property
    def flag_ack(self):
        """
        ACK flag
        """
        return utils.to_str(self._flag_ack)

    @flag_ack.setter
    def flag_ack(self, value):
        self._flag_ack = utils.parse(value)

    def _save_flag_ack(self, ext):
        ext.flags = self._flag_ack

    def _fetch_flag_ack(self, ext):
        self._flag_ack = ext.flags

    @property
    def header_length(self):
        """
        Size of the TCP header in 4 bytes words. This field is also known as "Data offset"
        """
        return utils.to_str(self._header_length)

    @header_length.setter
    def header_length(self, value):
        self._header_length = utils.parse(value)

    def _save_header_length(self, ext):
        ext.hdrlen_rsvd = self._header_length

    def _fetch_header_length(self, ext):
        self._header_length = ext.hdrlen_rsvd

    @property
    def reserved(self):
        """
        Reserved for future use and must be set to 0
        """
        return utils.to_str(self._reserved)

    @reserved.setter
    def reserved(self, value):
        self._reserved = utils.parse(value)

    def _save_reserved(self, ext):
        ext.hdrlen_rsvd = self._reserved

    def _fetch_reserved(self, ext):
        self._reserved = ext.hdrlen_rsvd

    @property
    def ack_num(self):
        """
        Acknowledgement number
        """
        return utils.to_str(self._ack_num)

    @ack_num.setter
    def ack_num(self, value):
        self._ack_num = utils.parse(value)

    def _save_ack_num(self, ext):
        ext.ack_num = self._ack_num

    def _fetch_ack_num(self, ext):
        self._ack_num = ext.ack_num

    @property
    def flag_rst(self):
        """
        Reset the connection
        """
        return utils.to_str(self._flag_rst)

    @flag_rst.setter
    def flag_rst(self, value):
        self._flag_rst = utils.parse(value)

    def _save_flag_rst(self, ext):
        ext.flags = self._flag_rst

    def _fetch_flag_rst(self, ext):
        self._flag_rst = ext.flags

    @property
    def window_size(self):
        """
        Size of the receive window, which specifies the number of window size units that the sender of this segment is currently willing to receive
        """
        return utils.to_str(self._window_size)

    @window_size.setter
    def window_size(self, value):
        self._window_size = utils.parse(value)

    def _save_window_size(self, ext):
        ext.window = self._window_size

    def _fetch_window_size(self, ext):
        self._window_size = ext.window

    @property
    def destination(self):
        """
        Destination port number
        """
        return utils.to_str(self._destination)

    @destination.setter
    def destination(self, value):
        self._destination = utils.parse(value)

    def _save_destination(self, ext):
        ext.dst_port = self._destination

    def _fetch_destination(self, ext):
        self._destination = ext.dst_port

    @property
    def flag_psh(self):
        """
        Push function
        """
        return utils.to_str(self._flag_psh)

    @flag_psh.setter
    def flag_psh(self, value):
        self._flag_psh = utils.parse(value)

    def _save_flag_psh(self, ext):
        ext.flags = self._flag_psh

    def _fetch_flag_psh(self, ext):
        self._flag_psh = ext.flags

    @property
    def urgent_pointer(self):
        """
        Urgent pointer.
        """
        return utils.to_str(self._urgent_pointer)

    @urgent_pointer.setter
    def urgent_pointer(self, value):
        self._urgent_pointer = utils.parse(value)

    def _save_urgent_pointer(self, ext):
        ext.urg_ptr = self._urgent_pointer

    def _fetch_urgent_pointer(self, ext):
        self._urgent_pointer = ext.urg_ptr

    @property
    def source(self):
        """
        Source port number
        """
        return utils.to_str(self._source)

    @source.setter
    def source(self, value):
        self._source = utils.parse(value)

    def _save_source(self, ext):
        ext.src_port = self._source

    def _fetch_source(self, ext):
        self._source = ext.src_port

    @property
    def flag_ece(self):
        """
        ECN-Echo flag. Its meaning depends on the :attr:`syn` field value.
        """
        return utils.to_str(self._flag_ece)

    @flag_ece.setter
    def flag_ece(self, value):
        self._flag_ece = utils.parse(value)

    def _save_flag_ece(self, ext):
        ext.flags = self._flag_ece

    def _fetch_flag_ece(self, ext):
        self._flag_ece = ext.flags

    @property
    def flag_urg(self):
        """
        Urgent pointer flag.
        """
        return utils.to_str(self._flag_urg)

    @flag_urg.setter
    def flag_urg(self, value):
        self._flag_urg = utils.parse(value)

    def _save_flag_urg(self, ext):
        ext.flags = self._flag_urg

    def _fetch_flag_urg(self, ext):
        self._flag_urg = ext.flags

    @property
    def sequence_num(self):
        """
        Sequence number of the datagram. Its meaning depends on the :attr:`syn` flag value.
        """
        return utils.to_str(self._sequence_num)

    @sequence_num.setter
    def sequence_num(self, value):
        self._sequence_num = utils.parse(value)

    def _save_sequence_num(self, ext):
        ext.seq_num = self._sequence_num

    def _fetch_sequence_num(self, ext):
        self._sequence_num = ext.seq_num

    @property
    def checksum(self):
        """
        Checksum of the datagram, calculated based on the IP pseudo-header. Its meaning depends on the value og the :attr:`ack` flag.. By default, this attribute is computed automatically.
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
    def flag_syn(self):
        """
        Synchronize sequence numbers
        """
        return utils.to_str(self._flag_syn)

    @flag_syn.setter
    def flag_syn(self, value):
        self._flag_syn = utils.parse(value)

    def _save_flag_syn(self, ext):
        ext.flags = self._flag_syn

    def _fetch_flag_syn(self, ext):
        self._flag_syn = ext.flags

    @property
    def flag_cwr(self):
        """
        Congestion Window Reduced flag
        """
        return utils.to_str(self._flag_cwr)

    @flag_cwr.setter
    def flag_cwr(self, value):
        self._flag_cwr = utils.parse(value)

    def _save_flag_cwr(self, ext):
        ext.flags = self._flag_cwr

    def _fetch_flag_cwr(self, ext):
        self._flag_cwr = ext.flags

    @property
    def flag_fin(self):
        """
        No more data from sender
        """
        return utils.to_str(self._flag_fin)

    @flag_fin.setter
    def flag_fin(self, value):
        self._flag_fin = utils.parse(value)

    def _save_flag_fin(self, ext):
        ext.flags = self._flag_fin

    def _fetch_flag_fin(self, ext):
        self._flag_fin = ext.flags

    @property
    def flag_ns(self):
        """
        ECN-nonce concealment protection (experimental)
        """
        return utils.to_str(self._flag_ns)

    @flag_ns.setter
    def flag_ns(self, value):
        self._flag_ns = utils.parse(value)

    def _save_flag_ns(self, ext):
        ext.hdrlen_rsvd = self._flag_ns

    def _fetch_flag_ns(self, ext):
        self._flag_ns = ext.hdrlen_rsvd

    def __str__(self):
        return 'Tcp(flag_ack={},header_length={},reserved={},ack_num={},flag_rst={},window_size={},destination={},flag_psh={},urgent_pointer={},source={},flag_ece={},flag_urg={},sequence_num={},checksum={},flag_syn={},flag_cwr={},flag_fin={},flag_ns={},)'.format(self.flag_ack,self.header_length,self.reserved,self.ack_num,self.flag_rst,self.window_size,self.destination,self.flag_psh,self.urgent_pointer,self.source,self.flag_ece,self.flag_urg,self.sequence_num,self.checksum,self.flag_syn,self.flag_cwr,self.flag_fin,self.flag_ns,)

    def to_dict(self):
        """
        Return the Tcp layer configuration as a
        dictionnary.
        """
        return { 
            'flag_ack': self.flag_ack,
            'header_length': self.header_length,
            'reserved': self.reserved,
            'ack_num': self.ack_num,
            'flag_rst': self.flag_rst,
            'window_size': self.window_size,
            'destination': self.destination,
            'flag_psh': self.flag_psh,
            'urgent_pointer': self.urgent_pointer,
            'source': self.source,
            'flag_ece': self.flag_ece,
            'flag_urg': self.flag_urg,
            'sequence_num': self.sequence_num,
            'checksum': self.checksum,
            'flag_syn': self.flag_syn,
            'flag_cwr': self.flag_cwr,
            'flag_fin': self.flag_fin,
            'flag_ns': self.flag_ns,
        }

    def from_dict(self):
        """
        Set the Tcp layer configuration from a
        dictionary. Keys must be the same as the attributes names, and values
        but by valid values for these attributes.
        """
        for attribute, value in dict_.items():
            setattr(self, attribute, value)


class _Payload(baseclass.Protocol):

    """
    Represent the payload. This layer can be encapsulated in any other layer
    """

    _protocol_id = 101
    _extension = payload_pb2.payload

    def __init__(self, pattern='00 00 00 00', mode='FIXED_WORD', **kwargs):
        super(_Payload, self).__init__(pattern=pattern, mode=mode, **kwargs)

    @property
    def pattern(self):
        """
        Payload initial word. Depending on the chosen mode, this word will be repeated unchanged, incremented/decremented, or randomized
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
        Mode to generate the payload content
        """
        return utils.to_str(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = utils.parse(value)

    def _save_mode(self, ext):
        ext.pattern_mode = self._mode

    def _fetch_mode(self, ext):
        self._mode = ext.pattern_mode

    def __str__(self):
        return 'Payload(pattern={},mode={},)'.format(self.pattern,self.mode,)

    def to_dict(self):
        """
        Return the Payload layer configuration as a
        dictionnary.
        """
        return { 
            'pattern': self.pattern,
            'mode': self.mode,
        }

    def from_dict(self):
        """
        Set the Payload layer configuration from a
        dictionary. Keys must be the same as the attributes names, and values
        but by valid values for these attributes.
        """
        for attribute, value in dict_.items():
            setattr(self, attribute, value)