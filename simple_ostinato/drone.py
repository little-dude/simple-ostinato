"""
The module defines the ``Drone`` class, which is a wrapper for all the protocol
buffer methods. It is usually the object to create when using
``ostinato-simple``:

.. code-block:: python

    from simple_ostinato import drone


    # By default, a connection is established when the object is created.
    # To prevent this, do instead:
    # drone_instance = drone.Drone('127.0.0.1', connect=False)
    drone_instance = drone.Drone('127.0.0.1')

    # Fetch the ports
    drone_instance.fetch_ports()

    # Start using the port with id 1 for example:
    my_port = drone_instance.ports[1]
"""
from ostinato.core import DroneProxy
from .port import Port


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

    def disconnect(self):
        """
        Disconnect from the remote drone instance.
        """
        self._drone.disconnect()

    def reconnect(self):
        """
        Reconnect to the remote drone instance.
        """
        self._drone.disconnect()
        self._drone.connect()

    def fetch_ports(self):
        """
        Get the list of all the ports on the remote host. They are stored in
        the :attr:`ports` dictionnary.
        """
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

    # ------------------------------------------------------------------------
    # procol buffer wrappers
    # ------------------------------------------------------------------------
    def _o_get_port_id_list(self):
        return self._drone.getPortIdList()

    def _o_get_port_list(self, o_port_id_list):
        return self._drone.getPortConfig(o_port_id_list)

    def _o_modify_port(self, o_port_list):
        return self._drone.modifyPort(o_port_list)

    def _o_get_stream_id_list(self, o_port_id):
        return self._drone.getStreamIdList(o_port_id)

    def _o_get_stream_list(self, o_stream_id_list):
        return self._drone.getStreamConfig(o_stream_id_list)

    def _o_add_stream(self, o_stream_id_list):
        return self._drone.addStream(o_stream_id_list)

    def _o_delete_stream(self, o_stream_id_list):
        return self._drone.deleteStream(o_stream_id_list)

    def _o_modify_stream(self, o_stream_id_list):
        return self._drone.modifyStream(o_stream_id_list)

    def _o_start_transmit(self, o_port_id_list):
        return self._drone.startTransmit(o_port_id_list)

    def _o_stop_transmit(self, o_port_id_list):
        return self._drone.stopTransmit(o_port_id_list)

    def _o_start_capture(self, o_port_id_list):
        return self._drone.startCapture(o_port_id_list)

    def _o_stop_capture(self, o_port_id_list):
        return self._drone.stopCapture(o_port_id_list)

    def _o_get_capture_buffer(self, o_port_id):
        return self._drone.getCaptureBuffer(o_port_id)

    def _o_port_stats_list(self, o_port_stats_list):
        return self._drone.getStats(o_port_stats_list)

    def _o_clear_stats(self, o_port_id_list):
        return self._drone.clearStats(o_port_id_list)

    def _o_check_version(self, o_version_info):
        return self._drone.checkVersion(o_version_info)

    def _o_save_capture_buffer(self, o_capture_buffer, path):
        return self._drone.saveCaptureBuffer(o_capture_buffer, path)
