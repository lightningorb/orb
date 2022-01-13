Heads-Up Display
================

The Heads-up Display, or HUD for short, display information about your node as an overlay.

.. image:: HUD.png
   :align: center
   :scale: 80%

Threads HUD
-----------

Orb has background *daemon* threads to perform various tasks. These can be seen and controlled in the Threads HUD. The ``H`` represents the ``HTLC`` thread, which streams HTLC data from the node and displays it by animating channels. The ``C`` represents the ``Channels`` thread, which streams data about channels (e.g when channels are added, or removed) and animates the channels accordingly.

.. note::

   Clicking on the letters in the Threads HUD terminates those threads.

BTC Price HUD
-------------

This HUD displays Bitcoin's monthly PA chart, as well as its current price in USD.

Mempool
-------

This HUD displays estimates for slow, medium and fast mempool transactions. Please note this data is pulled from `mempool.space <https://mempool.space>`_.

Fee Report
----------

This HUD displays the fees earned from routing on a daily, weekly, and monthly basis.

Balances
--------

This HUD displays the various balances. This can include, Chain Balances (confirmed and unconfirmed), Local / Remote Balances, Pending Open / Close Balances, Unsettled (In-Flight) Balances etc.

Connection Status
-----------------

This HUD simply displays whether a connection to the internet is available or not.

Graphics Info
-------------

This HUD displays Dots Per Pixel and Pixel Density information. This can be useful for debugging layout issues that arise on specific devices.