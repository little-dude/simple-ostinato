import time
import pyshark
from nose2.compat import unittest
from . import utils
from simple_ostinato import Drone
from simple_ostinato.protocols import Mac, Ethernet, IPv4, Payload


class BaseLayer(object):

    @classmethod
    def setUp(cls):
        # utils.create_ports()
        print 'a'
        cls._drone_pid = utils.start_drone()
        print 'b'
        cls.drone = Drone('localhost')
        print 'c'
        cls.drone.fetch_ports()
        cls.p0 = cls.drone.get_port_by_name('vostinato0')[0]
        cls.p1 = cls.drone.get_port_by_name('vostinato1')[0]
        cls.p0.fetch_streams()
        cls.p1.fetch_streams()
        print 'd'

    @classmethod
    def tearDown(cls):
        try:
            utils.stop_drone(cls._drone_pid)
        except:
            pass
        # utils.delete_ports()


class SimpleStreams(unittest.TestCase):

    layer = BaseLayer

    def test_send_and_capture(self):
        port_tx = self.layer.p0
        port_rx = self.layer.p1

        print 1
        stream = port_tx.add_stream(
            Mac(source='00:11:22:aa:bb:cc', destination='00:01:02:03:04:05'),
            Ethernet(),
            IPv4(source='10.0.0.1', destination='10.0.0.2'),
            Payload())

        print 2
        stream.name = 'simple_mac_stream'
        stream.packets_per_sec = 1000
        stream.num_packets = 100
        stream.enable()
        stream.save()

        print 3
        port_tx.clear_stats()
        port_rx.clear_stats()

        print 4
        port_rx.start_capture()
        port_tx.start_send()
        time.sleep(1)
        print 5
        port_tx.stop_send()
        port_rx.stop_capture()

        print 6
        tx_stats = port_tx.get_stats()
        rx_stats = port_rx.get_stats()
        capture = port_rx.save_capture(port_rx.get_capture(), 'capture.pcap')
        print 7
