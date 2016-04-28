from simple_ostinato import Drone
from nose2.compat import unittest
import socket
from . import utils


class BaseLayer(object):

    @classmethod
    def setUp(cls):
        utils.restart_drone(connect=False)

    @classmethod
    def tearDown(cls):
        utils.kill_drone()


class TestDroneConnect(unittest.TestCase):

    layer = BaseLayer

    def test_instantiate_and_connect(self):
        Drone('localhost')
        # if no exception is raised, assume connection is established.  afaik
        # there is no way to know if we're connected apart from trying to send
        # commands

    def test_reconnect(self):
        drone = Drone('localhost')
        drone.reconnect()

    def test_drone_disconnect_connect(self):
        drone = Drone('localhost')
        drone.disconnect()
        drone.connect()

    def test_instantiate_then_connect(self):
        drone = Drone('doesnotexist', connect=False)
        with self.assertRaises(socket.gaierror):
            drone.connect()
        drone._drone.host = 'localhost'
        drone.connect()

    def test_connect_multiple(self):
        d1 = Drone('localhost')
        d2 = Drone('localhost')
        del d1, d2
