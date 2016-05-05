import os
import pyshark
from nose2.compat import unittest
from nose2.tools.params import params
from . import utils


class BaseLayer(object):

    @classmethod
    def setUp(cls):
        utils.create_port('mac_eth')
        utils.create_veth_pair('v_mac_eth')
        utils.create_port('ip4')
        utils.create_veth_pair('v_ip4')
        cls.drone = utils.restart_drone()

    @classmethod
    def tearDown(cls):
        utils.kill_drone()
        utils.delete_port('mac_eth')
        utils.delete_veth_pair('v_mac_eth')
        utils.delete_port('ip4')
        utils.delete_veth_pair('v_ip4')


class ToFromDict(unittest.TestCase):

    layer = BaseLayer
    maxDiff = None

    @params('mac_eth', 'ip4')
    def test_mac_eth(self, protocol):
        port = self.layer.drone.get_port(protocol)
        port_config = utils.load_json('{}.json'.format(protocol))
        port_config['name'] = port.name
        port_config['is_enabled'] = port.is_enabled
        port.from_dict(port_config)
        self.assertDictEqual(utils.sanitize_dict(port.to_dict()), port_config)
        port.save()
        port.fetch()
        port.fetch_streams()
        self.assertDictEqual(utils.sanitize_dict(port.to_dict()), port_config)
        fresh_port = utils.get_fresh_port(protocol)
        fresh_port.fetch_streams()
        self.assertDictEqual(
            utils.sanitize_dict(port.to_dict()),
            utils.sanitize_dict(fresh_port.to_dict()))


class TrafficMacEthLayer(BaseLayer):

    @classmethod
    def setUp(cls):
        cls.tx = cls.drone.get_port('v_mac_eth0')
        cls.rx = cls.drone.get_port('v_mac_eth1')
        port_config = utils.load_json('mac_eth.json')
        cls.tx.from_dict(port_config)
        cls.tx.save()


class TrafficTests(unittest.TestCase):
    def setUp(self):
        self.layer.tx.fetch_streams()
        for stream in self.layer.tx.streams:
            stream.is_enabled = False
            stream.save()

    def tearDown(self):
        if os.path.isfile('capture.pcap'):
            os.remove('capture.pcap')


class TrafficMacEth(TrafficTests):

    layer = TrafficMacEthLayer

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


class TrafficIp4Layer(BaseLayer):

    @classmethod
    def setUp(cls):
        cls.tx = cls.drone.get_port('v_ip40')
        cls.rx = cls.drone.get_port('v_ip41')
        port_config = utils.load_json('ip4.json')
        cls.tx.from_dict(port_config)
        cls.tx.save()


class TrafficIp4(TrafficTests):

    layer = TrafficIp4Layer

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
        self.assertEqual(packet.ip.src, '0.0.0.0')
        self.assertEqual(packet.ip.dst, '0.0.0.0')
        self.assertEqual(int(packet.ip.ttl), 127)
        self.assertEqual(int(packet.ip.checksum, 16), 14079)
        self.assertEqual(int(packet.ip.flags, 16), 0)
        self.assertEqual(int(packet.ip.hdr_len), 5)
        self.assertEqual(int(packet.ip.proto), 0)
        self.assertEqual(int(packet.ip.id, 16), 1234)
        self.assertEqual(int(packet.ip.len), 46)
        self.assertEqual(int(packet.ip.version), 4)

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
        self.assertEqual(int(packet.ip.version), 4)
        self.assertEqual(int(packet.ip.ttl), 1)
        self.assertEqual(int(packet.ip.checksum, 16), 65535)
        self.assertEqual(int(packet.ip.flags, 16), 7)
        self.assertEqual(int(packet.ip.hdr_len), 6)
        self.assertEqual(int(packet.ip.proto), 8)
        self.assertEqual(int(packet.ip.id, 16), 4369)
        self.assertEqual(int(packet.ip.len), 50)

    # def test_traffic_variable(self):
    #     tx = self.layer.tx
    #     rx = self.layer.rx
    #     tx.streams[2].is_enabled = True
    #     tx.streams[2].save()
    #     utils.send_and_receive(tx, rx, duration=1, save_as='capture.pcap')
    #     if utils.is_pypy():
    #         return
    #     capture = pyshark.FileCapture('capture.pcap')
    #     for num_pkt, pkt in enumerate(capture):
    #         self.assertEqual((num_pkt + 1) * 10, int(pkt.eth.len))
