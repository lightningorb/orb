# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-27 13:05:47
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 16:19:44

from fabric import Connection
from invoke import task

blurb = """

The ORB CLI executes similarly regardless of the node
implementation. Currently only LND and CLN are supported.

Setting an alias
----------------

You may want to consider creating an alias, to run Orb
from any path on your system. On Linux you'd want to
add this to your .bashrc:

alias orb='/opt/orb/main.py ${*}'

Listing Commands
----------------

Appending `-l` lists all the available commands.

orb -l


Listing Collection Commands
---------------------------

Appending `-l` followed by the name of the collection
lists all commands available in the given collection.

orb -l node


Getting help on individual commands
-----------------------------------

To get help on individual commands, prepend the command
with `--help`.

orb --help node.use


"""


@task
def generate_cli_docs(c, namespace):
    """
    Generate CLI documentation.
    """
    c = Connection("localhost")
    commands = c.local("./main.py --list", hide=True).stdout
    with open("docs/source/commands.rst", "w") as wf:
        detailed = "ORB CLI\n========\n\n"
        detailed += blurb
        for cmd in namespace.task_names:
            if cmd == "generate-cli-docs":
                continue
            out = c.local(f"./main.py --help {cmd}", hide=True).stdout
            out = "\n".join(f"    {x}" for x in out.split("\n"))
            detailed += f"``orb {cmd}``\n-----------\n\n"
            detailed += ".. code:: bash\n\n"
            detailed += out
            detailed += "\n\n"
        wf.write(detailed)
