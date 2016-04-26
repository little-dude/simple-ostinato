================
The drone object
================

We suppose that drone is running on the local host.

-------------------
Connecting to drone
-------------------

All the operations are performed from a ``simple_ostinato.Drone`` object, that
holds the connection to a drone agent, and perform all the protocol buffer
calls.

.. code-block:: python

    from simple_ostinato import Drone

    # create an instance:
    drone = Drone('localhost')

When the object is initialized, a connection is established to the drone
instance running on `localhost`. This will fail if no drone instance is
running, so it is also possible to disable the automatic connection:


.. code-block:: python

    from simple_ostinato import Drone

    # create an instance:
    drone = Drone('localhost', connect=False)

    # do things...

    # later, the connection can be established:
    drone.connect()

--------------------
Retrieving the ports
--------------------

After establishing the connection we can fetch the ports available on the drone
instance:

.. code-block:: python

    drone.fetch_ports()
    for port in drone.ports:
        print str(port)

Output:

.. code-block:: none

    veth0 (id=0, enabled=True)
    veth1 (id=1, enabled=True)
    enp0s25 (id=2, enabled=True)
    any (id=3, enabled=True)
    lo (id=4, enabled=True)
    wlp3s0 (id=5, enabled=True)
    docker0 (id=6, enabled=True)
    bluetooth0 (id=7, enabled=True)
    bluetooth-monitor (id=8, enabled=True)
    dbus-system (id=9, enabled=True)
    dbus-session (id=10, enabled=True)

To get a port by name, we either iterate over the ports or just call
``get_port()``:

.. code-block:: python

    veth0 = drone.get_port('veth0')
    
    # this is equivalent to:
    for port in drone.ports:
        if port.name == 'veth0':
            veth0 = port
            break


It is also possible to get a port by id with by iterating over the ports, but
since I don't really see a use case for getting ports by ID, there is not
method for this at the moment:

.. code-block:: python

    for port in drone.ports:
        if port.port_id == 0:
            veth0 = port
            break

----------------
Complete example
----------------

.. code-block:: python

    from simple_ostinato import Drone

    drone = Drone('localhost')
    drone.fetch_ports()

    print 'printing all the ports available'
    print '--------------------------------'
    for port in drone.ports:
        print str(port)
    print '--------------------------------'

    print '\ngetting port "veth0" by name:'
    veth0 = drone.get_port('veth0')

    print '\ngetting port with id 1:'
    for port in drone.ports:
        if port.port_id == 1:
            port1 = port
            break
    print str(port1)

Output:

.. code-block:: none

    printing all the ports available
    --------------------------------
    veth0 (id=0, enabled=True)
    veth1 (id=1, enabled=True)
    enp0s25 (id=2, enabled=True)
    any (id=3, enabled=True)
    lo (id=4, enabled=True)
    wlp3s0 (id=5, enabled=True)
    docker0 (id=6, enabled=True)
    bluetooth0 (id=7, enabled=True)
    bluetooth-monitor (id=8, enabled=True)
    dbus-system (id=9, enabled=True)
    dbus-session (id=10, enabled=True)
    --------------------------------

    getting port "veth0" by name:
    veth0 (id=0, enabled=True)

    getting port with id 1:
    veth1 (id=1, enabled=True)
