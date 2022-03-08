from invoke import task, Collection
from fabric import Connection


def generate(c, namespace):
    """
    Generate this documentation.
    """
    c = Connection("localhost")
    commands = c.local("./rln --list", hide=True).stdout
    with open("docs/source/commands.rst", "w") as wf:
        detailed = "Commands\n========\n\n"
        for cmd in namespace.task_names:
            out = c.local(f"./rln --help {cmd}", hide=True).stdout
            out = "\n".join(f"    {x}" for x in out.split("\n"))
            detailed += f"``rln {cmd}``\n-----------\n\n"
            detailed += ".. code:: bash\n\n"
            detailed += out
            detailed += "\n\n"
        wf.write(detailed)
