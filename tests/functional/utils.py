import subprocess
import time
import os
import signal
from pyroute2 import IPRoute


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
    # with open(os.devnull, 'w') as devnull:
    pid = subprocess.Popen('drone') # , stdout=devnull, stderr=devnull).pid
    time.sleep(5)
    subprocess.Popen(['netstat', '-anp'])
    return pid


def stop_drone(pid):
    os.kill(pid, signal.SIGTERM)
