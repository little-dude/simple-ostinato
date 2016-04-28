from simple_ostinato import Drone, Port, Stream
from nose2.compat import unittest
from . import utils
from . import test_ports


class BaseLayer(test_ports.PortsFetchedLayer):

    @classmethod
    def setUp(cls):
        cls.drone = utils.restart_drone()
        cls.ost1 = cls.drone.get_port('ost1')
        cls.ost2 = cls.drone.get_port('ost2')
        cls.ost3 = cls.drone.get_port('ost3')
        cls.ost4 = cls.drone.get_port('ost4')

    @classmethod
    def tearDown(cls):
        utils.kill_drone()


class StreamCRUD(unittest.TestCase):

    layer = BaseLayer

    def test_add_delete_many(self):
        port = self.layer.ost1
        for i in range(0, 100):
            port.add_stream()
        assert len(port.streams) == 100
        port.fetch_streams()
        assert len(port.streams) == 100
        port.streams = []
        port.fetch_streams()
        assert len(port.streams) == 100

        other_port = self.layer.get_fresh_port('ost1')
        assert len(other_port.streams) == 0
        other_port.fetch_streams()
        assert len(other_port.streams) == 100

        while port.streams:
            port.del_stream(port.streams[-1].stream_id)

        assert len(port.streams) == 0
        port.fetch_streams()
        assert len(port.streams) == 0

        other_port = self.layer.get_fresh_port('ost1')
        other_port.fetch_streams()
        assert len(other_port.streams) == 0

    def test_add_fetch_delete_simple(self):
        port = self.layer.ost1
        assert len(port.streams) == 0
        port.add_stream()
        assert len(port.streams) == 1
        port.streams = []
        port.fetch_streams()
        assert len(port.streams) == 1

        other_port = self.layer.get_fresh_port('ost1')
        assert len(other_port.streams) == 0
        other_port.fetch_streams()
        assert len(other_port.streams) == 1

        port.del_stream(port.streams[0].stream_id)
        assert len(port.streams) == 0
        port.fetch_streams()
        assert len(port.streams) == 0

        other_port = self.layer.get_fresh_port('ost1')
        other_port.fetch_streams()
        assert len(other_port.streams) == 0

    def test_stream_attributes(self):
        port = self.layer.ost2
        stream = port.add_stream()
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
        assert stream.port == port

    # def test_update_attributes(self):
    #     stream.name = 'test_stream'
    #     stream.unit = 'BURSTS'
    #     stream.mode = 'CONTINUOUS'
    #     stream.next = 'STOP'
    #     stream.is_enabled = True
    #     stream.num_bursts = 2
    #     stream.num_packets = 2
    #     stream.packets_per_burst = 20
    #     stream.packets_per_sec = 2
    #     stream.burst_per_sec = 2
    #     stream.save()
    #     stream.fetch()
    #     assert stream.name == 'test_stream'
    #     assert stream.unit == 'BURSTS'
    #     assert stream.mode == 'CONTINUOUS'
    #     assert stream.next == 'STOP'
    #     assert stream.is_enabled is True
    #     assert stream.num_bursts == 2
    #     assert stream.num_packets == 2
    #     assert stream.packets_per_burst == 20
    #     assert stream.packets_per_sec == 2
    #     assert stream.burst_per_sec == 2
