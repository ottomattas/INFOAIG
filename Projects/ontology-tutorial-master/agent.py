from owlready2 import *
from pprint import pprint

# Ignore useless warnings
#warnings.filterwarnings("ignore")

## Optional: For debugging
owlready2.set_log_level(1) 

# Define a variable for the JRE location
# macOS Catalina
#java_home = ((subprocess.check_output(['which','java'])).decode('utf-8')).rstrip()
# macOS pre-Catalina
#java_home = "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"

# To load the reasoner, we need to load the JRE through the variable
owlready2.JAVA_EXE = "/usr/bin/java"

class Agent:

    def __init__(self, path="/Users/ottomattas/Documents/UU/INFOIAG/Project_2/ontology-tutorial-master/onto_pizza.owl"):
        # Load the desired ontology using the path file
        self.ontology = get_ontology(path)
        self.ontology.load()

        # Run the reasoner to obtain the inferences
        with self.ontology:
            sync_reasoner_pellet(infer_property_values=True)
        
        # Additional
        # Reference dictionaries between IRIs and given labels that might be usefull
        self.label_to_class = {ent.label[0]: ent for ent in self.ontology.classes()}
        self.label_to_prop = {prop.label[0]: prop for prop in self.ontology.properties()}

        self.class_to_label = {ent:ent.label[0] for ent in self.ontology.classes()}
        self.prop_to_label = {prop:prop.label[0] for prop in self.ontology.properties()}

        # Save types to help differentiate between classes and properties later on
        self.class_type = type(list(self.ontology.classes())[0])
        self.propery_type = type(list(self.ontology.properties())[0])
        
    def sanity_check(self):
        # Display the labels (the name given in Protege) of all the classes & properties present in the ontology 
        pprint(self.class_reference_dict)
        pprint(self.prop_reference_dict)
    
    def simple_queries(self):
        print("Query responses:")

        # Get all the classes with the label ending in "_topping"
        results = self.ontology.search(label="*_topping")
        class_results = [self.class_to_label[result] for result in results if type(result) == self.class_type]
        pprint(class_results)
        
        print("-" * 75)

        # Get all the classes that have "Vegetarian" as a superclass
        results2 = self.ontology.search(subclass_of=self.ontology.search_one(label="Vegetarian"))
        subclasses = [self.class_to_label[result] for result in results2 if type(result) == self.class_type]
        pprint(subclasses)
