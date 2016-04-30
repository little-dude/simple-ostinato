====================
Manipulating streams
====================

We suppose that drone is running on the local host.

--------
Creation
--------

To create an empty stream:

.. code-block:: python

    stream = lo.add_stream()


-------------
Configuration
-------------

At this point, the stream is created on the drone instance, but it has not
configuration. To configure it, we simply set the desired attributes on the
stream object, and then call ``save()`` to update the stream configuration on
the drone instance.

.. code-block:: python

    # we give a name to the stream, although it's optional
    stream.name = 'a_stream'
    # we want to send packets, not bursts of packets
    stream.unit = 'PACKETS'
    # we want the stream to finish after it sent a fixed amount of packets
    stream.mode = 'FIXED'
    # after this stream, we want to stop transmitting, even if there is another
    # stream enabled on this port
    stream.next = 'STOP'
    # we want to send 100 packets
    stream.num_packets = 100
    # at a rate of 50 packets per seconds
    stream.packets_per_sec = 50
    # finally, we enable the stream, otherwise, it won't send anything.
    stream.is_enabled = True

The stream object holds the configuration. To apply it we call ``save()``:

.. code-block:: python

    stream.save()

Protocols configuration
-----------------------

We will send a simple IP packet with fixed fields. We add the different layers
(or protocols) to the stream. Note that the order matters: adding an IPv4 layer
before a MAC layer will result in an invalid frame. Each layer correspond to a
class in ``simple_ostinato.protocols``:

.. code-block:: python

    from simple_ostinato.protocols import Mac, Ethernet, IPv4, Payload

    mac = Mac()
    mac.source = '00:00:11:11:22:22'
    mac.destination = 'FF:FF:FF:FF:FF:FF'
    stream.layers.append(mac)

    eth = Ethernet()
    eth.ether_type = 0x800
    stream.layers.append(eth)

    ip = IPv4()
    ip.source = '10.0.0.1'
    ip.destination = '10.0.0.2'
    stream.layers.append(ip)

    payload = Payload()
    stream.layers.append(payload)

    # finally, save the stream
    stream.save()

Since :attr:`simple_ostinato.stream.Stream.layers` is a simple list, we could
have writtend directly ``stream.layers = [mac, eth, ip, payload]``.

Also, all the attributes of the layers can be passed to the class constructor,
so the above could be just written:

.. code-block:: python

    from simple_ostinato.protocols import Mac, Ethernet, IPv4, Payload

    stream.layers = [
        Mac(source='00:00:11:11:22:22', destination='FF:FF:FF:FF:FF:FF'),
        Ethernet(ether_type=0x800),
        IPv4(source='10.0.0.1', destination='10.0.0.2'),
        Payload()]

To remove a layer, remove it from the
:attr:`simple_ostinato.stream.Stream.layers` list, and save the stream. For
instance, to delete the ``Payload`` and ``IPv4`` layers:

.. code-block:: python

    del stream.layers[-1]
    del stream.layers[-1]


--------
Deletion
--------

We can delete a stream by id:

.. code-block:: python

    lo.del_stream(stream.stream_id)


----------------
Complete example
----------------

.. code-block:: python

    from simple_ostinato import Drone
    from simple_ostinato.protocols import Mac, Ethernet, IPv4, Payload

    drone = Drone('localhost')
    drone.fetch_ports()
    lo = drone.get_port('lo')

    # create a stream
    stream = lo.add_stream()

    # configure the stream
    stream.name = 'a_stream'
    stream.unit = 'PACKETS'
    stream.mode = 'FIXED'
    stream.next = 'STOP'
    stream.num_packets = 100
    stream.packets_per_sec = 50
    stream.is_enabled = True

    # IMPORTANT: apply the configuration
    stream.save()

    # Add layers
    stream.layers = [
        Mac(source='00:00:11:11:22:22', destination='FF:FF:FF:FF:FF:FF'),
        Ethernet(ether_type=0x800),
        IPv4(source='10.0.0.1', destination='10.0.0.2'),
        Payload()]

    # Delete the ip and payload layers
    stream.layers = stream.layers[:-2]

    # Delete stream
    lo.del_stream(stream.stream_id)
