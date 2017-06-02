# simple-ostinato

[![Build Status](https://travis-ci.org/little-dude/simple-ostinato.svg?branch=master)](https://travis-ci.org/little-dude/simple-ostinato)
[![Coverage Status](https://coveralls.io/repos/github/little-dude/simple-ostinato/badge.svg?branch=master)](https://coveralls.io/github/little-dude/simple-ostinato?branch=master)

A wrapper for the ostinato python client.

Documentation (work in progress):
http://simple-ostinato.readthedocs.org/en/latest/

``simple_ostinato`` is a python package that makes it easy to use the ostinato
python agent ``python-ostinato``. It is basically a wrapper around
``python-ostinato`` that hides the RPC engineering.

### Example

We assume that ``drone`` is already running on the localhost, and that we created a veth pair of interfaces with:

```
ip link add veth0 type veth peer name veth1
ip link set veth0 up
ip link set veth1 up
```

The following script sends traffic on ``veth0`` and captures in on ``veth1``:

```python
import time
from simple_ostinato import Drone
from simple_ostinato.protocols import Mac, Ethernet, IPv4, Payload

# connect to the drone instance that runs on localhost
drone = Drone('localhost')

# fetch port information
drone.fetch_ports()

port_tx = drone.get_port('veth0')
port_rx = drone.get_port('veth1')

# Create a new stream
stream = port_tx.add_stream(
    Mac(source='00:11:22:aa:bb:cc', destination='00:01:02:03:04:05'),
    Ethernet(),
    IPv4(source='10.0.0.1', destination='10.0.0.2'),
    Payload())

# Configure the stream
stream.name = 'simple_mac_stream'
stream.packets_per_sec = 1000
stream.num_packets = 100
stream.enable()
stream.save()

# Clear the stats on the transmitting and receiving port
port_tx.clear_stats()
port_rx.clear_stats()

# Send and capture
port_rx.start_capture()
port_tx.start_send()
time.sleep(1)
port_tx.stop_send()
port_rx.stop_capture()

# Get the stats and print them
tx_stats = port_tx.get_stats()
rx_stats = port_rx.get_stats()
print str(tx_stats)
print str(rx_stats)

# We can also store the capture:
capture = port_rx.save_capture(port_rx.get_capture(), 'capture.pcap')
```
