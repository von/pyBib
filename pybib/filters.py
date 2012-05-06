"""Filter for use in tempaltes"""

import datetime
import re
import string

AUTHOR_SPLIT_RE = re.compile(",|\sand\s")

def authors_filter(s):
    """Given a list of authors, return a nice representation"""
    if s is None:
        return None
    authors = AUTHOR_SPLIT_RE.split(s)
    # Clean up whitespace and remove null authors
    authors = filter(lambda s: len(s) > 0, map(string.strip, authors))
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
    dt = None
    try:
        # Full month name
        dt = datetime.datetime.strptime(s, "%B")
    except ValueError:
        pass
    if dt is None:
        try:
            # Abbreviated month name
            dt = datetime.datetime.strptime(s, "%b")
        except ValueError:
            pass
    if dt is None:
        # Punt
        return s
    return dt.strftime("%B")
