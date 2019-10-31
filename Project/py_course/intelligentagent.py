#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Intelligent Agents
# Team project - coursePlanner agent
# Tjalle Galama, Ernö Groeneweg, Otto Mättas, Shaoya Ren, Vincent de Wit

from owlready2 import *
from rdflib import *
import numpy as np

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
        # print(response)
        return response
    
runQuery = SparqlQueries()
ontology_dictionaries = runQuery.search() 
# print(ontology_list)

def intersect(lst1, lst2): # to intersect two lists
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def extract_preferences():
    which_term = int(input('For which term (1/2/3/4) do you want to receive a recommendation? '))
    amount_of_courses_to_be_found = int(input('How many courses to you want to get recommended? (1/2/3) '))
    print('')
    print('For the following questions, press enter if you have no answer.')
    finished_course = input('Have you already finished a course in term {}? If yes type the course code. '.format(which_term))
    finished_courses = []
    finished_courses.append(finished_course)
    if len(finished_course) >= 1: # meaning the answer is not empty
        other_course = input('And maybe another one? Else press enter to continue. ')
        if other_course : # again meaning the answer is not empty
            finished_courses.append(other_course)
    elif finished_course == []:
        finished.course.append('empty')
    chosen_courses = [] 
    if which_term == 1:
        if intersect(finished_courses,['INFOMAIR']) == []:
            chosen_courses.append('INFOMAIR') # mandatory course 
            print('You have to take INFOMAIR. It is added as a chosen course.')
    if which_term == 3 and intersect(finished_courses,['WBMV05003']) == []:
        chosen_courses.append('WBMV05003') # mandatory course 
        print('You have to take WBMV05003. It is added as a chosen course.')
    elif chosen_courses == []:
        chosen_courses.append('empty')
    
    chosen_course = input('Have you already chosen a course for term {}? If yes type the course code. '.format(which_term))
    if len(chosen_course)>1:
        if intersect(chosen_course,chosen_courses) == []: # so we don't get duplicates 
            # here we could build in the isPrerequisiteFor relation,
            # which would block you to choose a course if you haven't fnished
            # the prerequisite + give some explanation 
            chosen_courses.append(chosen_course)
            amount_of_courses_to_be_found -= 1
            
            if amount_of_courses_to_be_found != 0:
                chosen_course = input('And maybe you already chose another one? ')
                if chosen_course:
                    if intersect(chosen_course,chosen_courses) == []:
                        chosen_courses.append(chosen_course)
                        amount_of_courses_to_be_found -= 1

    print('')
    print('The available lecturers are LECTURER_X with X in {A,B, .... , H,I}')
    lecturer_preference = input('Do you prefer or dislike a certain teacher? ')
    print('')
    print('The available time-slots are: SLOT_A, SLOT_B, SLOT_C, SLOT_D')
    time_preference = input('Do you prefer or dislike a certrain timeslot? ')
    print('')
    print('The available topics are:')
    print('[ADVANCED_ALGORITHM, AGENTS_FOUNDATION, AGENTS_COMMUNICATION,'
            'DESCRIPTION_LOGIC, ONTOLOGY, REASONING, MULTI_AGENTS,'
            ' CP_THEORY, FIRST_ORDER_LOGIC, NL_PROCESSING_SKILLS, '
            'PROGRAMMING_SKILLS, LOGIC_FORCOMPUTION, CP_RESEARCHMETHODS, ' 
            'DATA_PROCESSING, AI_PSYCHOLOGY, NL_THEORY, AI_PHILOSOPHY]')
    topic_preference = input('Do you prefer or dislike a certain topic? ')
    print('')
    print('The available locations are: [KBG_PANGEA, RUPPERT_D, BOL_1.138, '
                                        'BOL_3.100, RUPPERT_042, RUPPERT_115]')
    location_preference = input('Do you prefer or dislike certain location? ')
    print('')
    print('These are your friends: ANNE, BERT, JOHNNY, JOSIE, TRACY')
    friend_preference = input('Do you want to take the courses that a friend'
                              ' chooses into account? ')
    friends = [] 
    if friend_preference:
        friends.append(friend_preference)
        other_friend = input('One more friend? ')
        if other_friend:
            friends.append(other_friend)
    print('')
            
    preferences = []
    preferences.append(which_term)
    preferences.append(amount_of_courses_to_be_found)
    preferences.append(finished_courses)
    preferences.append(chosen_courses)
    preferences.append(lecturer_preference)
    preferences.append(time_preference)
    preferences.append(topic_preference)
    preferences.append(location_preference)
    preferences.append(friends)

    return preferences
    
