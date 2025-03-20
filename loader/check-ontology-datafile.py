#This script reads the RDF ontology and an RDF dataset file (both in turtle) and outputs statistics about all properties used in this file,
#distinguishing properties that are in our ontology and the ones that are not.

from rdflib import Graph
from rdflib.namespace import RDF
import sys
from SPARQLWrapper import SPARQLWrapper2, XML , RDF , JSON , TURTLE


def ontology_checker(ontology,datafile):

    ont = Graph()
    ont.parse(ontology, format="turtle")
    data = Graph()
    data.parse(datafile, format="turtle")
    ont.bind('rdf',RDF)

    result = ont.query("SELECT ?p WHERE {?p a rdf:Property}")

    properties = [str(b["p"]) for b in result.bindings]

    print("Checking all properties in our ontology:")
    for p in properties:
        print(p)

    result = data.query("SELECT ?p (count(?p) as ?c) WHERE {?s ?p ?o} GROUP BY ?p")
    dataprops = [(str(b["p"]), str(b["c"])) for b in result.bindings]
    print("Checking all properties in our dataset:")
    in_ontology = {}
    undocumented = {}
    for p in dataprops:
        if p[0] in properties:
            in_ontology[p[0]] = p[1]
        else:
            undocumented[p[0]] = p[1]

    print("Ontology statistics:")
    for i in range (0,len(in_ontology.items())):
        print(in_ontology.items()[i])

    print("Not in ontology:")
    print(undocumented)

    return


#insert the file name from the commant line
ontology = sys.argv[1]
datafile = sys.argv[2]

#insert the file name directly
#ontology = 'C:\Users\Maral\Desktop\judaicalink-ontology.ttl'
#datafile = 'C:\\Users\\Maral\\Desktop\\bhr-final-05.ttl'

ontology_checker(ontology,datafile)



