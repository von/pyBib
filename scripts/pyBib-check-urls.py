#!/usr/bin/env python
"""Check URLs in pyBib bibliography"""

import argparse
import ConfigParser
import httplib
import urlparse
import sys

import requests

from pybib import BibParser

######################################################################


def check_url(url):
    response = requests.get(url,
                            verify=False  # Ignore https certificates
                            )
    return response.status_code == 200

######################################################################


def main(argv=None):
    # Do argv default this way, as doing it in the functional
    # declaration sets it at compile time.
    if argv is None:
        argv = sys.argv

    # Argument parsing
    parser = argparse.ArgumentParser(
        description=__doc__,  # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # To have --help print defaults with trade-off it changes
        # formatting, use: ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-v", "--verbose",
                        action='store_const', dest='verbose',
                        const=True, default=False,
                        help="run verbosely")
    parser.add_argument('bibs', metavar='file', type=str, nargs='+',
                        help='bib files to use')
    args = parser.parse_args()
    bib_parser = BibParser()
    entries = bib_parser.parse_bib(args.bibs)
    status = 0
    for entry in entries:
        if entry.has_key("url"):
            url = entry["url"]
            if check_url(url):
                if args.verbose:
                    print "{} ... GOOD".format(url)
                else:
                    print "{} ... BAD".format(url)
                    status = 1
    return(status)

if __name__ == "__main__":
    sys.exit(main())
