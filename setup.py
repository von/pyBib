#!/usr/bin/env python
try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name = "pyBib",
    version = "0.1",
    scripts = [ 'scripts/pyBib.py' ],
    # May work with earlier version, but have not tried
    install_requires=['tempita >= 0.5'],

    author = "Von Welch",
    author_email = "von@vwelch.com",
    description = "A python bibliography manager",
    license = "Apache2",
)
