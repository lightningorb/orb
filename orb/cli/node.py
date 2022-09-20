# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:12:26
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-20 16:10:37

import re
import os
import codecs
from pathlib import Path
from typing import Optional
from tempfile import TemporaryDirectory
from pathlib import Path
from orb.misc.utils_no_kivy import get_user_data_dir_static
from orb.cli.utils import get_default_id
from fabric import Connection
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.certificate_secure import CertificateSecure
from orb.ln import Ln

from orb.ln import factory
from configparser import ConfigParser
from .chalk import chalk
from orb.cli.utils import pprint_from_ansi

import typer

app = typer.Typer(help="Commands to perform operations on nodes.")


@app.command()
def delete(
    pubkey: Optional[str] = typer.Argument(
        None, help="The pubkey of the node. If not provided, use the default node."
    )
):
    """
    Delete node information.

    Node data is saved in various places depending on your OS:

    - Linux: ~/.config/orb_<pubkey>/orb_<pubkey>.ini
    - OSX: ~/Library/Application Support/orb_<pubkey>/orb_<pubkey>.ini
    - Windows: ${APPDATA}/orb_<pubkey>/orb_<pubkey>.ini

    This command recursively deletes the node's folder. This is a destructive command. Use with care.

    .. asciinema:: /_static/orb-node-delete.cast

    """
    if not pubkey:
        pubkey = get_default_id()
    if not pubkey:
        pprint_from_ansi("No node pubkey provided. Quitting.")
        return
    conf_path = Path(get_user_data_dir_static()) / f"orb_{pubkey}"
    if conf_path.exists():
        from shutil import rmtree

        rmtree(conf_path.as_posix())
        pprint_from_ansi(chalk().green(f"{conf_path} deleted"))
    else:
        pprint_from_ansi(chalk().red(f"{conf_path} does not exist"))


@app.command()
def list(
    show_info: bool = typer.Option(
        help="If True, then connect and print node information", default=False
    )
):
    """
    Get a list of nodes known to Orb.

    Node data is saved in various places depending on your OS:

    - Linux: ~/.config/orb_<pubkey>/orb_<pubkey>.ini
    - OSX: ~/Library/Application Support/orb_<pubkey>/orb_<pubkey>.ini
    - Windows: ${APPDATA}/orb_<pubkey>/orb_<pubkey>.ini

    This command simply scans those folders for a matching pattern.

    If the `--show-info` is provided, then Orb attempts to connect to the node, and to invoke the :ref:`orb-node-info` command on the available nodes.

    .. asciinema:: /_static/orb-node-list.cast
    """

    data_dir = Path(get_user_data_dir_static())
    for x in data_dir.glob("orb_*"):
        m = re.match(r"^orb_([a-zA-Z0-9]{66})$", x.name)
        if m and x.is_dir():
            pk = m.group(1)
            if show_info:
                pprint_from_ansi(f"Showing info for: {chalk().greenBright(pk)}:")
                try:
                    info(pk)
                except:
                    pprint_from_ansi(f"Failed to get info for: {chalk().red(pk)}:")
            else:
                pprint_from_ansi(chalk().green(pk))


@app.command()
def info(
    pubkey: Optional[str] = typer.Argument(
        None, help="The pubkey of the node. If not provided, use the default node."
    )
):
    """
    Get node information.

    This command connects to the lightning node, gets basic information and prints it out in the console.

    .. asciinema:: /_static/orb-node-info.cast
    """
    if not pubkey:
        pubkey = get_default_id()
    for k, v in factory(pubkey).get_info().__dict__.items():
        pprint_from_ansi(f"{chalk().greenBright(k)}: {chalk().blueBright(v)}")


