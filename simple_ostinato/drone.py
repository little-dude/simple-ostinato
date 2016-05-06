"""
The module defines the ``Drone`` class, which is a wrapper for all the protocol
buffer methods. It is usually the object to create when using
``ostinato-simple``:
"""
from ostinato.core import DroneProxy
from .port import Port


global _DEBUG_PROTOBUF
_DEBUG_PROTOBUF = False


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
        o_ports = self._drone.getPortConfig(self._drone.getPortIdList())
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
