#!/usr/bin/env python
"""Convert a bibtex file to a pyBib file"""

import sys

from pybib import BibTexParser
from pybib import BibWriter

def main(argv=None):
    # Do argv default this way, as doing it in the function
    # declaration sets it at compile time.
    if argv is None:
        argv = sys.argv

    parser = BibTexParser()
    bib = parser.parse_bib(argv[1:])

    writer = BibWriter()
    writer.write(bib, sys.stdout)

if __name__ == "__main__":
    sys.exit(main())
