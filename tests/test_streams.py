import os
import time
from nose2.compat import unittest
from simple_ostinato import protocols
import pyshark
from . import utils
from . import test_ports


class BaseLayer(test_ports.PortsFetchedLayer):

    @classmethod
    def setUp(cls):
        utils.create_veth_pair('ost_veth')
        cls.drone = utils.restart_drone()
        cls.ost1 = cls.drone.get_port('ost1')
        cls.ost2 = cls.drone.get_port('ost2')
        cls.ost3 = cls.drone.get_port('ost3')
        cls.ost4 = cls.drone.get_port('ost4')
        cls.ost5 = cls.drone.get_port('ost5')
        cls.ost6 = cls.drone.get_port('ost6')
        cls.tx1 = cls.drone.get_port('ost_veth0')
        cls.rx1 = cls.drone.get_port('ost_veth1')

    @classmethod
    def tearDown(cls):
        if os.path.isfile('capture.pcap'):
            os.remove('capture.pcap')
        utils.kill_drone()
        utils.delete_veth_pair('ost_veth')


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

    def test_update_attributes(self):
        port = self.layer.ost3
        stream = port.add_stream()
        stream.name = 'test_stream'
        stream.unit = 'BURSTS'
        stream.mode = 'CONTINUOUS'
        stream.next = 'STOP'
        stream.is_enabled = True
        stream.num_bursts = 2
        stream.num_packets = 2
        stream.packets_per_burst = 20
        stream.packets_per_sec = 2
        stream.bursts_per_sec = 2
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
        assert stream.bursts_per_sec == 2

        other_port = self.layer.get_fresh_port('ost3')
        other_port.fetch_streams()
        other_stream = other_port.streams[0]
        assert other_stream.name == 'test_stream'
        assert other_stream.unit == 'BURSTS'
        assert other_stream.mode == 'CONTINUOUS'
        assert other_stream.next == 'STOP'
        assert other_stream.is_enabled is True
        assert other_stream.num_bursts == 2
        assert other_stream.num_packets == 2
        assert other_stream.packets_per_burst == 20
        assert other_stream.packets_per_sec == 2
        assert other_stream.bursts_per_sec == 2

    def test_to_dict(self):
        port = self.layer.ost4
        stream = port.add_stream()
        expected = {
            'is_enabled': False,
            'bursts_per_sec': 1,
            'unit': 'PACKETS',
            'layers': [],
            'name': '',
            'packets_per_sec': 1,
            'next': 'GOTO_NEXT',
            'num_bursts': 1,
            'num_packets': 1,
            'mode': 'FIXED',
            'packets_per_burst': 10,
        }
        assert stream.to_dict() == expected, str(stream.to_dict())

        stream.save()
        stream.fetch()
        assert stream.to_dict() == expected, str(stream.to_dict())

        other_port = self.layer.get_fresh_port('ost4')
        other_port.fetch_streams()
        other_stream = other_port.streams[0]
        assert other_stream.to_dict() == expected, str(stream.to_dict())

        layers = [protocols.Mac(),
                  protocols.Ethernet(),
                  protocols.IPv4(),
                  protocols.Tcp(),
                  protocols.Payload()]
        stream.layers = layers
        stream.save()
        stream.fetch()
        assert isinstance(stream.layers[0], protocols.Mac)
        assert isinstance(stream.layers[1], protocols.Ethernet)
        assert isinstance(stream.layers[2], protocols.IPv4)
        assert isinstance(stream.layers[3], protocols.Tcp)
        assert isinstance(stream.layers[4], protocols.Payload)

    def test_from_dict(self):
        port = self.layer.ost5
        stream = port.add_stream()
        layers = [protocols.Mac(),
                  protocols.Ethernet(),
                  protocols.IPv4(),
                  protocols.Udp(),
                  protocols.Payload()]
        stream.from_dict({
            'is_enabled': True,
            'bursts_per_sec': 999,
            'unit': 'BURSTS',
            'layers': layers,
            'name': 'test_from_dict',
            'packets_per_sec': 999,
            'next': 'STOP',
            'num_bursts': 999,
            'num_packets': 999,
            'mode': 'CONTINUOUS',
            'packets_per_burst': 999,
        })
        stream.save()
        stream.fetch()
        assert stream.name == 'test_from_dict'
        assert stream.unit == 'BURSTS'
        assert stream.mode == 'CONTINUOUS'
        assert stream.next == 'STOP'
        assert stream.is_enabled is True
        assert stream.num_bursts == 999
        assert stream.num_packets == 999
        assert stream.packets_per_burst == 999
        assert stream.packets_per_sec == 999
        assert stream.bursts_per_sec == 999

        other_port = self.layer.get_fresh_port('ost5')
        other_port.fetch_streams()
        other_stream = other_port.streams[0]
        assert other_stream.name == 'test_from_dict'
        assert other_stream.unit == 'BURSTS'
        assert other_stream.mode == 'CONTINUOUS'
        assert other_stream.next == 'STOP'
        assert other_stream.is_enabled is True
        assert other_stream.num_bursts == 999
        assert other_stream.num_packets == 999
        assert other_stream.packets_per_burst == 999
        assert other_stream.packets_per_sec == 999
        assert other_stream.bursts_per_sec == 999

    def test_traffic(self):
        tx = self.layer.tx1
        rx = self.layer.rx1

        stream = tx.add_stream(protocols.Mac(),
                               protocols.Ethernet(),
                               protocols.IPv4(),
                               protocols.Tcp(),
                               protocols.Payload())
        stream.packets_per_sec = 100
        stream.num_packets = 10
        stream.save()
        stats_dict = {
            'rx_bps': 0,
            'rx_bytes': 0,
            'rx_bytes_nic': 0,
            'rx_drops': 0,
            'rx_errors': 0,
            'rx_fifo_errors': 0,
            'rx_frame_errors': 0,
            'rx_pkts': 0,
            'rx_pkts_nic': 0,
            'rx_pps': 0,
            'tx_bps': 0,
            'tx_bytes': 0,
            'tx_bytes_nic': 0,
            'tx_pkts': 0,
            'tx_pkts_nic': 0,
            'tx_pps': 0,
        }
        tx.clear_stats()
        rx.clear_stats()
        tx_stats = tx.get_stats()
        rx_stats = rx.get_stats()
        assert tx_stats == stats_dict, str(tx_stats)
        assert rx_stats == stats_dict
        rx.start_capture()
        tx.start_send()
        time.sleep(1)
        rx.stop_capture()
        tx.stop_send()

        tx_stats = tx.get_stats()
        rx_stats = rx.get_stats()
        rx.get_capture(save_as='capture.pcap')
        assert tx_stats['tx_pkts'] == 10
        assert rx_stats['rx_pkts'] == 10
        assert tx_stats['tx_bytes'] == 600
        assert rx_stats['rx_bytes'] == 600
        for packet in pyshark.FileCapture('capture.pcap'):
            assert packet['eth'].dst == 'ff:ff:ff:ff:ff:ff'
            assert packet['eth'].src == '00:00:00:00:00:00'
            assert int(packet['eth'].type, 16) == 2048
            assert packet['ip'].dst == '127.0.0.1'
            assert packet['ip'].src == '127.0.0.1'
            assert int(packet['ip'].flags, 16) == 0
            assert int(packet['ip'].len) == 46
            assert int(packet['ip'].ttl) == 127
            assert int(packet['ip'].version) == 4
            assert int(packet['ip'].checksum, 16) == 15816
