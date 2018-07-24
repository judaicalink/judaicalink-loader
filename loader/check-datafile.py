'''
This script reads the RDF ontology and an RDF dataset file
(both in turtle) and outputs statistics about all properties
used in this file, distinguishing properties that are in our
ontology and the ones that are not.

TODO: Make it a module/function to be used from other code

TODO: Make it a proper CLI application
'''
from rdflib import Graph
from rdflib.namespace import RDF
import sys

ONTOLOGY = sys.argv[1]
DATAFILE = sys.argv[2]

ont = Graph()
ont.parse(ONTOLOGY, format="turtle")
ont.bind("rdf", RDF)

data = Graph()
data.parse(DATAFILE, format="turtle")

result = ont.query("SELECT ?p WHERE {?p a rdf:Property}")

properties = [b["p"] for b in result.bindings]

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
print(in_ontology)

print("Not in ontology:")
print(undocumented)
