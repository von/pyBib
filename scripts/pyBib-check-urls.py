#!/usr/bin/env python
"""Check URLs in pyBib bibliography"""

import argparse
import ConfigParser
import datetime
import httplib
import urlparse
import sys

import requests

#
# Following functions are modified not rely on tempita.bunch
#
def get_entry_datetime(entry):
    """Return a datetime object for an entry."""
    s = entry["month"] if entry["month"] else "Jan"
    s += " " + entry["year"]
    try:
        d = datetime.datetime.strptime(s, "%b %Y")
    except ValueError:
        d = datetime.datetime.strptime(s, "%B %Y")
    return d

def parse_bib(filenames, append_to=None):
    """Parse entries from given filenames

    filenames can be a single string instead of a list."""
    if append_to is not None:
        bibs = append_to
    else:
        bibs = [] 
    config = ConfigParser.SafeConfigParser()
    config.read(filenames)
    sections = config.sections()
    for section in sections:
        entry = dict(config.items(section))
        entry["key"] = section
        entry.setdefault("month", None)
        entry.setdefault("howpublished", None)
        entry["datetime"] = get_entry_datetime(entry)
        bibs.append(entry)
    # Sort descending by datetime
    bibs.sort(cmp=lambda a,b: cmp(b["datetime"], a["datetime"]))
    return bibs

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
        description=__doc__, # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # To have --help print defaults with trade-off it changes
        # formatting, use: ArgumentDefaultsHelpFormatter
        )
    parser.add_argument("-v", "--verbose",
                        action='store_const', dest='verbose',
                        const=True, default=False,
                        help="run verbosely")
    parser.add_argument('bibs', metavar='args', type=str, nargs='+',
                        help='bib files to use')
    args = parser.parse_args()
    entries = parse_bib(args.bibs)
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

    
