#Maral Dadvar
#15/03/2017
#This scrips reads the rdf files generated for person from dbpedia and enriches each file with GNDid URI from Wikidata.

import unicodedata
import os , glob
import rdflib
from rdflib import Namespace, URIRef, Graph , Literal , OWL, RDFS , RDF
from SPARQLWrapper import SPARQLWrapper2, XML  , JSON , TURTLE
import re
import pprint

os.chdir('C:\Users\Maral\Desktop\output')

sparql = SPARQLWrapper2("https://query.wikidata.org/sparql")

path = 'C:\Users\Maral\Desktop\generated_person' #adapted to the list file path

output = open('statistics.csv','w')

output.writelines([str('filename'),',',str('gnd'),',',str('nognd'),'\n'])


graph = Graph()

foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
jl = Namespace("http://data.judaicalink.org/ontology/")
gndo = Namespace("http://d-nb.info/standards/elementset/gnd#")

wikilist=[]

def GndGenerator (URI):

    "this function extracts the gndid of the author from Wikidata"

    spar1= """
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
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>

        SELECT ?id

        where {{

        {0} p:P227 ?gnd.
         ?gnd ps:P227 ?id

        }}


        """.format(URI)

    sparql.setQuery(spar1)
    sparql.setReturnFormat(TURTLE)
    results = sparql.query().convert()


    if (u"id") in results:
        bindings = results[u"id"]
        for b in bindings:
           return b[u"id"].value


for filename in glob.glob(os.path.join(path, '*.rdf')):

    ngnd = 0
    nognd=0
    print filename
    g = Graph()
    g.parse(filename, format="turtle")

    #this query will extract only the sameAs links to Wikidata

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

        SELECT ?x ?same

        where {

          ?x owl:sameAs ?same.
          FILTER ( strstarts(str(?same), "http://www.wikidata.org/entity/")). }

    """

    results = g.query(spar)

    g.bind('gndo',gndo)

    for item in results:

       URI = '<'+ str(item[1]) + '>' #turn it into query adaptable URI format

       wikilist.append(URI)

       gnd = GndGenerator(URI) #generate the GNDid

       outputfile = 'gnd_' + filename.rsplit('\\',1)[1].strip() #creat the output file name

       if gnd != None: #if an id was found
            ngnd = ngnd+1 #to count the number of entries with an id
            gndid = 'http://d-nb.info/gnd/' + gnd
            print gndid

            g.add( (URIRef(item[0]), gndo.gndIdentifier , URIRef(gndid) ) ) #add the GNDid to the graph
            g.serialize(destination = outputfile , format="turtle")

       else:
            nognd = nognd +1 #to count the number of entries without an id
            g.serialize(destination = outputfile , format="turtle")

    output.writelines([str(filename),',',str(ngnd),',',str(nognd),'\n'])


output.close()


