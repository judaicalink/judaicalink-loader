#This code reads the data from fuseki (Rabbis based on century) and creats a new rdf file with the existing datd and the new created ones.

from rdflib import Namespace, URIRef, Graph , Literal , OWL, RDFS , RDF
from SPARQLWrapper import SPARQLWrapper2, XML  , JSON , TURTLE
import os
import re

sparql = SPARQLWrapper2("http://localhost:3030/Datasets/sparql")

os.chdir('C:\Users\Maral\Desktop')

foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
jl = Namespace("http://data.judaicalink.org/ontology/")
gndo = Namespace("http://d-nb.info/standards/elementset/gnd#")

graph = Graph()

sparql.setQuery("""
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
    PREFIX bibtex: <http://data.bibbase.org/ontology/#>
    PREFIX Springer: <http://lod.springer.com/data/ontology/schema#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>

select ?x ?label ?same ?id

WHERE {
  GRAPH <http://maral.wisslab.org/graphs/dbp-rabbis> {


    ?x owl:sameAs  ?y .
    ?x rdfs:label  ?label.
    ?x owl:sameAs  ?same .


    FILTER ( strstarts(str(?y), "http://www.wikidata.org/entity/")).



     SERVICE <https://query.wikidata.org/sparql> {

      ?y p:P227 ?gnd.
      ?gnd ps:P227 ?id


  }
}
}

""")



sparql.setReturnFormat(TURTLE)
results = sparql.query().convert()

graph.bind('jl', jl)
graph.bind('owl',OWL)
graph.bind('rdfs',RDFS)
graph.bind('foaf',foaf)
graph.bind('gndo', gndo)

if (u"x",u"label",u"same",u"id") in results:
    bindings = results[u"x",u"label",u"same",u"id"]
    for b in bindings:
        print b

        jlend = b[u"x"].value.rsplit('/',1)[1]
        jlid = 'http://data.judaicalink.org/data/dbpedia/' + jlend
        gndid = 'http://d-nb.info/gnd/' + b[u"id"].value

        graph.add( (URIRef(jlid), RDF.type , foaf.Person ) )
        graph.add( (URIRef(jlid), OWL.sameAs , URIRef(b[u"x"].value) ) )
        graph.add( (URIRef(jlid), jl.occupation , Literal('Rabbi') ) )
        graph.add( (URIRef(jlid), gndo.gndIdentifier , URIRef(gndid) ) )
        graph.add( (URIRef(jlid), jl.hasLabel, Literal(b[u"label"].value) ) )
        graph.add( (URIRef(jlid), OWL.sameAs , URIRef(b[u"same"].value) ) )


        graph.serialize(destination='output.rdf', format="turtle")
