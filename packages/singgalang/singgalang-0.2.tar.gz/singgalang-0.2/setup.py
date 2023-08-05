from setuptools import setup

setup(
name="singgalang",
version="0.2",
description="Python Script dengan tempo yang sesingkat-singkatnya",
author="Muhammad Al Fajri",
url="https://github.com/aN4ksaL4y/hariansinggalang",
install_requires=["requests","bs4", "urwid"],
scripts=["bin/singgalang"],
packages=["singgalang"],
zip_safe=False
)
