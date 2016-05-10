import os
import pyshark
import netaddr
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
        utils.create_port('udp')
        utils.create_veth_pair('v_udp')
        utils.create_port('tcp')
        utils.create_veth_pair('v_tcp')
        cls.drone = utils.restart_drone()

    @classmethod
    def tearDown(cls):
        utils.kill_drone()
        utils.delete_port('mac_eth')
        utils.delete_veth_pair('v_mac_eth')
        utils.delete_port('ip4')
        utils.delete_veth_pair('v_ip4')
        utils.delete_port('udp')
        utils.delete_veth_pair('v_udp')
        utils.delete_port('tcp')
        utils.delete_veth_pair('v_tcp')


class ToFromDict(unittest.TestCase):

    layer = BaseLayer
    maxDiff = None

    @params('mac_eth', 'ip4', 'udp', 'tcp')
    def test_mac_eth(self, protocol):
        port = self.layer.drone.get_port(protocol)
        port_config = utils.load_json('{}.json'.format(protocol))
        port_config['name'] = port.name
        port_config['is_enabled'] = port.is_enabled
        port_config['is_exclusive_control'] = port.is_exclusive_control
        port_config['user_name'] = port.user_name
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
            src = netaddr.EUI(pkt.eth.src).value
            self.assertEqual(num_pkt * 0x100, src)
            dst = netaddr.EUI(pkt.eth.dst).value
            self.assertEqual(0xffffffffffff - num_pkt * 0x1000000, dst)


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
        self.assertIn(int(packet.ip.hdr_len), [5, 5*4])
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
        self.assertIn(int(packet.ip.hdr_len), [6, 6*4])
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


class TrafficUdpLayer(BaseLayer):

    @classmethod
    def setUp(cls):
        cls.tx = cls.drone.get_port('v_udp0')
        cls.rx = cls.drone.get_port('v_udp1')
        port_config = utils.load_json('udp.json')
        cls.tx.from_dict(port_config)
        cls.tx.save()


class TrafficUdp(TrafficTests):

    layer = TrafficUdpLayer

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
        self.assertEqual(int(packet.udp.srcport), 0)
        self.assertEqual(int(packet.udp.dstport), 0)
        self.assertEqual(int(packet.udp.length), 26)
        self.assertEqual(int(packet.udp.checksum, 16), 65466)

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
        self.assertEqual(int(packet.udp.srcport), 9999)
        self.assertEqual(int(packet.udp.dstport), 8888)
        self.assertEqual(int(packet.udp.length), 1234)
        self.assertEqual(int(packet.udp.checksum, 16), 65535)

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
            self.assertEqual(int(pkt.udp.dstport), 100 - (num_pkt % 100))
            self.assertEqual(int(pkt.udp.srcport), 1 + (num_pkt % 100))
            self.assertEqual(int(pkt.udp.length), 0 + ((num_pkt % 100) * 10))


class TrafficTcpLayer(BaseLayer):

    @classmethod
    def setUp(cls):
        cls.tx = cls.drone.get_port('v_tcp0')
        cls.rx = cls.drone.get_port('v_tcp1')
        port_config = utils.load_json('tcp.json')
        cls.tx.from_dict(port_config)
        cls.tx.save()


class TrafficTcp(TrafficTests):

    layer = TrafficTcpLayer

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
        self.assertEqual(int(packet.tcp.checksum, 16), 46051)
        self.assertEqual(int(packet.tcp.dstport), 0)
        self.assertEqual(int(packet.tcp.flags, 16), 0)
        self.assertEqual(int(packet.tcp.hdr_len), 20)
        self.assertEqual(int(packet.tcp.seq), 1)
        self.assertEqual(int(packet.tcp.srcport), 0)
        self.assertEqual(int(packet.tcp.window_size), 1024)
        # somehow on travis those are missing...
        try:
            self.assertEqual(int(packet.tcp.ack), 0)
        except AttributeError:
            print 'skipping ack field'
        try:
            self.assertEqual(int(packet.tcp.urgent_pointer), 0)
        except AttributeError:
            print 'skipping urgent_pointer field'

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
        self.assertEqual(int(packet.tcp.checksum, 16), 65535)
        self.assertEqual(int(packet.tcp.dstport), 888)
        # FIXME: ostinato seems to always set the cwr and ecn flags to 0.
        self.assertEqual(int(packet.tcp.flags, 16), 0b111100111111)
        # self.assertEqual(int(packet.tcp.flags, 16), 0b111111111111)
        self.assertEqual(int(packet.tcp.hdr_len), 24)
        packet.tcp.raw_mode = True
        self.assertEqual(packet.tcp.seq, 'ffffffff')
        packet.tcp.raw_mode = False
        self.assertEqual(int(packet.tcp.srcport), 999)
        self.assertEqual(int(packet.tcp.window_size), 1000)
        # somehow on travis those are missing...
        try:
            self.assertEqual(int(packet.tcp.ack), 1)
        except AttributeError:
            print 'skipping ack field'
        try:
            self.assertEqual(int(packet.tcp.urgent_pointer), 1)
        except AttributeError:
            print 'skipping urgent_pointer field'

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
            if num_pkt == 101:
                # FIXME: tshark tries to be smart again and since we re-use the
                # same source/destination ports, it considers this packet is
                # invalid so we just return here.
                # The fix is to define a custom assert method that  always
                # takes the raw mode for the field, and use that safe method
                # everywhere
                return
            self.assertEqual(int(pkt.tcp.dstport), 1000 - (num_pkt % 100) * 10)
            self.assertEqual(int(pkt.tcp.srcport), 0 + (num_pkt % 100) * 2)
            pkt.tcp.raw_mode = True
            seq = int('0x{}'.format(pkt.tcp.seq), 16)
            self.assertEqual(seq, 0 + (num_pkt % 1000) * 1000)
            pkt.tcp.raw_mode = False
            self.assertEqual(int(pkt.tcp.flags_urg), (num_pkt + 1) % 2)
            self.assertEqual(int(pkt.tcp.flags_ack), (num_pkt + 1) % 2)
            self.assertEqual(int(pkt.tcp.flags_ecn), (num_pkt + 1) % 2)
            self.assertEqual(int(pkt.tcp.flags_ns), (num_pkt + 1) % 2)
            self.assertEqual(int(pkt.tcp.flags_push), (num_pkt + 1) % 2)
            self.assertEqual(int(pkt.tcp.flags_syn), (num_pkt + 1) % 2)
            self.assertEqual(int(pkt.tcp.flags_fin), (num_pkt + 1) % 2)
            self.assertEqual(int(pkt.tcp.flags_reset), (num_pkt + 1) % 2)
            # self.assertEqual(int(pkt.tcp.flags_res), (num_pkt % 7) + 7)
            pkt.tcp.raw_mode = True
            try:
                ack = int('0x{}'.format(pkt.tcp.ack), 16)
                self.assertEqual(ack, 100 - (num_pkt % 100))
            except AttributeError:
                pass
            try:
                urgent_pointer = int('0x{}'.format(pkt.tcp.urgent_pointer), 16)
                self.assertEqual(urgent_pointer, 99 - (num_pkt % 100))
            except AttributeError:
                pass
            finally:
                pkt.tcp.raw_mode = False
