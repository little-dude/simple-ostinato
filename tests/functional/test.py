from simple_ostinato import Drone, Port
from nose2.compat import unittest
import copy
import socket
from . import utils


def setUpModule():
    # utils.create_ports()
    utils.start_drone()


def tearDownModule():
    utils.kill_drone()
    # utils.delete_ports()


class TestDroneConnect(unittest.TestCase):

    def test_instantiate_and_connect(self):
        Drone('localhost')

    def test_reconnect(self):
        drone = Drone('localhost')
        drone.reconnect()

    def test_instantiate_then_connect(self):
        drone = Drone('doesnotexist', connect=False)
        with self.assertRaises(socket.gaierror):
            drone.connect()
        drone._drone.host = 'localhost'
        drone.connect()
        drone.reconnect()


class TestPortFetchAndUpdate(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.drone = Drone('localhost')
        cls.drone.fetch_ports()

    def test_port_fetch(self):
        assert isinstance(self.drone.get_port('vostinato0'), Port)
        assert isinstance(self.drone.get_port('vostinato1'), Port)
        vostinato0 = self.drone.get_port('vostinato0')
        assert vostinato0.name == 'vostinato0'
        assert vostinato0.is_enabled is True
        assert vostinato0.transmit_mode == 'SEQUENTIAL'

    def test_port_update(self):
        port = self.drone.get_port('vostinato0')
        assert port.transmit_mode == 'SEQUENTIAL'
        port.transmit_mode = 'INTERLEAVED'
        port.save()
        port.fetch()
        assert port.transmit_mode == 'INTERLEAVED'


class StreamCRUD(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.drone = Drone('localhost')
        cls.drone.fetch_ports()
        cls.port = cls.drone.get_port('vostinato0')

    def test_add_delete_many(self):
        for i in range(0, 100):
            self.port.add_stream()
        assert len(self.port.streams) == 100
        self.port.fetch_streams()
        assert len(self.port.streams) == 100
        self.port.streams = []
        self.port.fetch_streams()
        assert len(self.port.streams) == 100
        streams = copy.deepcopy(self.port.streams)
        for stream in streams:
            self.port.del_stream(stream.stream_id)
        assert len(self.port.streams) == 0
        self.port.streams = []
        self.port.fetch_streams()
        assert len(self.port.streams) == 0

    def test_add_fetch_delete_simple(self):
        assert len(self.port.streams) == 0
        self.port.add_stream()
        assert len(self.port.streams) == 1
        self.port.streams = []
        self.port.fetch_streams()
        assert len(self.port.streams) == 1
        self.port.del_stream(self.port.streams[0].stream_id)
        assert len(self.port.streams) == 0
        self.port.fetch_streams()
        assert len(self.port.streams) == 0

    def test_stream_attributes(self):
        stream = self.port.add_stream()
        assert stream.name == ''
        assert stream.unit == 'PACKETS'
        assert stream.mode == 'FIXED'
        assert stream.next == 'GOTO_NEXT'
        assert stream.is_enabled is False
        assert stream.num_bursts == 1
        assert stream.num_packets == 1
        assert stream.packets_per_burst == 10
        assert stream.packets_per_sec == 1
        assert stream.bursts_per_sec == 1
        assert stream.port == self.port

        stream.name = 'test_stream'
        stream.unit = 'BURSTS'
        stream.mode = 'CONTINUOUS'
        stream.next = 'STOP'
        stream.is_enabled = True
        stream.num_bursts = 2
        stream.num_packets = 2
        stream.packets_per_burst = 20
        stream.packets_per_sec = 2
        stream.burst_per_sec = 2
        stream.save()
        stream.fetch()
        assert stream.name == 'test_stream'
        assert stream.unit == 'BURSTS'
        assert stream.mode == 'CONTINUOUS'
        assert stream.next == 'STOP'
        assert stream.is_enabled is True
        assert stream.num_bursts == 2
        assert stream.num_packets == 2
        assert stream.packets_per_burst == 20
        assert stream.packets_per_sec == 2
        assert stream.burst_per_sec == 2
        self.port.del_stream(stream.stream_id)
        self.port.fetch_streams()
        assert len(self.port.streams) == 0
