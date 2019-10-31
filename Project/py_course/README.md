# intelligentagent.py

## Requirements
### Install Python 3
Currently tested on versions [3.7.5](https://www.python.org/downloads/release/python-375/) and [3.8.0](https://www.python.org/downloads/release/python-380/).

### Install required Python libraries
For this, we use `pip` as the standard package manager for Python. In case you want to learn more, visit the [project website](https://pypi.org/project/pip/).

#### **owlready2** for importing the Ontology
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade Owlready2
```
#### **rdflib** for querying the ontology
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade rdflib
```

## Running the code
As the ontology file is loaded from this repository when agent is ran, you can make sure it is available [here](https://github.com/ottomattas/INFOIAG/blob/master/Project/courseOntology.owl).

### 

```

```

## Known issues
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