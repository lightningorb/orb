Installing
==========

Installing Orb should be straight-forward. Simply head over to `lnorb.com <https://lnorb.com>`_ and after purchasing a year-long license (or clicking on 'evaluate' on the front-page) there are just a few simple steps to follow, documented below.

.. note::

    Download and save orb to your **Desktop computer**, not on your node. Orb connects to LND remotely, and does not run on your node directly.


.. note::

    If you have any technical issues during installation, feel free to report them in our `tech-support group <https://t.me/+ItWJsyOBlDBjMmRl>`_

.. note::
    
    Please read our `security <https://lnorb.com/security>`_ page before running our software.

.. contents:: Table of Contents
    :depth: 3



License.lic
-----------

Before downloading the trial version, or immediately after payment for the full version, you'll be asked to save your license in a `license.lic` file. Keep a copy somewhere safe, e.g in your home directory.


MacOSX
------

- open the DMG
- drag & drop `lnorb` into the `Applications` folder
- Open Finder, then click on `Go` and `Go to folder`
- paste the following path: `/Applications/lnorb.app/Contents/MacOS`
- copy your license.lic to that folder
- run the lnorb application

If you get the message "lnorb can't be opened because Apple cannot check it for malicious software":

- in spotlight, type: Security and Privacy
- in the Security and Privacy screen, click "Open anyway"

If you are still having issues launching Orb:

- in stoplight type 'terminal'
- in the terminal paste
    - cd /Applications/lnorb.app/Contents/MacOS
    - ./lnorb
    - report back your issues in our tech-support group

Windows
-------

On Windows, after downloading Orb:

- unzip the downloaded zip file
- open the `lnorb` folder
- copy your `license.lic` inside the `lnorb` folder
- you are then free to save the `lnorb` folder wherever
    - e.g in your `program files` directory, and create appropriate launch shortcuts
- run lnorb.exe

Linux
-----

On Linux, after downloading Orb's tar file

- untar Orb
- cd into the `orb` directory
- copy your `license.lic` in that folder
- the linux version is currently deployed as the obfuscated sourcecode, so you'll need to inspect the contents of bootstrap.sh and run it once you are comfortable with the modifications it makes to your system's packages
- you're then free to move the orb folder to a directory of your choice (e.g `/opt/` or `~`) and create your alias as required