@app.command()
def use(pubkey: str = typer.Argument(None, help="The pubkey of the node.")):
    """
    Make all subsequent commands use this node.

    This command inserts the pubkey in the config files of the orbconnector app.

    - Linux: ~/.config/orbconnector/orbconnector.ini
    - OSX: ~/Library/Application Support/orbconnector/orbconnector.ini
    - Windows: ${APPDATA}/orbconnector/orbconnector.ini

    All subsequent orb invocations will use this node by default, unless otherwise specified.

    .. asciinema:: /_static/orb-node-use.cast
    """
    conf_dir = Path(get_user_data_dir_static()) / "orbconnector"
    if not conf_dir.is_dir():
        os.makedirs(conf_dir.as_posix(), exist_ok=True)
    conf_path = conf_dir / "orbconnector.ini"
    conf = ConfigParser()
    conf.filename = conf_path.as_posix()
    conf.add_section("ln")
    conf.set("ln", "identity_pubkey", pubkey)
    conf.write(conf_path.open("w"))
    print(chalk().green(f"Setting {pubkey} as default"))


@app.command()
def create_orb_public(
    node_type: str = typer.Argument(..., help="lnd or cln."),
    protocol: str = typer.Argument(..., help="rest or grpc."),
    use_node: bool = typer.Option(help="Set this node as the default.", default=True),
):
    """
    Create public testnet node.

    This command enables users to quickly create node connection information for orb's public nodes. The typical invocates are:

    .. code:: bash

        orb node create-orb-public cln rest
        orb node create-orb-public lnd rest
        orb node create-orb-public lnd grpc

    Since Core-Lightning's GRPC interface is still new and not used a lot, it is currently unsupported by Orb, which is why the `cln grpc` node flavor isn't available.

    After the public node has been created, if `--use-node` was specified then subsequent orb commands will use it by default. These nodes have admin macaroons, and are used by the integration tests, so please keep the in a sane state so they don't need to be re-created.

    .. asciinema:: /_static/orb-node-create-orb-public.cast
    """
    from orb.misc.macaroon_secure import MacaroonSecure

    hostname = dict(cln="regtest.cln.lnorb.com", lnd="signet.lnd.lnorb.com")[node_type]
    rest_port = dict(cln="3001", lnd="8080")[node_type]
    grpc_port = dict(cln="10010", lnd="10009")[node_type]
    cert = dict(
        cln="2d2d2d2d2d424547494e2043455254494649434154452d2d2d2d2d0a4d494944707a4343416f2b6741774942416749554f7555694a71543367567638637373646d534f31736b38364a4d38774451594a4b6f5a496876634e4151454c0a42514177556a454c4d416b474131554542684d4356564d784444414b42674e564241674d41305a76627a454d4d416f474131554542777744516d46794d5177770a436759445651514b44414e4359586f784754415842674e5642414d4d45474d7462476c6e614852756157356e4c584a6c633351774868634e4d6a49774f5449770a4d4467774d5455335768634e4d6a4d774f5449774d4467774d545533576a42534d517377435159445651514745774a56557a454d4d416f4741315545434177440a526d39764d517777436759445651514844414e43595849784444414b42674e5642416f4d41304a68656a455a4d4263474131554541777751597931736157646f0a64473570626d6374636d567a64444343415349774451594a4b6f5a496876634e4151454242514144676745504144434341516f4367674542414c416d657335620a682b73553461326267613130462b684b4d367a456a6e6370586948332b7a4670435758736e4741367843544c5035686b364b62304d4b446c452f6e77457369300a477364454938503538524a717341706c755870555774584f72516f5a33722f5239756d4c356859556d5056624e4f794c4a38694b48657a554c39376b6a76467a0a56346872772f6375634151784b435a4b774663714651416f6770436e515856485852796156505a74676b6e5a67587245754546594839597a6e6f7a417777584b0a364b7a4c4a38622f746576535258554e77773763364346585442566d6c5a6b31676b7570786270766e51525836462f6156646374702f523152794a32434d36530a6f4852494b6f2b6e4a374271334c7466505067666c457a7a426d7639464e533273744467392b4e5a67634b6c3563305241775a697a2b715171744e4c6e7566620a3672336676424f66643462696c3273434177454141614e314d484d77485159445652304f424259454645636830786c632b58345755636f54517130502b7045450a744f32444d42384741315564497751594d4261414645636830786c632b58345755636f54517130502b704545744f32444d41384741315564457745422f7751460a4d414d4241663877494159445652305242426b7746344956636d566e6447567a6443356a6247347562473576636d4975593239744d41304743537147534962330a445145424377554141344942415141594d7649415a526c704b50394a385137583648714b4477566b67563075704f5a4c463439665661514d5977306b456a71350a312f78395734515569703465594c422b54696e4a6f2b68486944573672756372564a4a5864764137356471772b62366f635132553046484741666a4b377a66700a666f7257394c68524b564c752f6955743657456f614646497a633035726c6f79494b3961514d7a30506c4863724d786c592f467a6f377353785a45586f7177370a3169474c4a417434505a61767775756e3279714a4855743637773336495a415a65664541442b4874545a757136336d6b4742642b4b4847446a4572644c4d65660a3052326a3534505146772f4652706f4c6a6a716c4b796e766b4a30337268474f363068635342516957744757682f47652b5a2f46596c6d4e47594a71486334790a6d536459446b69632f626a4c536370496743534f2f316a6454677063626c5741455943770a2d2d2d2d2d454e442043455254494649434154452d2d2d2d2d0a",
        lnd="2d2d2d2d2d424547494e2043455254494649434154452d2d2d2d2d0a4d4949434f6a434341654367417749424167495145334d79326731673579527344333576322f34716644414b42676771686b6a4f50515144416a41344d5238770a485159445651514b45785a73626d5167595856306232646c626d56795958526c5a43426a5a584a304d5255774577594456515144457777344e6a42695954566a0a4e5451334e7a41774868634e4d6a49774f4449774d6a45314d4451315768634e4d6a4d784d4445314d6a45314d445131576a41344d523877485159445651514b0a45785a73626d5167595856306232646c626d56795958526c5a43426a5a584a304d5255774577594456515144457777344e6a42695954566a4e5451334e7a41770a5754415442676371686b6a4f5051494242676771686b6a4f50514d4242774e43414152526e534b7933754e565672515857687845486f54587a777143753459430a6453524456715179724a77523331334f70305343685a5a616e5a7869676a46424b6c61706d51764e52793149684e5578646b4e32655451346f34484c4d4948490a4d41344741315564447745422f775145417749437044415442674e56485355454444414b4267677242674546425163444154415042674e5648524d42416638450a425441444151482f4d42304741315564446751574242547534795467394a30316c33726f6a457a5369445364335246777a7a427842674e5648524545616a426f0a676777344e6a42695954566a4e5451334e7a434343577876593246736147397a6449495563326c6e626d56304c6d78755a433573626d39795969356a623232430a4248567561586943436e56756158687759574e725a58534342324a315a6d4e76626d3648424838414141474845414141414141414141414141414141414141410a41414748424b775741415177436759494b6f5a497a6a30454177494453414177525149676377525376544e714a5072563678642b53464b5a566738416a4951770a6a59635136644e51305039775479454349514434566a3361632b622b33357456656459525835734f4a374b5741456448656d77766c354f515334456733773d3d0a2d2d2d2d2d454e442043455254494649434154452d2d2d2d2d",
    )[node_type]
    mac = dict(
        cln="02010b632d6c696768746e696e67023e5475652053657020323020323032322030383a30313a353720474d542b303030302028436f6f7264696e6174656420556e6976657273616c2054696d652900000620e51c2529161fa69b4210c50b9b1b0d1c96e6cdfbb4bc47629cbf559b1399be0e",
        lnd="0201036c6e6402f801030a106fb784f1598e0ce2f89c050b98139c8e1201301a160a0761646472657373120472656164120577726974651a130a04696e666f120472656164120577726974651a170a08696e766f69636573120472656164120577726974651a210a086d616361726f6f6e120867656e6572617465120472656164120577726974651a160a076d657373616765120472656164120577726974651a170a086f6666636861696e120472656164120577726974651a160a076f6e636861696e120472656164120577726974651a140a057065657273120472656164120577726974651a180a067369676e6572120867656e6572617465120472656164000006205d186c6864b437cd5d723eef6d064eae85467e7913f876a8b49bfe962028a2e8",
    )[node_type]
    network = dict(cln="regtest", lnd="signet")[node_type]
    create(
        hostname=hostname,
        mac_hex=mac,
        node_type=node_type,
        protocol=protocol,
        network=network,
        cert_hex=cert,
        rest_port=rest_port,
        grpc_port=grpc_port,
        use_node=use_node,
    )


