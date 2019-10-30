# Python implementation

## Requirements
### Install Python 3.8
https://www.python.org/downloads/release/python-380/

### Run Certificates.command in the installation folder or upgrade via pip to be able to handle TLS certificates properly
#### Reference: https://bugs.python.org/issue29480
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade certifi
```

### Install **owlready2** Python module for importing the Ontology
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade Owlready2
```

### Install **rdflib** for querying the ontology
```
sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade rdflib
```