import os
from jinja2 import Environment, PackageLoader
from ostinato.core import ost_pb
from . import constants


class _Generator(object):

    class Attribute(object):

        def __init__(self, name, offset, default_value, full_mask, mask, ext_name, override, doc):
            self.name = name
            self.offset = offset
            self.default_value = default_value
            self.mask = mask
            self.ext_name = ext_name
            if override:
                self.auto = True
                self.ext_override = override
                doc = '{}. By default, this attribute is set automatically. Set :attr:`{}_override` to ``True`` to override this field'.format(doc, name)
            else:
                self.auto = False
                self.ext_override = None
            self.doc = doc
            if mask == 0:
                self.shift = 0
            else:
                shift = 0
                while (mask >> shift) % 2 == 0:
                    shift += 1
                self.shift = shift
            self.full_mask = full_mask
            if self.full_mask > 0xffff:
                self.counter = ost_pb.VariableField.kCounter32
            elif self.full_mask > 0xff:
                self.counter = ost_pb.VariableField.kCounter16
            else:
                self.counter = ost_pb.VariableField.kCounter8

    def __init__(self, attributes, class_name=None, protocol_id=None, extension=None, doc=None):
        self.class_name = class_name
        self.protocol_id = protocol_id
        self.extension = extension
        self.doc = doc
        self.attributes = []
        for attribute_name, attribute in attributes.iteritems():
            self.attributes.append(self.Attribute(attribute_name, *attribute))


