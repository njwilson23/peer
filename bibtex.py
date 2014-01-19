""" Basic BibTeX interface.

Treats a BibTeX file as a collection of entries (read by the `readentries`
function. List of entries can be searched using the `scan` function, which
returns a list of matches.
"""

from collections import namedtuple
import re

BibEntry = namedtuple("Entry", ("author", "title", "year", "journal", "file"))

def parseline(s):
    """ Given a line from a BibTeX entry, try to return a key-value pair.
    Returns None if the key is not for the Title, Journal, Author, or Year. """
    key, value = s.split("=", 1)
    key = key.strip()
    value = value.strip().strip(",").strip("{").strip("}")

    if key.lower() in ("title", "journal", "author", "file"):
        return (key.lower(), value)
    elif key == "year":
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
            entry = BibEntry(author=d.get("author", ""),
                             title=d.get("title", ""),
                             year=d.get("year", ""),
                             journal=d.get("journal", ""),
                             file=d.get("file", ""))
            entries.append(entry)

    return entries

def scan(entries, *funcs):
    """ Scan a list of BibTeX entries for items that match all `*funcs` and
    return a generator or positive matches. """
    def matches_all(entry):
        return False not in (f(entry) for f in funcs)
    return filter(matches_all, entries)