@app.command()
def create(
    hostname: str = typer.Option(
        ..., help="IP address or DNS-resolvable name for this host."
    ),
    mac_hex: str = typer.Option(..., help="The node macaroon in hex format."),
    node_type: str = typer.Option(..., help="cln or lnd."),
    protocol: str = typer.Option(..., help="rest or grpc."),
    network: str = typer.Option(
        ..., help="IP address or DNS-resovable name for this host."
    ),
    cert_hex: str = typer.Option("", help="The node certificate in hex format."),
    rest_port: int = typer.Option(8080, help="REST port."),
    grpc_port: int = typer.Option(10009, help="GRPC port."),
    use_node: bool = typer.Option(True, help="Whether to set as default."),
):
    """
    Create a node.

    This command encrypts the mac / certs, and attempts to connect to the node. If the connection is successful, then it saves the node information for later access.

    If `use-node` is `True` then all subsequent commands will use this node as the default node.

    A **node** is essentially the bare-minimum data Orb requires to connect to a lightning node.

    Node data is saved in various places depending on your OS:

    - Linux: ~/.config/orb_<pubkey>/orb_<pubkey>.ini
    - OSX: ~/Library/Application Support/orb_<pubkey>/orb_<pubkey>.ini
    - Windows: ${APPDATA}/orb_<pubkey>/orb_<pubkey>.ini

    This command is used by other commands, e.g:

    * :ref:`orb-node-create-orb-public`
    * :ref:`orb-node-create-from-cert-files`
    * :ref:`orb-node-ssh-wizard`

    .. asciinema:: /_static/orb-node-create.cast
    """

    pprint_from_ansi(chalk().cyan(f"Encrypting mac"))
    mac_secure = MacaroonSecure.init_from_plain(mac_hex).macaroon_secure.decode()
    pprint_from_ansi(chalk().cyan(f"Encrypting cert"))
    if cert_hex:
        cert_secure = CertificateSecure.init_from_hex(cert_hex).cert_secure.decode()
    else:
        cert_secure = ""
    pprint_from_ansi(chalk().cyan(f"Connecting to: {hostname}"))
    ln = Ln(
        node_type=node_type,
        fallback_to_mock=False,
        cache=False,
        use_prefs=False,
        hostname=hostname,
        protocol=protocol,
        mac_secure=mac_secure,
        cert_secure=cert_secure,
        rest_port=rest_port,
        grpc_port=grpc_port,
    )
    try:
        pubkey = ln.get_info().identity_pubkey
        pprint_from_ansi(chalk().greenBright(f"Connected to: {pubkey}"))
    except Exception as e:
        pprint_from_ansi(chalk().red(f"Failed to connect: {e}"))
        return
    conf_dir = Path(get_user_data_dir_static()) / f"orb_{pubkey}"
    if not conf_dir.is_dir():
        conf_dir.mkdir()
        pprint_from_ansi(chalk().green(f"{conf_dir} created"))
    conf_path = conf_dir / f"orb_{pubkey}.ini"
    conf = ConfigParser()
    conf.filename = conf_path.as_posix()
    conf.add_section("host")
    conf.set("host", "hostname", hostname)
    conf.set("host", "type", node_type)
    conf.add_section("ln")
    conf.set("ln", "macaroon_admin", mac_secure)
    conf.set("ln", "tls_certificate", cert_secure)
    conf.set("ln", "network", network)
    conf.set("ln", "protocol", protocol)
    conf.set("ln", "rest_port", str(rest_port))
    conf.set("ln", "grpc_port", str(grpc_port))
    conf.set("ln", "identity_pubkey", pubkey)
    conf.write(conf_path.open("w"))
    pprint_from_ansi(chalk().green(f"{conf_path} created"))
    if use_node:
        use(pubkey)


