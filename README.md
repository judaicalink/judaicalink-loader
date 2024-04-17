# General description 

#### Generated by: Maral Dadvar


This repository contains Python source codes for Hugo-based dataset loader. 

The main JudaicaLink website is driven by the static site generator Hugo. We use the metadata of the web pages (Hugo frontmatter) to control the data publication process which is fully automated. On every push to the master branch, Github triggers an update script on our server that pulls the latest changes, rebuilds the website using Hugo and updates the data in the triple store according to the page metadata.
This way we ensure that the dataset descriptions on the web site, the data dumps and the data loaded in JudaicaLink are always consistent. The Hugo sources are collaboratively maintained using GitHub. 

Moreover there are two scripts regarding the ontology. The ontology-md-to-rdf.py which takes the judaicalink-ontology.md file as first argument/input file and outputs only the code parts as an rdf file. The ontology file can be found in judaidalink-ontology repository. 
The other script check-ontology-datafile.py, reads the RDF ontology generated by the previous script, and an RDF dataset file (both in turtle) and outputs statistics about all properties used in this file, distinguishing properties that are in our ontology and the ones that are not.



 