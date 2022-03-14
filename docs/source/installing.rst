Installing
==========

.. note::

    Download and save orb to your **Desktop computer**, not on your node. Orb connects to LND remotely, and does not run on your node directly.


.. note::

    If you have any technical issues during installation, feel free to report them in our `tech-support group <https://t.me/+ItWJsyOBlDBjMmRl>`_

.. note::
    
    Please read our `security <https://lnorb.com/security>`_ page before running our software.

.. contents:: Table of Contents
    :depth: 3



MacOSX
------

Security on OSX can be a little overzealous. Please follow these steps carefully, in order.

- open the DMG
- drag & drop `lnorb` into the `Applications` folder
- In Spotlight (CMD Space), type lnorb
- Once lnorb appears in Spotlight, try running it
- You may be presented with the following two dialogs:

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Monosnap_2022-03-02_02-52-22.png
    :width: 500px
    :align: center

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Monosnap_2022-03-02_02-53-03.png
    :width: 500px
    :align: center

- in spotlight, type: Security and Privacy
- in the Security and Privacy screen, click "Open anyway", and "Open"
- run the lnorb application
- Orb should open

If Orb does not open:

- in stoplight type 'terminal'
- in the terminal paste
    - cd /Applications/lnorb.app/Contents/MacOS
    - ./lnorb
    - report back your issues in our tech-support group (link at top of this page)

Windows
-------

On Windows, after downloading Orb:

- unzip the downloaded zip file
- open the `lnorb` folder
- you are then free to save the `lnorb` folder wherever
    - e.g in your `program files` directory, and create appropriate launch shortcuts
- run lnorb.exe

Linux
-----

On Linux, after downloading Orb's tar file

- untar Orb
- cd into the `orb` directory
- the linux version is currently deployed as the obfuscated sourcecode, so you'll need to inspect the contents of bootstrap.sh and run it once you are comfortable with the modifications it makes to your system's packages
- you're then free to move the orb folder to a directory of your choice (e.g `/opt/` or `~`) and create your alias as required