@app.command()
def create_from_cert_files(
    hostname: str = typer.Option(
        ..., help="IP address or DNS-resolvable name for this host."
    ),
    mac_file_path: str = typer.Option(..., help="Path to the node macaroon."),
    node_type: str = typer.Option(..., help="cln or lnd."),
    protocol: str = typer.Option(..., help="rest or grpc."),
    network: str = typer.Option(
        ..., help="IP address or DNS-resovable name for this host."
    ),
    cert_file_path: str = typer.Option(..., help="Path to the node certificate."),
    rest_port: int = typer.Option(8080, help="REST port."),
    grpc_port: int = typer.Option(10009, help="GRPC port."),
    use_node: bool = typer.Option(True, help="Whether to set as default."),
):
    """
    Create node and use certificate files.

    This command is very similar to :ref:`orb-node-create`, the difference being that instead of taking certificate and macaroon data, it takes in paths to those files, with:

    `--mac-file-path=...`
    `--cert-file-path=...`

    This is practical for creating nodes after certificates and macaroons have been copied locally.

    .. asciinema:: /_static/orb-node-create-from-cert-files.cast
    """
    pprint_from_ansi(chalk().cyan(f"Reading mac: {mac_file_path}"))
    cert_hex, mac_hex = "", ""
    with open(mac_file_path, "rb") as f:
        mac_hex = codecs.encode(f.read(), "hex")
    if cert_file_path:
        pprint_from_ansi(chalk().cyan(f"Reading cert: {cert_file_path}"))
        with open(cert_file_path, "rb") as f:
            cert_hex = codecs.encode(f.read(), "hex")

    create(
        hostname=hostname,
        mac_hex=mac_hex,
        node_type=node_type,
        protocol=protocol,
        network=network,
        cert_hex=cert_hex,
        rest_port=rest_port,
        grpc_port=grpc_port,
        use_node=use_node,
    )


