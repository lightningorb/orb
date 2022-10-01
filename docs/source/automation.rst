Automation
==========

Currently the best approaches to automating your node are:

Cron job
~~~~~~~~

- Install orb using the :ref:`installation script <installing-ubuntu>` or :ref:`docker <orb-docker-cli>`.

- Set up your node.
- Create a cron job, e.g:

.. code::

    0 * * * * timeout 3600 orb pay lnurl ...@walletofsatoshi.com --total-amount-sat 5_000_000 --chunks 100 --fee-rate 800 &> ~/orb.log

.. note::

    Every hour this cron job will attempt to send 5M sats to WOS, in 50k sats chunks, on 5 concurrent threads, at a fee rate of 800 PPM. `timeout 3600` kills the job after 1 hour (just as cron starts a new).



Orb VNC
~~~~~~~

