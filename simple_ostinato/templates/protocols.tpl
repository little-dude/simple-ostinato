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

    _protocol_id = {{ class.protocol_id}}
    _extension = {{ class.extension }}

    def __init__(self{% for attribute in class.attributes %}, {{ attribute.name}}={% if attribute.default_value is string %}'{% endif %}{{attribute.default_value}}{% if attribute.default_value is string %}'{% endif %}{% endfor %}, **kwargs):
        super(_{{class.class_name}}, self).__init__({% for attribute in class.attributes %}{{ attribute.name}}={{ attribute.name }}, {% endfor %}**kwargs)
        {% for attribute in class.attributes %}
        self.{{ attribute.name }}_mode = 'FIXED'
        self.{{ attribute.name }}_step = 1
        self.{{ attribute.name }}_count = 1{% if attribute.auto == true %}
        self.{{ attribute.name }}_override = False{% endif %}{% endfor %}{% for attribute in class.attributes %}

    @property
    def {{ attribute.name }}(self):
        """
        {{ attribute.doc }}
        """
        {% if attribute.shift is equalto 0 %}return self._{{ attribute.ext_name }} & {{ attribute.mask }}{% else %}return (self._{{ attribute.ext_name }} & {{ attribute.mask }}) >> {{ attribute.shift }}{% endif %}

    @{{ attribute.name }}.setter
    def {{ attribute.name }}(self, value):
        current_value = getattr(self, '_{{ attribute.ext_name }}', 0)
        self._{{ attribute.ext_name }} = (current_value & (~{{ attribute.mask }} & {{ attribute.full_mask }})) + ((utils.parse(value) << {{ attribute.shift }}) & {{ attribute.mask }})

    @property
    def {{ attribute.name }}_mode(self):
        """
        By default, :attr:`{{ attribute.name }}_mode` is ``FIXED``.
        Possible values are: ``INCREMENT``, ``DECREMENT``, ``RANDOM``, ``FIXED``.
        """
        return baseclass.FieldMode.get_key(self._{{ attribute.name }}_mode)

    @{{ attribute.name }}_mode.setter
    def {{ attribute.name }}_mode(self, mode):
        self._{{ attribute.name}}_mode = baseclass.FieldMode.get_value(mode)

    _{{ attribute.name }}_offset = {{ attribute.offset }}
    _{{ attribute.name }}_type = {{ attribute.counter }}
    _{{ attribute.name }}_full_mask = {{ attribute.full_mask }}
    _{{ attribute.name }}_mask = {{ attribute.mask }}

    @property
    def {{ attribute.name }}_step(self):
        """
        If :attr:`{{ attribute.name }}_mode` is set to ``INCREMENT`` or ``DECREMENT``, specifies the increment or decrement step.
        """
        return self._{{ attribute.name }}_step

    @{{ attribute.name }}_step.setter
    def {{ attribute.name }}_step(self, step):
        self._{{ attribute.name}}_step = step

    @property
    def {{ attribute.name }}_count(self):
        """
        If :attr:`{{ attribute.name }}_mode` is ``INCREMENT``, ``DECREMENT``, specifies the number of packets before resetting the field to its initial value.
        """
        return self._{{ attribute.name }}_count

    @{{ attribute.name }}_count.setter
    def {{ attribute.name }}_count(self, count):
        self._{{ attribute.name}}_count = count{% if attribute.auto == true %}

    @property
    def {{ attribute.name }}_override(self):
        return self._{{ attribute.name }}_override

    @{{ attribute.name }}_override.setter
    def {{ attribute.name }}_override(self, override):
        self._{{ attribute.name }}_override = override{% endif %}

    def _save_{{ attribute.name }}(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]{% if attribute.auto == true %}
        ext.is_override_{{ attribute.ext_override }} = self.{{ attribute.name }}_override{% endif %}
        if self.{{ attribute.name }}_mode == 'FIXED':
            ext.{{ attribute.ext_name }} = self._{{ attribute.ext_name }}
        else:
            o_variable_field = o_protocol.variable_field.add()
            o_variable_field.step = self._{{ attribute.name }}_step
            o_variable_field.mask = self._{{ attribute.name }}_mask
            o_variable_field.type = self._{{ attribute.name }}_type
            o_variable_field.offset = self._{{ attribute.name }}_offset
            o_variable_field.mode = self._{{ attribute.name }}_mode
            o_variable_field.count = self._{{ attribute.name }}_count
            o_variable_field.value = self._{{ attribute.ext_name }}

    def _fetch_{{ attribute.name }}(self, o_protocol):
        ext = o_protocol.Extensions[self._extension]{% if attribute.auto == true %}
        self.{{ attribute.name }}_override = ext.is_override_{{ attribute.ext_override }}{% endif %}
        for o_variable_field in o_protocol.variable_field:
            offset, mask = o_variable_field.offset, o_variable_field.mask
            if offset == self._{{ attribute.name }}_offset and mask == self._{{ attribute.name }}_mask:
                self._{{ attribute.ext_name }} = o_variable_field.value
                self._{{ attribute.name }}_mode = o_variable_field.mode
                self._{{ attribute.name }}_count = o_variable_field.count
                self._{{ attribute.name }}_step = o_variable_field.step
                return
        else:
            self._{{ attribute.ext_name }} = ext.{{ attribute.ext_name }}{% endfor %}

    def __str__(self):
        return '{{ class.class_name }}({% for attribute in class.attributes %}{{ attribute.name }}={},{% endfor %})'.format({% for attribute in class.attributes %}self.{{ attribute.name }},{% endfor %})

    def to_dict(self):
        """
        Return the {{ class.class_name }} layer configuration as a
        dictionnary.
        """
        return { {% for attribute in class.attributes %}
            '{{ attribute.name }}': self.{{ attribute.name }},
            '{{ attribute.name }}_mode': self.{{ attribute.name }}_mode,
            '{{ attribute.name }}_count': self.{{ attribute.name }}_count,
            '{{ attribute.name }}_step': self.{{ attribute.name }}_step,{% if attribute.auto == true %}
            '{{ attribute.name }}_override': self.{{ attribute.name }}_override,{% endif %}{% endfor %}
        }

    def from_dict(self, dict_):
        """
        Set the {{ class.class_name }} layer configuration from a
        dictionary. Keys must be the same as the attributes names, and values
        but by valid values for these attributes.
        """
        for attribute, value in dict_.items():
            setattr(self, attribute, value){% endfor %}
