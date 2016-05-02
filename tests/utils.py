import platform
from simple_ostinato import Drone
import logging
import time
from pyroute2 import IPRoute
import os
import sys
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


DRONE_RUNNING = False
DRONE = None
LOG = logging.getLogger(__name__)


def link_down(name):
    ip = IPRoute()
    ip.link('set', index=ip.link_lookup(ifname=name)[0], state='down')


def link_up(name):
    ip = IPRoute()
    ip.link('set', index=ip.link_lookup(ifname=name)[0], state='up')


def create_veth_pair(name):
    ip = IPRoute()
    peers = ('{}0'.format(name), '{}1'.format(name))
    LOG.info('creating veth pair {}'.format(peers))
    ip.link('add', kind='veth', ifname=peers[0], peer=peers[1])
    link_up(peers[0])
    link_up(peers[1])


def delete_veth_pair(name):
    ip = IPRoute()
    peers = ('{}0'.format(name), '{}1'.format(name))
    LOG.info('deleting veth pair {}'.format(peers))
    link_down(peers[0])
    link_down(peers[1])
    ip.link('del', index=ip.link_lookup(ifname=peers[0])[0])


def create_port(name):
    LOG.info('creating port {}'.format(name))
    ip = IPRoute()
    ip.link('add', ifname=name, kind='dummy')
    link_up(name)


def delete_port(name):
    LOG.info('deleting port {}'.format(name))
    ip = IPRoute()
    link_down(name)
    ip.link('del', index=ip.link_lookup(ifname=name)[0])


def start_drone():
    global DRONE, DRONE_RUNNING
    LOG.info('starting drone')
    if DRONE_RUNNING is True:
        LOG.warning('drone is running already. not starting a second instance')
    with open(os.devnull, 'w') as devnull:
        DRONE = subprocess.Popen('drone', stdout=devnull, stderr=devnull)
        LOG.info('drone started with pid {}'.format(DRONE.pid))
    time.sleep(7)
    DRONE_RUNNING = True


def kill_drone():
    global DRONE_RUNNING
    LOG.info('stopping drone')
    if DRONE_RUNNING is False:
        LOG.warning('drone is not running, nothing to do')
        return
    LOG.info('trying to stop drone gracefully')
    DRONE.terminate()
    try:
        DRONE.wait(timeout=10)
        LOG.info('drone exited gracefully')
    except subprocess.TimeoutExpired:
        LOG.info('could not terminate drone properly, kill it.')
        DRONE.kill()
        DRONE.wait(timeout=10)
        LOG.info('drone has been killed')
    DRONE_RUNNING = False


def restart_drone(connect=True, fetch_ports=True):
    kill_drone()
    start_drone()
    if not connect:
        return
    drone = Drone('localhost')
    if not fetch_ports:
        return drone
    drone.fetch_ports()
    return drone


def is_pypy():
    if platform.python_implementation() == 'PyPy':
        return True
    return False
