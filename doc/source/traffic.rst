=======
Traffic
=======

-----
Setup
-----

We suppose that drone is running on the local host. We will also use a veth
pair than can be created like this:

.. code-block:: none

    ip link add veth0 type veth peer name veth1
    ip link set veth0 up
    ip link set veth1 up

-----
Steps
-----

We first create a valid stream as shown in the previous section, but on
`veth0`, that will be the transmitting port:

.. code-block:: python

    from simple_ostinato import Drone
    from simple_ostinato.protocols import Mac, Ethernet, IPv4, Payload

    drone = Drone('localhost')
    drone.fetch_ports()

    tx_port = drone.get_port('veth0')

    stream = tx_port.add_stream()
    stream.name = 'a_stream'
    stream.unit = 'PACKETS'
    stream.mode = 'FIXED'
    stream.next = 'STOP'
    stream.num_packets = 100
    stream.packets_per_sec = 50
    stream.is_enabled = True
    stream.save()
    stream.add_layers(
        Mac(source='00:00:11:11:22:22', destination='FF:FF:FF:FF:FF:FF'),
        Ethernet(ether_type=0x800),
        IPv4(source='10.0.0.1', destination='10.0.0.2'),
        Payload())

`veth1` will be capturing traffic:

.. code-block:: python

    rx_port = drone.get_port('veth1')


We first clear the statistics on both ports:


.. code-block:: python

    rx_port.clear_stats()
    tx_port.clear_stats()

Sending and capturing is straightforward:

.. code-block:: python

    import time

    rx_port.start_capture()
    tx_port.start_send()
    time.sleep(3)
    tx_port.stop_send()
    rx_port.stop_capture()

We can get the stats to perform verifications:

.. code-block:: python

    rx_stats = rx_port.get_stats()
    rx_stats = tx_port.get_stats()

The capture can also be retrieved as a string, and/or saved as a pcap file:

.. code-block:: python

    capture_str = rx_port.get_capture()
    rx_port.save_capture(capture_str, 'capture.pcap')

If you just want to save it, you can directly do:

.. code-block:: python

    rx_port.get_capture(save_as='capture.pcap')


----------------
Complete example
----------------

.. code-block:: python

    import time
    from simple_ostinato import Drone
    from simple_ostinato.protocols import Mac, Ethernet, IPv4, Payload

    drone = Drone('localhost')
    drone.fetch_ports()

    tx_port = drone.get_port('veth0')

    stream = tx_port.add_stream()
    stream.name = 'a_stream'
    stream.unit = 'PACKETS'
    stream.mode = 'FIXED'
    stream.next = 'STOP'
    stream.num_packets = 100
    stream.packets_per_sec = 50
    stream.is_enabled = True
    stream.save()
    stream.add_layers(
        Mac(source='00:00:11:11:22:22', destination='FF:FF:FF:FF:FF:FF'),
        Ethernet(ether_type=0x800),
        IPv4(source='10.0.0.1', destination='10.0.0.2'),
        Payload())

    rx_port = drone.get_port('veth1')

    rx_port.clear_stats()
    tx_port.clear_stats()
    rx_port.start_capture()
    tx_port.start_send()
    time.sleep(3)
    tx_port.stop_send()
    rx_port.stop_capture()

    print 'tx stats:'
    pprint.pprint(tx_port.get_stats())
    print 'rx stats:'
    pprint.pprint(rx_port.get_stats())

    print 'saving capture as capture.pcap'
    rx_port.get_capture(save_as='capture.pcap')

Output:

.. code-block:: python

    tx stats:
    {'rx_bps': 0L,
     'rx_bytes': 0L,
     'rx_bytes_nic': 0,
     'rx_drops': 0L,
     'rx_errors': 0L,
     'rx_fifo_errors': 0L,
     'rx_frame_errors': 0L,
     'rx_pkts': 0L,
     'rx_pkts_nic': 0,
     'rx_pps': 0L,
     'tx_bps': 0L,
     'tx_bytes': 6000L,
     'tx_bytes_nic': 0,
     'tx_pkts': 100L,
     'tx_pkts_nic': 0,
     'tx_pps': 0L}
    rx stats:
    {'rx_bps': 0L,
     'rx_bytes': 6000L,
     'rx_bytes_nic': 0,
     'rx_drops': 0L,
     'rx_errors': 0L,
     'rx_fifo_errors': 0L,
     'rx_frame_errors': 0L,
     'rx_pkts': 100L,
     'rx_pkts_nic': 0,
     'rx_pps': 0L,
     'tx_bps': 0L,
     'tx_bytes': 0L,
     'tx_bytes_nic': 0,
     'tx_pkts': 0L,
     'tx_pkts_nic': 0,
     'tx_pps': 0L}
    saving capture as capture.pcap