def generate_classes():
    protocols = [
        {
            'class_name':   'Mac',
            'doc':          'Represent the MAC layer. Since we make a distiction between the MAC layer and the Ethernet layer, this layer defines the source and destination MAC addresses.',
            'protocol_id':  constants._Protocols.MAC,
            'extension':    'mac_pb2.mac',
            'attributes': {
                'destination': (0, 'FF:FF:FF:FF:FF:FF', 0xffffffffffff, 0xffffffffffff, 'dst_mac', None, 'Destination MAC address'),
                'source':      (6, '00:00:00:00:00:00', 0xffffffffffff, 0xffffffffffff, 'src_mac', None, 'Source MAC address'),
            },
        },
        {
            'class_name':   'Ethernet',
            'doc':          'Represent the ethernet layer. Since we make a distinction between the MAC layer and the Ethernet layer, this layer only defines the ethernet type',
            'protocol_id':  constants._Protocols.ETHERNET_II,
            'extension':    'eth2_pb2.eth2',
            'attributes': {
                'ether_type': (0, '0x0800', 0xffff, 0xffff, 'type', 'type', 'Ethernet type field. 0x800 is for IPv4 inner packets.'),
            },
        },
        {
            'class_name':   'IPv4',
            'doc':          'Represent the IPv4 layer.',
            'protocol_id':  constants._Protocols.IP4,
            'extension':    'ip4_pb2.ip4',
            'attributes': {
                'version':          (0,  4,           0xff      , 0xf0,       'ver_hdrlen', 'ver',    'Version of the protocol (usually 4 or 6)'),
                'header_length':    (0,  5,           0xff      , 0x0f,       'ver_hdrlen', 'hdrlen', 'Internet Header Length (IHL): number of 4 bytes words in the header. The minimum valid value is 5, and maximum valid value is 15.'),
                'tos':              (1,  0,           0xff      , 0xff,       'tos'       , None,     'Type Of Service (TOS) field. This field is now the Differentiated Services Code Point (DSCP) field.'),
                'dscp':             (1,  0,           0xff      , 0xff,       'tos'       , None,     'Differentiated Services Code Point (DSCP) field (previously known as Type Of Service (TOS) field'),
                'total_length':     (2,  0,           0xffff    , 0xffff,     'totlen'    , 'totlen', 'Total length of the IP packet in bytes. The minimum valid value is 20, and the maxium is 65,535'),
                'identification':   (2,  0,           0xffff    , 0xffff,     'id'        , None,     'Identification field. This is used to identify packet fragments'),
                # normally the mask is 0b10000000 but it has special handling in ostinato
                'flag_unused':      (6,  0,           0xff      , 0x04,       'flags'     , None,     'A 1 bit unused flag'),
                # normally the mask is 0b01000000 but it has special handling in ostinato
                'flag_df':          (6,  0,           0xff      , 0x02,       'flags'     , None,     'The "Don\'t Fragment" (DF) 1 bit flag'),
                # normally the mask is 0b00100000 but it has special handling in ostinato
                'flag_mf':          (6,  0,           0xff      , 0x01,       'flags'     , None,     'The "More Fragments" (MF) 1 bit flag'),
                'fragments_offset': (6,  0,           0xffff    , 0x1fff,     'frag_ofs'  , None,     'The Fragment Offset field indicates the offset of a packet fragment in the original IP packet'),
                'ttl':              (8,  127,         0xff      , 0xff,       'ttl'       , None,     'Time To Live (TTL) field.'),
                'protocol':         (9,  0,           0xff      , 0xff,       'proto'     , 'proto',  'Indicates the protocol that is encapsulated in the IP packet.'),
                'checksum':         (10, 0,           0xffff    , 0xffff,     'cksum'     , 'cksum',  'Header checksum'),
                'source':           (12, '127.0.0.1', 0xffffffff, 0xffffffff, 'src_ip'    , None,     'Source IP address'),
                'destination':      (16, '127.0.0.1', 0xffffffff, 0xffffffff, 'dst_ip'    , None,     'Destination IP address'),
            },
        },
        {
            'class_name':   'Udp',
            'doc':          'Represent an UDP datagram',
            'protocol_id':  constants._Protocols.UDP,
            'extension':    'udp_pb2.udp',
            'attributes': {
                'source':       (0, 49152, 0xffff, 0xffff, 'src_port', 'src_port', 'Source port number'),
                'destination':  (2, 49153, 0xffff, 0xffff, 'dst_port', 'dst_port', 'Destination port number'),
                'length':       (4, 0,     0xffff, 0xffff, 'totlen',   'totlen',   'Length of the UDP datagram (header and payload).'),
                'checksum':     (6, 0,     0xffff, 0xffff, 'cksum',    'cksum',    'Checksum of the datagram, calculated based on the IP pseudo-header.')
            },
        },
        {
            'class_name':   'Tcp',
            'doc':          'Represent an TCP datagram',
            'protocol_id':  constants._Protocols.TCP,
            'extension':    'tcp_pb2.tcp',
            'attributes': {
                'source':           (0,  49152, 0xffff    , 0xffff,      'src_port',    'src_port', 'Source port number'),
                'destination':      (2,  49153, 0xffff    , 0xffff,      'dst_port',    'dst_port', 'Destination port number'),
                'sequence_num':     (4,  0,     0xffffffff, 0xffffffff,  'seq_num',     None,       'Sequence number of the datagram. Its meaning depends on the :attr:`syn` flag value.'),
                'ack_num':          (8,  0,     0xffffffff, 0xffffffff,  'ack_num',     None,       'Acknowledgement number'),
                'header_length':    (12, 0,     0xff      , 0xf0,        'hdrlen_rsvd', 'hdrlen',   'Size of the TCP header in 4 bytes words. This field is also known as "Data offset"'),
                'reserved':         (12, 0,     0xff      , 0x0e,        'hdrlen_rsvd', 'hdrlen',   'Reserved for future use and must be set to 0'),
                'flag_ns':          (12, 0,     0xff      , 0x01,        'hdrlen_rsvd', 'hdrlen',   'ECN-nonce concealment protection (experimental)'),
                'flag_cwr':         (13, 0,     0xff      , 0x01 << 7,   'flags',       None,       'Congestion Window Reduced flag'),
                'flag_ece':         (13, 0,     0xff      , 0x01 << 6,   'flags',       None,       'ECN-Echo flag. Its meaning depends on the :attr:`syn` field value.'),
                'flag_urg':         (13, 0,     0xff      , 0x01 << 5,   'flags',       None,       'Urgent pointer flag.'),
                'flag_ack':         (13, 0,     0xff      , 0x01 << 4,   'flags',       None,       'ACK flag'),
                'flag_psh':         (13, 0,     0xff      , 0x01 << 3,   'flags',       None,       'Push function'),
                'flag_rst':         (13, 0,     0xff      , 0x01 << 2,   'flags',       None,       'Reset the connection'),
                'flag_syn':         (13, 0,     0xff      , 0x01 << 1,   'flags',       None,       'Synchronize sequence numbers'),
                'flag_fin':         (13, 0,     0xff      , 0x01,        'flags',       None,       'No more data from sender'),
                'window_size':      (14, 0,     0xffff    , 0xffff,      'window',      None,       'Size of the receive window, which specifies the number of window size units that the sender of this segment is currently willing to receive'),
                'checksum':         (16, 0,     0xffff    , 0xffff,      'cksum',       'cksum',    'Checksum of the datagram, calculated based on the IP pseudo-header. Its meaning depends on the value og the :attr:`ack` flag.'),
                'urgent_pointer':   (18, 0,     0xffff    , 0xffff,      'urg_ptr',     None,       'Urgent pointer.')
            },
        },
        # {
        #     'class_name': 'Payload',
        #     'doc':        'Represent the payload. This layer can be encapsulated in any other layer',
        #     'protocol_id': constants._Protocols.PAYLOAD,
        #     'extension': 'payload_pb2.payload',
        #     'attributes': {
        #         'mode':     (-1,   'FIXED_WORD',  0,      0,      'pattern_mode', None, 'Mode to generate the payload content'),
        #         'pattern':  (0,    '00 00 00 00', 0xffff, 0xffff, 'pattern',      None, 'Payload initial word. Depending on the chosen mode, this word will be repeated unchanged, incremented/decremented, or randomized'),
        #     },
        # },
    ]
    data = []
    for protocol in protocols:
        data.append(_Generator(**protocol))
    env = Environment(loader=PackageLoader('simple_ostinato', 'templates'))
    template = env.get_template('protocols.tpl')
    pkg_dir = os.path.dirname(os.path.realpath(__file__))
    target = os.path.join(pkg_dir, 'protocols', 'autogenerates.py')
    with open(target, 'w') as file_:
        file_.write(template.render(classes=data))

if __name__ == '__main__':
    generate_classes()
