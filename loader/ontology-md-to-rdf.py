#This script takes the judaicalink-ontology.md file as first argument/input file and outputs only the code parts as an rdf file.

import sys
import os
import re

def ontology_rdf(ontologyfile ):

    f = open(ontologyfile, 'r')
    output = open('judaicalink-ontology.ttl','w')

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
    return


#insert the file name directly
ontologyfile ='C:\Users\Maral\Desktop\judaicalink-ontology.md'

#insert the file name from the commant line
#ontologyfile = sys.argv[1]

ontology_rdf(ontologyfile)


