#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 12:30:23 2019

@author: promeaoeg
"""

# pip install owlready2 (in terminal)

'''
Simple queries can be performed with the .search() method of the ontology. 
It expects one or several keyword arguments. The supported keywords are:

iri , for searching entities by its full IRI
type , for searching Individuals of a given Class
subclass_of , for searching subclasses of a given Class
is_a , for searching both Individuals and subclasses of a given Class
any object , data or annotation property name

# https://pythonhosted.org/Owlready2/onto.html#loading-an-ontology-from-owl-files

'''
from owlready2 import *
import owlready2

# Load the ontology
onto = get_ontology("https://raw.githubusercontent.com/ottomattas/INFOIAG/master/Project/courseOntology.owl")
onto.load() 
    
# we have to define the location of JRE, otherwise the reasoner won't load
owlready2.JAVA_EXE ="/usr/bin/java"
sync_reasoner()