#!/usr/bin/env python
"""Bibliography handler"""

import argparse
import datetime
import configparser
import logging
import re
import string
import sys

import mako
from mako.template import Template
from mako.lookup import TemplateLookup

from pybib import BibParser

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
    parser.add_argument("-t", "--template", required=True,
                        help="template file", metavar="FILE")
    parser.add_argument("-T", "--template_path",
                        action='append',
                        help="search PATH for templates", metavar="PATH")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    parser.add_argument('bibs', metavar='args', type=str, nargs='+',
                        help='bib files to use')
    args = parser.parse_args()
    output_handler.setLevel(args.output_level)

    output.info("Reading template from {}".format(args.template))
    mylookup = TemplateLookup(directories=args.template_path,
                              input_encoding='utf-8',
                              output_encoding='utf-8')
    with open(args.template) as f:
        template_string = "".join(f.readlines())
        template = Template(template_string,
                            lookup=mylookup,
                            default_filters=['decode.utf8'],
                            input_encoding='utf-8',
                            output_encoding='utf-8')

    output.info("Parsing bib files")
    try:
        bib_parser = BibParser()
        entries = bib_parser.parse_bib(args.bibs)
    except Exception as e:
        output.error("Error parsing bibliography files")
        output.error(str(e))
        return 1

    substitutions = {
        "entries" : entries,
    }

    try:
        # Mako doesn't seem to be rendering into utf-8
        # hance decode() here
        print(template.render(**substitutions).decode())
    except Exception as e:
        output.error("Error filling in template")
        output.error(str(e))
        output.error(mako.exceptions.text_error_template().render())
        return 1

    return(0)

if __name__ == "__main__":
    sys.exit(main())
