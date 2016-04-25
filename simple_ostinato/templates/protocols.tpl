from ostinato.protocols import arp_pb2, gmp_pb2, ip4over6_pb2, mld_pb2, \
    tcp_pb2, dot2llc_pb2, hexdump_pb2, ip6_pb2, payload_pb2, textproto_pb2, \
    dot2snap_pb2, icmp_pb2, ip6over4_pb2, protocol_pb2, udp_pb2, dot3_pb2, \
    igmp_pb2, ip6over6_pb2, sample_pb2, userscript_pb2, eth2_pb2, ip4_pb2, \
    llc_pb2, snap_pb2, vlan_pb2, fileformat_pb2, ip4over4_pb2, mac_pb2, \
    svlan_pb2, vlanstack_pb2
from . import baseclass
from .. import utils{% for class in classes %}


class _{{class.class_name}}(baseclass.Protocol):

    """
    {{ class.doc }}
    """

    protocol_id = {{ class.protocol_id}}
    _extension = {{ class.extension }}

    def __init__(self{% for attribute in class.attributes %}, {{ attribute.name}}={% if attribute.default_value is string %}'{% endif %}{{attribute.default_value}}{% if attribute.default_value is string %}'{% endif %}{% endfor %}, **kwargs):
        super(_{{class.class_name}}, self).__init__({% for attribute in class.attributes %}{{ attribute.name}}={{ attribute.name }}, {% endfor %}**kwargs){% for attribute in class.attributes %}

    @property
    def {{ attribute.name }}(self):
        """
        {{ attribute.doc }}
        """
        return utils.to_str(self._{{ attribute.name }})

    @{{ attribute.name }}.setter
    def {{ attribute.name }}(self, value):
        self._{{ attribute.name }} = utils.parse(value)

    def _save_{{ attribute.name }}(self, ext):
        ext.{{ attribute.ext_name }} = self._{{ attribute.name }}

    def _fetch_{{ attribute.name }}(self, ext):
        self._{{ attribute.name }} = ext.{{ attribute.ext_name }}{% endfor %}{% endfor %}
