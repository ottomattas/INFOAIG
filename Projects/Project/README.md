# courseplanner.py

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