def utility_function(preferences):
    print('You may set utility values on each constraint. ')
    print('heavy preference = 1, medium = 0.5, no preference = 0, dislike = -0.5')
    weights = []
    weights.append(float(input('Choose the utility value for \'lecturer\': ')))
    weights.append(float(input('Choose the utility value for \'time\': ')))
    weights.append(float(input('Choose the utility value for \'topic\': ')))
    weights.append(float(input('Choose the utility value for \'location\': ')))
    weights.append(float(input('Choose the utility value for \'friend\': ')))

    
    # here we have to retrieve courses of term {which_term}
    which_term = int(preferences[0])
    courses = [] 
    # dictionairies in the ontology_disctionaries look like:
    # {'s': 'http://webprotege.stanford.edu/INFOMDM', 'p': 'type', 'o': 'term1_course'}
    
    # translate dictionary d to a list
    ontology_list = []
    for i in range(0,len(ontology_dictionaries)):
        d = ontology_dictionaries[i]
        templist = [] # temporary
        for k, v in d.items():
            templist.append(k)
            templist.append(v)
        ontology_list.append(templist)
        
    term_course = 'term{}_course'.format(which_term)
    
    for i in range(0,len(ontology_list)):
        for j in range(0,len(ontology_list[i])):
            if ontology_list[i][j][:31] == 'http://webprotege.stanford.edu/':
                replace = ontology_list[i][j][31:]
                ontology_list[i][j] = replace
        if ontology_list[i][5] == term_course:
            if ontology_list[i][3] != 'onClass':
                if intersect(courses,[ontology_list[i][1]]) == []:
                    courses.append(ontology_list[i][1])
    # print(ontology_list)                
    print('')   
    print('The available courses in your chosen term are:')
    print(courses)
    print('')
    
    # take out the {finished_courses}
    # if len(preferences[2]) >= 1: 
    finished = intersect(preferences[2],courses)
    for i in finished:
        courses.remove(i)
    print('The finished courses are taken out:') # grounding
    print(courses)
    print('')
    
    # take out the {chosen_courses}
    if len(preferences[3])>=1:
        chosen = intersect(preferences[3],courses)
        for i in chosen:
            courses.remove(i)
        print('The already chosen courses are taken out:')
        print(courses)
        print('')
        
    # each of the remaining courses gets a utility value.
    courses_utilities = [] # list of utility values of the deduced courses
    # elements of this list will soon look like:
    # [coursecode,pref_lecturer,pref_time,pref_topic,pref_location,pref_friend]
    for j in range(0,len(courses)):
        x = courses[j]
        courses_utilities.append([x])
        for i in range(0,len(ontology_list)):
            # seek the course code + the requested lecturer ( = preference[4] )
            if intersect([preferences[4],x],ontology_list[i]) == [preferences[4],x]: 
                pref_lecturer = weights[0]
                courses_utilities[j].append(pref_lecturer)
                break
        if courses_utilities[j] == [x]:
            courses_utilities[j].append(0)
    
    for j in range(0,len(courses)):
        x = courses[j]
        for i in range(0,len(ontology_list)):
            # seek the course code + the requested time slot 
            if intersect([preferences[5],x],ontology_list[i]) == [preferences[5],x]: 
                pref_time = weights[1]
                courses_utilities[j].append(pref_time)
                break
        if len(courses_utilities[j]) == 2:
            courses_utilities[j].append(0)

    # the following six lines merely served to access the KB 
    available_topics = [] 
    # unfortunately only the instances and not subclasses themselves 
    for i in range(0,len(ontology_list)):
        if ontology_list[i][3] == 'covers':
            if intersect(available_topics,[ontology_list[i][5]]) == []:
                available_topics.append(ontology_list[i][5])
    
    for j in range(0,len(courses)):
        x = courses[j]
        for i in range(0,len(ontology_list)):
            # seek the course code + the requested topic
            if intersect([preferences[6],x],ontology_list[i]) == [preferences[6],x]: 
                pref_topic = weights[2]
                courses_utilities[j].append(pref_topic)
                break
        if len(courses_utilities[j]) == 3:
            courses_utilities[j].append(0)

    # the following five lines merely served to access the KB 
    available_locations = []
    for i in range(0,len(ontology_list)):
        if ontology_list[i][3] == 'http://webprotege.stanford.edu/isTaughtIn':
            if intersect(available_locations,[ontology_list[i][5]]) == []:
                available_locations.append(ontology_list[i][5])
    
    for j in range(0,len(courses)):
        x = courses[j]
        for i in range(0,len(ontology_list)):
            # seek the course code + the requested location
            if intersect([preferences[7],x],ontology_list[i]) == [preferences[7],x]: 
                pref_location = weights[3]
                courses_utilities[j].append(pref_location)
                break
        if len(courses_utilities[j]) == 4:
            courses_utilities[j].append(0)
       
    for j in range(0,len(courses)):
        x = courses[j]
        if len(preferences[8]) == 1:
            for i in range(0,len(ontology_list)):
                # seek the course code + the requested friend
                if intersect([preferences[8],x],ontology_list[i]) == [preferences[8],x]: 
                    pref_friend = weights[4]
                    courses_utilities[j].append(pref_friend)
            if len(courses_utilities[j]) == 5:
                courses_utilities[j].append(0)
        if len(preferences[8]) == 2:
            friend1 = preferences[8][0]
            pref_friend1 = 0 
            for i in range(0,len(ontology_list)):
                if intersect([friend1,x],ontology_list[i]) == [friend1,x]: 
                    pref_friend1 = weights[4]
                    break
            friend2 = preferences[8][1]
            pref_friend2 = 0
            for i in range(0,len(ontology_list)):
                if intersect([friend2,x],ontology_list[i]) == [friend2,x]: 
                    pref_friend2 = weights[4]
                    break
            courses_utilities[j].append(pref_friend1 + pref_friend2)    
        if len(courses_utilities[j]) == 5:
            courses_utilities[j].append(0)
    ''' 
    for j in range(0,len(courses)):
        x = courses[j]
        requested_is_course_similar_to = preferences[9]
        for i in range(0,len(ontology_list)):
            if intersect([preferences[9],x],ontology_list[i]) == [preferences[9],x]: 
                pref_similar = temp_weight = 5
                courses_utilities[j].append(pref_similar)
    
    '''
    print('What follows is an overview (the \'world-states\') of the assigned' 
          ' utility values:' )
          
    overview_values = ['course','U_teacher','U_time','U_topic',
                       'U_location', 'U_friend']
    print('')
    courses_utilities.insert(0,overview_values)
    print(np.array(courses_utilities))
    print('')
    
    summed_utility = []
    for j in range(1,len(courses_utilities)):
        summed = 0
        for i in range(1,6):
            summed += float(courses_utilities[j][i])
        summed_utility.append(summed)
    
    sorted_sums = sorted(summed_utility, reverse = True)
    max1 = summed_utility.index(sorted_sums[0])
    # if sorted_sums[0] != sorted_sums[1]:
    if len(sorted_sums)>1:
        max2 = summed_utility.index(sorted_sums[1])
        if max2 == max1:
            summed_utility.pop(max1)
            summed_utility.insert(max1,-10)
            max2 = summed_utility.index(sorted_sums[1])
    if len(sorted_sums) > 2:
        max3 = summed_utility.index(sorted_sums[2])
        if max3 == max2:
            summed_utility.pop(max2)
            summed_utility.insert(max2,-10)
            max3 = summed_utility.index(sorted_sums[2])

    if preferences[3] != ['empty']:
        if len(preferences[3]) == 2:
            print('Your first recommendation is {}'.format(preferences[3][0]))
            print(' - because this course is mandatory.')
            print('Your second recommendation is {}'.format(preferences[3][1]))
            print(' - because this course was already chosen.')
            print('Your third recommendation is {}'.format(courses[max1]))
            
        if len(preferences[3]) == 1:
            print('Your first recommendation is {}'.format(preferences[3]))
            print(' - because this course was already chosen or is mandatory.')
            y = float(preferences[1])
            if y > 1:
                print('The second recommendation is the course: {}'.format(courses[max1]))
            if y > 2:
                print('The third recommendation is the course: {}'.format(courses[max2]))
    else:       
        print('Your first recommendation is {}'.format(courses[max1]))
        y = float(preferences[1])
        if y > 1:
            print('The second recommendation is the course: {}'.format(courses[max2]))
        if y > 2:
            print('The third recommendation is the course: {}'.format(courses[max3]))
        
utility_function(extract_preferences()) 

restart_or_not = input('Do you want to run through the program again for '
                       'another term? YES / NO ')
if restart_or_not == 'YES':
    utility_function(extract_preferences())

# the agent should take the history into account,
# such as noting the chosen courses could be PreRquisite for others etc.


# def evaluation_metric(preferences):
    
