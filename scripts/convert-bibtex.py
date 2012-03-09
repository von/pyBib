#!/usr/bin/env python
"""Convert a bibtex file to a pyBib file"""

import re
import sys

empty_string_re = re.compile("^\s*$")
entry_start_re = re.compile("@\w+[{(](\S+),")
entry_line_re = re.compile("^(\w+)\s*=\s*(.*?),?\s*$")
entry_end_re = re.compile("^[})]$")

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

def main(argv=None):
    # Do argv default this way, as doing it in the functional
    # declaration sets it at compile time.
    if argv is None:
        argv = sys.argv

    #print "# mode: conf-colon-mode"

    for file in argv[1:]:
        with open(file) as f:
            for line in f.readlines():
                match = empty_string_re.match(line)
                if match:
                    continue
                match = entry_start_re.match(line)
                if match:
                    print "[{}]".format(match.group(1))
                    continue
                match = entry_line_re.match(line)
                if match:
                    var = match.group(1)
                    value = match.group(2)
                    value = remove_curly_brackets(value)
                    value = remove_quotes(value)
                    value = unescape_chars(value)
                    value = escape_chars(value)
                    if empty_string_re.match(value):
                        continue
                    print "{}: {}".format(var, value)
                    continue
                match = entry_end_re.match(line)
                if match:
                    print ""
                    continue
                print "ERROR, unrecognized line: " + line

if __name__ == "__main__":
    sys.exit(main())

  
