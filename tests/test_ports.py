from simple_ostinato import Drone, Port
from nose2.compat import unittest
from . import utils


class BaseLayer(object):

    @classmethod
    def setUp(cls):
        for itf in ['ost1', 'ost2', 'ost3', 'ost4', 'ost5', 'ost6']:
            utils.create_port(itf)
        cls.drone = utils.restart_drone(fetch_ports=False)

    @classmethod
    def tearDown(cls):
        utils.kill_drone()
        for itf in ['ost1', 'ost2', 'ost3', 'ost4', 'ost5', 'ost6']:
            utils.delete_port(itf)


class TestFetch(unittest.TestCase):

    layer = BaseLayer

    def test_fetch(self):
        drone = Drone('localhost')
        drone.fetch_ports()
        assert isinstance(drone.get_port('ost1'), Port)
        assert isinstance(drone.get_port('ost2'), Port)


class PortsFetchedLayer(BaseLayer):

    @classmethod
    def setUp(cls):
        drone = Drone('localhost')
        drone.fetch_ports()
        cls.ost1 = drone.get_port('ost1')
        cls.ost2 = drone.get_port('ost2')
        cls.ost3 = drone.get_port('ost3')
        cls.ost4 = drone.get_port('ost4')
        cls.ost5 = drone.get_port('ost5')
        cls.ost6 = drone.get_port('ost6')

    @classmethod
    def tearDown(cls):
        pass


class TestPortConfig(unittest.TestCase):

    layer = PortsFetchedLayer

    def test_default_attrs(self):
        port = self.layer.ost1
        assert port.name == 'ost1'
        assert port.is_enabled is True
        assert port.transmit_mode == 'SEQUENTIAL'
        # assert port.user_name == ???

    def test_setattrs(self):
        port = self.layer.ost2
        with self.assertRaises(ValueError):
            port.name = 'should_faild'
        assert port.name == 'ost2'

        with self.assertRaises(ValueError):
            port.is_enabled = False
        assert port.is_enabled is True

        with self.assertRaises(ValueError):
            port.transmit_mode = 'SOMETHING_WRONG'
        assert port.transmit_mode == 'SEQUENTIAL'
        port.transmit_mode = 'INTERLEAVED'
        assert port.transmit_mode == 'INTERLEAVED'

    def test_save_config(self):
        port = self.layer.ost3
        assert port.transmit_mode == 'SEQUENTIAL'

        port.transmit_mode = 'INTERLEAVED'
        port.save()
        port.fetch()
        assert port.transmit_mode == 'INTERLEAVED'

        other_port = utils.get_fresh_port('ost3')
        assert other_port.transmit_mode == 'INTERLEAVED'

    def test_to_dict(self):
        port = self.layer.ost4
        expected = {
            'name': 'ost4',
            'transmit_mode': 'SEQUENTIAL',
            'user_name': '',
            'is_exclusive_control': False,
            'is_enabled': True,
            'streams': []
        }
        self.assertDictEqual(
            utils.sanitize_dict(port.to_dict()),
            utils.sanitize_dict(expected))

        port.transmit_mode = 'INTERLEAVED'
        expected = {
            'name': 'ost4',
            'transmit_mode': 'INTERLEAVED',
            'user_name': '',
            'is_exclusive_control': False,
            'is_enabled': True,
            'streams': []
        }
        self.assertDictEqual(
            utils.sanitize_dict(port.to_dict()),
            utils.sanitize_dict(expected))

        port.save()
        other_port = utils.get_fresh_port('ost4')
        self.assertDictEqual(
            utils.sanitize_dict(other_port.to_dict()),
            utils.sanitize_dict(expected))

    def test_from_dict(self):
        port = self.layer.ost5
        assert port.is_enabled is True
        assert port.transmit_mode == 'SEQUENTIAL'
        assert port.name == 'ost5'
        assert port.streams == []

        port.from_dict({'name': 'should_be_ignored',
                        'transmit_mode': 'INTERLEAVED',
                        'is_enabled': False,
                        'streams': []})
        assert port.is_enabled is True
        assert port.transmit_mode == 'INTERLEAVED'
        assert port.name == 'ost5'
        assert port.streams == []

        port.save()
        other_port = utils.get_fresh_port('ost5')
        assert other_port.is_enabled is True
        assert other_port.transmit_mode == 'INTERLEAVED'
        assert other_port.name == 'ost5'
        assert other_port.streams == []
