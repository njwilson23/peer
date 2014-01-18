""" Basic BibTeX interface.

Design:

peer will typically need one-time access to a BibTeX file in order to search
for entries matching a particular author, title, year, or journal.

In order to make this fast, I'll define a `scan` function that takes BibTeX
file ID and a list of match functions as input.

For each entry in the BibTeX file, test each provided function (using a `map`,
and return the union of positive matches.
"""

from collections import namedtuple
import re

BibEntry = namedtuple("Entry", ("author", "title", "year", "journal"))

def parseline(s):
    """ Given a line from a BibTeX entry, try to return a key-value pair.
    Returns None if the key is not for the Title, Journal, Author, or Year. """
    key, value = s.split("=", 1)
    key = key.strip()
    value = value.strip().strip(",").strip("{").strip("}")

    if key in ("Title", "Journal", "Author"):
        return (key, value)
    elif key == "Year":
        try:
            return (key, int(value))
        except ValueError:
            return (key, None)
    else:
        return (key, None)

def countbraces(s):
    """ Count unescaped open (+1) and closed (-1) brackets in a string. """
    return len(re.findall(r"(?<!\\){", s)) - len(re.findall(r"(?<!\\)}", s))

def readentries(f):
    """ Return a list of BibTeX entries from a file-like object.
    """
    # State-machine implementation
    inentry = False
    entries = []
    d = dict()

    for i, line in enumerate(f):

        if (line[0] == "%") or (len(line.strip()) == 0):
            pass

        elif inentry and (nbrac > 0) and ("=" in line):
            fieldname, value = parseline(line)
            d[fieldname] = value
            nbrac += countbraces(line)

        elif not inentry and (line.lstrip()[0] == "@"):
            inentry = True
            nbrac = countbraces(line)

        elif inentry:
            nbrac += countbraces(line)

        if inentry and (nbrac == 0):
            inentry = False
            entry = BibEntry(author=d["Author"],
                             title=d["Title"],
                             year=d["Year"],
                             journal=d["Journal"])
            entries.append(entry)

    return entries

def scan(entries, *funcs):
    """ Scan a list of BibTeX entries for items that match all `*funcs` and
    return a generator or positive matches. """
    def matches_all(entry):
        return False not in (f(entry) for f in funcs)
    return filter(matches_all, entries)

