#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Intelligent Agents
# Team project - coursePlanner agent
# Tjalle Galama, Ernö Groeneweg, Otto Mättas, Shaoya Ren, Vincent de Wit

from owlready2 import *
from rdflib import *

## Optional: For debugging
#owlready2.set_log_level(9) 

# Get Java environment variable
java_home = ((subprocess.check_output(['which','java'])).decode('utf-8')).rstrip()
# To load the reasoner, we need to define the location of JRE
owlready2.JAVA_EXE = java_home

class SparqlQueries:
    def __init__(self):
        my_world = World()

        # Load the OWL ontology
        my_world.get_ontology("https://raw.githubusercontent.com/ottomattas/INFOIAG/master/Project/courseOntology.owl").load()

        # Start and sync the reasoner
        sync_reasoner(my_world)
        # Start and sync the reasoner; optional for debugging
        #sync_reasoner(my_world, debug=9)

        # Make a graph for SPARQL
        self.graph = my_world.as_rdflib_graph()

    def search(self):
        #Search query is given here
        #Base URL of your ontology has to be given here
        query = "SELECT ?s ?p ?o " \
                "WHERE { " \
                "?s ?p ?o . " \
                "}"

        query_2 = "SELECT ?p " \
                "WHERE { " \
                "?s ?p ?o . " \
                "}"

        query_3 = "SELECT ?class " \
                "WHERE { " \
                "?class rdfs:subClassOf ?course " \
                "}"

        # Run the query
        resultsList = self.graph.query(query_3)

        ################
        # Create JSON object
        #response = []
        #for item in resultsList:
        #    s = str(item['s'].toPython())
        #    s = re.sub(r'.*#',"",s)

        #    p = str(item['p'].toPython())
        #    p = re.sub(r'.*#', "", p)

        #    o = str(item['o'].toPython())
        #    o = re.sub(r'.*#', "", o)
        #    response.append({'s' : s, 'p' : p, "o" : o})

        # Print out the response for temporary visualisation
        #print(response)
        #return response

        ################
        #for item in resultsList:
        #    print(item)

        response = []
        for item in resultsList:
           s = str(item['class'].toPython())
           s = re.sub(r'.*#',"",s)
           response.append(s)

        print(response)
        return ", ".join(response).replace("_", " ")

runQuery = SparqlQueries()
runQuery.search()