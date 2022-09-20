MacOSX
======

Install Script
~~~~~~~~~~~~~~

If you are feeling brave, then:

- read the contents of `install.lnorb.com <https://install.lnorb.com>`_.
- if you feel comfortable with what it does, then run the code below.

.. code:: bash

    curl install.lnorb.com | bash

You should then be able to run the `orb` command from a terminal, or launch the `lnorb` application from spotlight.

If you are not feeling brave, the follow the steps below.

Manual install
~~~~~~~~~~~~~~

Security on OSX can be a little overzealous when installing DMGs by hand. Please follow these steps carefully, in order.

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


