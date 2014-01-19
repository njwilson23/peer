#peer

## Article searches

`peer` is a commandline utility for searching and accessing a researcher's
library of PDF files. To search for a particular file, use something like

    peer [author] [date] [keyword]

If any matching documents are found, they will be printed to the screen. To open
the first result, use

    peer [author] [date] [keyword] -o

Right now, `peer` only searches filenames, although integration with BibTeX
databases is something I'm working on.

## Piping

It's possible to pipe results in a Unix-y way. For example, to do a regex search
of article text:

    peer -rp [author] | xargs less | grep -e [pattern]

The `r` flag prints the "raw" output to _stdout_, while the `p` flag includes
the full file path in the output. For a full list of options, type `peer
--help`. The behaviour of `peer` can be customized to some extent through a
configuration file (`.peerrc.json`).