@app.command()
def ssh_wizard(
    hostname: str = typer.Option(
        ..., help="IP address or DNS-resolvable name for this host."
    ),
    node_type: str = typer.Option(..., help="cln or lnd."),
    ssh_cert_path: Path = typer.Option(
        None, help="Certificate to use for the SSH session."
    ),
    ssh_password: str = typer.Option(None, help="Password to use for the SSH session."),
    ln_cert_path: Path = typer.Option(
        None, help="Path of the node certificate on the target host."
    ),
    ln_macaroon_path: Path = typer.Option(
        None, help="Path of the node macaroon on the target host."
    ),
    network: str = typer.Option(
        ..., help="IP address or DNS-resovable name for this host."
    ),
    protocol: str = typer.Option(..., help="rest or grpc."),
    rest_port: int = typer.Option(8080, help="REST port."),
    grpc_port: int = typer.Option(10009, help="GRPC port."),
    ssh_user: str = typer.Option("ubuntu", help="Username for SSH session."),
    ssh_port: int = typer.Option(22, help="Port for SSH session."),
    use_node: bool = typer.Option(True, help="Whether to set as default."),
):
    """
    SSH into the node, copy the cert and mac, and create the node.

    The command sshes into a host, and copies the certificate and macaroon from the paths specified with `--ln-cert-path=...` and `--ln-macaroon-path=...` flags.

    The remainder of the operations is invoking the :ref:`orb_node_create` command.

    .. asciinema:: /_static/orb-node-ssh-wizard.cast
    """
    if type(ssh_cert_path) is str:
        ssh_cert_path = Path(ssh_cert_path)

    connect_kwargs = {}
    if ssh_cert_path:
        connect_kwargs["key_filename"] = ssh_cert_path.as_posix()
    elif ssh_password:
        connect_kwargs["password"] = ssh_password
    with Connection(
        hostname, connect_kwargs=connect_kwargs, user=ssh_user, port=ssh_port
    ) as con:
        pprint_from_ansi(chalk().magenta("ssh session connected!"))
        try:
            pprint_from_ansi(
                chalk().green(f'OS:       {con.run("uname", hide=True).stdout.strip()}')
            )
            pprint_from_ansi(
                chalk().green(
                    f'Hostname: {con.run("hostname", hide=True).stdout.strip()}'
                )
            )
        except:
            pass

        with TemporaryDirectory() as d:
            d = Path(d)
            tmp_ln_cert_path = d / Path(ln_cert_path).name
            tmp_ln_macaroon_path = d / Path(ln_macaroon_path).name
            pprint_from_ansi(chalk().cyan(f"Securely copying: {ln_cert_path}"))
            con.get(
                f"{ln_cert_path}",
                tmp_ln_cert_path.as_posix(),
            )
            pprint_from_ansi(chalk().cyan(f"Securely copying: {ln_macaroon_path}"))
            con.get(
                f"{ln_macaroon_path}",
                tmp_ln_macaroon_path.as_posix(),
            )

            pprint_from_ansi(chalk().cyan(f"Encrypting: {tmp_ln_cert_path}"))
            pprint_from_ansi(chalk().cyan(f"Encrypting: {tmp_ln_macaroon_path}"))

            with tmp_ln_macaroon_path.open("rb") as f:
                mac_hex = codecs.encode(f.read(), "hex")
            with tmp_ln_cert_path.open("rb") as f:
                cert_hex = codecs.encode(f.read(), "hex")
            from orb.ln import Ln

            create(
                hostname=hostname,
                mac_hex=mac_hex,
                node_type=node_type,
                protocol=protocol,
                network=network,
                cert_hex=cert_hex,
                rest_port=rest_port,
                grpc_port=grpc_port,
                use_node=use_node,
            )


