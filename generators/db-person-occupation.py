#Maral Dadvar
#14/03/2017
#This scrips reads a list of Occupations URIs extracted from DBPedia and extracts the Persons label and sameAs links from each URI.
#Each occupation is stored in a separate rdf file.

import unicodedata
import os , glob
from rdflib import Namespace, URIRef, Graph , Literal , OWL, RDFS , RDF
from SPARQLWrapper import SPARQLWrapper2, XML  , JSON , TURTLE
import re


os.chdir('C:\Users\Maral\Desktop') #adapted to the list file path

sparql = SPARQLWrapper2("http://dbpedia.org/sparql")

foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
jl = Namespace("http://data.judaicalink.org/ontology/")

graph = Graph()

def PersonGenerator (URI,filename):

    "This function generates a rdf file of the person based on their occupation."

    spar= """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX gndo: <http://d-nb.info/standards/elementset/gnd#>
    PREFIX pro: <http://purl.org/hpi/patchr#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX edm: <http://www.europeana.eu/schemas/edm/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dblp: <http://dblp.org/rdf/schema-2015-01-26#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX dbpedia: <http://dbpedia.org/resource/>

    SELECT ?occ ?x ?name ?lan ?same

    where {{

      {0} rdfs:label ?occ.
      ?x dct:subject {0}.
      ?x rdfs:label ?name.
      bind(lang(?name) as ?lan).
      ?x owl:sameAs ?same.

    }}


    """.format(URI)

    sparql.setQuery(spar)
    sparql.setReturnFormat(TURTLE)
    results = sparql.query().convert()

    graph.bind('jl', jl)
    graph.bind('owl',OWL)
    graph.bind('rdfs',RDFS)
    graph.bind('foaf',foaf)


    if (u"x",u"name",u"occ",u"lan",u"same") in results:
        bindings = results[u"x",u"name",u"occ",u"lan","same"]
        for b in bindings:

            jlend = b[u"x"].value.rsplit('/',1)[1]
            jlid = 'http://data.judaicalink.org/data/dbpedia/' + jlend #change to Judaicalink URI

            names = b[u"name"].value + '@' + b[u"lan"].value #add the language tag of each label

            graph.add( (URIRef(jlid), RDF.type , foaf.Person ) )
            graph.add( (URIRef(jlid), OWL.sameAs , URIRef(b[u"x"].value) ) )
            graph.add( (URIRef(jlid), jl.occupation , Literal(b[u"occ"].value) ) )
            graph.add( (URIRef(jlid), jl.hasLabel, Literal(names) ) )
            graph.add( (URIRef(jlid), OWL.sameAs , URIRef(b[u"same"].value) ) )

            graph.serialize(destination= filename , format="turtle")

    return


URIs = []
URIlist = open ('C:\Users\Maral\Desktop\Occ_URI.txt' , 'r') #read the list of occupation URIs
list = URIlist.readlines()
for l in list:
    URIs.append(str(l))

for i in range (0,len(URIs)):

    filename = URIs[i].rsplit(':',1)[1].strip()
    filename = filename.replace('>','') + '.rdf' #generate a name for the output rdf file based on the occupation

    PersonGenerator(URIs[i],filename) # send to the function the occupation URI and the generated file name






