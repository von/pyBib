"""Bib class: represents a bibliography"""

class Bib(list):
    """Class representing a bliography"""

    def __init__(self, entries=None):
        """Initialize Bib instance

        If entries is not None, it must be Bib instance or list of entries."""
        if entries is not None:
            self.extend(entries)

    def sort_by_date(reverse=True):
        """Sort entries by date in place

        If reverse == True, then will be newest to older."""
        self.sort(cmp=lambda a,b: cmp(a["datetime"], b["datetime"]),
                  reverse=reverse)
