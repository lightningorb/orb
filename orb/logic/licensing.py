# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-15 13:04:42
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 10:30:48

import json
import codecs
import requests
from threading import Thread

import rsa
import arrow

from orb.misc.utils import pref
from orb.misc.utils import mobile
from orb.misc.sec_rsa import encrypt_long
from orb.misc.sec_rsa import decrypt_long

from kivy.clock import Clock
from kivy.app import App


def get_code():
    try:
        from pytransform import get_license_info
    except:
        if not mobile:
            return "satoshi_0_paid"
        else:
            return "free_0_paid"
    return get_license_info()["CODE"]


def get_days_left():
    try:
        from pytransform import get_license_info
    except:
        pass
    return (
        arrow.get(get_license_info()["EXPIRED"], "MMM DD HH:mm:ss YYYY")
        - arrow.utcnow()
    ).days


def is_valid():
    return get_days_left() > 0


def is_paid():
    _, _, paid_status = get_code().split("_")
    return paid_status == "paid"


def is_trial():
    _, _, paid_status = get_code().split("_")
    return paid_status == "eval"


def is_satoshi():
    # edition, _, _ = get_code().split("_")
    # return edition == "satoshi"
    return True


def is_digital_gold():
    edition, _, _ = get_code().split("_")
    return edition == "digital-gold"


def is_free():
    edition, _, _ = get_code().split("_")
    return edition == "free"


def get_edition():
    edition, _, _ = get_code().split("_")
    return edition


def is_registered(*_):
    edition, invoice, paid_status = get_code().split("_")
    # if get_code() == "satoshi_0_paid":
    #     return
    app = App.get_running_app()
    if app.pubkey == "mock_pubkey":
        return

    ks1_pub = rsa.PublicKey.load_pkcs1(
        b"-----BEGIN RSA PUBLIC KEY-----\nMIGJAoGBAKqD3NOvCvPNSrG4kYKwoe6QATU4Cjdr0ecmbVXQJfoLkmiZlN4Yn3fI\nbzImSczCdrr+J8J9LgIMdSRfPvE/fnydXpeS6kdRSp5Vk+Gwh0ehlNskzwdzrG/Z\nXI1wf3yt4CvHiUbbWGL9nL/Py3+ec8hjdT12zkCgwjj+72U4j0dfAgMBAAE=\n-----END RSA PUBLIC KEY-----\n"
    )
    ks2_priv = rsa.PrivateKey.load_pkcs1(
        b"-----BEGIN RSA PRIVATE KEY-----\nMIICYAIBAAKBgQCqVhUb7sH52zkl/s62ex7IvmeNw7SB9VBf+JtQXtNP/pdfFwpa\ncm+z1vTjq5sbJYG4f0WMZC1YXgo36baX7Ioa0zullXk/jugLaGX1+e4PPvVZVxdt\n/kUgYtazEilYAi2JWHJ9WAsbs5ekAEKfSF+bCzfqiD6MhZrRYskSlkrLsQIDAQAB\nAoGAQjOIqr2FuFUChgjdUEDTuxN9bbSVMDkmjtYxju/70shRDo0G4hY94bh2nxGw\nC8HtA8a7QhAhK4oJEKgNorT/QEohlPg2ZHnKRf3A5MAxFTtRytLHGzUeBn/8st9v\nmmYS+IWchE4wtMWVG1nUU5LaQ5fXtPQEdcU+TRNDM2IQId0CRQCt3kSaCEWD+Qbj\nqz+K3SCMcfacKfkO6gO7cBIZpvxmBYygeH9Czqloowr8Ke56YJbYzwvBIVroS1Ss\nl/HdzAQTLpDcVwI9APrMsia4Z75Gtv7IQdTM4LNFkGNVY9jnxH53Vmig7YmpgoGD\n/bTuvNTHIq68F5nNWBtBc+fdiDvHnxcTNwJEdLnJ2JdBBC7FX0dyq2l1FpTT+Vd8\na3TT+JxuqmYfAOcs1/bNiS5xMVx0XYJRJjt+SiQGQiyAeX9JY23G5R64haA3hJUC\nPQCKcJOmbARYNBCvcztji/Q9ARlCu8/x233LkXRRLQPyCW/QrltNlLsHeSTb71fX\nvlH0OZ0RUGfzF63pvuECRCs27Ke9L4g+cgML6/DcNkqM6rEYBP8+vgARAPjNFrVN\novKmuK7fUUgFdylyB7QCoz6N18d4aXXOSiSMTeBcUIUKTzt+\n-----END RSA PRIVATE KEY-----\n"
    )

    def do_exit(_):
        App.get_running_app().stop()

    cached = App.get_running_app().store.get("licensing", {}).get("datav2", "")
    if cached:
        decrypted = json.loads(
            decrypt_long(
                codecs.decode(cached.encode(), "hex"), ks2_priv.save_pkcs1()
            ).decode()
        )
        if (
            decrypted["detail"] == "looks good"
            and arrow.utcnow().timestamp() - decrypted["timestamp"] < 60 * 60 * 24 * 7
        ):
            return
        else:
            print("License call-home failed")

    def func():
        r = requests.post(
            f"{pref('url.appstore')}/api/orb/buy/call-home-v2",
            data=json.dumps(
                dict(
                    encoded=codecs.encode(
                        encrypt_long(
                            json.dumps(
                                dict(
                                    pk=app.pubkey,
                                    edition=edition,
                                    invoice=invoice,
                                    paid_status=paid_status,
                                )
                            ),
                            ks1_pub.save_pkcs1(),
                            encoded=False,
                        ),
                        "hex",
                    ).decode()
                )
            ),
        )

        resp = r.json()
        if type(resp) is str:
            decrypted = json.loads(
                decrypt_long(
                    codecs.decode(r.json().encode(), "hex"), ks2_priv.save_pkcs1()
                ).decode()
            )
            if (
                decrypted["detail"] == "looks good"
                and arrow.utcnow().timestamp() - decrypted["timestamp"] < 30
            ):
                App.get_running_app().store.put("licensing", **{"datav2": resp})
            else:
                print(f"Call-home failed: {decrypted['detail']}")
                Clock.schedule_once(do_exit, 10)
            return
        print(resp)
        print("Call-home failed. Please connect to the internet or contact support.")
        Clock.schedule_once(do_exit, 10)

    Thread(target=func).start()
