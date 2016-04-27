"""
This module implement a class that represents a remote port, controlled by a
:class:`Drone` instance.
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

        drone (:class:`Drone`): an object that wraps the underlying protocol
            buffer calls.
        port_id (int): id of the port.

    Attributes:

        streams (dict): a dictionnary with all the streams configured on this
            port. It can be refreshed with :meth:`fetch_streams()`.
        port_id (int): id of the port
    """

    def __init__(self, drone, port_id):
        self.drone = drone
        self.port_id = port_id
        self.streams = []
        self.log = self.drone.log.getChild('port[{}]'.format(port_id))
        self.fetch()

    @property
    def drone(self):
        """
        :class:`Drone` object, used internally to \
            perform the protocol buffer calls.
        """
        if not hasattr(self, '_drone'):
            return None
        return self._drone()

    def get_stream(self, stream_id):
        """
        Return a the :class:`Stream` object corresponding to the given stream
        ID (:class:`int`)
        """
        for stream in self.streams:
            if stream.stream_id == stream_id:
                return stream

    def get_streams_by_name(self, name):
        """
        Return a list of :class:`Stream` s that have the given name
        (:class:str). Since most often names are unique, it is common to get a
        stream doing:

            >>> my_stream_foo = my_port.get_streams_by_name('stream_foo')[0]
        """
        streams = []
        for stream in self.streams:
            if stream.name == name:
                streams.append(stream)
        return streams

    @drone.setter
    def drone(self, value):
        """
        A reference to the :class:`Drone` object. This is mostly for internal
        use.
        """
        self._drone = weakref.ref(value)

    def _fetch(self):
        o_ports = self.drone._o_get_port_list(self._get_o_port_id_list())
        return o_ports

    def save(self):
        """
        Save the current port configuration on the remote drone instance.
        """
        self.log.info('saving configuration')
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
        self.log.info('fetching configuration')
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
        instance. The streams are stored in :attr:`streams`.
        """
        self.log.info('fetching streams')
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
        if value and getattr(self, '_name', None) is None:
            self.log.info('port name is "{}"'.format(value))
            self.log.name = '{}.{}'.format(self.drone.log.name, value)
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

    class _TransmitMode(utils.Enum):

        SEQUENTIAL = ost_pb.kSequentialTransmit
        INTERLEAVED = ost_pb.kInterleavedTransmit

    @property
    def transmit_mode(self):
        """
        Can be ``SEQUENTIAL`` or ``INTERLEAVED``.
        """
        return self._TransmitMode.get_key(self._transmit_mode)

    @transmit_mode.setter
    def transmit_mode(self, value):
        self._transmit_mode = self._TransmitMode.get_value(value)

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
        :attr:`streams`.

        Layers must be instances of :class:`simple_ostinato.protocols.Protocol`

            >>> from simple_ostinato import protocols
            >>> my_port.add_stream(protocols.Mac(), protocols.Ethernet())
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
        self.log.info('deleting stream with id {}'.format(stream_id))
        o_stream_ids = ost_pb.StreamIdList()
        o_stream_ids.port_id.id = self.port_id
        o_stream_ids.stream_id.add().id = stream_id
        self.drone._o_delete_stream(o_stream_ids)
        self.streams.remove(self.get_stream(stream_id))

    def start_send(self, streams=None):
        """
        Start transmitting the streams that are enabled on this port.

        Args:

            streams (list): a list of :class:`Stream` to send. If such a list \
                is provided, the corresponding streams will be enabled, and \
                the other disabled.
        """
        self.log.info('start sending')
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
        """
        Stop sending
        """
        self.log.info('stop sending')
        self.drone._o_stop_transmit(self._get_o_port_id_list())

    def start_capture(self, block=-1, stop=False):
        """
        Start capturing. By default, this method is non-blocking and returns
        immediately, and :meth:`stop_send()` must be called to stop the
        capture.

        Args:

            block (int): make this method blocking for ``block`` seconds

            stop (bool): if True, and if ``block`` is a positive integer, the \
                capture will be stopped after ``block`` seconds.
        """
        self.log.info('start capturing')
        self.drone._o_start_capture(self._get_o_port_id_list())
        if block > 0:
            time.sleep(block)
            if stop:
                self.stop_capture()

    def stop_capture(self):
        """
        Stop the current capture
        """
        self.log.info('stop capturing')
        self.drone._o_stop_capture(self._get_o_port_id_list())

    def clear_stats(self):
        """
        Clear the port statistics
        """
        self.log.info('clearing statistics')
        self.drone._o_clear_stats(self._get_o_port_id_list())

    def get_stats(self):
        """
        Fetch the port statistics, and return them as a dictionary.
        """
        self.log.info('fetching statistics')
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

    def get_capture(self, save_as=None):
        """
        Get the lastest capture and return is as a string.

        Args:

            save_as (str): if provided, the capture will also be saved as a \
                pcap file at the specified location `on the host that runs \
                drone`.
        """
        o_port_id = self._fetch().port[0].port_id
        o_buff = self.drone._o_get_capture_buffer(o_port_id)
        if save_as:
            self.save_capture(o_buff, save_as)
        return o_buff

    def save_capture(self, o_capture_buffer, path):
        self.log.info('saving capture as {}'.format(path))
        self.drone._o_save_capture_buffer(o_capture_buffer, path)

    def _get_o_port_id_list(self):
        o_port_ids = ost_pb.PortIdList()
        o_port_ids.port_id.add().id = self.port_id
        return o_port_ids

    def __str__(self):
        name = getattr(self, 'name', '??')
        return 'port[{}:{}]'.format(self.port_id, name)
