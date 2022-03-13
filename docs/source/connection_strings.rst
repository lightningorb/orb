.. _connection-string:

Connection Strings
==================


Orb encrypts your TLS certificate and Macaroon using a unique (to your device) 512 bits RSA key. This is because this information should never exist outside of your node unencrypted.

The connection strings are denser forms of:

.. code:: python

    import rsa
    import base64
    import os

    pub_key = rsa.PublicKey.load_pkcs1(
        b"-----BEGIN RSA PUBLIC KEY-----\n...\n-----END RSA PUBLIC KEY-----\n"
    )

    cert = open(os.path.expanduser("~/.lnd/tls.cert")).read()

    for i in range(0, len(cert), 53):
        # get the 53 character long chunk from the certificate
        cert_chunk = cert[i : i + 53].encode()
        # encrypt it using the 512 bit RSA key
        cert_chunk_rsa = rsa.encrypt(cert_chunk, pub_key)
        # encoded as base64
        cert_chunk_rsa_base64 = base64.b64encode(cert_chunk_rsa).decode()
        # print the encoded chunk
        print(cert_chunk_rsa_base64)


The command is similar for the Macaroon, although the path is simply substituted for `~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon`.

The `53` is because a 512 bit RSA key can only encode a maximum of `53 characters <https://stackoverflow.com/questions/68785815/how-can-i-encrypt-a-large-message-with-a-512-rsa-key>`_.

512 bits is not considered `enough <https://www.laits.utexas.edu/~anorman/BUS.FOR/course.mat/SSim/key.html#:~:text=RSA%20recommends%20that%20512%2Dbit,pair%20of%20a%20certifying%20authority.>`_, and we will consider using a larger key once we have more clarity surrounding the use of encryption in IOS App Store applications.

