"""BibParser: Parse a bibliography from a conf file"""

from ConfigParser import SafeConfigParser

from bib import Bib
from entry import Entry

class BibParser(object):

    def __init__(self):
        """Initialize ConfigParser instance"""
        pass

    def parse_bib(self, filenames, append_to=None):
        """Parse files and create Bib instance.

        If append_to is not None, it should be an existing Bib instance
        that will be appended to."""
        bib = append_to if append_to else Bib()
        config = SafeConfigParser()
        config.read(filenames)
        sections = config.sections()
        for section in sections:
            entry = Entry(config.items(section))
            entry["key"] = section
            entry.setdefault("month", None)
            entry.setdefault("howpublished", None)
            bib.append(entry)
        return bib
