=============
Miscellaneous
=============

-------------------------
Working with other agents
-------------------------

Often, the drone instance to which we connect already has some ports and
streams configured. We usually want to fetch this configuration. This is easy
with the various ``fetch`` methods of the different objects:

- To fetch the ports (overriding ``drone.ports``): ``drone.fetch_ports()``
- To fetch the configuration of a specifig port (overriding any custom
  configuration the port object holds): ``myport.fetch()``
- To fetch the streams configured on a port (overriding the streams in
  ``myport.streams``): ``myport.fetch_streams()``
- To fetch the configuration and the layers of a specifig stream (overriding
  any custom configuration/layers the stream object holds):
  ``mystream.fetch()``

The symmetric operation, `i.e.` applying the configuration of the local objects
on the remote drone instance, use the ``save`` methods:

- To apply a port configuration: ``myport.save()``
- To apply a stream configuration: ``mystream.save()``. Note that layers are a
  special case: when adding or deleting a layer, the operation is always
  applied on the remote drone instance.

-----------------------------
Saving/Loading configurations
-----------------------------

:class:`simple_ostinato.Port` and :class:`simple_ostinato.Stream` classes have
a ``to_dict()`` and ``from_dict()`` method, which respectively dump and load
the object configuration to/from a dictionary. It can be useful to save stream,
or port configurations as json or yaml.

For example:

.. code-block:: python

    import json

    # save the "my_port" configuration (including all the streams) in a file
    with open('myport.json', 'w') as f:
        json.dump(myport.to_dict(), f)

    # later, load this configuration for another port when loading a
    # configuration, the `name` and `is_enable` keys are ignored, since they
    # are readonly properties. this allows to re-use the same configuration on
    # different ports.
    with open('myport.json', 'r') as f:
        anotherport.from_dict(json.load(f))
    anotherport.save()

    # in case you only want to load the streams:
    with open('myport.json', 'r') as f:
        anotherport.from_dict({'streams': json.load(f)['streams']})
    anotherport.save()
