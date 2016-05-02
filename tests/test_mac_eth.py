import os
import pyshark
from nose2.compat import unittest
from . import utils
from . import test_streams


class BaseLayer(test_streams.BaseLayer):

    @classmethod
    def setUp(cls):
        cls.drone = utils.restart_drone()
        cls.ost1 = cls.drone.get_port('ost1')

    @classmethod
    def tearDown(cls):
        utils.kill_drone()


class MacEthLoad(unittest.TestCase):

    layer = BaseLayer
    maxDiff = None

    def test_load_streams(self):
        port = self.layer.ost1
        port_config = utils.load_json('mac_eth.json')
        port_config['name'] = port.name
        port_config['is_enabled'] = port.is_enabled
        port.from_dict(port_config)
        self.assertDictEqual(utils.sanitize_dict(port.to_dict()), port_config)
        port.save()
        port.fetch()
        port.fetch_streams()
        self.assertDictEqual(utils.sanitize_dict(port.to_dict()), port_config)
        fresh_port = self.layer.get_fresh_port('ost1')
        fresh_port.fetch_streams()
        self.assertDictEqual(
            utils.sanitize_dict(port.to_dict()),
            utils.sanitize_dict(fresh_port.to_dict()))


class TrafficLayer(BaseLayer):

    @classmethod
    def setUp(cls):
        cls.tx = cls.drone.get_port('ost_veth0')
        cls.rx = cls.drone.get_port('ost_veth1')
        port_config = utils.load_json('mac_eth.json')
        cls.tx.from_dict(port_config)
        cls.tx.save()


class Traffic(unittest.TestCase):

    layer = TrafficLayer

    def setUp(self):
        self.layer.tx.fetch_streams()
        for stream in self.layer.tx.streams:
            stream.is_enabled = False
            stream.save()

    def tearDown(self):
        if os.path.isfile('capture.pcap'):
            os.remove('capture.pcap')

    def test_traffic_default(self):
        tx = self.layer.tx
        rx = self.layer.rx
        tx.streams[0].is_enabled = True
        tx.streams[0].save()
        utils.send_and_receive(tx, rx, duration=0.5, save_as='capture.pcap')
        if utils.is_pypy():
            return
        capture = pyshark.FileCapture('capture.pcap')
        packet = capture[0]
        self.assertEqual(packet.eth.src, '00:00:00:00:00:00')
        self.assertEqual(packet.eth.dst, '00:00:00:00:00:00')
        self.assertEqual(int(packet.eth.type, 16), 0)

    def test_traffic_static(self):
        tx = self.layer.tx
        rx = self.layer.rx
        tx.streams[1].is_enabled = True
        tx.streams[1].save()
        utils.send_and_receive(tx, rx, duration=0.5, save_as='capture.pcap')
        if utils.is_pypy():
            return
        capture = pyshark.FileCapture('capture.pcap')
        packet = capture[0]
        self.assertEqual(packet.eth.dst, 'aa:bb:cc:dd:ee:ff')
        self.assertEqual(packet.eth.src, '11:22:33:44:55:66')
        self.assertEqual(int(packet.eth.type, 16), 2457)

    def test_traffic_variable(self):
        tx = self.layer.tx
        rx = self.layer.rx
        tx.streams[2].is_enabled = True
        tx.streams[2].save()
        utils.send_and_receive(tx, rx, duration=1, save_as='capture.pcap')
        if utils.is_pypy():
            return
        capture = pyshark.FileCapture('capture.pcap')
        for num_pkt, pkt in enumerate(capture):
            self.assertEqual((num_pkt + 1) * 10, int(pkt.eth.len))
