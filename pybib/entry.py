"""Entry class: represents a bibliography entry"""

import collections
import datetime

class Entry(collections.defaultdict):
    """Class representing a bibliography entry"""

    def __init__(self, initial_values=None):
        """Initialize entry

        If initial_values is not None, it must be a dictionary of initial values."""
        def default_factory():
            return None
        super(Entry, self).__init__(default_factory)
        if initial_values is not None:
            self.update(initial_values)

    def __getattr__(self, name):
        """Mimic __getitem__(name)"""
        return self[name]

    def datetime(self):
        """Return datetime object representing publication date of entry"""
        s = self["month"] if self["month"] else "Jan"
        s += " " + self["year"]
        try:
            dt = datetime.datetime.strptime(s, "%b %Y")
        except ValueError:
            dt = datetime.datetime.strptime(s, "%B %Y")
        return dt
