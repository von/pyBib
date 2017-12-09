#!/usr/bin/env python
try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name = "pyBib",
    version = "0.7",
    packages = [ "pybib" ],
    scripts = [
        'scripts/figshare-publish.py',
        'scripts/pyBib.py',
        'scripts/pyBib-check-urls.py',
        ],
    install_requires=[
        'mako >= 0.7.0', # May work with earlier version
        'pigshare == 0.5.0', # My modified version of 0.5.0 is needed
        'requests >= 0.11.2',  # Might work with earlier version
        ],

    author = "Von Welch",
    author_email = "von@vwelch.com",
    description = "A python bibliography manager",
    license = "Apache2",
)
