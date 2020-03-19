"""BibTexParser: Parse a BibTex file"""

import re

from bib import Bib
from entry import Entry

EMPTY_STRING_RE = re.compile("^\s*$")
ENTRY_START_RE = re.compile("@\w+[{(](\S+),")
ENTRY_LINE_RE = re.compile("^(\w+)\s*=\s*(.*?),?\s*$")
ENTRY_END_RE = re.compile("^[})]$")

def remove_quotes(s):
    """Remove quote or curley brackets around string"""
    return s.strip("\"{}\"")

def remove_curly_brackets(s):
    """Remove curly brackets around characters in string"""
    return re.sub("\{(?P<char>\S+?)\}", "\g<char>", s)

def unescape_chars(s):
    """Unescape any characters"""
    return re.sub("\\\\&", "&", s) # "\\\\" matches single "\"

def escape_chars(s):
    """Escape any characters that need to be"""
    return re.sub("%", "%%", s)

class BibTexParser(object):

    def parse_bib(self, filenames, append_to=None):
        """Parse bibtexfiles and create Bib instance.

        If append_to is not None, it should be an existing Bib instance
        that will be appended to."""
        bib = append_to if append_to else Bib()
        entry = None
        for file in filenames:
            with open(file) as f:
                for line in f.readlines():
                    match = EMPTY_STRING_RE.match(line)
                    if match:
                        continue
                    match = ENTRY_START_RE.match(line)
                    if match:
                        entry = Entry()
                        bib.append(entry)
                        entry["key"] = match.group(1)
                        continue
                    match = ENTRY_LINE_RE.match(line)
                    if match:
                        var = match.group(1)
                        value = match.group(2)
                        value = remove_curly_brackets(value)
                        value = remove_quotes(value)
                        value = unescape_chars(value)
                        value = escape_chars(value)
                        if EMPTY_STRING_RE.match(value):
                            continue
                        entry[var] = value
                        continue
                    match = ENTRY_END_RE.match(line)
                    if match:
                        entry = None
                        continue
                    # unrecognized line
        return bib
