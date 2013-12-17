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

BibEntry = namedtuple("Entry", ("authors", "title", "year", "journal"))

def parseline(s):
    """ Given a line from a BibTeX entry, try to return a key-value pair.
    Returns None if the key is not for the Title, Journal, Author, or Year. """
    key = s.split("=", 1)[0].strip()
    if key in ("Title", "Journal", "Author", "Year"):
        value = s.split("=", 1)[1].strip().strip("{}")
        return (key, value)
    else:
        return (key, None)


def readentries(f):
    """ Return a list of BibTeX entries from a file-like object.

    EXPERIMENTAL WIP STATE!
    """
    # State-machine implementation
    inentry = False
    entries = []
    d = dict()

    for line in f:
        if not inentry and (line.lstrip()[0] == "@"):
            inentry = True
        elif inentry and (line.lstrip() == "}"):
            # WARNING! This is not robust to free-styling BibTeX entries - only
            # for proof-of-concept
            inentry = False
            entry = BibEntry(authors=d["authors"],
                             title=d["title"],
                             year=d["year"],
                             journal=d["journal"])
            entries.append(entry)
        elif inentry:
            fieldname, value = parseline(line)
            d[fieldname] = values
        else:
            pass

    return entries




def scan(entries, *funcs):
    """ Scan a list of BibTeX entries for items that match all `*funcs` and
    return a generator or positive matches. """
    matches = []
    for func in funcs:
        f.seek(0)
        matches.append(map(func, entries))

    def matches_all(i, matches):
        if False not in (m[i] for m in matches):
            return True
        else:
            return False

    return (entry for i, entry in entries if matches_all(i, matches))



