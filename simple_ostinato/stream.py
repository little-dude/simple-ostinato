"""
This module provide a class to manipulate streams.
"""
from ostinato.protocols.protocol_pb2 import StreamControl, StreamCore
from ostinato.core import ost_pb
import time
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

class _FrameLengthMode(utils.Enum):

    FIXED = StreamCore.FrameLengthMode.Value('e_fl_fixed')
    INC = StreamCore.FrameLengthMode.Value('e_fl_inc')
    DEC = StreamCore.FrameLengthMode.Value('e_fl_dec')
    RANDOM = StreamCore.FrameLengthMode.Value('e_fl_random')


class Stream(object):

    """
    Represent a stream configured on a port. Besides all the stream
    configuration parameters, a stream class has `layers` which define the
    packets to be sent.

    Args:

        port (:class:`Port`): the port instance on which the stream
            is defined.
        stream_id (int): the stream ID.
    """

    def __init__(self, port, stream_id, layers=None):
        self.last_check = time.time()
        self.port_id = port.port_id
        self._drone = port._drone
        self.stream_id = stream_id
        self.fetch()
        if layers:
            self.layers.extend(layers)

    @property
    def layers(self):
        """
        List of all the layers configured for this stream.
        """
        return self._layers

    @layers.setter
    def layers(self, value):
        self._layers = value

    def _fetch_layers(self, o_stream):
        o_protocols = o_stream.protocol
        self.layers = []
        for o_protocol in o_protocols:
            protocol_id = o_protocol.protocol_id.id
            self.layers.append(_protocol_factory(protocol_id, o_protocol))

    def _save_layers(self):
        # remove the existing layers
        o_streams = self._fetch()
        o_stream = o_streams.stream[0]
        o_protocols = o_stream.protocol
        while len(o_protocols) > 0:
            o_protocols.remove(o_protocols[-1])
        # add the layers from self.layers
        for layer in self.layers:
            o_protocol = o_stream.protocol.add()
            o_protocol.protocol_id.id = layer._protocol_id
            layer._save(o_protocol)
        # apply the changes
        self._drone.modifyStream(o_streams)

    def save(self):
        """
        Save the current stream configuration (including the protocols).
        """
        o_streams = self._fetch()
        o_stream = o_streams.stream[0]
        o_stream.core.is_enabled = self._is_enabled
        o_stream.core.name = self._name
        o_stream.core.len_mode = self._len_mode
        o_stream.core.frame_len = self._frame_len
        o_stream.core.frame_len_min = self._frame_len_min
        o_stream.core.frame_len_max = self._frame_len_max
        o_stream.control.unit = self._unit
        o_stream.control.mode = self._mode
        o_stream.control.num_bursts = self._num_bursts
        o_stream.control.num_packets = self._num_packets
        o_stream.control.packets_per_burst = self._packets_per_burst
        o_stream.control.next = self._next
        o_stream.control.bursts_per_sec = self._bursts_per_sec
        o_stream.control.packets_per_sec = self._packets_per_sec
        self._drone.modifyStream(o_streams)
        self._save_layers()

    def fetch(self):
        """
        Fetch the stream configuration on the remote drone instance (including
        all the layers).
        """
        o_stream = self._fetch().stream[0]
        self._name = o_stream.core.name
        self._is_enabled = o_stream.core.is_enabled
        self._len_mode = o_stream.core.len_mode
        self._frame_len = o_stream.core.frame_len
        self._frame_len_min = o_stream.core.frame_len_min
        self._frame_len_max = o_stream.core.frame_len_max
        self._unit = o_stream.control.unit
        self._mode = o_stream.control.mode
        self._num_bursts = o_stream.control.num_bursts
        self._num_packets = o_stream.control.num_packets
        self._packets_per_burst = o_stream.control.packets_per_burst
        self._next = o_stream.control.next
        self._bursts_per_sec = o_stream.control.bursts_per_sec
        self._packets_per_sec = o_stream.control.packets_per_sec
        self._fetch_layers(o_stream)

    def _fetch(self):
        o_stream_ids = ost_pb.StreamIdList()
        o_stream_ids.port_id.id = self.port_id
        o_stream_id = o_stream_ids.stream_id.add()
        o_stream_id.id = self.stream_id
        o_streams = self._drone.getStreamConfig(o_stream_ids)
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

    @property
    def len_mode(self):
        """
        Length mode. It must be either ``FIXED`` (the default), ``INC``,
        ``DEC`` or ``RANDOM``
        """
        return _FrameLengthMode.get_key(self._len_mode)

    @len_mode.setter
    def len_mode(self, mode):
        self._len_mode = _FrameLengthMode.get_value(mode)

    @property
    def frame_len(self):
        return self._frame_len

    @frame_len.setter
    def frame_len(self, value):
        self._frame_len = value

    @property
    def frame_len_min(self):
        return self._frame_len_min

    @frame_len_min.setter
    def frame_len_min(self, value):
        self._frame_len_min = value

    @property
    def frame_len_max(self):
        return self._frame_len_max

    @frame_len_max.setter
    def frame_len_max(self, value):
        self._frame_len_max = value

    def enable(self):
        """
        Enable the stream. It is equivalent to setting :attr:`is_enabled` to
        ``True``.
        """
        self._is_enabled = True

    def disable(self):
        """
        Disable the stream. It is equivalent to setting :attr:`is_enabled` to
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
        Unit to send. It must be either ``PACKETS`` (the default) or
        ``BURSTS``.
        """
        return _SendUnit.get_key(self._unit)

    @unit.setter
    def unit(self, unit):
        self._unit = _SendUnit.get_value(unit)

    @property
    def mode(self):
        """
        Sending mode. It must be either ``FIXED`` (the default) or
        ``CONTINUOUS``.

        If set to ``FIXED``, a fixed number of packets or bursts is sent. If
        :attr:`unit` is set to ``PACKETS``, then :attr:`num_packets` packets
        are sent. If it is set to ``BURSTS`` then :attr:`num_bursts` bursts
        are sent.

        If set to ``CONTINUOUS``, packets or bursts are sent continuously until
        the port stop transmitting.
        """
        return _SendMode.get_key(self._mode)

    @mode.setter
    def mode(self, mode):
        self._mode = _SendMode.get_value(mode)

    @property
    def num_packets(self):
        """
        Number of packets to send. This is ignored if :attr:`mode` is set to
        ``CONTINUOUS`` or if :attr:`unit` is set to ``BURSTS``.
        """
        return self._num_packets

    @num_packets.setter
    def num_packets(self, value):
        self._num_packets = int(value)

    @property
    def num_bursts(self):
        """
        Number of bursts to send. This is ignored if :attr:`mode` is set to
        ``CONTINUOUS`` or if :attr:`unit` is set to ``PACKETS``.
        """
        return self._num_bursts

    @num_bursts.setter
    def num_bursts(self, value):
        self._num_bursts = int(value)

    @property
    def packets_per_burst(self):
        """
        Number of packets per burst. This is ignored if :attr:`mode` is set to
        ``CONTINUOUS`` or if :attr:`unit` is set to ``PACKETS``
        """
        return self._packets_per_burst

    @packets_per_burst.setter
    def packets_per_burst(self, value):
        self._packets_per_burst = value

    @property
    def next(self):
        """
        What to do after the current stream finishes. It is ignored if
        :attr:`mode` is set to ``CONTINUOUS``.

        - ``STOP``: stop after this stream
        - ``GOTO_NEXT``: send the next enabled stream
        - ``GOTO_ID``: send a stream with a given ID.
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
            return 'stream[{}]'.format(self.stream_id)
        return 'stream[{}:{}]'.format(self.stream_id, self.name)

    def to_dict(self):
        layers = []
        for layer in self.layers:
            layers.append([layer._protocol_id, layer.to_dict()])
        return {
            'name': self.name,
            'is_enabled': self.is_enabled,
            'unit': self.unit,
            'mode': self.mode,
            'num_bursts': self.num_bursts,
            'num_packets': self.num_packets,
            'packets_per_burst': self.packets_per_burst,
            'next': self.next,
            'bursts_per_sec': self.bursts_per_sec,
            'packets_per_sec': self.packets_per_sec,
            'layers': layers,
        }

    def from_dict(self, dictionary):
        for key, value in dictionary.iteritems():
            if key == 'layers':
                layers = []
                for (protocol_id, layer_dict) in value:
                    layer = _protocol_factory(protocol_id)
                    layer.from_dict(layer_dict)
                    layers.append(layer)
                self.layers = layers
            else:
                setattr(self, key, value)


def _protocol_factory(protocol_id, o_protocol=None):
    proto_cls_mapping = {
        constants._Protocols.MAC: protocols.Mac,
        constants._Protocols.ETHERNET_II: protocols.Ethernet,
        constants._Protocols.IP4: protocols.IPv4,
        constants._Protocols.TCP: protocols.Tcp,
        constants._Protocols.UDP: protocols.Udp,
        constants._Protocols.PAYLOAD: protocols.Payload,
    }
    protocol_cls = proto_cls_mapping[protocol_id]
    protocol = protocol_cls()
    if o_protocol:
        protocol._fetch(o_protocol)
    return protocol
