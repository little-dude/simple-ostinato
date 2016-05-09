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
        
        self.source_mode = 'FIXED'
        self.source_step = 1 << 0
        self.source_count = 1
        self.destination_mode = 'FIXED'
        self.destination_step = 1 << 0
        self.destination_count = 1

    @property
    def source(self):
        """
        Source MAC address
        """
        return self._src_mac & 281474976710655

    @source.setter
    def source(self, value):
        current_value = getattr(self, '_src_mac', 0)
        self._src_mac = (current_value & (~281474976710655 & 281474976710655)) + ((utils.parse(value) << 0) & 281474976710655)

    @property
    def source_mode(self):
        """
        By default, :attr:`source_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._source_mode)

    @source_mode.setter
    def source_mode(self, mode):
        self._source_mode = baseclass.FieldMode.get_value(mode)

    _source_offset = 6
    _source_type = 2
    _source_full_mask = 281474976710655
    _source_mask = 281474976710655

    @property
    def source_step(self):
        """
        If :attr:`source_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._source_step >> 0

    @source_step.setter
    def source_step(self, step):
        self._source_step = step << 0

    @property
    def source_count(self):
        """
        If :attr:`source_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._source_count

    @source_count.setter
    def source_count(self, count):
        self._source_count = count

    def _save_source(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.source_mode == 'FIXED':
            ext.src_mac = self._src_mac
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._source_step
            o_variable_field.mask = self._source_mask
            o_variable_field.type = self._source_type
            o_variable_field.offset = self._source_offset
            o_variable_field.mode = self._source_mode
            o_variable_field.count = self._source_count
            o_variable_field.value = self._src_mac

    def _fetch_source(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._source_offset and mask == self._source_mask:
                self._src_mac = o_variable_field.value
                self._source_mode = o_variable_field.mode
                self._source_count = o_variable_field.count
                self._source_step = o_variable_field.step
                return
        else:
            self._src_mac = ext.src_mac

    @property
    def destination(self):
        """
        Destination MAC address
        """
        return self._dst_mac & 281474976710655

    @destination.setter
    def destination(self, value):
        current_value = getattr(self, '_dst_mac', 0)
        self._dst_mac = (current_value & (~281474976710655 & 281474976710655)) + ((utils.parse(value) << 0) & 281474976710655)

    @property
    def destination_mode(self):
        """
        By default, :attr:`destination_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._destination_mode)

    @destination_mode.setter
    def destination_mode(self, mode):
        self._destination_mode = baseclass.FieldMode.get_value(mode)

    _destination_offset = 0
    _destination_type = 2
    _destination_full_mask = 281474976710655
    _destination_mask = 281474976710655

    @property
    def destination_step(self):
        """
        If :attr:`destination_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._destination_step >> 0

    @destination_step.setter
    def destination_step(self, step):
        self._destination_step = step << 0

    @property
    def destination_count(self):
        """
        If :attr:`destination_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._destination_count

    @destination_count.setter
    def destination_count(self, count):
        self._destination_count = count

    def _save_destination(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.destination_mode == 'FIXED':
            ext.dst_mac = self._dst_mac
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._destination_step
            o_variable_field.mask = self._destination_mask
            o_variable_field.type = self._destination_type
            o_variable_field.offset = self._destination_offset
            o_variable_field.mode = self._destination_mode
            o_variable_field.count = self._destination_count
            o_variable_field.value = self._dst_mac

    def _fetch_destination(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._destination_offset and mask == self._destination_mask:
                self._dst_mac = o_variable_field.value
                self._destination_mode = o_variable_field.mode
                self._destination_count = o_variable_field.count
                self._destination_step = o_variable_field.step
                return
        else:
            self._dst_mac = ext.dst_mac

    def __str__(self):
        return 'Mac(source={},destination={},)'.format(self.source,self.destination,)

    def to_dict(self):
        """
        Return the Mac layer configuration as a
        dictionnary.
        """
        return { 
            'source': self.source,
            'source_mode': self.source_mode,
            'source_count': self.source_count,
            'source_step': self.source_step,
            'destination': self.destination,
            'destination_mode': self.destination_mode,
            'destination_count': self.destination_count,
            'destination_step': self.destination_step,
        }

    def from_dict(self, dict_):
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
        
        self.ether_type_mode = 'FIXED'
        self.ether_type_step = 1 << 0
        self.ether_type_count = 1
        self.ether_type_override = False

    @property
    def ether_type(self):
        """
        Ethernet type field. 0x800 is for IPv4 inner packets.. By default, this attribute is set automatically. Set :attr:`ether_type_override` to ``True`` to override this field
        """
        return self._type & 65535

    @ether_type.setter
    def ether_type(self, value):
        current_value = getattr(self, '_type', 0)
        self._type = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def ether_type_mode(self):
        """
        By default, :attr:`ether_type_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._ether_type_mode)

    @ether_type_mode.setter
    def ether_type_mode(self, mode):
        self._ether_type_mode = baseclass.FieldMode.get_value(mode)

    _ether_type_offset = 0
    _ether_type_type = 1
    _ether_type_full_mask = 65535
    _ether_type_mask = 65535

    @property
    def ether_type_step(self):
        """
        If :attr:`ether_type_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._ether_type_step >> 0

    @ether_type_step.setter
    def ether_type_step(self, step):
        self._ether_type_step = step << 0

    @property
    def ether_type_count(self):
        """
        If :attr:`ether_type_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._ether_type_count

    @ether_type_count.setter
    def ether_type_count(self, count):
        self._ether_type_count = count

    @property
    def ether_type_override(self):
        return self._ether_type_override

    @ether_type_override.setter
    def ether_type_override(self, override):
        self._ether_type_override = override

    def _save_ether_type(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_type = self.ether_type_override
        if self.ether_type_mode == 'FIXED':
            ext.type = self._type
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._ether_type_step
            o_variable_field.mask = self._ether_type_mask
            o_variable_field.type = self._ether_type_type
            o_variable_field.offset = self._ether_type_offset
            o_variable_field.mode = self._ether_type_mode
            o_variable_field.count = self._ether_type_count
            o_variable_field.value = self._type

    def _fetch_ether_type(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.ether_type_override = ext.is_override_type
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._ether_type_offset and mask == self._ether_type_mask:
                self._type = o_variable_field.value
                self._ether_type_mode = o_variable_field.mode
                self._ether_type_count = o_variable_field.count
                self._ether_type_step = o_variable_field.step
                return
        else:
            self._type = ext.type

    def __str__(self):
        return 'Ethernet(ether_type={},)'.format(self.ether_type,)

    def to_dict(self):
        """
        Return the Ethernet layer configuration as a
        dictionnary.
        """
        return { 
            'ether_type': self.ether_type,
            'ether_type_mode': self.ether_type_mode,
            'ether_type_count': self.ether_type_count,
            'ether_type_step': self.ether_type_step,
            'ether_type_override': self.ether_type_override,
        }

    def from_dict(self, dict_):
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

    def __init__(self, flag_unused=0, dscp=0, flag_mf=0, ttl=127, protocol=0, header_length=5, fragments_offset=0, tos=0, destination='127.0.0.1', source='127.0.0.1', version=4, identification=0, checksum=0, flag_df=0, total_length=0, **kwargs):
        super(_IPv4, self).__init__(flag_unused=flag_unused, dscp=dscp, flag_mf=flag_mf, ttl=ttl, protocol=protocol, header_length=header_length, fragments_offset=fragments_offset, tos=tos, destination=destination, source=source, version=version, identification=identification, checksum=checksum, flag_df=flag_df, total_length=total_length, **kwargs)
        
        self.flag_unused_mode = 'FIXED'
        self.flag_unused_step = 1 << 2
        self.flag_unused_count = 1
        self.dscp_mode = 'FIXED'
        self.dscp_step = 1 << 0
        self.dscp_count = 1
        self.flag_mf_mode = 'FIXED'
        self.flag_mf_step = 1 << 0
        self.flag_mf_count = 1
        self.ttl_mode = 'FIXED'
        self.ttl_step = 1 << 0
        self.ttl_count = 1
        self.protocol_mode = 'FIXED'
        self.protocol_step = 1 << 0
        self.protocol_count = 1
        self.protocol_override = False
        self.header_length_mode = 'FIXED'
        self.header_length_step = 1 << 0
        self.header_length_count = 1
        self.header_length_override = False
        self.fragments_offset_mode = 'FIXED'
        self.fragments_offset_step = 1 << 0
        self.fragments_offset_count = 1
        self.tos_mode = 'FIXED'
        self.tos_step = 1 << 0
        self.tos_count = 1
        self.destination_mode = 'FIXED'
        self.destination_step = 1 << 0
        self.destination_count = 1
        self.source_mode = 'FIXED'
        self.source_step = 1 << 0
        self.source_count = 1
        self.version_mode = 'FIXED'
        self.version_step = 1 << 4
        self.version_count = 1
        self.version_override = False
        self.identification_mode = 'FIXED'
        self.identification_step = 1 << 0
        self.identification_count = 1
        self.checksum_mode = 'FIXED'
        self.checksum_step = 1 << 0
        self.checksum_count = 1
        self.checksum_override = False
        self.flag_df_mode = 'FIXED'
        self.flag_df_step = 1 << 1
        self.flag_df_count = 1
        self.total_length_mode = 'FIXED'
        self.total_length_step = 1 << 0
        self.total_length_count = 1
        self.total_length_override = False

    @property
    def flag_unused(self):
        """
        A 1 bit unused flag
        """
        return (self._flags & 4) >> 2

    @flag_unused.setter
    def flag_unused(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~4 & 255)) + ((utils.parse(value) << 2) & 4)

    @property
    def flag_unused_mode(self):
        """
        By default, :attr:`flag_unused_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_unused_mode)

    @flag_unused_mode.setter
    def flag_unused_mode(self, mode):
        self._flag_unused_mode = baseclass.FieldMode.get_value(mode)

    _flag_unused_offset = 6
    _flag_unused_type = 0
    _flag_unused_full_mask = 255
    _flag_unused_mask = 4

    @property
    def flag_unused_step(self):
        """
        If :attr:`flag_unused_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_unused_step >> 2

    @flag_unused_step.setter
    def flag_unused_step(self, step):
        self._flag_unused_step = step << 2

    @property
    def flag_unused_count(self):
        """
        If :attr:`flag_unused_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_unused_count

    @flag_unused_count.setter
    def flag_unused_count(self, count):
        self._flag_unused_count = count

    def _save_flag_unused(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_unused_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_unused_step
            o_variable_field.mask = self._flag_unused_mask
            o_variable_field.type = self._flag_unused_type
            o_variable_field.offset = self._flag_unused_offset
            o_variable_field.mode = self._flag_unused_mode
            o_variable_field.count = self._flag_unused_count
            o_variable_field.value = self._flags

    def _fetch_flag_unused(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_unused_offset and mask == self._flag_unused_mask:
                self._flags = o_variable_field.value
                self._flag_unused_mode = o_variable_field.mode
                self._flag_unused_count = o_variable_field.count
                self._flag_unused_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def dscp(self):
        """
        Differentiated Services Code Point (DSCP) field (previously known as Type Of Service (TOS) field
        """
        return self._tos & 255

    @dscp.setter
    def dscp(self, value):
        current_value = getattr(self, '_tos', 0)
        self._tos = (current_value & (~255 & 255)) + ((utils.parse(value) << 0) & 255)

    @property
    def dscp_mode(self):
        """
        By default, :attr:`dscp_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._dscp_mode)

    @dscp_mode.setter
    def dscp_mode(self, mode):
        self._dscp_mode = baseclass.FieldMode.get_value(mode)

    _dscp_offset = 1
    _dscp_type = 0
    _dscp_full_mask = 255
    _dscp_mask = 255

    @property
    def dscp_step(self):
        """
        If :attr:`dscp_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._dscp_step >> 0

    @dscp_step.setter
    def dscp_step(self, step):
        self._dscp_step = step << 0

    @property
    def dscp_count(self):
        """
        If :attr:`dscp_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._dscp_count

    @dscp_count.setter
    def dscp_count(self, count):
        self._dscp_count = count

    def _save_dscp(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.dscp_mode == 'FIXED':
            ext.tos = self._tos
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._dscp_step
            o_variable_field.mask = self._dscp_mask
            o_variable_field.type = self._dscp_type
            o_variable_field.offset = self._dscp_offset
            o_variable_field.mode = self._dscp_mode
            o_variable_field.count = self._dscp_count
            o_variable_field.value = self._tos

    def _fetch_dscp(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._dscp_offset and mask == self._dscp_mask:
                self._tos = o_variable_field.value
                self._dscp_mode = o_variable_field.mode
                self._dscp_count = o_variable_field.count
                self._dscp_step = o_variable_field.step
                return
        else:
            self._tos = ext.tos

    @property
    def flag_mf(self):
        """
        The "More Fragments" (MF) 1 bit flag
        """
        return self._flags & 1

    @flag_mf.setter
    def flag_mf(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~1 & 255)) + ((utils.parse(value) << 0) & 1)

    @property
    def flag_mf_mode(self):
        """
        By default, :attr:`flag_mf_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_mf_mode)

    @flag_mf_mode.setter
    def flag_mf_mode(self, mode):
        self._flag_mf_mode = baseclass.FieldMode.get_value(mode)

    _flag_mf_offset = 6
    _flag_mf_type = 0
    _flag_mf_full_mask = 255
    _flag_mf_mask = 1

    @property
    def flag_mf_step(self):
        """
        If :attr:`flag_mf_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_mf_step >> 0

    @flag_mf_step.setter
    def flag_mf_step(self, step):
        self._flag_mf_step = step << 0

    @property
    def flag_mf_count(self):
        """
        If :attr:`flag_mf_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_mf_count

    @flag_mf_count.setter
    def flag_mf_count(self, count):
        self._flag_mf_count = count

    def _save_flag_mf(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_mf_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_mf_step
            o_variable_field.mask = self._flag_mf_mask
            o_variable_field.type = self._flag_mf_type
            o_variable_field.offset = self._flag_mf_offset
            o_variable_field.mode = self._flag_mf_mode
            o_variable_field.count = self._flag_mf_count
            o_variable_field.value = self._flags

    def _fetch_flag_mf(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_mf_offset and mask == self._flag_mf_mask:
                self._flags = o_variable_field.value
                self._flag_mf_mode = o_variable_field.mode
                self._flag_mf_count = o_variable_field.count
                self._flag_mf_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def ttl(self):
        """
        Time To Live (TTL) field.
        """
        return self._ttl & 255

    @ttl.setter
    def ttl(self, value):
        current_value = getattr(self, '_ttl', 0)
        self._ttl = (current_value & (~255 & 255)) + ((utils.parse(value) << 0) & 255)

    @property
    def ttl_mode(self):
        """
        By default, :attr:`ttl_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._ttl_mode)

    @ttl_mode.setter
    def ttl_mode(self, mode):
        self._ttl_mode = baseclass.FieldMode.get_value(mode)

    _ttl_offset = 8
    _ttl_type = 0
    _ttl_full_mask = 255
    _ttl_mask = 255

    @property
    def ttl_step(self):
        """
        If :attr:`ttl_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._ttl_step >> 0

    @ttl_step.setter
    def ttl_step(self, step):
        self._ttl_step = step << 0

    @property
    def ttl_count(self):
        """
        If :attr:`ttl_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._ttl_count

    @ttl_count.setter
    def ttl_count(self, count):
        self._ttl_count = count

    def _save_ttl(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.ttl_mode == 'FIXED':
            ext.ttl = self._ttl
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._ttl_step
            o_variable_field.mask = self._ttl_mask
            o_variable_field.type = self._ttl_type
            o_variable_field.offset = self._ttl_offset
            o_variable_field.mode = self._ttl_mode
            o_variable_field.count = self._ttl_count
            o_variable_field.value = self._ttl

    def _fetch_ttl(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._ttl_offset and mask == self._ttl_mask:
                self._ttl = o_variable_field.value
                self._ttl_mode = o_variable_field.mode
                self._ttl_count = o_variable_field.count
                self._ttl_step = o_variable_field.step
                return
        else:
            self._ttl = ext.ttl

    @property
    def protocol(self):
        """
        Indicates the protocol that is encapsulated in the IP packet.. By default, this attribute is set automatically. Set :attr:`protocol_override` to ``True`` to override this field
        """
        return self._proto & 255

    @protocol.setter
    def protocol(self, value):
        current_value = getattr(self, '_proto', 0)
        self._proto = (current_value & (~255 & 255)) + ((utils.parse(value) << 0) & 255)

    @property
    def protocol_mode(self):
        """
        By default, :attr:`protocol_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._protocol_mode)

    @protocol_mode.setter
    def protocol_mode(self, mode):
        self._protocol_mode = baseclass.FieldMode.get_value(mode)

    _protocol_offset = 9
    _protocol_type = 0
    _protocol_full_mask = 255
    _protocol_mask = 255

    @property
    def protocol_step(self):
        """
        If :attr:`protocol_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._protocol_step >> 0

    @protocol_step.setter
    def protocol_step(self, step):
        self._protocol_step = step << 0

    @property
    def protocol_count(self):
        """
        If :attr:`protocol_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._protocol_count

    @protocol_count.setter
    def protocol_count(self, count):
        self._protocol_count = count

    @property
    def protocol_override(self):
        return self._protocol_override

    @protocol_override.setter
    def protocol_override(self, override):
        self._protocol_override = override

    def _save_protocol(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_proto = self.protocol_override
        if self.protocol_mode == 'FIXED':
            ext.proto = self._proto
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._protocol_step
            o_variable_field.mask = self._protocol_mask
            o_variable_field.type = self._protocol_type
            o_variable_field.offset = self._protocol_offset
            o_variable_field.mode = self._protocol_mode
            o_variable_field.count = self._protocol_count
            o_variable_field.value = self._proto

    def _fetch_protocol(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.protocol_override = ext.is_override_proto
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._protocol_offset and mask == self._protocol_mask:
                self._proto = o_variable_field.value
                self._protocol_mode = o_variable_field.mode
                self._protocol_count = o_variable_field.count
                self._protocol_step = o_variable_field.step
                return
        else:
            self._proto = ext.proto

    @property
    def header_length(self):
        """
        Internet Header Length (IHL): number of 4 bytes words in the header. The minimum valid value is 5, and maximum valid value is 15.. By default, this attribute is set automatically. Set :attr:`header_length_override` to ``True`` to override this field
        """
        return self._ver_hdrlen & 15

    @header_length.setter
    def header_length(self, value):
        current_value = getattr(self, '_ver_hdrlen', 0)
        self._ver_hdrlen = (current_value & (~15 & 255)) + ((utils.parse(value) << 0) & 15)

    @property
    def header_length_mode(self):
        """
        By default, :attr:`header_length_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._header_length_mode)

    @header_length_mode.setter
    def header_length_mode(self, mode):
        self._header_length_mode = baseclass.FieldMode.get_value(mode)

    _header_length_offset = 0
    _header_length_type = 0
    _header_length_full_mask = 255
    _header_length_mask = 15

    @property
    def header_length_step(self):
        """
        If :attr:`header_length_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._header_length_step >> 0

    @header_length_step.setter
    def header_length_step(self, step):
        self._header_length_step = step << 0

    @property
    def header_length_count(self):
        """
        If :attr:`header_length_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._header_length_count

    @header_length_count.setter
    def header_length_count(self, count):
        self._header_length_count = count

    @property
    def header_length_override(self):
        return self._header_length_override

    @header_length_override.setter
    def header_length_override(self, override):
        self._header_length_override = override

    def _save_header_length(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_hdrlen = self.header_length_override
        if self.header_length_mode == 'FIXED':
            ext.ver_hdrlen = self._ver_hdrlen
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._header_length_step
            o_variable_field.mask = self._header_length_mask
            o_variable_field.type = self._header_length_type
            o_variable_field.offset = self._header_length_offset
            o_variable_field.mode = self._header_length_mode
            o_variable_field.count = self._header_length_count
            o_variable_field.value = self._ver_hdrlen

    def _fetch_header_length(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.header_length_override = ext.is_override_hdrlen
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._header_length_offset and mask == self._header_length_mask:
                self._ver_hdrlen = o_variable_field.value
                self._header_length_mode = o_variable_field.mode
                self._header_length_count = o_variable_field.count
                self._header_length_step = o_variable_field.step
                return
        else:
            self._ver_hdrlen = ext.ver_hdrlen

    @property
    def fragments_offset(self):
        """
        The Fragment Offset field indicates the offset of a packet fragment in the original IP packet
        """
        return self._frag_ofs & 8191

    @fragments_offset.setter
    def fragments_offset(self, value):
        current_value = getattr(self, '_frag_ofs', 0)
        self._frag_ofs = (current_value & (~8191 & 65535)) + ((utils.parse(value) << 0) & 8191)

    @property
    def fragments_offset_mode(self):
        """
        By default, :attr:`fragments_offset_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._fragments_offset_mode)

    @fragments_offset_mode.setter
    def fragments_offset_mode(self, mode):
        self._fragments_offset_mode = baseclass.FieldMode.get_value(mode)

    _fragments_offset_offset = 6
    _fragments_offset_type = 1
    _fragments_offset_full_mask = 65535
    _fragments_offset_mask = 8191

    @property
    def fragments_offset_step(self):
        """
        If :attr:`fragments_offset_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._fragments_offset_step >> 0

    @fragments_offset_step.setter
    def fragments_offset_step(self, step):
        self._fragments_offset_step = step << 0

    @property
    def fragments_offset_count(self):
        """
        If :attr:`fragments_offset_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._fragments_offset_count

    @fragments_offset_count.setter
    def fragments_offset_count(self, count):
        self._fragments_offset_count = count

    def _save_fragments_offset(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.fragments_offset_mode == 'FIXED':
            ext.frag_ofs = self._frag_ofs
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._fragments_offset_step
            o_variable_field.mask = self._fragments_offset_mask
            o_variable_field.type = self._fragments_offset_type
            o_variable_field.offset = self._fragments_offset_offset
            o_variable_field.mode = self._fragments_offset_mode
            o_variable_field.count = self._fragments_offset_count
            o_variable_field.value = self._frag_ofs

    def _fetch_fragments_offset(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._fragments_offset_offset and mask == self._fragments_offset_mask:
                self._frag_ofs = o_variable_field.value
                self._fragments_offset_mode = o_variable_field.mode
                self._fragments_offset_count = o_variable_field.count
                self._fragments_offset_step = o_variable_field.step
                return
        else:
            self._frag_ofs = ext.frag_ofs

    @property
    def tos(self):
        """
        Type Of Service (TOS) field. This field is now the Differentiated Services Code Point (DSCP) field.
        """
        return self._tos & 255

    @tos.setter
    def tos(self, value):
        current_value = getattr(self, '_tos', 0)
        self._tos = (current_value & (~255 & 255)) + ((utils.parse(value) << 0) & 255)

    @property
    def tos_mode(self):
        """
        By default, :attr:`tos_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._tos_mode)

    @tos_mode.setter
    def tos_mode(self, mode):
        self._tos_mode = baseclass.FieldMode.get_value(mode)

    _tos_offset = 1
    _tos_type = 0
    _tos_full_mask = 255
    _tos_mask = 255

    @property
    def tos_step(self):
        """
        If :attr:`tos_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._tos_step >> 0

    @tos_step.setter
    def tos_step(self, step):
        self._tos_step = step << 0

    @property
    def tos_count(self):
        """
        If :attr:`tos_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._tos_count

    @tos_count.setter
    def tos_count(self, count):
        self._tos_count = count

    def _save_tos(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.tos_mode == 'FIXED':
            ext.tos = self._tos
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._tos_step
            o_variable_field.mask = self._tos_mask
            o_variable_field.type = self._tos_type
            o_variable_field.offset = self._tos_offset
            o_variable_field.mode = self._tos_mode
            o_variable_field.count = self._tos_count
            o_variable_field.value = self._tos

    def _fetch_tos(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._tos_offset and mask == self._tos_mask:
                self._tos = o_variable_field.value
                self._tos_mode = o_variable_field.mode
                self._tos_count = o_variable_field.count
                self._tos_step = o_variable_field.step
                return
        else:
            self._tos = ext.tos

    @property
    def destination(self):
        """
        Destination IP address
        """
        return self._dst_ip & 4294967295

    @destination.setter
    def destination(self, value):
        current_value = getattr(self, '_dst_ip', 0)
        self._dst_ip = (current_value & (~4294967295 & 4294967295)) + ((utils.parse(value) << 0) & 4294967295)

    @property
    def destination_mode(self):
        """
        By default, :attr:`destination_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._destination_mode)

    @destination_mode.setter
    def destination_mode(self, mode):
        self._destination_mode = baseclass.FieldMode.get_value(mode)

    _destination_offset = 16
    _destination_type = 2
    _destination_full_mask = 4294967295
    _destination_mask = 4294967295

    @property
    def destination_step(self):
        """
        If :attr:`destination_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._destination_step >> 0

    @destination_step.setter
    def destination_step(self, step):
        self._destination_step = step << 0

    @property
    def destination_count(self):
        """
        If :attr:`destination_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._destination_count

    @destination_count.setter
    def destination_count(self, count):
        self._destination_count = count

    def _save_destination(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.destination_mode == 'FIXED':
            ext.dst_ip = self._dst_ip
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._destination_step
            o_variable_field.mask = self._destination_mask
            o_variable_field.type = self._destination_type
            o_variable_field.offset = self._destination_offset
            o_variable_field.mode = self._destination_mode
            o_variable_field.count = self._destination_count
            o_variable_field.value = self._dst_ip

    def _fetch_destination(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._destination_offset and mask == self._destination_mask:
                self._dst_ip = o_variable_field.value
                self._destination_mode = o_variable_field.mode
                self._destination_count = o_variable_field.count
                self._destination_step = o_variable_field.step
                return
        else:
            self._dst_ip = ext.dst_ip

    @property
    def source(self):
        """
        Source IP address
        """
        return self._src_ip & 4294967295

    @source.setter
    def source(self, value):
        current_value = getattr(self, '_src_ip', 0)
        self._src_ip = (current_value & (~4294967295 & 4294967295)) + ((utils.parse(value) << 0) & 4294967295)

    @property
    def source_mode(self):
        """
        By default, :attr:`source_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._source_mode)

    @source_mode.setter
    def source_mode(self, mode):
        self._source_mode = baseclass.FieldMode.get_value(mode)

    _source_offset = 12
    _source_type = 2
    _source_full_mask = 4294967295
    _source_mask = 4294967295

    @property
    def source_step(self):
        """
        If :attr:`source_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._source_step >> 0

    @source_step.setter
    def source_step(self, step):
        self._source_step = step << 0

    @property
    def source_count(self):
        """
        If :attr:`source_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._source_count

    @source_count.setter
    def source_count(self, count):
        self._source_count = count

    def _save_source(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.source_mode == 'FIXED':
            ext.src_ip = self._src_ip
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._source_step
            o_variable_field.mask = self._source_mask
            o_variable_field.type = self._source_type
            o_variable_field.offset = self._source_offset
            o_variable_field.mode = self._source_mode
            o_variable_field.count = self._source_count
            o_variable_field.value = self._src_ip

    def _fetch_source(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._source_offset and mask == self._source_mask:
                self._src_ip = o_variable_field.value
                self._source_mode = o_variable_field.mode
                self._source_count = o_variable_field.count
                self._source_step = o_variable_field.step
                return
        else:
            self._src_ip = ext.src_ip

    @property
    def version(self):
        """
        Version of the protocol (usually 4 or 6). By default, this attribute is set automatically. Set :attr:`version_override` to ``True`` to override this field
        """
        return (self._ver_hdrlen & 240) >> 4

    @version.setter
    def version(self, value):
        current_value = getattr(self, '_ver_hdrlen', 0)
        self._ver_hdrlen = (current_value & (~240 & 255)) + ((utils.parse(value) << 4) & 240)

    @property
    def version_mode(self):
        """
        By default, :attr:`version_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._version_mode)

    @version_mode.setter
    def version_mode(self, mode):
        self._version_mode = baseclass.FieldMode.get_value(mode)

    _version_offset = 0
    _version_type = 0
    _version_full_mask = 255
    _version_mask = 240

    @property
    def version_step(self):
        """
        If :attr:`version_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._version_step >> 4

    @version_step.setter
    def version_step(self, step):
        self._version_step = step << 4

    @property
    def version_count(self):
        """
        If :attr:`version_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._version_count

    @version_count.setter
    def version_count(self, count):
        self._version_count = count

    @property
    def version_override(self):
        return self._version_override

    @version_override.setter
    def version_override(self, override):
        self._version_override = override

    def _save_version(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_ver = self.version_override
        if self.version_mode == 'FIXED':
            ext.ver_hdrlen = self._ver_hdrlen
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._version_step
            o_variable_field.mask = self._version_mask
            o_variable_field.type = self._version_type
            o_variable_field.offset = self._version_offset
            o_variable_field.mode = self._version_mode
            o_variable_field.count = self._version_count
            o_variable_field.value = self._ver_hdrlen

    def _fetch_version(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.version_override = ext.is_override_ver
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._version_offset and mask == self._version_mask:
                self._ver_hdrlen = o_variable_field.value
                self._version_mode = o_variable_field.mode
                self._version_count = o_variable_field.count
                self._version_step = o_variable_field.step
                return
        else:
            self._ver_hdrlen = ext.ver_hdrlen

    @property
    def identification(self):
        """
        Identification field. This is used to identify packet fragments
        """
        return self._id & 65535

    @identification.setter
    def identification(self, value):
        current_value = getattr(self, '_id', 0)
        self._id = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def identification_mode(self):
        """
        By default, :attr:`identification_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._identification_mode)

    @identification_mode.setter
    def identification_mode(self, mode):
        self._identification_mode = baseclass.FieldMode.get_value(mode)

    _identification_offset = 2
    _identification_type = 1
    _identification_full_mask = 65535
    _identification_mask = 65535

    @property
    def identification_step(self):
        """
        If :attr:`identification_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._identification_step >> 0

    @identification_step.setter
    def identification_step(self, step):
        self._identification_step = step << 0

    @property
    def identification_count(self):
        """
        If :attr:`identification_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._identification_count

    @identification_count.setter
    def identification_count(self, count):
        self._identification_count = count

    def _save_identification(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.identification_mode == 'FIXED':
            ext.id = self._id
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._identification_step
            o_variable_field.mask = self._identification_mask
            o_variable_field.type = self._identification_type
            o_variable_field.offset = self._identification_offset
            o_variable_field.mode = self._identification_mode
            o_variable_field.count = self._identification_count
            o_variable_field.value = self._id

    def _fetch_identification(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._identification_offset and mask == self._identification_mask:
                self._id = o_variable_field.value
                self._identification_mode = o_variable_field.mode
                self._identification_count = o_variable_field.count
                self._identification_step = o_variable_field.step
                return
        else:
            self._id = ext.id

    @property
    def checksum(self):
        """
        Header checksum. By default, this attribute is set automatically. Set :attr:`checksum_override` to ``True`` to override this field
        """
        return self._cksum & 65535

    @checksum.setter
    def checksum(self, value):
        current_value = getattr(self, '_cksum', 0)
        self._cksum = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def checksum_mode(self):
        """
        By default, :attr:`checksum_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._checksum_mode)

    @checksum_mode.setter
    def checksum_mode(self, mode):
        self._checksum_mode = baseclass.FieldMode.get_value(mode)

    _checksum_offset = 10
    _checksum_type = 1
    _checksum_full_mask = 65535
    _checksum_mask = 65535

    @property
    def checksum_step(self):
        """
        If :attr:`checksum_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._checksum_step >> 0

    @checksum_step.setter
    def checksum_step(self, step):
        self._checksum_step = step << 0

    @property
    def checksum_count(self):
        """
        If :attr:`checksum_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._checksum_count

    @checksum_count.setter
    def checksum_count(self, count):
        self._checksum_count = count

    @property
    def checksum_override(self):
        return self._checksum_override

    @checksum_override.setter
    def checksum_override(self, override):
        self._checksum_override = override

    def _save_checksum(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_cksum = self.checksum_override
        if self.checksum_mode == 'FIXED':
            ext.cksum = self._cksum
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._checksum_step
            o_variable_field.mask = self._checksum_mask
            o_variable_field.type = self._checksum_type
            o_variable_field.offset = self._checksum_offset
            o_variable_field.mode = self._checksum_mode
            o_variable_field.count = self._checksum_count
            o_variable_field.value = self._cksum

    def _fetch_checksum(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.checksum_override = ext.is_override_cksum
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._checksum_offset and mask == self._checksum_mask:
                self._cksum = o_variable_field.value
                self._checksum_mode = o_variable_field.mode
                self._checksum_count = o_variable_field.count
                self._checksum_step = o_variable_field.step
                return
        else:
            self._cksum = ext.cksum

    @property
    def flag_df(self):
        """
        The "Don't Fragment" (DF) 1 bit flag
        """
        return (self._flags & 2) >> 1

    @flag_df.setter
    def flag_df(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~2 & 255)) + ((utils.parse(value) << 1) & 2)

    @property
    def flag_df_mode(self):
        """
        By default, :attr:`flag_df_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_df_mode)

    @flag_df_mode.setter
    def flag_df_mode(self, mode):
        self._flag_df_mode = baseclass.FieldMode.get_value(mode)

    _flag_df_offset = 6
    _flag_df_type = 0
    _flag_df_full_mask = 255
    _flag_df_mask = 2

    @property
    def flag_df_step(self):
        """
        If :attr:`flag_df_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_df_step >> 1

    @flag_df_step.setter
    def flag_df_step(self, step):
        self._flag_df_step = step << 1

    @property
    def flag_df_count(self):
        """
        If :attr:`flag_df_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_df_count

    @flag_df_count.setter
    def flag_df_count(self, count):
        self._flag_df_count = count

    def _save_flag_df(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_df_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_df_step
            o_variable_field.mask = self._flag_df_mask
            o_variable_field.type = self._flag_df_type
            o_variable_field.offset = self._flag_df_offset
            o_variable_field.mode = self._flag_df_mode
            o_variable_field.count = self._flag_df_count
            o_variable_field.value = self._flags

    def _fetch_flag_df(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_df_offset and mask == self._flag_df_mask:
                self._flags = o_variable_field.value
                self._flag_df_mode = o_variable_field.mode
                self._flag_df_count = o_variable_field.count
                self._flag_df_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def total_length(self):
        """
        Total length of the IP packet in bytes. The minimum valid value is 20, and the maxium is 65,535. By default, this attribute is set automatically. Set :attr:`total_length_override` to ``True`` to override this field
        """
        return self._totlen & 65535

    @total_length.setter
    def total_length(self, value):
        current_value = getattr(self, '_totlen', 0)
        self._totlen = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def total_length_mode(self):
        """
        By default, :attr:`total_length_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._total_length_mode)

    @total_length_mode.setter
    def total_length_mode(self, mode):
        self._total_length_mode = baseclass.FieldMode.get_value(mode)

    _total_length_offset = 2
    _total_length_type = 1
    _total_length_full_mask = 65535
    _total_length_mask = 65535

    @property
    def total_length_step(self):
        """
        If :attr:`total_length_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._total_length_step >> 0

    @total_length_step.setter
    def total_length_step(self, step):
        self._total_length_step = step << 0

    @property
    def total_length_count(self):
        """
        If :attr:`total_length_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._total_length_count

    @total_length_count.setter
    def total_length_count(self, count):
        self._total_length_count = count

    @property
    def total_length_override(self):
        return self._total_length_override

    @total_length_override.setter
    def total_length_override(self, override):
        self._total_length_override = override

    def _save_total_length(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_totlen = self.total_length_override
        if self.total_length_mode == 'FIXED':
            ext.totlen = self._totlen
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._total_length_step
            o_variable_field.mask = self._total_length_mask
            o_variable_field.type = self._total_length_type
            o_variable_field.offset = self._total_length_offset
            o_variable_field.mode = self._total_length_mode
            o_variable_field.count = self._total_length_count
            o_variable_field.value = self._totlen

    def _fetch_total_length(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.total_length_override = ext.is_override_totlen
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._total_length_offset and mask == self._total_length_mask:
                self._totlen = o_variable_field.value
                self._total_length_mode = o_variable_field.mode
                self._total_length_count = o_variable_field.count
                self._total_length_step = o_variable_field.step
                return
        else:
            self._totlen = ext.totlen

    def __str__(self):
        return 'IPv4(flag_unused={},dscp={},flag_mf={},ttl={},protocol={},header_length={},fragments_offset={},tos={},destination={},source={},version={},identification={},checksum={},flag_df={},total_length={},)'.format(self.flag_unused,self.dscp,self.flag_mf,self.ttl,self.protocol,self.header_length,self.fragments_offset,self.tos,self.destination,self.source,self.version,self.identification,self.checksum,self.flag_df,self.total_length,)

    def to_dict(self):
        """
        Return the IPv4 layer configuration as a
        dictionnary.
        """
        return { 
            'flag_unused': self.flag_unused,
            'flag_unused_mode': self.flag_unused_mode,
            'flag_unused_count': self.flag_unused_count,
            'flag_unused_step': self.flag_unused_step,
            'dscp': self.dscp,
            'dscp_mode': self.dscp_mode,
            'dscp_count': self.dscp_count,
            'dscp_step': self.dscp_step,
            'flag_mf': self.flag_mf,
            'flag_mf_mode': self.flag_mf_mode,
            'flag_mf_count': self.flag_mf_count,
            'flag_mf_step': self.flag_mf_step,
            'ttl': self.ttl,
            'ttl_mode': self.ttl_mode,
            'ttl_count': self.ttl_count,
            'ttl_step': self.ttl_step,
            'protocol': self.protocol,
            'protocol_mode': self.protocol_mode,
            'protocol_count': self.protocol_count,
            'protocol_step': self.protocol_step,
            'protocol_override': self.protocol_override,
            'header_length': self.header_length,
            'header_length_mode': self.header_length_mode,
            'header_length_count': self.header_length_count,
            'header_length_step': self.header_length_step,
            'header_length_override': self.header_length_override,
            'fragments_offset': self.fragments_offset,
            'fragments_offset_mode': self.fragments_offset_mode,
            'fragments_offset_count': self.fragments_offset_count,
            'fragments_offset_step': self.fragments_offset_step,
            'tos': self.tos,
            'tos_mode': self.tos_mode,
            'tos_count': self.tos_count,
            'tos_step': self.tos_step,
            'destination': self.destination,
            'destination_mode': self.destination_mode,
            'destination_count': self.destination_count,
            'destination_step': self.destination_step,
            'source': self.source,
            'source_mode': self.source_mode,
            'source_count': self.source_count,
            'source_step': self.source_step,
            'version': self.version,
            'version_mode': self.version_mode,
            'version_count': self.version_count,
            'version_step': self.version_step,
            'version_override': self.version_override,
            'identification': self.identification,
            'identification_mode': self.identification_mode,
            'identification_count': self.identification_count,
            'identification_step': self.identification_step,
            'checksum': self.checksum,
            'checksum_mode': self.checksum_mode,
            'checksum_count': self.checksum_count,
            'checksum_step': self.checksum_step,
            'checksum_override': self.checksum_override,
            'flag_df': self.flag_df,
            'flag_df_mode': self.flag_df_mode,
            'flag_df_count': self.flag_df_count,
            'flag_df_step': self.flag_df_step,
            'total_length': self.total_length,
            'total_length_mode': self.total_length_mode,
            'total_length_count': self.total_length_count,
            'total_length_step': self.total_length_step,
            'total_length_override': self.total_length_override,
        }

    def from_dict(self, dict_):
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
        
        self.source_mode = 'FIXED'
        self.source_step = 1 << 0
        self.source_count = 1
        self.source_override = False
        self.length_mode = 'FIXED'
        self.length_step = 1 << 0
        self.length_count = 1
        self.length_override = False
        self.destination_mode = 'FIXED'
        self.destination_step = 1 << 0
        self.destination_count = 1
        self.destination_override = False
        self.checksum_mode = 'FIXED'
        self.checksum_step = 1 << 0
        self.checksum_count = 1
        self.checksum_override = False

    @property
    def source(self):
        """
        Source port number. By default, this attribute is set automatically. Set :attr:`source_override` to ``True`` to override this field
        """
        return self._src_port & 65535

    @source.setter
    def source(self, value):
        current_value = getattr(self, '_src_port', 0)
        self._src_port = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def source_mode(self):
        """
        By default, :attr:`source_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._source_mode)

    @source_mode.setter
    def source_mode(self, mode):
        self._source_mode = baseclass.FieldMode.get_value(mode)

    _source_offset = 0
    _source_type = 1
    _source_full_mask = 65535
    _source_mask = 65535

    @property
    def source_step(self):
        """
        If :attr:`source_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._source_step >> 0

    @source_step.setter
    def source_step(self, step):
        self._source_step = step << 0

    @property
    def source_count(self):
        """
        If :attr:`source_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._source_count

    @source_count.setter
    def source_count(self, count):
        self._source_count = count

    @property
    def source_override(self):
        return self._source_override

    @source_override.setter
    def source_override(self, override):
        self._source_override = override

    def _save_source(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_src_port = self.source_override
        if self.source_mode == 'FIXED':
            ext.src_port = self._src_port
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._source_step
            o_variable_field.mask = self._source_mask
            o_variable_field.type = self._source_type
            o_variable_field.offset = self._source_offset
            o_variable_field.mode = self._source_mode
            o_variable_field.count = self._source_count
            o_variable_field.value = self._src_port

    def _fetch_source(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.source_override = ext.is_override_src_port
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._source_offset and mask == self._source_mask:
                self._src_port = o_variable_field.value
                self._source_mode = o_variable_field.mode
                self._source_count = o_variable_field.count
                self._source_step = o_variable_field.step
                return
        else:
            self._src_port = ext.src_port

    @property
    def length(self):
        """
        Length of the UDP datagram (header and payload).. By default, this attribute is set automatically. Set :attr:`length_override` to ``True`` to override this field
        """
        return self._totlen & 65535

    @length.setter
    def length(self, value):
        current_value = getattr(self, '_totlen', 0)
        self._totlen = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def length_mode(self):
        """
        By default, :attr:`length_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._length_mode)

    @length_mode.setter
    def length_mode(self, mode):
        self._length_mode = baseclass.FieldMode.get_value(mode)

    _length_offset = 4
    _length_type = 1
    _length_full_mask = 65535
    _length_mask = 65535

    @property
    def length_step(self):
        """
        If :attr:`length_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._length_step >> 0

    @length_step.setter
    def length_step(self, step):
        self._length_step = step << 0

    @property
    def length_count(self):
        """
        If :attr:`length_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._length_count

    @length_count.setter
    def length_count(self, count):
        self._length_count = count

    @property
    def length_override(self):
        return self._length_override

    @length_override.setter
    def length_override(self, override):
        self._length_override = override

    def _save_length(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_totlen = self.length_override
        if self.length_mode == 'FIXED':
            ext.totlen = self._totlen
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._length_step
            o_variable_field.mask = self._length_mask
            o_variable_field.type = self._length_type
            o_variable_field.offset = self._length_offset
            o_variable_field.mode = self._length_mode
            o_variable_field.count = self._length_count
            o_variable_field.value = self._totlen

    def _fetch_length(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.length_override = ext.is_override_totlen
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._length_offset and mask == self._length_mask:
                self._totlen = o_variable_field.value
                self._length_mode = o_variable_field.mode
                self._length_count = o_variable_field.count
                self._length_step = o_variable_field.step
                return
        else:
            self._totlen = ext.totlen

    @property
    def destination(self):
        """
        Destination port number. By default, this attribute is set automatically. Set :attr:`destination_override` to ``True`` to override this field
        """
        return self._dst_port & 65535

    @destination.setter
    def destination(self, value):
        current_value = getattr(self, '_dst_port', 0)
        self._dst_port = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def destination_mode(self):
        """
        By default, :attr:`destination_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._destination_mode)

    @destination_mode.setter
    def destination_mode(self, mode):
        self._destination_mode = baseclass.FieldMode.get_value(mode)

    _destination_offset = 2
    _destination_type = 1
    _destination_full_mask = 65535
    _destination_mask = 65535

    @property
    def destination_step(self):
        """
        If :attr:`destination_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._destination_step >> 0

    @destination_step.setter
    def destination_step(self, step):
        self._destination_step = step << 0

    @property
    def destination_count(self):
        """
        If :attr:`destination_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._destination_count

    @destination_count.setter
    def destination_count(self, count):
        self._destination_count = count

    @property
    def destination_override(self):
        return self._destination_override

    @destination_override.setter
    def destination_override(self, override):
        self._destination_override = override

    def _save_destination(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_dst_port = self.destination_override
        if self.destination_mode == 'FIXED':
            ext.dst_port = self._dst_port
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._destination_step
            o_variable_field.mask = self._destination_mask
            o_variable_field.type = self._destination_type
            o_variable_field.offset = self._destination_offset
            o_variable_field.mode = self._destination_mode
            o_variable_field.count = self._destination_count
            o_variable_field.value = self._dst_port

    def _fetch_destination(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.destination_override = ext.is_override_dst_port
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._destination_offset and mask == self._destination_mask:
                self._dst_port = o_variable_field.value
                self._destination_mode = o_variable_field.mode
                self._destination_count = o_variable_field.count
                self._destination_step = o_variable_field.step
                return
        else:
            self._dst_port = ext.dst_port

    @property
    def checksum(self):
        """
        Checksum of the datagram, calculated based on the IP pseudo-header.. By default, this attribute is set automatically. Set :attr:`checksum_override` to ``True`` to override this field
        """
        return self._cksum & 65535

    @checksum.setter
    def checksum(self, value):
        current_value = getattr(self, '_cksum', 0)
        self._cksum = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def checksum_mode(self):
        """
        By default, :attr:`checksum_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._checksum_mode)

    @checksum_mode.setter
    def checksum_mode(self, mode):
        self._checksum_mode = baseclass.FieldMode.get_value(mode)

    _checksum_offset = 6
    _checksum_type = 1
    _checksum_full_mask = 65535
    _checksum_mask = 65535

    @property
    def checksum_step(self):
        """
        If :attr:`checksum_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._checksum_step >> 0

    @checksum_step.setter
    def checksum_step(self, step):
        self._checksum_step = step << 0

    @property
    def checksum_count(self):
        """
        If :attr:`checksum_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._checksum_count

    @checksum_count.setter
    def checksum_count(self, count):
        self._checksum_count = count

    @property
    def checksum_override(self):
        return self._checksum_override

    @checksum_override.setter
    def checksum_override(self, override):
        self._checksum_override = override

    def _save_checksum(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_cksum = self.checksum_override
        if self.checksum_mode == 'FIXED':
            ext.cksum = self._cksum
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._checksum_step
            o_variable_field.mask = self._checksum_mask
            o_variable_field.type = self._checksum_type
            o_variable_field.offset = self._checksum_offset
            o_variable_field.mode = self._checksum_mode
            o_variable_field.count = self._checksum_count
            o_variable_field.value = self._cksum

    def _fetch_checksum(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.checksum_override = ext.is_override_cksum
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._checksum_offset and mask == self._checksum_mask:
                self._cksum = o_variable_field.value
                self._checksum_mode = o_variable_field.mode
                self._checksum_count = o_variable_field.count
                self._checksum_step = o_variable_field.step
                return
        else:
            self._cksum = ext.cksum

    def __str__(self):
        return 'Udp(source={},length={},destination={},checksum={},)'.format(self.source,self.length,self.destination,self.checksum,)

    def to_dict(self):
        """
        Return the Udp layer configuration as a
        dictionnary.
        """
        return { 
            'source': self.source,
            'source_mode': self.source_mode,
            'source_count': self.source_count,
            'source_step': self.source_step,
            'source_override': self.source_override,
            'length': self.length,
            'length_mode': self.length_mode,
            'length_count': self.length_count,
            'length_step': self.length_step,
            'length_override': self.length_override,
            'destination': self.destination,
            'destination_mode': self.destination_mode,
            'destination_count': self.destination_count,
            'destination_step': self.destination_step,
            'destination_override': self.destination_override,
            'checksum': self.checksum,
            'checksum_mode': self.checksum_mode,
            'checksum_count': self.checksum_count,
            'checksum_step': self.checksum_step,
            'checksum_override': self.checksum_override,
        }

    def from_dict(self, dict_):
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
        
        self.flag_ack_mode = 'FIXED'
        self.flag_ack_step = 1 << 4
        self.flag_ack_count = 1
        self.header_length_mode = 'FIXED'
        self.header_length_step = 1 << 4
        self.header_length_count = 1
        self.header_length_override = False
        self.reserved_mode = 'FIXED'
        self.reserved_step = 1 << 1
        self.reserved_count = 1
        self.reserved_override = False
        self.ack_num_mode = 'FIXED'
        self.ack_num_step = 1 << 0
        self.ack_num_count = 1
        self.flag_rst_mode = 'FIXED'
        self.flag_rst_step = 1 << 2
        self.flag_rst_count = 1
        self.window_size_mode = 'FIXED'
        self.window_size_step = 1 << 0
        self.window_size_count = 1
        self.destination_mode = 'FIXED'
        self.destination_step = 1 << 0
        self.destination_count = 1
        self.destination_override = False
        self.flag_psh_mode = 'FIXED'
        self.flag_psh_step = 1 << 3
        self.flag_psh_count = 1
        self.urgent_pointer_mode = 'FIXED'
        self.urgent_pointer_step = 1 << 0
        self.urgent_pointer_count = 1
        self.source_mode = 'FIXED'
        self.source_step = 1 << 0
        self.source_count = 1
        self.source_override = False
        self.flag_ece_mode = 'FIXED'
        self.flag_ece_step = 1 << 6
        self.flag_ece_count = 1
        self.flag_urg_mode = 'FIXED'
        self.flag_urg_step = 1 << 5
        self.flag_urg_count = 1
        self.sequence_num_mode = 'FIXED'
        self.sequence_num_step = 1 << 0
        self.sequence_num_count = 1
        self.checksum_mode = 'FIXED'
        self.checksum_step = 1 << 0
        self.checksum_count = 1
        self.checksum_override = False
        self.flag_syn_mode = 'FIXED'
        self.flag_syn_step = 1 << 1
        self.flag_syn_count = 1
        self.flag_cwr_mode = 'FIXED'
        self.flag_cwr_step = 1 << 7
        self.flag_cwr_count = 1
        self.flag_fin_mode = 'FIXED'
        self.flag_fin_step = 1 << 0
        self.flag_fin_count = 1
        self.flag_ns_mode = 'FIXED'
        self.flag_ns_step = 1 << 0
        self.flag_ns_count = 1
        self.flag_ns_override = False

    @property
    def flag_ack(self):
        """
        ACK flag
        """
        return (self._flags & 16) >> 4

    @flag_ack.setter
    def flag_ack(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~16 & 255)) + ((utils.parse(value) << 4) & 16)

    @property
    def flag_ack_mode(self):
        """
        By default, :attr:`flag_ack_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_ack_mode)

    @flag_ack_mode.setter
    def flag_ack_mode(self, mode):
        self._flag_ack_mode = baseclass.FieldMode.get_value(mode)

    _flag_ack_offset = 13
    _flag_ack_type = 0
    _flag_ack_full_mask = 255
    _flag_ack_mask = 16

    @property
    def flag_ack_step(self):
        """
        If :attr:`flag_ack_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_ack_step >> 4

    @flag_ack_step.setter
    def flag_ack_step(self, step):
        self._flag_ack_step = step << 4

    @property
    def flag_ack_count(self):
        """
        If :attr:`flag_ack_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_ack_count

    @flag_ack_count.setter
    def flag_ack_count(self, count):
        self._flag_ack_count = count

    def _save_flag_ack(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_ack_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_ack_step
            o_variable_field.mask = self._flag_ack_mask
            o_variable_field.type = self._flag_ack_type
            o_variable_field.offset = self._flag_ack_offset
            o_variable_field.mode = self._flag_ack_mode
            o_variable_field.count = self._flag_ack_count
            o_variable_field.value = self._flags

    def _fetch_flag_ack(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_ack_offset and mask == self._flag_ack_mask:
                self._flags = o_variable_field.value
                self._flag_ack_mode = o_variable_field.mode
                self._flag_ack_count = o_variable_field.count
                self._flag_ack_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def header_length(self):
        """
        Size of the TCP header in 4 bytes words. This field is also known as "Data offset". By default, this attribute is set automatically. Set :attr:`header_length_override` to ``True`` to override this field
        """
        return (self._hdrlen_rsvd & 240) >> 4

    @header_length.setter
    def header_length(self, value):
        current_value = getattr(self, '_hdrlen_rsvd', 0)
        self._hdrlen_rsvd = (current_value & (~240 & 255)) + ((utils.parse(value) << 4) & 240)

    @property
    def header_length_mode(self):
        """
        By default, :attr:`header_length_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._header_length_mode)

    @header_length_mode.setter
    def header_length_mode(self, mode):
        self._header_length_mode = baseclass.FieldMode.get_value(mode)

    _header_length_offset = 12
    _header_length_type = 0
    _header_length_full_mask = 255
    _header_length_mask = 240

    @property
    def header_length_step(self):
        """
        If :attr:`header_length_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._header_length_step >> 4

    @header_length_step.setter
    def header_length_step(self, step):
        self._header_length_step = step << 4

    @property
    def header_length_count(self):
        """
        If :attr:`header_length_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._header_length_count

    @header_length_count.setter
    def header_length_count(self, count):
        self._header_length_count = count

    @property
    def header_length_override(self):
        return self._header_length_override

    @header_length_override.setter
    def header_length_override(self, override):
        self._header_length_override = override

    def _save_header_length(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_hdrlen = self.header_length_override
        if self.header_length_mode == 'FIXED':
            ext.hdrlen_rsvd = self._hdrlen_rsvd
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._header_length_step
            o_variable_field.mask = self._header_length_mask
            o_variable_field.type = self._header_length_type
            o_variable_field.offset = self._header_length_offset
            o_variable_field.mode = self._header_length_mode
            o_variable_field.count = self._header_length_count
            o_variable_field.value = self._hdrlen_rsvd

    def _fetch_header_length(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.header_length_override = ext.is_override_hdrlen
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._header_length_offset and mask == self._header_length_mask:
                self._hdrlen_rsvd = o_variable_field.value
                self._header_length_mode = o_variable_field.mode
                self._header_length_count = o_variable_field.count
                self._header_length_step = o_variable_field.step
                return
        else:
            self._hdrlen_rsvd = ext.hdrlen_rsvd

    @property
    def reserved(self):
        """
        Reserved for future use and must be set to 0. By default, this attribute is set automatically. Set :attr:`reserved_override` to ``True`` to override this field
        """
        return (self._hdrlen_rsvd & 14) >> 1

    @reserved.setter
    def reserved(self, value):
        current_value = getattr(self, '_hdrlen_rsvd', 0)
        self._hdrlen_rsvd = (current_value & (~14 & 255)) + ((utils.parse(value) << 1) & 14)

    @property
    def reserved_mode(self):
        """
        By default, :attr:`reserved_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._reserved_mode)

    @reserved_mode.setter
    def reserved_mode(self, mode):
        self._reserved_mode = baseclass.FieldMode.get_value(mode)

    _reserved_offset = 12
    _reserved_type = 0
    _reserved_full_mask = 255
    _reserved_mask = 14

    @property
    def reserved_step(self):
        """
        If :attr:`reserved_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._reserved_step >> 1

    @reserved_step.setter
    def reserved_step(self, step):
        self._reserved_step = step << 1

    @property
    def reserved_count(self):
        """
        If :attr:`reserved_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._reserved_count

    @reserved_count.setter
    def reserved_count(self, count):
        self._reserved_count = count

    @property
    def reserved_override(self):
        return self._reserved_override

    @reserved_override.setter
    def reserved_override(self, override):
        self._reserved_override = override

    def _save_reserved(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_hdrlen = self.reserved_override
        if self.reserved_mode == 'FIXED':
            ext.hdrlen_rsvd = self._hdrlen_rsvd
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._reserved_step
            o_variable_field.mask = self._reserved_mask
            o_variable_field.type = self._reserved_type
            o_variable_field.offset = self._reserved_offset
            o_variable_field.mode = self._reserved_mode
            o_variable_field.count = self._reserved_count
            o_variable_field.value = self._hdrlen_rsvd

    def _fetch_reserved(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.reserved_override = ext.is_override_hdrlen
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._reserved_offset and mask == self._reserved_mask:
                self._hdrlen_rsvd = o_variable_field.value
                self._reserved_mode = o_variable_field.mode
                self._reserved_count = o_variable_field.count
                self._reserved_step = o_variable_field.step
                return
        else:
            self._hdrlen_rsvd = ext.hdrlen_rsvd

    @property
    def ack_num(self):
        """
        Acknowledgement number
        """
        return self._ack_num & 4294967295

    @ack_num.setter
    def ack_num(self, value):
        current_value = getattr(self, '_ack_num', 0)
        self._ack_num = (current_value & (~4294967295 & 4294967295)) + ((utils.parse(value) << 0) & 4294967295)

    @property
    def ack_num_mode(self):
        """
        By default, :attr:`ack_num_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._ack_num_mode)

    @ack_num_mode.setter
    def ack_num_mode(self, mode):
        self._ack_num_mode = baseclass.FieldMode.get_value(mode)

    _ack_num_offset = 8
    _ack_num_type = 2
    _ack_num_full_mask = 4294967295
    _ack_num_mask = 4294967295

    @property
    def ack_num_step(self):
        """
        If :attr:`ack_num_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._ack_num_step >> 0

    @ack_num_step.setter
    def ack_num_step(self, step):
        self._ack_num_step = step << 0

    @property
    def ack_num_count(self):
        """
        If :attr:`ack_num_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._ack_num_count

    @ack_num_count.setter
    def ack_num_count(self, count):
        self._ack_num_count = count

    def _save_ack_num(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.ack_num_mode == 'FIXED':
            ext.ack_num = self._ack_num
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._ack_num_step
            o_variable_field.mask = self._ack_num_mask
            o_variable_field.type = self._ack_num_type
            o_variable_field.offset = self._ack_num_offset
            o_variable_field.mode = self._ack_num_mode
            o_variable_field.count = self._ack_num_count
            o_variable_field.value = self._ack_num

    def _fetch_ack_num(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._ack_num_offset and mask == self._ack_num_mask:
                self._ack_num = o_variable_field.value
                self._ack_num_mode = o_variable_field.mode
                self._ack_num_count = o_variable_field.count
                self._ack_num_step = o_variable_field.step
                return
        else:
            self._ack_num = ext.ack_num

    @property
    def flag_rst(self):
        """
        Reset the connection
        """
        return (self._flags & 4) >> 2

    @flag_rst.setter
    def flag_rst(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~4 & 255)) + ((utils.parse(value) << 2) & 4)

    @property
    def flag_rst_mode(self):
        """
        By default, :attr:`flag_rst_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_rst_mode)

    @flag_rst_mode.setter
    def flag_rst_mode(self, mode):
        self._flag_rst_mode = baseclass.FieldMode.get_value(mode)

    _flag_rst_offset = 13
    _flag_rst_type = 0
    _flag_rst_full_mask = 255
    _flag_rst_mask = 4

    @property
    def flag_rst_step(self):
        """
        If :attr:`flag_rst_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_rst_step >> 2

    @flag_rst_step.setter
    def flag_rst_step(self, step):
        self._flag_rst_step = step << 2

    @property
    def flag_rst_count(self):
        """
        If :attr:`flag_rst_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_rst_count

    @flag_rst_count.setter
    def flag_rst_count(self, count):
        self._flag_rst_count = count

    def _save_flag_rst(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_rst_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_rst_step
            o_variable_field.mask = self._flag_rst_mask
            o_variable_field.type = self._flag_rst_type
            o_variable_field.offset = self._flag_rst_offset
            o_variable_field.mode = self._flag_rst_mode
            o_variable_field.count = self._flag_rst_count
            o_variable_field.value = self._flags

    def _fetch_flag_rst(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_rst_offset and mask == self._flag_rst_mask:
                self._flags = o_variable_field.value
                self._flag_rst_mode = o_variable_field.mode
                self._flag_rst_count = o_variable_field.count
                self._flag_rst_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def window_size(self):
        """
        Size of the receive window, which specifies the number of window size units that the sender of this segment is currently willing to receive
        """
        return self._window & 65535

    @window_size.setter
    def window_size(self, value):
        current_value = getattr(self, '_window', 0)
        self._window = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def window_size_mode(self):
        """
        By default, :attr:`window_size_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._window_size_mode)

    @window_size_mode.setter
    def window_size_mode(self, mode):
        self._window_size_mode = baseclass.FieldMode.get_value(mode)

    _window_size_offset = 14
    _window_size_type = 1
    _window_size_full_mask = 65535
    _window_size_mask = 65535

    @property
    def window_size_step(self):
        """
        If :attr:`window_size_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._window_size_step >> 0

    @window_size_step.setter
    def window_size_step(self, step):
        self._window_size_step = step << 0

    @property
    def window_size_count(self):
        """
        If :attr:`window_size_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._window_size_count

    @window_size_count.setter
    def window_size_count(self, count):
        self._window_size_count = count

    def _save_window_size(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.window_size_mode == 'FIXED':
            ext.window = self._window
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._window_size_step
            o_variable_field.mask = self._window_size_mask
            o_variable_field.type = self._window_size_type
            o_variable_field.offset = self._window_size_offset
            o_variable_field.mode = self._window_size_mode
            o_variable_field.count = self._window_size_count
            o_variable_field.value = self._window

    def _fetch_window_size(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._window_size_offset and mask == self._window_size_mask:
                self._window = o_variable_field.value
                self._window_size_mode = o_variable_field.mode
                self._window_size_count = o_variable_field.count
                self._window_size_step = o_variable_field.step
                return
        else:
            self._window = ext.window

    @property
    def destination(self):
        """
        Destination port number. By default, this attribute is set automatically. Set :attr:`destination_override` to ``True`` to override this field
        """
        return self._dst_port & 65535

    @destination.setter
    def destination(self, value):
        current_value = getattr(self, '_dst_port', 0)
        self._dst_port = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def destination_mode(self):
        """
        By default, :attr:`destination_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._destination_mode)

    @destination_mode.setter
    def destination_mode(self, mode):
        self._destination_mode = baseclass.FieldMode.get_value(mode)

    _destination_offset = 2
    _destination_type = 1
    _destination_full_mask = 65535
    _destination_mask = 65535

    @property
    def destination_step(self):
        """
        If :attr:`destination_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._destination_step >> 0

    @destination_step.setter
    def destination_step(self, step):
        self._destination_step = step << 0

    @property
    def destination_count(self):
        """
        If :attr:`destination_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._destination_count

    @destination_count.setter
    def destination_count(self, count):
        self._destination_count = count

    @property
    def destination_override(self):
        return self._destination_override

    @destination_override.setter
    def destination_override(self, override):
        self._destination_override = override

    def _save_destination(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_dst_port = self.destination_override
        if self.destination_mode == 'FIXED':
            ext.dst_port = self._dst_port
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._destination_step
            o_variable_field.mask = self._destination_mask
            o_variable_field.type = self._destination_type
            o_variable_field.offset = self._destination_offset
            o_variable_field.mode = self._destination_mode
            o_variable_field.count = self._destination_count
            o_variable_field.value = self._dst_port

    def _fetch_destination(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.destination_override = ext.is_override_dst_port
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._destination_offset and mask == self._destination_mask:
                self._dst_port = o_variable_field.value
                self._destination_mode = o_variable_field.mode
                self._destination_count = o_variable_field.count
                self._destination_step = o_variable_field.step
                return
        else:
            self._dst_port = ext.dst_port

    @property
    def flag_psh(self):
        """
        Push function
        """
        return (self._flags & 8) >> 3

    @flag_psh.setter
    def flag_psh(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~8 & 255)) + ((utils.parse(value) << 3) & 8)

    @property
    def flag_psh_mode(self):
        """
        By default, :attr:`flag_psh_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_psh_mode)

    @flag_psh_mode.setter
    def flag_psh_mode(self, mode):
        self._flag_psh_mode = baseclass.FieldMode.get_value(mode)

    _flag_psh_offset = 13
    _flag_psh_type = 0
    _flag_psh_full_mask = 255
    _flag_psh_mask = 8

    @property
    def flag_psh_step(self):
        """
        If :attr:`flag_psh_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_psh_step >> 3

    @flag_psh_step.setter
    def flag_psh_step(self, step):
        self._flag_psh_step = step << 3

    @property
    def flag_psh_count(self):
        """
        If :attr:`flag_psh_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_psh_count

    @flag_psh_count.setter
    def flag_psh_count(self, count):
        self._flag_psh_count = count

    def _save_flag_psh(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_psh_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_psh_step
            o_variable_field.mask = self._flag_psh_mask
            o_variable_field.type = self._flag_psh_type
            o_variable_field.offset = self._flag_psh_offset
            o_variable_field.mode = self._flag_psh_mode
            o_variable_field.count = self._flag_psh_count
            o_variable_field.value = self._flags

    def _fetch_flag_psh(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_psh_offset and mask == self._flag_psh_mask:
                self._flags = o_variable_field.value
                self._flag_psh_mode = o_variable_field.mode
                self._flag_psh_count = o_variable_field.count
                self._flag_psh_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def urgent_pointer(self):
        """
        Urgent pointer.
        """
        return self._urg_ptr & 65535

    @urgent_pointer.setter
    def urgent_pointer(self, value):
        current_value = getattr(self, '_urg_ptr', 0)
        self._urg_ptr = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def urgent_pointer_mode(self):
        """
        By default, :attr:`urgent_pointer_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._urgent_pointer_mode)

    @urgent_pointer_mode.setter
    def urgent_pointer_mode(self, mode):
        self._urgent_pointer_mode = baseclass.FieldMode.get_value(mode)

    _urgent_pointer_offset = 18
    _urgent_pointer_type = 1
    _urgent_pointer_full_mask = 65535
    _urgent_pointer_mask = 65535

    @property
    def urgent_pointer_step(self):
        """
        If :attr:`urgent_pointer_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._urgent_pointer_step >> 0

    @urgent_pointer_step.setter
    def urgent_pointer_step(self, step):
        self._urgent_pointer_step = step << 0

    @property
    def urgent_pointer_count(self):
        """
        If :attr:`urgent_pointer_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._urgent_pointer_count

    @urgent_pointer_count.setter
    def urgent_pointer_count(self, count):
        self._urgent_pointer_count = count

    def _save_urgent_pointer(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.urgent_pointer_mode == 'FIXED':
            ext.urg_ptr = self._urg_ptr
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._urgent_pointer_step
            o_variable_field.mask = self._urgent_pointer_mask
            o_variable_field.type = self._urgent_pointer_type
            o_variable_field.offset = self._urgent_pointer_offset
            o_variable_field.mode = self._urgent_pointer_mode
            o_variable_field.count = self._urgent_pointer_count
            o_variable_field.value = self._urg_ptr

    def _fetch_urgent_pointer(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._urgent_pointer_offset and mask == self._urgent_pointer_mask:
                self._urg_ptr = o_variable_field.value
                self._urgent_pointer_mode = o_variable_field.mode
                self._urgent_pointer_count = o_variable_field.count
                self._urgent_pointer_step = o_variable_field.step
                return
        else:
            self._urg_ptr = ext.urg_ptr

    @property
    def source(self):
        """
        Source port number. By default, this attribute is set automatically. Set :attr:`source_override` to ``True`` to override this field
        """
        return self._src_port & 65535

    @source.setter
    def source(self, value):
        current_value = getattr(self, '_src_port', 0)
        self._src_port = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def source_mode(self):
        """
        By default, :attr:`source_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._source_mode)

    @source_mode.setter
    def source_mode(self, mode):
        self._source_mode = baseclass.FieldMode.get_value(mode)

    _source_offset = 0
    _source_type = 1
    _source_full_mask = 65535
    _source_mask = 65535

    @property
    def source_step(self):
        """
        If :attr:`source_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._source_step >> 0

    @source_step.setter
    def source_step(self, step):
        self._source_step = step << 0

    @property
    def source_count(self):
        """
        If :attr:`source_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._source_count

    @source_count.setter
    def source_count(self, count):
        self._source_count = count

    @property
    def source_override(self):
        return self._source_override

    @source_override.setter
    def source_override(self, override):
        self._source_override = override

    def _save_source(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_src_port = self.source_override
        if self.source_mode == 'FIXED':
            ext.src_port = self._src_port
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._source_step
            o_variable_field.mask = self._source_mask
            o_variable_field.type = self._source_type
            o_variable_field.offset = self._source_offset
            o_variable_field.mode = self._source_mode
            o_variable_field.count = self._source_count
            o_variable_field.value = self._src_port

    def _fetch_source(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.source_override = ext.is_override_src_port
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._source_offset and mask == self._source_mask:
                self._src_port = o_variable_field.value
                self._source_mode = o_variable_field.mode
                self._source_count = o_variable_field.count
                self._source_step = o_variable_field.step
                return
        else:
            self._src_port = ext.src_port

    @property
    def flag_ece(self):
        """
        ECN-Echo flag. Its meaning depends on the :attr:`syn` field value.
        """
        return (self._flags & 64) >> 6

    @flag_ece.setter
    def flag_ece(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~64 & 255)) + ((utils.parse(value) << 6) & 64)

    @property
    def flag_ece_mode(self):
        """
        By default, :attr:`flag_ece_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_ece_mode)

    @flag_ece_mode.setter
    def flag_ece_mode(self, mode):
        self._flag_ece_mode = baseclass.FieldMode.get_value(mode)

    _flag_ece_offset = 13
    _flag_ece_type = 0
    _flag_ece_full_mask = 255
    _flag_ece_mask = 64

    @property
    def flag_ece_step(self):
        """
        If :attr:`flag_ece_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_ece_step >> 6

    @flag_ece_step.setter
    def flag_ece_step(self, step):
        self._flag_ece_step = step << 6

    @property
    def flag_ece_count(self):
        """
        If :attr:`flag_ece_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_ece_count

    @flag_ece_count.setter
    def flag_ece_count(self, count):
        self._flag_ece_count = count

    def _save_flag_ece(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_ece_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_ece_step
            o_variable_field.mask = self._flag_ece_mask
            o_variable_field.type = self._flag_ece_type
            o_variable_field.offset = self._flag_ece_offset
            o_variable_field.mode = self._flag_ece_mode
            o_variable_field.count = self._flag_ece_count
            o_variable_field.value = self._flags

    def _fetch_flag_ece(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_ece_offset and mask == self._flag_ece_mask:
                self._flags = o_variable_field.value
                self._flag_ece_mode = o_variable_field.mode
                self._flag_ece_count = o_variable_field.count
                self._flag_ece_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def flag_urg(self):
        """
        Urgent pointer flag.
        """
        return (self._flags & 32) >> 5

    @flag_urg.setter
    def flag_urg(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~32 & 255)) + ((utils.parse(value) << 5) & 32)

    @property
    def flag_urg_mode(self):
        """
        By default, :attr:`flag_urg_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_urg_mode)

    @flag_urg_mode.setter
    def flag_urg_mode(self, mode):
        self._flag_urg_mode = baseclass.FieldMode.get_value(mode)

    _flag_urg_offset = 13
    _flag_urg_type = 0
    _flag_urg_full_mask = 255
    _flag_urg_mask = 32

    @property
    def flag_urg_step(self):
        """
        If :attr:`flag_urg_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_urg_step >> 5

    @flag_urg_step.setter
    def flag_urg_step(self, step):
        self._flag_urg_step = step << 5

    @property
    def flag_urg_count(self):
        """
        If :attr:`flag_urg_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_urg_count

    @flag_urg_count.setter
    def flag_urg_count(self, count):
        self._flag_urg_count = count

    def _save_flag_urg(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_urg_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_urg_step
            o_variable_field.mask = self._flag_urg_mask
            o_variable_field.type = self._flag_urg_type
            o_variable_field.offset = self._flag_urg_offset
            o_variable_field.mode = self._flag_urg_mode
            o_variable_field.count = self._flag_urg_count
            o_variable_field.value = self._flags

    def _fetch_flag_urg(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_urg_offset and mask == self._flag_urg_mask:
                self._flags = o_variable_field.value
                self._flag_urg_mode = o_variable_field.mode
                self._flag_urg_count = o_variable_field.count
                self._flag_urg_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def sequence_num(self):
        """
        Sequence number of the datagram. Its meaning depends on the :attr:`syn` flag value.
        """
        return self._seq_num & 4294967295

    @sequence_num.setter
    def sequence_num(self, value):
        current_value = getattr(self, '_seq_num', 0)
        self._seq_num = (current_value & (~4294967295 & 4294967295)) + ((utils.parse(value) << 0) & 4294967295)

    @property
    def sequence_num_mode(self):
        """
        By default, :attr:`sequence_num_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._sequence_num_mode)

    @sequence_num_mode.setter
    def sequence_num_mode(self, mode):
        self._sequence_num_mode = baseclass.FieldMode.get_value(mode)

    _sequence_num_offset = 4
    _sequence_num_type = 2
    _sequence_num_full_mask = 4294967295
    _sequence_num_mask = 4294967295

    @property
    def sequence_num_step(self):
        """
        If :attr:`sequence_num_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._sequence_num_step >> 0

    @sequence_num_step.setter
    def sequence_num_step(self, step):
        self._sequence_num_step = step << 0

    @property
    def sequence_num_count(self):
        """
        If :attr:`sequence_num_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._sequence_num_count

    @sequence_num_count.setter
    def sequence_num_count(self, count):
        self._sequence_num_count = count

    def _save_sequence_num(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.sequence_num_mode == 'FIXED':
            ext.seq_num = self._seq_num
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._sequence_num_step
            o_variable_field.mask = self._sequence_num_mask
            o_variable_field.type = self._sequence_num_type
            o_variable_field.offset = self._sequence_num_offset
            o_variable_field.mode = self._sequence_num_mode
            o_variable_field.count = self._sequence_num_count
            o_variable_field.value = self._seq_num

    def _fetch_sequence_num(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._sequence_num_offset and mask == self._sequence_num_mask:
                self._seq_num = o_variable_field.value
                self._sequence_num_mode = o_variable_field.mode
                self._sequence_num_count = o_variable_field.count
                self._sequence_num_step = o_variable_field.step
                return
        else:
            self._seq_num = ext.seq_num

    @property
    def checksum(self):
        """
        Checksum of the datagram, calculated based on the IP pseudo-header. Its meaning depends on the value og the :attr:`ack` flag.. By default, this attribute is set automatically. Set :attr:`checksum_override` to ``True`` to override this field
        """
        return self._cksum & 65535

    @checksum.setter
    def checksum(self, value):
        current_value = getattr(self, '_cksum', 0)
        self._cksum = (current_value & (~65535 & 65535)) + ((utils.parse(value) << 0) & 65535)

    @property
    def checksum_mode(self):
        """
        By default, :attr:`checksum_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._checksum_mode)

    @checksum_mode.setter
    def checksum_mode(self, mode):
        self._checksum_mode = baseclass.FieldMode.get_value(mode)

    _checksum_offset = 16
    _checksum_type = 1
    _checksum_full_mask = 65535
    _checksum_mask = 65535

    @property
    def checksum_step(self):
        """
        If :attr:`checksum_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._checksum_step >> 0

    @checksum_step.setter
    def checksum_step(self, step):
        self._checksum_step = step << 0

    @property
    def checksum_count(self):
        """
        If :attr:`checksum_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._checksum_count

    @checksum_count.setter
    def checksum_count(self, count):
        self._checksum_count = count

    @property
    def checksum_override(self):
        return self._checksum_override

    @checksum_override.setter
    def checksum_override(self, override):
        self._checksum_override = override

    def _save_checksum(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_cksum = self.checksum_override
        if self.checksum_mode == 'FIXED':
            ext.cksum = self._cksum
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._checksum_step
            o_variable_field.mask = self._checksum_mask
            o_variable_field.type = self._checksum_type
            o_variable_field.offset = self._checksum_offset
            o_variable_field.mode = self._checksum_mode
            o_variable_field.count = self._checksum_count
            o_variable_field.value = self._cksum

    def _fetch_checksum(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.checksum_override = ext.is_override_cksum
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._checksum_offset and mask == self._checksum_mask:
                self._cksum = o_variable_field.value
                self._checksum_mode = o_variable_field.mode
                self._checksum_count = o_variable_field.count
                self._checksum_step = o_variable_field.step
                return
        else:
            self._cksum = ext.cksum

    @property
    def flag_syn(self):
        """
        Synchronize sequence numbers
        """
        return (self._flags & 2) >> 1

    @flag_syn.setter
    def flag_syn(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~2 & 255)) + ((utils.parse(value) << 1) & 2)

    @property
    def flag_syn_mode(self):
        """
        By default, :attr:`flag_syn_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_syn_mode)

    @flag_syn_mode.setter
    def flag_syn_mode(self, mode):
        self._flag_syn_mode = baseclass.FieldMode.get_value(mode)

    _flag_syn_offset = 13
    _flag_syn_type = 0
    _flag_syn_full_mask = 255
    _flag_syn_mask = 2

    @property
    def flag_syn_step(self):
        """
        If :attr:`flag_syn_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_syn_step >> 1

    @flag_syn_step.setter
    def flag_syn_step(self, step):
        self._flag_syn_step = step << 1

    @property
    def flag_syn_count(self):
        """
        If :attr:`flag_syn_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_syn_count

    @flag_syn_count.setter
    def flag_syn_count(self, count):
        self._flag_syn_count = count

    def _save_flag_syn(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_syn_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_syn_step
            o_variable_field.mask = self._flag_syn_mask
            o_variable_field.type = self._flag_syn_type
            o_variable_field.offset = self._flag_syn_offset
            o_variable_field.mode = self._flag_syn_mode
            o_variable_field.count = self._flag_syn_count
            o_variable_field.value = self._flags

    def _fetch_flag_syn(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_syn_offset and mask == self._flag_syn_mask:
                self._flags = o_variable_field.value
                self._flag_syn_mode = o_variable_field.mode
                self._flag_syn_count = o_variable_field.count
                self._flag_syn_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def flag_cwr(self):
        """
        Congestion Window Reduced flag
        """
        return (self._flags & 128) >> 7

    @flag_cwr.setter
    def flag_cwr(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~128 & 255)) + ((utils.parse(value) << 7) & 128)

    @property
    def flag_cwr_mode(self):
        """
        By default, :attr:`flag_cwr_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_cwr_mode)

    @flag_cwr_mode.setter
    def flag_cwr_mode(self, mode):
        self._flag_cwr_mode = baseclass.FieldMode.get_value(mode)

    _flag_cwr_offset = 13
    _flag_cwr_type = 0
    _flag_cwr_full_mask = 255
    _flag_cwr_mask = 128

    @property
    def flag_cwr_step(self):
        """
        If :attr:`flag_cwr_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_cwr_step >> 7

    @flag_cwr_step.setter
    def flag_cwr_step(self, step):
        self._flag_cwr_step = step << 7

    @property
    def flag_cwr_count(self):
        """
        If :attr:`flag_cwr_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_cwr_count

    @flag_cwr_count.setter
    def flag_cwr_count(self, count):
        self._flag_cwr_count = count

    def _save_flag_cwr(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_cwr_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_cwr_step
            o_variable_field.mask = self._flag_cwr_mask
            o_variable_field.type = self._flag_cwr_type
            o_variable_field.offset = self._flag_cwr_offset
            o_variable_field.mode = self._flag_cwr_mode
            o_variable_field.count = self._flag_cwr_count
            o_variable_field.value = self._flags

    def _fetch_flag_cwr(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_cwr_offset and mask == self._flag_cwr_mask:
                self._flags = o_variable_field.value
                self._flag_cwr_mode = o_variable_field.mode
                self._flag_cwr_count = o_variable_field.count
                self._flag_cwr_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def flag_fin(self):
        """
        No more data from sender
        """
        return self._flags & 1

    @flag_fin.setter
    def flag_fin(self, value):
        current_value = getattr(self, '_flags', 0)
        self._flags = (current_value & (~1 & 255)) + ((utils.parse(value) << 0) & 1)

    @property
    def flag_fin_mode(self):
        """
        By default, :attr:`flag_fin_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_fin_mode)

    @flag_fin_mode.setter
    def flag_fin_mode(self, mode):
        self._flag_fin_mode = baseclass.FieldMode.get_value(mode)

    _flag_fin_offset = 13
    _flag_fin_type = 0
    _flag_fin_full_mask = 255
    _flag_fin_mask = 1

    @property
    def flag_fin_step(self):
        """
        If :attr:`flag_fin_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_fin_step >> 0

    @flag_fin_step.setter
    def flag_fin_step(self, step):
        self._flag_fin_step = step << 0

    @property
    def flag_fin_count(self):
        """
        If :attr:`flag_fin_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_fin_count

    @flag_fin_count.setter
    def flag_fin_count(self, count):
        self._flag_fin_count = count

    def _save_flag_fin(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        if self.flag_fin_mode == 'FIXED':
            ext.flags = self._flags
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_fin_step
            o_variable_field.mask = self._flag_fin_mask
            o_variable_field.type = self._flag_fin_type
            o_variable_field.offset = self._flag_fin_offset
            o_variable_field.mode = self._flag_fin_mode
            o_variable_field.count = self._flag_fin_count
            o_variable_field.value = self._flags

    def _fetch_flag_fin(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_fin_offset and mask == self._flag_fin_mask:
                self._flags = o_variable_field.value
                self._flag_fin_mode = o_variable_field.mode
                self._flag_fin_count = o_variable_field.count
                self._flag_fin_step = o_variable_field.step
                return
        else:
            self._flags = ext.flags

    @property
    def flag_ns(self):
        """
        ECN-nonce concealment protection (experimental). By default, this attribute is set automatically. Set :attr:`flag_ns_override` to ``True`` to override this field
        """
        return self._hdrlen_rsvd & 1

    @flag_ns.setter
    def flag_ns(self, value):
        current_value = getattr(self, '_hdrlen_rsvd', 0)
        self._hdrlen_rsvd = (current_value & (~1 & 255)) + ((utils.parse(value) << 0) & 1)

    @property
    def flag_ns_mode(self):
        """
        By default, :attr:`flag_ns_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._flag_ns_mode)

    @flag_ns_mode.setter
    def flag_ns_mode(self, mode):
        self._flag_ns_mode = baseclass.FieldMode.get_value(mode)

    _flag_ns_offset = 12
    _flag_ns_type = 0
    _flag_ns_full_mask = 255
    _flag_ns_mask = 1

    @property
    def flag_ns_step(self):
        """
        If :attr:`flag_ns_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._flag_ns_step >> 0

    @flag_ns_step.setter
    def flag_ns_step(self, step):
        self._flag_ns_step = step << 0

    @property
    def flag_ns_count(self):
        """
        If :attr:`flag_ns_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._flag_ns_count

    @flag_ns_count.setter
    def flag_ns_count(self, count):
        self._flag_ns_count = count

    @property
    def flag_ns_override(self):
        return self._flag_ns_override

    @flag_ns_override.setter
    def flag_ns_override(self, override):
        self._flag_ns_override = override

    def _save_flag_ns(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        ext.is_override_hdrlen = self.flag_ns_override
        if self.flag_ns_mode == 'FIXED':
            ext.hdrlen_rsvd = self._hdrlen_rsvd
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._flag_ns_step
            o_variable_field.mask = self._flag_ns_mask
            o_variable_field.type = self._flag_ns_type
            o_variable_field.offset = self._flag_ns_offset
            o_variable_field.mode = self._flag_ns_mode
            o_variable_field.count = self._flag_ns_count
            o_variable_field.value = self._hdrlen_rsvd

    def _fetch_flag_ns(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]
        self.flag_ns_override = ext.is_override_hdrlen
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._flag_ns_offset and mask == self._flag_ns_mask:
                self._hdrlen_rsvd = o_variable_field.value
                self._flag_ns_mode = o_variable_field.mode
                self._flag_ns_count = o_variable_field.count
                self._flag_ns_step = o_variable_field.step
                return
        else:
            self._hdrlen_rsvd = ext.hdrlen_rsvd

    def __str__(self):
        return 'Tcp(flag_ack={},header_length={},reserved={},ack_num={},flag_rst={},window_size={},destination={},flag_psh={},urgent_pointer={},source={},flag_ece={},flag_urg={},sequence_num={},checksum={},flag_syn={},flag_cwr={},flag_fin={},flag_ns={},)'.format(self.flag_ack,self.header_length,self.reserved,self.ack_num,self.flag_rst,self.window_size,self.destination,self.flag_psh,self.urgent_pointer,self.source,self.flag_ece,self.flag_urg,self.sequence_num,self.checksum,self.flag_syn,self.flag_cwr,self.flag_fin,self.flag_ns,)

    def to_dict(self):
        """
        Return the Tcp layer configuration as a
        dictionnary.
        """
        return { 
            'flag_ack': self.flag_ack,
            'flag_ack_mode': self.flag_ack_mode,
            'flag_ack_count': self.flag_ack_count,
            'flag_ack_step': self.flag_ack_step,
            'header_length': self.header_length,
            'header_length_mode': self.header_length_mode,
            'header_length_count': self.header_length_count,
            'header_length_step': self.header_length_step,
            'header_length_override': self.header_length_override,
            'reserved': self.reserved,
            'reserved_mode': self.reserved_mode,
            'reserved_count': self.reserved_count,
            'reserved_step': self.reserved_step,
            'reserved_override': self.reserved_override,
            'ack_num': self.ack_num,
            'ack_num_mode': self.ack_num_mode,
            'ack_num_count': self.ack_num_count,
            'ack_num_step': self.ack_num_step,
            'flag_rst': self.flag_rst,
            'flag_rst_mode': self.flag_rst_mode,
            'flag_rst_count': self.flag_rst_count,
            'flag_rst_step': self.flag_rst_step,
            'window_size': self.window_size,
            'window_size_mode': self.window_size_mode,
            'window_size_count': self.window_size_count,
            'window_size_step': self.window_size_step,
            'destination': self.destination,
            'destination_mode': self.destination_mode,
            'destination_count': self.destination_count,
            'destination_step': self.destination_step,
            'destination_override': self.destination_override,
            'flag_psh': self.flag_psh,
            'flag_psh_mode': self.flag_psh_mode,
            'flag_psh_count': self.flag_psh_count,
            'flag_psh_step': self.flag_psh_step,
            'urgent_pointer': self.urgent_pointer,
            'urgent_pointer_mode': self.urgent_pointer_mode,
            'urgent_pointer_count': self.urgent_pointer_count,
            'urgent_pointer_step': self.urgent_pointer_step,
            'source': self.source,
            'source_mode': self.source_mode,
            'source_count': self.source_count,
            'source_step': self.source_step,
            'source_override': self.source_override,
            'flag_ece': self.flag_ece,
            'flag_ece_mode': self.flag_ece_mode,
            'flag_ece_count': self.flag_ece_count,
            'flag_ece_step': self.flag_ece_step,
            'flag_urg': self.flag_urg,
            'flag_urg_mode': self.flag_urg_mode,
            'flag_urg_count': self.flag_urg_count,
            'flag_urg_step': self.flag_urg_step,
            'sequence_num': self.sequence_num,
            'sequence_num_mode': self.sequence_num_mode,
            'sequence_num_count': self.sequence_num_count,
            'sequence_num_step': self.sequence_num_step,
            'checksum': self.checksum,
            'checksum_mode': self.checksum_mode,
            'checksum_count': self.checksum_count,
            'checksum_step': self.checksum_step,
            'checksum_override': self.checksum_override,
            'flag_syn': self.flag_syn,
            'flag_syn_mode': self.flag_syn_mode,
            'flag_syn_count': self.flag_syn_count,
            'flag_syn_step': self.flag_syn_step,
            'flag_cwr': self.flag_cwr,
            'flag_cwr_mode': self.flag_cwr_mode,
            'flag_cwr_count': self.flag_cwr_count,
            'flag_cwr_step': self.flag_cwr_step,
            'flag_fin': self.flag_fin,
            'flag_fin_mode': self.flag_fin_mode,
            'flag_fin_count': self.flag_fin_count,
            'flag_fin_step': self.flag_fin_step,
            'flag_ns': self.flag_ns,
            'flag_ns_mode': self.flag_ns_mode,
            'flag_ns_count': self.flag_ns_count,
            'flag_ns_step': self.flag_ns_step,
            'flag_ns_override': self.flag_ns_override,
        }

    def from_dict(self, dict_):
        """
        Set the Tcp layer configuration from a
        dictionary. Keys must be the same as the attributes names, and values
        but by valid values for these attributes.
        """
        for attribute, value in dict_.items():
            setattr(self, attribute, value)