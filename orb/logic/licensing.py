# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-15 13:04:42
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-04 09:34:43

import arrow
from orb.misc import data_manager
from orb.misc.utils import mobile
from kivy.clock import Clock
from orb.misc.utils import pref
from kivy.app import App
from threading import Thread
import rsa
import json
import requests
import codecs


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
    edition, _, _ = get_code().split("_")
    return edition == "satoshi"


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
    if get_code() == "satoshi_0_paid":
        return
    if not paid_status == "paid":
        return

    ks1_pub = rsa.PublicKey.load_pkcs1(
        b"-----BEGIN RSA PUBLIC KEY-----\nMIGJAoGBAKqD3NOvCvPNSrG4kYKwoe6QATU4Cjdr0ecmbVXQJfoLkmiZlN4Yn3fI\nbzImSczCdrr+J8J9LgIMdSRfPvE/fnydXpeS6kdRSp5Vk+Gwh0ehlNskzwdzrG/Z\nXI1wf3yt4CvHiUbbWGL9nL/Py3+ec8hjdT12zkCgwjj+72U4j0dfAgMBAAE=\n-----END RSA PUBLIC KEY-----\n"
    )
    ks2_priv = rsa.PrivateKey.load_pkcs1(
        b"-----BEGIN RSA PRIVATE KEY-----\nMIICYAIBAAKBgQCqVhUb7sH52zkl/s62ex7IvmeNw7SB9VBf+JtQXtNP/pdfFwpa\ncm+z1vTjq5sbJYG4f0WMZC1YXgo36baX7Ioa0zullXk/jugLaGX1+e4PPvVZVxdt\n/kUgYtazEilYAi2JWHJ9WAsbs5ekAEKfSF+bCzfqiD6MhZrRYskSlkrLsQIDAQAB\nAoGAQjOIqr2FuFUChgjdUEDTuxN9bbSVMDkmjtYxju/70shRDo0G4hY94bh2nxGw\nC8HtA8a7QhAhK4oJEKgNorT/QEohlPg2ZHnKRf3A5MAxFTtRytLHGzUeBn/8st9v\nmmYS+IWchE4wtMWVG1nUU5LaQ5fXtPQEdcU+TRNDM2IQId0CRQCt3kSaCEWD+Qbj\nqz+K3SCMcfacKfkO6gO7cBIZpvxmBYygeH9Czqloowr8Ke56YJbYzwvBIVroS1Ss\nl/HdzAQTLpDcVwI9APrMsia4Z75Gtv7IQdTM4LNFkGNVY9jnxH53Vmig7YmpgoGD\n/bTuvNTHIq68F5nNWBtBc+fdiDvHnxcTNwJEdLnJ2JdBBC7FX0dyq2l1FpTT+Vd8\na3TT+JxuqmYfAOcs1/bNiS5xMVx0XYJRJjt+SiQGQiyAeX9JY23G5R64haA3hJUC\nPQCKcJOmbARYNBCvcztji/Q9ARlCu8/x233LkXRRLQPyCW/QrltNlLsHeSTb71fX\nvlH0OZ0RUGfzF63pvuECRCs27Ke9L4g+cgML6/DcNkqM6rEYBP8+vgARAPjNFrVN\novKmuK7fUUgFdylyB7QCoz6N18d4aXXOSiSMTeBcUIUKTzt+\n-----END RSA PRIVATE KEY-----\n"
    )

    def do_exit(_):
        data_manager.data_man = None
        App.get_running_app().stop()

    cached = data_manager.data_man.store.get("licensing", {}).get("data", "")
    if cached:
        decrypted = json.loads(
            rsa.decrypt(codecs.decode(cached.encode(), "hex"), ks2_priv).decode()
        )
        if (
            decrypted["detail"] == "looks good"
            and arrow.utcnow().timestamp() - decrypted["timestamp"] < 60 * 60 * 24 * 7
        ):
            return
        else:
            print("License call-home failed - please contact support")
            Clock.schedule_once(do_exit, 10)

    def func():
        r = requests.post(
            f"{pref('url.appstore')}/api/orb/buy/call-home",
            data=json.dumps(
                dict(
                    encoded=codecs.encode(
                        rsa.encrypt(
                            json.dumps(
                                dict(
                                    pk=data_manager.data_man.pubkey,
                                    invoice=invoice,
                                )
                            ).encode(),
                            ks1_pub,
                        ),
                        "hex",
                    ).decode()
                )
            ),
        )

        resp = r.json()
        if type(resp) is str:
            decrypted = json.loads(
                rsa.decrypt(codecs.decode(r.json().encode(), "hex"), ks2_priv).decode()
            )
            if (
                decrypted["detail"] == "looks good"
                and arrow.utcnow().timestamp() - decrypted["timestamp"] < 30
            ):
                data_manager.data_man.store.put("licensing", **{"data": resp})
            return
        print(resp)
        print("Call-home failed. Please connect to the internet or contact support.")
        Clock.schedule_once(do_exit, 10)

    Thread(target=func).start()
