# ZCS Python Core Library

This repository contains the core python library developed by Madness Lab Team at Zucchetti Centro Sistemi.

The library provides a `Logger` allowing the user to receive logging messages from Uvicorn and send them to Google Cloud.

```text

░▒▓████████▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░                                             
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                                                    
     ░▒▓██▓▒░░▒▓█▓▒░      ░▒▓█▓▒░                                                    
   ░▒▓██▓▒░  ░▒▓█▓▒░       ░▒▓██████▓▒░                                              
 ░▒▓██▓▒░    ░▒▓█▓▒░             ░▒▓█▓▒░                                             
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░                                             
░▒▓████████▓▒░░▒▓██████▓▒░░▒▓███████▓▒░                                              
                                                                                     
                                                                                     
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░       
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      
░▒▓███████▓▒░ ░▒▓██████▓▒░   ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      
░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      
░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      
░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░      
                                                                                     
                                                                                     
 ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░                                
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                                       
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                                       
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░                                  
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                                       
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                                       
 ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░                                
                                                                                     
                                                                                                                  
```

## Usage

### Requirements

The library doesn't require directly third party dependencies. This will let you install only the requirements needed by the utils you will effectively use.

### Use the library in your project

To use the library from ZCS repository you need to have a valid access.

Add the following line to the top of your `requirements.txt` file:

```bash
--extra-index-url https://europe-west1-python.pkg.dev/ai-accounting-405809/python/simple/
```

Then add the library `zcs-python-core` to the same file.

In your code, you can import and use the library like this:

```python
from zcs.core.exception import ZCSException
```

```python
from zcs.core.logger import Logger
```

## Local development

### Run library tests

If you want to run libraray tests against your local docker development environment, you can run:

```bash
./run.sh -t
```

### Run tests in a dist docker image

To be sure that anything is going the right way, you can run the library tests against a dist docker image. This will assure that anything is working properly in a fresh installed environment.

```bash
./run.sh -i
```

### Other commands and help

```bash
./run.sh -h
```

## Support

[Claudio Cavina](mailto:c.cavina@zcscompany.com)  
[Michele Mondelli](mailto:m.mondelli@zcscompany.com)
