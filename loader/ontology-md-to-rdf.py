##This script takes the judaicalink-ontology.md file as first argument/input file 
##and outputs only the code parts as an rdf file.

import sys
import os

#f = open('C:\Users\Maral\Desktop\judaicalink-ontology.md', 'r') #insert the file name directly

files = sys.argv[1] #insert the file name from the commant line
f = open(files, 'r')

output = open('judaicalink-ontology.rdf','w')

incode = False
for line in f:

    if re.match(r'^\s*$', line):
        continue
    elif line.startswith("```"):
        incode = not incode
        continue
    elif incode:
        print(line)
        output.write(line)


output.close()

