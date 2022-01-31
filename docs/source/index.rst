.. orb documentation master file, created by
   sphinx-quickstart on Sat Dec 11 06:30:37 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Orb
===

Orb is a cross-platform (Mac / Windows / OSX / Android) application for managing an LND Lightning node. It features an awesome community, editor, API, App Store, full node automation engines and a lot more.

It is actively developed, maintained and used by *top 30* node operators on `lightning terminal <https://terminal.lightning.engineering>`_.


Overview
========


Fun & ease of use
-----------------

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/orb_ipad.png
   :align: left
   :height: 150

Orb runs on your phone, and supports multi-touch gestures. Take your node wherever you go, and swipe channels to rebalance.

Orb puts the power of a full Lightning Network node in the palms of your hands in a beautiful, portable and fun interface.


Security
--------

.. image:: https://upload.wikimedia.org/wikipedia/commons/3/3b/RSA_logo_2008-to_present.jpg
   :align: right
   :width: 150


Convenience should never come at the cost of security. Orb runs on your phone, tablet and laptop–not on your node–and encrypts the certificate & macaroon with an **RSA encryption key tied to the device**.


Automation
----------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Finding_Balance_Part_2_Examining_the_Shortcomings_of_Typical_Engine_Balancing_Techniques_-_OnAllCylinders_2022-01-31_10-05-19.p_2022-01-31_10-06-00.jpg
   :align: left
   :width: 150

Setting fees and balancing a node by hand is time consuming. Orb provides fully automated fee-setting and rebalancing engines.

Apps
----

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Cross-Platform_Must_Have_Apps_For_The_College_Student_2022-01-31_10-11-48.png
   :align: right
   :width: 150


The Lightning Network is constantly evolving and growing; so should its tools. Orb's API enables you to 'scratch your own itch', and the app store enables you to deploy tools securely and rapily.

Data Science
------------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Data_science_concepts_you_need_to_know_Part_1__by_Michael_Barber__Towards_Data_Science_2022-01-31_10-15-17.jpg
   :align: left
   :width: 150

Orb caches transactions and payments locally, and provides you with the information you actually want, such as how much channels are earning, their fee profiles etc. it also exposes this data conveniently to libraries like Numpy, Pandas, TensorFlow etc.

The Lightning Network should be data-driven. Orb makes this goal easy to attain.

.. toctree::
   :maxdepth: 3
   :glob:
   :caption: Contents:

   installing
   configuring
   lightning
   script_editor
   extending


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
