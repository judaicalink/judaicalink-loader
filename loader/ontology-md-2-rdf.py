'''
This script takes the judaicalink-ontology.md file as
first argument and outputs only the code parts in
``` backticks.

TODO: Get rid of blank lines, probably due to different
line endings in .md file

TODO: optionally provide output filename to write to.

TODO: Create a function/module that can be used from other
python code.
'''
import sys

FILE = sys.argv[1]

with open(FILE, 'r') as mdfile:
    incode = False
    for line in mdfile:
        if line.startswith("```"):
            incode = not incode
            continue
        if incode:
            print(line)
