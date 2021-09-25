# courseplanner.py

[Assignment description](#description) is given below the [install guide](#requirements).

## Requirements
### Install Python 3
Currently tested on versions [3.7.5](https://www.python.org/downloads/release/python-375/) and [3.8.0](https://www.python.org/downloads/release/python-380/).

### Install required Python libraries
For this, we use `pip` as the standard package manager for Python. In case you want to learn more, visit the [project website](https://pypi.org/project/pip/). 
We use `sudo` with the `-H` flag which makes sure we have all the environment variables loaded from the user _HOME_. Also, we call `pip` via the proper Python implemetation, using the `-m` flag.

#### **owlready2** for importing the ontology
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade owlready2
```
#### **rdflib** for querying the ontology
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade rdflib
```
#### **numpy** for the utility function
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade numpy
```

## Running the code
As the ontology file is loaded from this repository when agent is ran, you can make sure it is available [here](https://github.com/ottomattas/INFOIAG/blob/master/Project/courseOntology.owl).
```
python3 intelligentagent.py
```

## Known issues

### Python and TLS
To load the ontology file from an online repository, we need to instruct Python to get it for us. Under some circumstances, Python might have trouble retrieving it due to issues with TLS/SSL Root Certificates.
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:749)
```
This can mean that the collection of Root Certificates that Python has included is outdated and/or the certificate needed is not present in the collection at all.

- In case you installed Python via an installer, you should check the source folder for a separate file `Install Certificates.command` which is meant for updating the Root Certificates in the implementation. [Reference](https://bugs.python.org/issue29480)
- In case you use pip, you can upgrade the relevant library:
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade certifi
```

### JRE
Depending on your OS, our program might not find the path to your Java Runtime Environment. You can clear the error by adjusting the `java_home` variable at the head of the program. Some options are already presented while hardcoding the path also works.
```
# Define a variable for the JRE location
# macOS Catalina
java_home = ((subprocess.check_output(['which','java'])).decode('utf-8')).rstrip()
# macOS pre-Catalina
#java_home = "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"
```

## ASSIGNMENT: Intelligent Agents Project 2019

### Description
You will design and implement a personal assistant agent that will help a new master student choose courses. The student might have certain courses already in mind (e.g., definitely take Multiagent Systems), preferences for type of courses she would like to take (e.g., follow courses that require logic), preferences for courses to avoid based on a property (e.g., never take a course on Friday or never take a course with a final exam) as well as obligations to follow (e.g., each student must take Methods of AI Research course).

The agent should take into account the student's preferences and obligations and generate a schedule for the student. The schedule should be for a few semesters. When doing so, the agent should use knowledge about the program, the courses, and the user and reason on this knowledge to make choices. Ideally, the agent should be able to provide explanations as to why each course is chosen.

You should be able to show how the agent produces schedules for different users.

Details of the masters program:

- [Course] Each course is taught by at least one lecturer. The course is taught on exactly two different days. Each lecturer teaches at most one course every period. Each course is on a set of topics (e.g., operation systems or description logics) and uses exactly one research methodology (e.g., theory or simulation). A course might be a prerequisite for a course, which might be a prerequisite for another course. A course is considered similar to another course if there is an overlap on topics and the same research methodology is used. When more topics overlap, the similarity is higher.
- [Topic] Topics are organized in a hierarchy, e.g., database systems is a subtopic of systems, which is a subtopic of computer systems. Two topics could be disjoint or have overlaps.
- [Student] A student might prefer (not) to take a course by a certain lecturer, or on a certain day, or on a certain topic. At any given period, a student can take at least two and at most three courses. A student cannot register for a course more than once. A student can take a course only if she has taken the prerequisite (if there is one) or a course similar to a prerequisite. When a student has an option between two courses that are equally preferable, the student would like to take a course that her friend takes.

### Tasks
- Design an ontology: Your ontology should contain the information above as much as possible. Additionally, think through two other main concepts and their constraints and add them to the ontology. You should have at least 10 topics, 5 research methodologies, 15-20 courses to choose from, and 3-5 students. Populate the other concepts you choose as appropriate.
- Define scenarios: Create "stories" that correspond to real life usage of your agent. For example, "Alice is a student who has already taken Intelligent Agents and Probabilistic Reasoning courses. She would like to take a course similar to Intelligent Agents. She would rather not come to the university on Fridays." Make sure that these scenarios are not simple database look-ups but actually require reasoning, such as finding similar courses, understanding a course is a prerequisite through a transitive property, understanding that a course is not taught by a particular lecturer because she is already teaching another course in that period, etc.
For each such scenario, explain how you expect your agent to act. That is, what are the possible schedules that can be produced? Is one preferable over another?
- Implement your ontology using Protégé: Make sure you study existing ontologies first. Develop your ontology incrementally by adding concepts, data properties, and object properties. Doing it incrementally will help you debug in case you make mistakes. You should have at least one transitive, one symmetric, one functional and one inverse functional object property.
- Write DL queries: Decide on the information needed for your agent to make decisions and formulate them as queries. For example, you might need to find courses that are taught by Pinar Yolum and are similar to Multiagent Systems. BUT, note that this might be information that is not included as a fact in the ontology but is inferred through other information. Write the queries needed to extract these from the ontology. Try your queries in the Protégé DL Tab to make sure they return the results that you expect.
- Design an agent: Various agent architectures will be covered in the first lectures, though you can choose a different architecture available in the literature or combine existing ones as you see fit. Depending on your agent architecture, design each component and be as precise as possible. For example, if you have a goal-based agent, think through what actions the agent has, what are the effects, what is your goal representation, what are possible goals. Or, if you have a utility-based agent, design a utility function.
- Develop your agent: You are free to use any programming language you like. However, generally Java and Python have the most support to work with ontologies. You can use existing APIs, such as OWL API, to access the ontology and execute the DL queries you have written.
Evaluate your agent: - As discussed in class, the agent should have a performance metric using which you can assess how well it works. Run your scenarios on the agent and check how well the agent achieves the target results. If some of the results are not as expected, discuss why that might be the case.
- Bonus: Design a trust function for your agent, which would be used to recommend courses among friends. That is, after a student takes a course, she assigns an evaluation to the course. Agents can consult other agents that they trust to ask about course evaluations. Note that not all evaluations will be compatible. A student who has done well in a course would assign a positive evaluation, whereas a student who has done might not. Hence, the agent needs a trust function to decide whose recommendation to take. To facilitate this, you can implement any of the trust methods that will be covered in class or you can come up with your own.
- Bonus: To make your agent more realistic, you can use auxiliary information about the user and factor that into your reasoning. For example, when scheduling courses, you can read a user's schedule from Google Calendar to understand that the student is already full on Fridays. Or, in order to interact with the user, you can use Google Assistant. Feel free to suggest other APIs relevant to your agent. But, only work on the bonus if you have finished the other parts. It is not meaningful to have an insufficient ontology but read information from Google calendar.
- Report and presentation: Be specific in explaining what you have done. Specify clearly which agent architecture you have used, how you have designed its various components, why this was better than alternative architectures. Describe your ontology and its usage by the agent. Provide a few scenarios to demonstrate how your agent uses the ontology for reasoning.
- Version 4.9.2019
