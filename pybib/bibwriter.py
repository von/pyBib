"""BibWriter.py: Write out a Bibliography"""

from configparser import RawConfigParser

class BibWriter(object):
    """Write a Bib object out to a file object"""

    def write(self, bib, fileobject):
        """Write the given Bib instance to the given fileobject"""
        if bib is None:
            return
        parser = RawConfigParser()
        for entry in bib:
            key = entry.key
            parser.add_section(key)
            for item,value in list(entry.items()):
                parser.set(key, item, value)
        parser.write(fileobject)
