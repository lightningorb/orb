from invoke import task

tor_list = "/etc/apt/sources.list.d/tor.list"


@task
def setup(c):
    """
    Configure tor from start to finish.
    """
    c.sudo("apt-get update")
    c.sudo("apt install -y apt-transport-https")
    tor_src = "https://deb.torproject.org/torproject.org"
    c.sudo(f"echo 'deb {tor_src} focal main' | sudo tee -a {tor_list}")
    c.sudo(f"echo 'deb-src {tor_src} focal main' | sudo tee -a {tor_list}")
    c.sudo(
        f"curl {tor_src}/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | sudo gpg --import"
    )
    c.sudo("gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -")
    c.sudo("apt update")
    c.sudo("apt install -y tor deb.torproject.org-keyring")
    c.sudo("usermod -a -G debian-tor ubuntu")
    c.sudo("chmod a+r /run/tor/control.authcookie")
    c.sudo("echo 'ControlPort 9051' | sudo tee -a /etc/tor/torrc")
    c.sudo("echo 'CookieAuthentication 1' | sudo tee -a /etc/tor/torrc")
    c.sudo("echo 'CookieAuthFileGroupReadable 1' | sudo tee -a /etc/tor/torrc")
    c.sudo("echo 'Log notice stdout' | sudo tee -a /etc/tor/torrc")
    c.sudo("echo 'SOCKSPort 9050' | sudo tee -a /etc/tor/torrc")
    c.sudo("service tor restart")
    check(c)


@task
def uninstall(c):
    c.sudo(f"rm -f {tor_list}")
    c.sudo("apt-get purge -y tor deb.torproject.org-keyring")


@task
def check(c):
    """
    Check whether tor is running
    """
    c.sudo(
        "curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs"
    )
