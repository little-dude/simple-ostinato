import os
import textwrap
from jinja2 import Environment, PackageLoader
from . import constants


class _Generator(object):

    class Attribute(object):

        def __init__(self, name, offset, default_value, mask, ext_name, computed, doc):
            self.name = name
            self.offset = offset
            self.default_value = default_value
            self.mask = mask
            self.ext_name = ext_name
            if computed is True:
                doc = '{}\nBy default, this attribute is computed automatically.'.format(doc)
            self.doc = textwrap.wrap(doc, 79)

    def __init__(self, attributes, class_name=None, protocol_id=None, extension=None, doc=None):
        self.class_name = class_name
        self.protocol_id = protocol_id
        self.extension = extension
        self.doc = textwrap.wrap(doc, 79)
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
                'destination': (0, '00:00:00:00:00:00', 0xffffffffffff, 'dst_mac', False, 'Destination MAC address'),
                'source':      (6, 'FF:FF:FF:FF:FF:FF', 0xffffffffffff, 'src_mac', False, 'Source MAC address'),
            },
        },
        {
            'class_name':   'Ethernet',
            'doc':          'Represent the ethernet layer. Since we make a distinction between the MAC layer and the Ethernet layer, this layer only defines the ethernet type',
            'protocol_id':  constants._Protocols.ETHERNET_II,
            'extension':    'eth2_pb2.eth2',
            'attributes': {
                'ether_type': (0, '0x0800', 0xffff, 'type', False, 'Ethernet type field. 0x800 is for IPv4 inner packets.'),
            },
        },
        {
            'class_name':   'IPv4',
            'doc':          'Represent the IPv4 layer.',
            'protocol_id':  constants._Protocols.IP4,
            'extension':    'ip4_pb2.ip4',
            'attributes': {
                'version':          (0,  4,           '0xf0',       'ver_hdrlen', False, 'Version of the protocol (usually 4 or 6)'),
                'header_length':    (0,  5,           '0x0f',       'ver_hdrlen', True,  'Internet Header Length (IHL): number of 4 bytes words in the header. The minimum valid value is 5, and maximum valid value is 15.'),
                'tos':              (1,  0,           '0xff',       'tos'       , False, 'Type Of Service (TOS) field. This field is now the Differentiated Services Code Point (DSCP) field.'),
                'dscp':             (1,  0,           '0xff',       'tos'       , False, 'Differentiated Services Code Point (DSCP) field (previously known as Type Of Service (TOS) field'),
                'total_length':     (2,  0,           '0xffff',     'totlen'    , True,  'Total length of the IP packet in bytes. The minimum valid value is 20, and the maxium is 65,535'),
                'identification':   (2,  0,           '0xffff',     'id'        , False, 'Identification field. This is used to identify packet fragments'),
                'flags':            (6,  0,           '0xe0',       'flags'     , False, 'A three bits field: bit 0 is reserved, bit 1 is the Don\'t Fragment (DF) flag, and bit 2 is the More Fragments (MF) flags'),
                'fragments_offset': (6,  0,           '0x1fff',     'frag_ofs'  , False, 'The Fragment Offset field indicates the offset of a packet fragment in the original IP packet'),
                'ttl':              (8,  127,         '0xff',       'ttl'       , False, 'Time To Live (TTL) field.'),
                'protocol':         (9,  0,           '0xff',       'proto'     , False, 'Indicates the protocol that is encapsulated in the IP packet.'),
                'checksum':         (10, 0,           '0xffff',     'cksum'     , True,  'Header checksum'),
                'source':           (12, '127.0.0.1', '0xffffffff', 'src_ip'    , False, 'Source IP address'),
                'destination':      (16, '127.0.0.1', '0xffffffff', 'dst_ip'    , False, 'Destination IP address'),
            },
        },
        {
            'class_name': 'Payload',
            'doc':        'Represent the payload. This layer can be encapsulated in any other layer',
            'protocol_id': constants._Protocols.PAYLOAD,
            'extension': 'payload_pb2.payload',
            'attributes': {
                'mode':     (None, 'FIXED_WORD',  None,   'pattern_mode', False, 'Mode to generate the payload content'),
                'pattern':  (0,    '00 00 00 00', 0xffff, 'pattern',      False, 'Payload initial word. Depending on the chosen mode, this word will be repeated unchanged, incremented/decremented, or randomized'),
            },
        },
    ]
    data = []
    for protocol in protocols:
        data.append(_Generator(**protocol))
    env = Environment(loader=PackageLoader('ostinato_client', 'templates'))
    template = env.get_template('protocols.tpl')
    pkg_dir = os.path.dirname(os.path.realpath(__file__))
    target = os.path.join(pkg_dir, 'protocols', 'autogenerates.py')
    with open(target, 'w') as file_:
        file_.write(template.render(classes=data))

if __name__ == '__main__':
    generate_classes()
