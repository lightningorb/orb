Peeps
=====

The peeps allow you to 'peep' into a variety of information.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-45-36.png
   :align: center

Threads HUD
-----------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-51-17.png
   :align: center

Orb has background *daemon* threads to perform various tasks. These can be seen and controlled in the Threads HUD. 

H
..

The ``H`` represents the ``HTLC`` thread, which streams HTLC data from the node and displays it by animating channels.

C
..

The ``C`` represents the ``Channels`` thread, which streams data about channels (e.g when channels are added, or removed) and animates the channels accordingly.

F
..

The ``F`` represents the automated Fee setting app (available from the App Store).

R
..

The ``R`` represents the automated Rebalancing app (available from the App Store).

A
..

The ``A`` represents the Automated rebalancing thread (spawned during auto-rebalancing).


U
..

The ``U`` stands for Update Max HTLC (available from the App Store).

P
..

The ``P`` stands for Payment threads (spawned during payments).


.. note::

   Clicking on the letters in the Threads HUD terminates those threads.

BTC Price HUD
-------------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-56-01.png
   :align: center

This HUD displays Bitcoin's monthly PA chart, as well as its current price in USD.

Mempool
-------


.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-57-11.png
   :align: center

This HUD displays estimates for slow, medium and fast mempool transactions. Please note this data is pulled from `mempool.space <https://mempool.space>`_.

Fee Report
----------


.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-59-02.png
   :align: center

This HUD displays the fees earned from routing on a daily, weekly, and monthly basis.

Global Ratio
------------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-58-41.png
   :align: center

The global ratio is the ``total local balance / capacity``.

Pan Zoom / Gestures
-------------------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_12-00-02.png
   :align: center

Toggles between gestures, and pan / zoom. Please refer to the gestures documentation to find out more about rebalancing with swipes.

Balances
--------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-57-35.png
   :align: center

This HUD displays the various balances. This can include, Chain Balances (confirmed and unconfirmed), Local / Remote Balances, Pending Open / Close Balances, Unsettled (In-Flight) Balances etc.

Connection Status
-----------------


.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_12-02-06.png
   :align: center

This HUD simply displays whether a connection to the internet is available or not.

Graphics Info
-------------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_12-02-21.png
   :align: center

This HUD displays Dots Per Pixel and Pixel Density information. This can be useful for debugging layout issues that arise on specific devices.