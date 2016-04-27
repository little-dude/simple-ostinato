import time
from nose2.compat import unittest
from . import utils
from simple_ostinato import Drone
from simple_ostinato.protocols import Mac, Ethernet, IPv4, Payload


class BaseLayer(object):

    @classmethod
    def setUp(cls):
        utils.start_drone()
        cls.drone = Drone('localhost')
        cls.drone.fetch_ports()
        cls.p0 = cls.drone.get_port('vostinato0')
        cls.p1 = cls.drone.get_port('vostinato1')
        cls.p0.fetch_streams()
        cls.p1.fetch_streams()

    @classmethod
    def tearDown(cls):
        utils.kill_drone()


class SimpleStreams(unittest.TestCase):

    layer = BaseLayer

    def test_send_and_capture(self):
        port_tx = self.layer.p0
        port_rx = self.layer.p1

        stream = port_tx.add_stream(
            Mac(source='00:11:22:aa:bb:cc', destination='00:01:02:03:04:05'),
            Ethernet(),
            IPv4(source='10.0.0.1', destination='10.0.0.2'),
            Payload())

        stream.name = 'simple_mac_stream'
        stream.packets_per_sec = 1000
        stream.num_packets = 100
        stream.enable()
        stream.save()

        port_tx.clear_stats()
        port_rx.clear_stats()

        port_rx.start_capture()
        port_tx.start_send()
        time.sleep(1)
        port_tx.stop_send()
        port_rx.stop_capture()

        tx_stats = port_tx.get_stats()
        rx_stats = port_rx.get_stats()
        capture = port_rx.save_capture(port_rx.get_capture(), 'capture.pcap')
