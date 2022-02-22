Installing
==========

Installing Orb should be straight-forward. Simply head over to `lnorb.com <https://lnorb.com>`_ and after purchasing a year-long license (or clicking on 'evaluate' on the front-page) there are just a few simple steps to follow, documented below.

.. note::

    Download and save orb to your **Desktop computer**, not on your node. Orb connects to LND remotely, and does not run on your node directly.

License.lic
-----------

Before downloading the trial version, or immediately after payment for the full version, you'll be asked to save your license in a `license.lic` file. After Orb has installed, this `license.lic` file must be saved in the same directory as the orb binary.


License.lic on MacOSX
~~~~~~~~~~~~~~~~~~~~~

On MacOSX, after opening the DMG and drag & dropping `lnorb` into the `Applications` folder, open Finder, then click on `Go` and `Go to folder`. Paste the following path: `/Applications/lnorb.app/Contents/MacOS`. Finally save your license.lic in that folder.


License.lic on Windows
~~~~~~~~~~~~~~~~~~~~~~

On Windows, after downloading and unzipping Orb, simply save your `license.lic` inside the `lnorb` folder. You are then free to save the `lnorb` folder wherever, e.g in your `program files` directory, and create appropriate launch shortcuts.


License.lic on Linux
~~~~~~~~~~~~~~~~~~~~

On Linux, after downloading and untarring Orb, simply cd into the `orb` directory and save your `license.lic`. The linux version is currently deployed as the obfuscated sourcecode, so you'll need to inspect the contents of bootstrap.sh and run it once you are comfortable with the modifications it makes to your system's packages.

You're then free to move the orb folder to a directory of your choice (e.g `/opt/` or `~`) and create your alias as required.