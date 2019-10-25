package main;

import java.nio.file.Files;
import java.nio.file.Paths;

import org.semanticweb.HermiT.Reasoner;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.io.StringDocumentSource;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassExpression;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLEntity;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.util.ShortFormProvider;
import org.semanticweb.owlapi.util.SimpleShortFormProvider;

public class Agent {

	public static void main(String[] args) throws Exception{
        String onto = new String(Files.readAllBytes(Paths.get("../courseOntology.owl")), "UTF-8");
        // Load an example ontology.
        final OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        final OWLOntology ontology = manager
                .loadOntologyFromOntologyDocument(new StringDocumentSource(onto));
        
        // We need a reasoner to do our query answering
        // This example uses HermiT: http://hermit-reasoner.com/
        OWLReasoner reasoner = new Reasoner.ReasonerFactory().createReasoner(ontology);
        // We also need a short form provider, to get the names of objects in the ontology from their IRIs
        ShortFormProvider shortFormProvider = new SimpleShortFormProvider();
        
        // initialise a DL Query Engine, to query the ontology directly from here.
        DLQueryEngine engine = new DLQueryEngine(reasoner, shortFormProvider);

        // Test print
        // This also shows how querying is done; we need the engine and the shortformprovider for it
    	String query = "course and isTaughtBy value LECTURER_B";
        for (OWLEntity entity : engine.getInstances(query, false)) {
        	System.out.println(shortFormProvider.getShortForm(entity));
        }
        
        // System.out.println(dlQueryPrinter.getInstances("course and isTaughtBy value LECTURER_B"));
            
	}
}

