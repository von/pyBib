#!/usr/bin/env python
"""Bibliography handler"""

import argparse
import datetime
import ConfigParser
import logging
import re
import sys

from tempita import HTMLTemplate, Template, bunch

######################################################################
#
# Filter functions

AUTHOR_SPLIT_RE = re.compile(",|\sand\s")

def authors_filter(s):
    """Given a list of authors, return a nice representation"""
    if s is None:
        return None
    authors = AUTHOR_SPLIT_RE.split(s)
    for index in range(len(authors)):
        author = authors[index].strip()
        authors[index] = author
    if len(authors) > 1:
        authors_string = ", ".join(authors[:-1]) + " and " + authors[len(authors)-1]
    else:
        authors_string = authors[0]
    return authors_string

def first_name_initial_filter(s):
    """Make first name an initial and return"""
    parts = s.split()
    if len(parts) == 0:
        return s
    first_name = parts[0]
    parts[0] = first_name[0].upper() + "."
    return " ".join(parts)

def month_filter(s):
    """Given any reasonable month representation, return a nice string"""
    if s is None:
        return None
    return datetime.datetime.strptime(s, "%b").strftime("%B")

######################################################################

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
        entry = bunch(**dict(config.items(section)))
        entry.key = section
        entry.setdefault("month", None)
        entry.setdefault("howpublished", None)
        entry.datetime = get_entry_datetime(entry)
        bibs.append(entry)
    # Sort descending by datetime
    bibs.sort(cmp=lambda a,b: cmp(b.datetime, a.datetime))
    return bibs

def main(argv=None):
    # Do argv default this way, as doing it in the functional
    # declaration sets it at compile time.
    if argv is None:
        argv = sys.argv

    # Set up out output via logging module
    output = logging.getLogger(argv[0])
    output.setLevel(logging.DEBUG)
    output_handler = logging.StreamHandler() # Default is sys.stderr
    # Set up formatter to just print message without preamble
    output_handler.setFormatter(logging.Formatter("%(message)s"))
    output.addHandler(output_handler)

    # Argument parsing
    parser = argparse.ArgumentParser(
        description=__doc__, # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # To have --help print defaults with trade-off it changes
        # formatting, use: ArgumentDefaultsHelpFormatter
        )
    # Only allow one of debug/quiet mode
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("-d", "--debug",
                                 action='store_const', const=logging.DEBUG,
                                 dest="output_level", default=logging.INFO,
                                 help="print debugging")
    verbosity_group.add_argument("-q", "--quiet",
                                 action="store_const", const=logging.WARNING,
                                 dest="output_level",
                                 help="run quietly")
    parser.add_argument("-H", "--html",
                        action='store_const', dest='template_class',
                        const=HTMLTemplate, default=Template,
                        help="Do HTML escaping")
    parser.add_argument("-t", "--template", required=True,
                        help="template file", metavar="FILE")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    parser.add_argument('bibs', metavar='args', type=str, nargs='+',
                        help='bib files to use')
    args = parser.parse_args()
    output_handler.setLevel(args.output_level)

    output.info("Reading template from {}".format(args.template))
    with open(args.template) as f:
        template_string = "".join(f.readlines())
    template = args.template_class(template_string)

    output.info("Parsing bib files")
    entries = parse_bib(args.bibs)

    substitutions = {
        "entries" : entries,
        # Filters
        "authors_filter" : authors_filter,
        "first_name_initial_filter" : first_name_initial_filter,
        "month_filter" : month_filter,
        }
    print template.substitute(substitutions)
    
    return(0)

if __name__ == "__main__":
    sys.exit(main())

    
