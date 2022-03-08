from distutils.core import setup
from os import path, unlink
from shutil import copyfile

long_description = ""
if path.exists("README"):
    with open("README", encoding="utf-8") as f:
        long_description = f.read()

version = open("VERSION").read().strip()

setup(
    name="rln",
    packages=["rlnd", "rlnd.commands"],
    version=version,
    license="MIT",
    description="A fabric script for easily provisioning, deploying and configuring your lightning node securely",
    long_description=long_description,
    author="getlightning",
    author_email="getlightning@protonmail.com",
    url="https://github.com/getlightning/getlightning",
    download_url=f"https://github.com/getlightning/getlightning/archive/refs/tags/v{version}.tar.gz",
    keywords=["lightning", "lnd", "bitcoin"],
    install_requires=["fabric", "boto3", "quantumrandom", "pyzipper", "arrow", "toml"],
    scripts=["rln"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
