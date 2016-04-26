"""
This module provide a class to manipulate streams.
"""
from ostinato.protocols.protocol_pb2 import StreamControl
from ostinato.core import ost_pb
import weakref
from . import utils
from . import protocols
from . import constants


class _SendMode(utils.Enum):

    FIXED = StreamControl.SendMode.Value('e_sm_fixed')
    CONTINUOUS = StreamControl.SendMode.Value('e_sm_continuous')


class _SendUnit(utils.Enum):

    PACKETS = StreamControl.SendUnit.Value('e_su_packets')
    BURSTS = StreamControl.SendUnit.Value('e_su_bursts')


class _SendNext(utils.Enum):

    STOP = StreamControl.NextWhat.Value('e_nw_stop')
    GOTO_NEXT = StreamControl.NextWhat.Value('e_nw_goto_next')
    GOTO_ID = StreamControl.NextWhat.Value('e_nw_goto_id')


class Stream(object):

    """
    Represent a stream configured on a port. Besides all the stream
    configuration parameters, a stream class has `layers` which define the
    packets to be sent.

    Args:

        port (simple_ostinato.port.Port): the port instance on which the stream
            is defined.
        stream_id (int): the stream ID.
    """

    def __init__(self, port, stream_id, clean_layers=True):
        self.port = port
        self.layers = []
        self.stream_id = stream_id
        self.fetch()
        if clean_layers:
            self.del_layers(*self.layers.keys())

    @property
    def port(self):
        """
        Reference to the port on which this stream is configured.
        """
        if not hasattr(self, '_port'):
            return None
        return self._port()

    @port.setter
    def port(self, value):
        self._port = weakref.ref(value)

    @property
    def drone(self):
        """
        Reference to the ``simple_ostinato.drone.Drone`` instance. This is
        mostly for internal use.
        """
        return self.port.drone

    @drone.setter
    def drone(self, value):
        raise ValueError('Read-only attribute')

    @property
    def layers(self):
        """
        Dictionnary of all the layers configured for this stream. For now,
        layers cannot be removed. To remove layers, the entire stream must be
        deleted and another one re-created.
        """
        return self._layers

    @layers.setter
    def layers(self, value):
        self._layers = value

    def _fetch_layers(self, o_stream):
        o_protocols = o_stream.protocol
        empty_protocols = []
        self.layers = {}
        for o_protocol in o_protocols:
            protocol_id = o_protocol.protocol_id.id
            if protocol_id == 0:
                empty_protocols.append(o_protocol)
                continue
            self.add_layers(_protocol_factory(o_protocol))

    def _save_layers(self):
        o_streams = self._fetch()
        o_stream = o_streams.stream[0]
        o_protocols = o_stream.protocol
        # remove the deleted layers, or update the existing ones
        remove_list = []
        for o_protocol in o_protocols:
            protocol_name = _protocol_factory(o_protocol).__class__.__name__
            if protocol_name not in self.layers:
                remove_list.append(o_protocol)
            else:
                self.layers[protocol_name]._save(o_protocol)
        for o_protocol in remove_list:
            o_protocols.remove(o_protocol)
        # add the new layers:
        for layer in self.layers.values():
            is_new_layer = True
            for o_protocol in o_protocols:
                if layer._protocol_id == o_protocol.protocol_id.id:
                    is_new_layer = False
                    break
            if is_new_layer is True:
                o_protocol = o_stream.protocol.add()
                o_protocol.protocol_id.id = layer._protocol_id
                layer._save(o_protocol)
        self.drone._o_modify_stream(o_streams)

    def add_layers(self, *layers):
        """
        Add a layer to the stream. Note that it is added to the remote drone
        instance only after calling ``self.save()``.

        There is not equivalent ``self.del_layer``, so the whole stream must be
        deleted and recreated to remove a layer.

        Args:

            layer (simple_ostinato.protocols.Protocol): the layer to add.
        """
        for layer in layers:
            layer_name = layer.__class__.__name__
            if layer_name in self.layers:
                err = '{} found twice in {} protocols'
                raise Exception(err.format(layer_name, self))
            else:
                self.layers[layer_name] = layer
                self._save_layers()

    def del_layers(self, *layer_names):
        for name in layer_names:
            del self.layers[name]
            self._save_layers()

    def save(self):
        """
        Save the current stream configuration (including the protocols).
        """
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
        self.drone._o_modify_stream(o_streams)
        self._save_layers()

    def fetch(self):
        """
        Fetch the stream configuration on the remote drone instance (including
        all the layers).
        """
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
        """
        Name of the stream (optional)
        """
        if not hasattr(self, '_name'):
            return ''
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def enable(self):
        """
        Enable the stream. It is equivalent to setting ``self.is_enabled`` to
        ``True``.
        """
        self._is_enabled = True

    def disable(self):
        """
        Disable the stream. It is equivalent to setting ``self.is_enabled`` to
        ``False``.
        """
        self._is_enabled = False

    @property
    def is_enabled(self):
        """
        Return ``True`` if the stream is enabled, ``False`` otherwise. By
        default, streams are not enabled.
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError('expected boolean value')
        self._is_enabled = value

    @property
    def unit(self):
        """
        Unit to send. It must be either `"PACKETS"` (the default) or `BURSTS`.
        """
        return _SendUnit.get_key(self._unit)

    @unit.setter
    def unit(self, unit):
        self._unit = _SendUnit.get_value(unit)

    @property
    def mode(self):
        """
        Sending mode. It must be either `"FIXED"` (the default) or
        `"CONTINUOUS"`.

        If set to `"FIXED"`, a fixed number of packets or bursts is sent. If
        ``self.unit`` is set to `"PACKETS"`, then ``self.num_packets`` packets
        are sent. If it is set to ``"BURSTS"`` then ``self.num_bursts`` bursts
        are sent.

        If set to `"CONTINUOUS"`, packets or bursts are sent continuously until
        the port stop transmitting.
        """
        return _SendMode.get_key(self._mode)

    @mode.setter
    def mode(self, mode):
        self._mode = _SendMode.get_value(mode)

    @property
    def num_packets(self):
        """
        Number of packets to send. This is ignored if ``self.mode`` is set to
        `"CONTINUOUS"` or if ``self.unit`` is set to `"BURSTS"`.
        """
        return self._num_packets

    @num_packets.setter
    def num_packets(self, value):
        self._num_packets = int(value)

    @property
    def num_bursts(self):
        """
        Number of bursts to send. This is ignored if ``self.mode`` is set to
        `"CONTINUOUS"` or if ``self.unit`` is set to `"PACKETS"`.
        """
        return self._num_bursts

    @num_bursts.setter
    def num_bursts(self, value):
        self._num_bursts = int(value)

    @property
    def packets_per_burst(self):
        """
        Number of packets per burst. This is ignored if ``self.mode`` is set to
        `"CONTINUOUS"` or if ``self.unit`` is set to `"PACKETS"`
        """
        return self._packets_per_burst

    @packets_per_burst.setter
    def packets_per_burst(self, value):
        self._packets_per_burst = value

    @property
    def next(self):
        """
        What to do after the current stream finishes. It is ignored if
        ``self.mode`` is set to `"CONTINUOUS"`.

        - `"STOP"`: stop after this stream
        - `"GOTO_NEXT"`: send the next enabled stream
        - `"GOTO_ID"`: send a stream with a given ID.
        """
        return _SendNext.get_key(self._next)

    @next.setter
    def next(self, value):
        self._next = _SendNext.get_value(value)

    @property
    def bursts_per_sec(self):
        """
        Number of bursts to send per second.
        """
        return self._bursts_per_sec

    @bursts_per_sec.setter
    def bursts_per_sec(self, value):
        self._bursts_per_sec = int(value)

    @property
    def packets_per_sec(self):
        """
        Number of bursts to send per second.
        """
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


def _protocol_factory(o_protocol):
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
