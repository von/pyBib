#!/usr/bin/env python
try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name = "pyBib",
    version = "0.3",
    packages = [ "pybib" ],
    scripts = [
        'scripts/pyBib.py',
        'scripts/pyBib-check-urls.py'
        ],
    install_requires=[
        'mako >= 0.7.0', # May work with earlier version
        'requests >= 0.11.2',  # Might work with earlier version
        ],

    author = "Von Welch",
    author_email = "von@vwelch.com",
    description = "A python bibliography manager",
    license = "Apache2",
)
