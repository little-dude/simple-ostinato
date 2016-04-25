from ostinato.protocols.protocol_pb2 import StreamControl
from ostinato.core import ost_pb
import weakref
from . import utils
from . import protocols
from . import constants


class SendMode(utils.Enum):

    FIXED = StreamControl.SendMode.Value('e_sm_fixed')
    CONTINUOUS = StreamControl.SendMode.Value('e_sm_continuous')


class SendUnit(utils.Enum):

    PACKETS = StreamControl.SendUnit.Value('e_su_packets')
    BURSTS = StreamControl.SendUnit.Value('e_su_bursts')


class SendNext(utils.Enum):

    STOP = StreamControl.NextWhat.Value('e_nw_stop')
    GOTO_NEXT = StreamControl.NextWhat.Value('e_nw_goto_next')
    GOTO_ID = StreamControl.NextWhat.Value('e_nw_goto_id')


class Stream(object):

    def __init__(self, port, stream_id):
        self.port = port
        self.stream_id = stream_id
        self.fetch()

    @property
    def port(self):
        if not hasattr(self, '_port'):
            return None
        return self._port()

    @port.setter
    def port(self, value):
        self._port = weakref.ref(value)

    @property
    def drone(self):
        return self.port.drone

    @drone.setter
    def drone(self, value):
        raise ValueError('Read-only attribute')

    def _fetch_layers(self, o_stream):
        o_protocols = o_stream.protocol
        empty_protocols = []
        self.layers = {}
        for o_protocol in o_protocols:
            protocol_id = o_protocol.protocol_id.id
            if protocol_id == 0:
                empty_protocols.append(o_protocol)
                continue
            protocol_name = constants._Protocols.get_key(protocol_id)
            if protocol_name in self.layers:
                err = '{} found twice in {} protocols'
                raise Exception(err.format(protocol_name, self))
            self.layers[protocol_name] = protocol_factory(o_protocol)

    def _save_layers(self, o_stream):
        o_protocols = o_stream.protocol
        for layer in self.layers.values():
            is_new_layer = True
            for o_protocol in o_protocols:
                if layer.protocol_id == o_protocol.protocol_id.id:
                    is_new_layer = False
                    layer._save(o_protocol)
                    break
            if is_new_layer is True:
                # the layer has not been added to the stream yet.
                o_protocol = o_stream.protocol.add()
                o_protocol.protocol_id.id = layer.protocol_id
                layer._save(o_protocol)

    def add_layer(self, layer):
        self.layers[layer.__class__.__name__] = layer

    def save(self):
        o_streams = self._fetch()
        o_stream = o_streams.stream[0]
        o_stream.core.is_enabled = self.is_enabled
        o_stream.core.name = self.name
        o_stream.control.unit = self._unit
        o_stream.control.mode = self._mode
        o_stream.control.num_bursts = self.num_bursts
        o_stream.control.num_packets = self.num_packets
        o_stream.control.packets_per_burst = self.packets_per_burst
        o_stream.control.next = self._next
        o_stream.control.bursts_per_sec = self.bursts_per_sec
        o_stream.control.packets_per_sec = self.packets_per_sec
        self._save_layers(o_stream)
        self.drone._o_modify_stream(o_streams)

    def fetch(self):
        o_stream = self._fetch().stream[0]
        self.name = o_stream.core.name
        self.is_enabled = o_stream.core.is_enabled
        self._unit = o_stream.control.unit
        self._mode = o_stream.control.mode
        self.num_bursts = o_stream.control.num_bursts
        self.num_packets = o_stream.control.num_packets
        self.packets_per_burst = o_stream.control.packets_per_burst
        self._next = o_stream.control.next
        self.bursts_per_sec = o_stream.control.bursts_per_sec
        self.packets_per_sec = o_stream.control.packets_per_sec
        self._fetch_layers(o_stream)

    def _fetch(self):
        o_stream_ids = ost_pb.StreamIdList()
        o_stream_ids.port_id.id = self.port.port_id
        o_stream_id = o_stream_ids.stream_id.add()
        o_stream_id.id = self.stream_id
        o_streams = self.drone._o_get_stream_list(o_stream_ids)
        return o_streams

    @property
    def name(self):
        if not hasattr(self, '_name'):
            return ''
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def enable(self):
        self._is_enabled = True

    def disable(self):
        self._is_enabled = False

    @property
    def is_enabled(self):
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError('expected boolean value')
        self._is_enabled = value

    @property
    def unit(self):
        return SendUnit.get_key(self._unit)

    @unit.setter
    def unit(self, unit):
        self._unit = SendUnit.get_value(unit)

    @property
    def mode(self):
        return SendMode.get_key(self._mode)

    @mode.setter
    def mode(self, mode):
        self._mode = SendMode.get_value(mode)

    @property
    def num_packets(self):
        return self._num_packets

    @num_packets.setter
    def num_packets(self, value):
        self._num_packets = int(value)

    @property
    def num_bursts(self):
        return self._num_bursts

    @num_bursts.setter
    def num_bursts(self, value):
        self._num_bursts = int(value)

    @property
    def packets_per_burst(self):
        return self._packets_per_burst

    @packets_per_burst.setter
    def packets_per_burst(self, value):
        self._packets_per_burst = value

    @property
    def next(self):
        return SendNext.get_key(self._next)

    @next.setter
    def next(self, value):
        self._next = SendNext.get_value(value)

    @property
    def bursts_per_sec(self):
        return self._bursts_per_sec

    @bursts_per_sec.setter
    def bursts_per_sec(self, value):
        self._bursts_per_sec = int(value)

    @property
    def packets_per_sec(self):
        return self._packets_per_sec

    @packets_per_sec.setter
    def packets_per_sec(self, value):
        self._packets_per_sec = int(value)

    def __str__(self):
        if not self.name:
            name = 'None'
        else:
            name = self.name
        return 'Stream (id={}, name={})'.format(self.stream_id, name)


def protocol_factory(o_protocol):
    proto_cls_mapping = {
        constants._Protocols.MAC: protocols.Mac,
        constants._Protocols.ETHERNET_II: protocols.Ethernet,
        constants._Protocols.IP4: protocols.IPv4,
        constants._Protocols.PAYLOAD: protocols.Payload,
    }
    protocol_id = o_protocol.protocol_id.id
    protocol_cls = proto_cls_mapping[protocol_id]
    protocol = protocol_cls()
    protocol._fetch(o_protocol)
    return protocol
