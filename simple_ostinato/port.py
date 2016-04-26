"""
This module implement a class that represents a remote port, controlled by a
`Drone` instance. Multiple actions can be performed on a port:

- adding and deleting streams
- start/stop sending sending streams
- start/stop capturing traffic

Example:

.. code-block:: python

    import time
    from simple_ostinato.drone import Drone

    # Connect to a drone instance, fetch the ports, and start using one of
    # them:
    drone = Drone('localhost')
    drone.fetch_ports()
    port = drone.ports[0]

    # List the streams that are already configured on this port:
    port.fetch_streams()
    for stream in port.streams:
        print stream.name

    # Create a new stream
    new_stream = port.add_stream()
    # configure the stream. This is covered in `simple_ostinato.stream`
    # [...]

    # Start sending traffic, and wait a little bit
    port.send(streams=[1,2,4])
    time.sleep(5)

    # Stop sending
    port.stop_sending()

    # Capture for 5 other seconds
    port.start_capture()
    time.sleep(5)
    port.stop_capture()
"""
import weakref
import time
from ostinato.core import ost_pb
from .stream import Stream
from . import utils


class Port(object):

    """
    Represent a remote port. This class provides simple methods to add/remove
    streams, and send/capture traffic.

    Args:

        drone (simple_ostinato.drone.Drone): an object that wraps the
            underlying protocol buffer calls.
        port_id (int): id of the port.

    Attributes:

        streams (dict): a dictionnary with all the streams configured on this
            port. It can be refreshed with ``self.fetch_streams()``.
        port_id (int): id of the port
    """

    def __init__(self, drone, port_id):
        self.drone = drone
        self.port_id = port_id
        self.streams = []
        self.fetch()

    @property
    def drone(self):
        """
        ``simple_ostinato.drone.Drone`` object, used internally to perform the
        protocol buffer calls.
        """
        if not hasattr(self, '_drone'):
            return None
        return self._drone()

    def get_stream(self, stream_id):
        for stream in self.streams:
            if stream.stream_id == stream_id:
                return stream

    def get_streams_by_name(self, name):
        streams = []
        for stream in self.streams:
            if stream.name == name:
                streams.append(stream)
        return streams

    @drone.setter
    def drone(self, value):
        self._drone = weakref.ref(value)

    def _fetch(self):
        o_ports = self.drone._o_get_port_list(self._get_o_port_id_list())
        return o_ports

    def save(self):
        """
        Save the current port configuration on the remote drone instance.
        """
        o_ports = self._fetch()
        o_port = o_ports.port[0]
        o_port.name = self.name
        o_port.description = self.description
        o_port.notes = self.notes
        o_port.is_enabled = self.is_enabled
        o_port.transmit_mode = self._transmit_mode
        o_port.user_name = self.user_name
        self.drone._o_modify_port(o_ports)

    def fetch(self):
        """
        Fetch the current port configuration from the remote drone instance.
        """
        o_port = self._fetch().port[0]
        self.name = o_port.name
        self.description = o_port.description
        self.notes = o_port.notes
        self.is_enabled = o_port.is_enabled
        self._transmit_mode = o_port.transmit_mode
        self.user_name = o_port.user_name

    def _fetch_stream_ids(self):
        o_port_ids = ost_pb.PortIdList()
        o_port_id = o_port_ids.port_id.add()
        o_port_id.id = self.port_id
        return self.drone._o_get_stream_id_list(o_port_id)

    def _fetch_streams(self):
        o_stream_ids = self._fetch_stream_ids()
        return self.drone._o_get_stream_list(o_stream_ids)

    def fetch_streams(self):
        """
        Fetch the streams configured on this port, from the remote drone
        instance. The streams are stored in ``self.streams``.
        """
        o_streams = self._fetch_streams()
        for o_stream in o_streams.stream:
            stream_id = o_stream.stream_id.id
            stream = self.get_stream(stream_id)
            if stream is None:
                self.streams.append(Stream(self, stream_id))
            else:
                stream.fetch()

    @property
    def id(self):
        """
        ID of the port. This is a read-only attribute.
        """
        return self.port_id

    @id.setter
    def id(self, value):
        raise ValueError('read-only attribute')

    @property
    def name(self):
        """
        Name of the port. This is a read-only attribute.
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def description(self):
        """
        Optional description for the port.
        """
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value)

    @property
    def notes(self):
        """
        Optional note for the port.
        """
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = str(value)

    @property
    def is_enabled(self):
        """
        If ``True`` the port is enabled. Otherwise, it is disabled.
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected boolean')
        self._is_enabled = value

    def enable(self):
        """
        Enable the port.
        It is actually a shortcut for ``self.is_enabled = True``.
        """
        self.is_enabled = True

    def disable(self):
        """
        Disable the port.
        It is actually a shortcut for ``self.is_enabled = False``.
        """
        self.is_enabled = False

    @property
    def is_exclusive_control(self):
        """
        """
        return self._is_exclusive_control

    @is_exclusive_control.setter
    def is_exclusive_control(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected boolean')
        self._is_exclusive_control = value

    class TransmitMode(utils.Enum):

        SEQUENTIAL = ost_pb.kSequentialTransmit
        INTERLEAVED = ost_pb.kInterleavedTransmit

    @property
    def transmit_mode(self):
        """
        """
        return self.TransmitMode.get_key(self._transmit_mode)

    @transmit_mode.setter
    def transmit_mode(self, value):
        self._transmit_mode = self.TransmitMode.get_value(value)

    @property
    def user_name(self):
        """
        Name of the port user.
        """
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        self._user_name = str(value)

    def _get_new_stream_id(self):
        new_id = 0
        while self.get_stream(new_id) is not None:
            new_id += 1
        return new_id

    def add_stream(self, *layers):
        """
        Create a new stream, on the remote drone instance, and return the
        corresponding Stream object. The object is also added to
        ``self.streams``.
        """
        o_stream_ids = ost_pb.StreamIdList()
        o_stream_ids.port_id.id = self.port_id
        stream_id = self._get_new_stream_id()
        o_stream_ids.stream_id.add().id = stream_id
        self.drone._o_add_stream(o_stream_ids)
        new_stream = Stream(self, stream_id)
        self.streams.append(new_stream)
        new_stream.add_layers(*layers)
        return new_stream

    def del_stream(self, stream_id):
        """
        Delete the stream provided as argument.

        Args:

            stream_id (int): id of the stream to delete from the port.
        """
        o_stream_ids = ost_pb.StreamIdList()
        o_stream_ids.port_id.id = self.port_id
        o_stream_ids.stream_id.add().id = stream_id
        self.drone._o_delete_stream(o_stream_ids)
        self.streams.remove(self.get_stream(stream_id))

    def start_send(self, streams=None):
        if streams is None:
            streams = self.streams
        for stream in self.streams:
            if stream in streams:
                stream.enable()
            else:
                stream.disable()
            stream.save()
        self.drone._o_start_transmit(self._get_o_port_id_list())

    def stop_send(self):
        self.drone._o_stop_transmit(self._get_o_port_id_list())

    def start_capture(self, block=-1, stop=False):
        self.drone._o_start_capture(self._get_o_port_id_list())
        if block > 0:
            time.sleep(block)
            if stop:
                self.stop_capture()

    def stop_capture(self):
        self.drone._o_stop_capture(self._get_o_port_id_list())

    def clear_stats(self):
        self.drone._o_clear_stats(self._get_o_port_id_list())

    def get_stats(self):
        o_stats = self.drone._o_port_stats_list(self._get_o_port_id_list())
        o_stats = o_stats.port_stats[0]
        return {
            'rx_bps': o_stats.rx_bps,
            'rx_bytes': o_stats.rx_bytes,
            'rx_bytes_nic': o_stats.rx_bytes_nic,
            'rx_drops': o_stats.rx_drops,
            'rx_errors': o_stats.rx_errors,
            'rx_fifo_errors': o_stats.rx_fifo_errors,
            'rx_frame_errors': o_stats.rx_frame_errors,
            'rx_pkts': o_stats.rx_pkts,
            'rx_pkts_nic': o_stats.rx_pkts_nic,
            'rx_pps': o_stats.rx_pps,
            'tx_bps': o_stats.tx_bps,
            'tx_bytes': o_stats.tx_bytes,
            'tx_bytes_nic': o_stats.tx_bytes_nic,
            'tx_pkts': o_stats.tx_pkts,
            'tx_pkts_nic': o_stats.tx_pkts_nic,
            'tx_pps': o_stats.tx_pps,
        }

    def get_capture(self, save_path=None):
        o_port_id = self._fetch().port[0].port_id
        o_buff = self.drone._o_get_capture_buffer(o_port_id)
        if save_path:
            self.save_path(o_buff, save_path)
        return o_buff

    def save_capture(self, o_capture_buffer, path):
        self.drone._o_save_capture_buffer(o_capture_buffer, path)

    def _get_o_port_id_list(self):
        o_port_ids = ost_pb.PortIdList()
        o_port_ids.port_id.add().id = self.port_id
        return o_port_ids

    def __str__(self):
        string = '{} (id={}, enabled={})'
        return string.format(self.name, self.id, self.is_enabled)
