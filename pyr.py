#!/usr/bin/env python
# Search for and open a PDF with the given name. Searches within a specified
# list of directories, hardcoded as *search_dirs*. For now, only check whether
# the path contains the directory name, which happens to be good enough.

import sys
import os
import subprocess
import traceback
import getopt

options, other_args = getopt.gnu_getopt(sys.argv[1:], "lf:", [])
optdict = dict(options)

if len(other_args) == 0:
    print """
    USAGE: readpdf [-f filter_term] [-l] search_terms

        search_terms    One or more case-insensitive words to search for

        -f filter_term  Name of a directory to filter by

        -l              List matches and quit
    """
    sys.exit()

search_dirs = ['Documents', 'Downloads']
eitherin = lambda L, s: True in ((a in s) for a in L)

sterm = '*' + reduce(lambda a,b: a+'*'+b, other_args) + '*'

# Use locate to search for PDFs
try:
    results = subprocess.check_output(('locate', '-e', '-b', '-i', sterm))
    results = results.split('\n')
    results = filter(lambda s: s[-4:].lower()=='.pdf', results)
    results = filter(lambda s: eitherin(search_dirs, s), results)
except subprocess.CalledProcessError:
    results = []

# Filter by a directory arg
if '-f' in optdict.keys():
    results = filter(lambda s: optdict['-f'] in s.split('/'), results)

# Print them to screen and exit
for i, result in enumerate(results):
    print i+1,'\t', result
    if i > 10:
        break

if ('-l' not in optdict) and (len(results) > 0):
    proc = subprocess.Popen(('evince', results[0]), stdin=None, stdout=None,
                            stderr=None, close_fds=True, shell=False)

