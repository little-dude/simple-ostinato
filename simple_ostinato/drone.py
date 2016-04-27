"""
The module defines the ``Drone`` class, which is a wrapper for all the protocol
buffer methods. It is usually the object to create when using
``ostinato-simple``:
"""
import time
from . import log
from ostinato.core import DroneProxy
from .port import Port


global _DEBUG_PROTOBUF
_DEBUG_PROTOBUF = False


def _log_protobuf_calls(decorator_arg):

    def decorator(func):

        def wrapper(self, *args, **kwargs):
            if not _DEBUG_PROTOBUF:
                return func(self, *args, **kwargs)
            start = time.time()
            res = func(self, *args, **kwargs)
            duration = time.time() - start
            self.log.debug('called {} ({}s)'.format(decorator_arg, duration))
            return res

        return wrapper

    return decorator


class Drone(object):
    """Wrapper for ``ostinato.core.DroneProxy``.

    All the protocol buffer related methods are prefixed with ``_o_`` and are
    for internal use only.

    Args:

        host (str): ip address or hostname of the host running the drone
            instance you want to connect to.
        connect (bool): if True, attempt to connect to the remote instance when
            the object is initialized. Otherwise, it can be done manually later
            with :meth:`connect()`
    """

    def __init__(self, host, connect=True):
        self.log = log.new_logger('{}'.format(host))
        self._drone = DroneProxy(host)
        if connect is True:
            self.connect()
        self.ports = []

    def connect(self):
        """
        Connect to the remote drone instance. By default, it is already called
        when the object is created.
        """
        self._drone.connect()
        self.log.info('connected')

    def disconnect(self):
        """
        Disconnect from the remote drone instance.
        """
        self._drone.disconnect()
        self.log.info('disconnected')

    def reconnect(self):
        """
        Reconnect to the remote drone instance.
        """
        self._drone.disconnect()
        self._drone.connect()
        self.log.info('reconnected')

    def fetch_ports(self):
        """
        Get the list of all the ports on the remote host. They are stored in
        the :attr:`ports` dictionnary.
        """
        self.log.info('fetching ports')
        o_ports = self._o_get_port_list(self._o_get_port_id_list())
        for o_port in o_ports.port:
            port_id = o_port.port_id.id
            port = self.get_port_by_id(port_id)
            if port is None:
                self.ports.append(Port(self, port_id))
            else:
                port.fetch()

    def get_port_by_id(self, port_id):
        for port in self.ports:
            if port.port_id == port_id:
                return port

    def get_port(self, name):
        """
        Get ports from :attr:`ports` by name. If the port is not found,
        ``None`` is returned.
        """
        for port in self.ports:
            if port.name == name:
                return port

    def __str__(self):
        return 'drone({})'.format(self._drone.host)

    # ------------------------------------------------------------------------
    # procol buffer wrappers
    # ------------------------------------------------------------------------
    @_log_protobuf_calls('getPortIdList')
    def _o_get_port_id_list(self):
        return self._drone.getPortIdList()

    @_log_protobuf_calls('getPortConfig')
    def _o_get_port_list(self, o_port_id_list):
        return self._drone.getPortConfig(o_port_id_list)

    @_log_protobuf_calls('modifyPort')
    def _o_modify_port(self, o_port_list):
        return self._drone.modifyPort(o_port_list)

    @_log_protobuf_calls('getStreamIdList')
    def _o_get_stream_id_list(self, o_port_id):
        return self._drone.getStreamIdList(o_port_id)

    @_log_protobuf_calls('getStreamConfig')
    def _o_get_stream_list(self, o_stream_id_list):
        return self._drone.getStreamConfig(o_stream_id_list)

    @_log_protobuf_calls('addStream')
    def _o_add_stream(self, o_stream_id_list):
        return self._drone.addStream(o_stream_id_list)

    @_log_protobuf_calls('deleteStream')
    def _o_delete_stream(self, o_stream_id_list):
        return self._drone.deleteStream(o_stream_id_list)

    @_log_protobuf_calls('modifyStream')
    def _o_modify_stream(self, o_stream_id_list):
        return self._drone.modifyStream(o_stream_id_list)

    @_log_protobuf_calls('startTransmit')
    def _o_start_transmit(self, o_port_id_list):
        return self._drone.startTransmit(o_port_id_list)

    @_log_protobuf_calls('stopTransmit')
    def _o_stop_transmit(self, o_port_id_list):
        return self._drone.stopTransmit(o_port_id_list)

    @_log_protobuf_calls('startCapture')
    def _o_start_capture(self, o_port_id_list):
        return self._drone.startCapture(o_port_id_list)

    @_log_protobuf_calls('stopCapture')
    def _o_stop_capture(self, o_port_id_list):
        return self._drone.stopCapture(o_port_id_list)

    @_log_protobuf_calls('getCaptureBuffer')
    def _o_get_capture_buffer(self, o_port_id):
        return self._drone.getCaptureBuffer(o_port_id)

    @_log_protobuf_calls('getStats')
    def _o_port_stats_list(self, o_port_stats_list):
        return self._drone.getStats(o_port_stats_list)

    @_log_protobuf_calls('clearStats')
    def _o_clear_stats(self, o_port_id_list):
        return self._drone.clearStats(o_port_id_list)

    @_log_protobuf_calls('checkVersion')
    def _o_check_version(self, o_version_info):
        return self._drone.checkVersion(o_version_info)

    @_log_protobuf_calls('saveCaptureBuffer')
    def _o_save_capture_buffer(self, o_capture_buffer, path):
        return self._drone.saveCaptureBuffer(o_capture_buffer, path)
