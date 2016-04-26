import time
from pyroute2 import IPRoute
import os
import sys
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


global DRONE
DRONE = None


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
    with open(os.devnull, 'w') as devnull:
        DRONE = subprocess.Popen('drone', stdout=devnull, stderr=devnull)
    time.sleep(7)


def kill_drone():
    DRONE.terminate()
    try:
        DRONE.wait(timeout=10)
    except subprocess.TimeoutExpired:
        DRONE.kill()
        DRONE.wait(timeout=10)