@app.command()
def ssh_fetch_certs(
    hostname: str = typer.Option(
        ..., help="IP address or DNS-resolvable name for this host."
    ),
    ssh_cert_path: Path = typer.Option(
        None, help="Certificate to use for the SSH session."
    ),
    ssh_password: str = typer.Option(None, help="Password to use for the SSH session."),
    ln_cert_path: Path = typer.Option(
        None, help="Path of the node certificate on the target host."
    ),
    ln_macaroon_path: Path = typer.Option(
        None, help="Path of the node macaroon on the target host."
    ),
    ssh_user: str = typer.Option("ubuntu", help="Username for SSH session."),
    ssh_port: int = typer.Option(22, help="Port for SSH session."),
):
    """
    SSH into the node, copy the cert and mac into the current folder.

    .. asciinema:: /_static/orb-node-ssh-fetch-certs.cast
    """
    if type(ssh_cert_path) is str:
        ssh_cert_path = Path(ssh_cert_path)

    connect_kwargs = {}
    if ssh_cert_path:
        connect_kwargs["key_filename"] = ssh_cert_path.as_posix()
    elif ssh_password:
        connect_kwargs["password"] = ssh_password
    with Connection(
        hostname, connect_kwargs=connect_kwargs, user=ssh_user, port=ssh_port
    ) as con:
        pprint_from_ansi(chalk().magenta("ssh session connected!"))
        try:
            pprint_from_ansi(
                chalk().green(f'OS:       {con.run("uname", hide=True).stdout.strip()}')
            )
            pprint_from_ansi(
                chalk().green(
                    f'Hostname: {con.run("hostname", hide=True).stdout.strip()}'
                )
            )
        except:
            pass

        pprint_from_ansi(chalk().cyan(f"Copying: {ln_cert_path}"))
        con.get(f"{ln_cert_path.as_posix()}", ln_cert_path.name)
        pprint_from_ansi(chalk().cyan(f"Copying: {ln_macaroon_path}"))
        con.get(f"{ln_macaroon_path.as_posix()}", ln_macaroon_path.name)
