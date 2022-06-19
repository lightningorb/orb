.. _ssh-connection-wizard:

SSH Connection Wizard
---------------------

If your node does not provide an lndconnectUrl, or a clearly accessible API Endpoint / TLS Cert / Macaroon via an interface, you may need to configure your node and Orb yourself.

Luckily the SSH Connection Wizard tries to automate the process for you by:

- remotely connecting to your node via SSH
- attempting to detect the type of node you are running
- attempting to locate the lnd directory, and location of important files
- attempting to modify your lnd.conf (with option to first create / restore a backup)
- attempting to restart your node
- attempting to copy the TLS cert and Macaroon

.. note::
   
   This feature was introduced in Orb 0.15.0, is only available on Desktop, and may need more extensive testing with a wide variety of nodes. It's currently tested with a standard bare setup (lnd directory saved in `~/lnd`), and Umbrel >= 0.5.


- Click on `Orb > SSH Connection Wizard`

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Orb+2022-06-19+15-32-34.png
   :alt: protocol
   :align: center

|br|

- Enter the hostname / API Endpoint
- Port, if it's not the standard port 22
- Specify whether to SSH with a password, or certificate
- Enter the SSH username
- Enter the SSH password / certificate path
- Click 'Test Connection'
- If the connection is successful, click 'Save'

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Orb+2022-06-19+15-39-52.png
   :alt: protocol
   :align: center

|br|

- Click 'Detect Node'
- Make sure all fields should get auto-filled
- Click 'Save'

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Orb+2022-06-19+15-41-38.png
   :alt: protocol
   :align: center

|br|

(Skip this step on Umbrel nodes)

- Click the 'Check lnd.conf' button
- If modifications are required:
   - they're displayed under the button, e.g 'tlsextradomain needs modifying'
   - Click the 'Back up lnd.conf' button
   - Click 'Modify lnd.conf'

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Orb+2022-06-19+15-43-34.png
   :alt: protocol
   :align: center

|br|

(Skip this step on Umbrel nodes)

- If tlsextradomain or tlsextraip were modified in the previous step:
   - Click 'Restart LND'
   - Keep reading the logs to ascertain whether restart was successful

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Orb+2022-06-19+15-44-17.png
   :alt: protocol
   :align: center

|br|

- Once lnd has successfully restarted:
   - Click 'Copy keys'
   - Restart Orb

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Orb+2022-06-19+15-44-51.png
   :alt: protocol
   :align: center


