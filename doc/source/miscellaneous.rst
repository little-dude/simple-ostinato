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

---------------
Variable fields
---------------

TODO (not yet implemented)
