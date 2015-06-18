#peer

`peer` is a commandline utility for searching and accessing a researcher's
library of PDF files. 

> **Update**
> `peer` does what it does. Additional features like BibTeX parsing are developed seperately in a new project, [`peer2`](https://github.com/njwilson23/peer2).

## Installation

Either `git clone` or
[download](https://github.com/njwilson23/peer/archive/master.zip) and unzip from
Github. From the package directory, run

    pip install -r requirements.txt
    pip install . -U

## Article searches

To search for a particular file, use something like

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
--help`.

## Customization

The behaviour of `peer` can be customized through a configuration file
(`.peer.yaml`) located in either the current directory or the user home
directory (i.e. `$HOME` on Linux). An example configuration looks like:

    # This is the default PDF reader to use when invoked with the '-o' flag
    reader: "evince"

    # Search roots are the root nodes for the document scanner
    search_roots:
      - "~/Downloads"
      - "~/Documents/pdfs"
      - "~/Documents/books"

