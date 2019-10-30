#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Intelligent Agents
# Team project - coursePlanner agent
# Tjalle Galama, Ernö Groeneweg, Otto Mättas, Shaoya Ren, Vincent de Wit

from owlready2 import *
from rdflib import *

## Optional: For debugging
#owlready2.set_log_level(9) 

# To load the reasoner, we need to define the location of JRE
owlready2.JAVA_EXE = owlready2.JAVA_EXE ="/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"

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
        query = "base <http://webprotege.stanford.edu/project/jXugAxnqqUMqXPExOa310> " \
                "SELECT ?s ?p ?o " \
                "WHERE { " \
                "?s ?p ?o . " \
                "}"

        # Run the query
        resultsList = self.graph.query(query)

        # Create JSON object
        response = []
        for item in resultsList:
            s = str(item['s'].toPython())
            s = re.sub(r'.*#',"",s)

            p = str(item['p'].toPython())
            p = re.sub(r'.*#', "", p)

            o = str(item['o'].toPython())
            o = re.sub(r'.*#', "", o)
            response.append({'s' : s, 'p' : p, "o" : o})

        # Print out the response for temporary visualisation
        print(response)
        return response
    
def intersect(lst1, lst2): # to intersect two lists
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def extract_preferences():
    which_term = input('for which term (1/2/3/4) do you want to receive a recommendation? ')
    amount_of_courses_to_be_found = int(input('How many courses to you want to take? (1/2/3) '))
    print('For the following questions, press enter if you have no answer.')
    finished_courses = []
    finished_course = input('Have you already finished a course in term {}? If yes type the course code. '.format(which_term))
    if finished_course : # meaning the answer is not empty
        other_course = input('And maybe another one? Else press enter to continue. ')
        if other_course : # again meaning the answer is not empty
            finished_courses.append(other_course)
    chosen_courses = [] 
    if which_term == 1 and intersect(finished_courses,'INFOMAIR') == []:
        chosen_courses.append('INFOMAIR') # mandatory course 
        print('You have to take INFOMAIR.')
        amount_of_courses_to_be_found -= 1 
    if which_term == 3 and intersect(finished_courses,'WBMV05003') == []:
        chosen_courses.append('WBMV05003') # mandatory course 
        print('You have to take WBMV05003.')
        amount_of_courses_to_be_found -= 1 
    chosen_course = input('Have you already chosen a course for term {}? If yes type the course code. '.format(which_term))
    if chosen_course:
        if intersect(chosen_course,chosen_courses) == []: # so we don't get duplicates 
            # here we could build in the isPrerequisiteFor relation,
            # which would block you to choose a course if you haven't fnished
            # the prerequisite + give some explanation 
            chosen_courses.append(chosen_course)
            amount_of_courses_to_be_found -= 1
            if amount_of_courses_to_be_found != 0:
                chosen_course = input('And maybe you already chose another one? ')
                if chosen_course:
                    chosen_courses.append(chosen_course)
    
    # can we query + print the available lectureres here?
    lecturer_preference = input('Do you prefer or dislike a certain teacher? ')
    
    # print available time slots / weeks day
    time_preference = input('Do you prefer or dislike a certrain time?')
    
    # print available topics 
    topic_preference = input('Do you prefer or dislike a certain topic? ')
    
    # print available locations 
    location_preference = input('Do you prefer or dislike certain location? ')
    
    friends = []
    # print list of possible friends
    friend = input('Is any of these your friend?')
    if friend:
        friends.append(friend)
        other_friend = input('One more?')
        if other_friend:
            friends.append(other_friend)
            
    preferences = []
    preferences.append(which_term)
    preferences.append(amount_of_courses_to_be_found)
    preferences.append(finished_courses)
    preferences.append(chosen_courses)
    preferences.append(lecturer_preference)
    preferences.append(time_preference)
    preferences.append(topic_preference)
    preferences.append(friends)

    return preferences
    
def utility_function(preferences):
    print('This agent will set utility values on each constraint. ')
    print('heavy preference = 1, medium = 0.5, no preference = 0, dislike = -0.5')
    weights = []
    weights.append(float(input('Choose the utility value for \'lecturer\': ')))
    weights.append(float(input('Choose the utility value for \'time\': ')))
    weights.append(float(input('Choose the utility value for \'topic\': ')))
    weights.append(float(input('Choose the utility value for \'location\': ')))
    
    # here we have to retrieve courses of term {which_term}
    courses = [] 
    # take out the {finished_courses}
    # take out the {chosen_courses}
    deduced_courses = [] # after applying those constraints
    # each of those gets a utility value.
    courses_utilities = [] # list of utility values of the deduced courses
    
    """
    for x in courses:
        if x isTaughtBy preferences[4]: # (=lecturer)
            pref_lecturer = weights[0]
        else: pref_lecturer = 0
        
        if x hasTime preferences[5]:
            pref_time = weights[1]
        else: pref_time = 0 
        
        if x hasTopic preferences[6]:
            pref_topic = weights[2]
        else: pref_topic = 0
        
        if x hasLocation preferences[7]:
            pref_location = weights[3]
        else: pref_location = [0]
        
        
    courses_utilities.append(pref_lecturer+pref_time+pref_topic+pref_location)
    """
    highest_utility = courses_utilities.index(max(courses_utilities)) # finds index of the maximum utility sum
    first_recommendation = deduced_courses[highest_utility]
    

utility_function(extract_preferences()) 
    

# runQuery = SparqlQueries()
# runQuery.search()


    


    