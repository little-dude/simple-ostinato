import logging
import time
from pyroute2 import IPRoute
import os
import sys
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


DRONE = None
LOG = logging.getLogger(__name__)


def link_down(name):
    ip = IPRoute()
    ip.link('set', index=ip.link_lookup(ifname=name)[0], state='down')


def link_up(name):
    ip = IPRoute()
    ip.link('set', index=ip.link_lookup(ifname=name)[0], state='up')


def create_ports():
    ip = IPRoute()
    ip.link_create(ifname='vostinato0', peer='vostinato1', kind='veth')
    link_up('vostinato0')
    link_up('vostinato1')


def delete_ports():
    ip = IPRoute()
    link_down('vostinato0')
    link_down('vostinato1')
    ip.link('del', index=ip.link_lookup(ifname='vostinato0')[0])


def start_drone():
    global DRONE
    LOG.info('starting drone')
    with open(os.devnull, 'w') as devnull:
        DRONE = subprocess.Popen('drone', stdout=devnull, stderr=devnull)
        LOG.info('drone start with pid {}'.format(DRONE.pid))
    time.sleep(7)


def kill_drone():
    LOG.info('terminating drone properly')
    DRONE.terminate()
    try:
        DRONE.wait(timeout=10)
    except subprocess.TimeoutExpired:
        LOG.info('could not terminate drone properly, kill it.')
        DRONE.kill()
        DRONE.wait(timeout=10)
        LOG.info('drone has been killed')
