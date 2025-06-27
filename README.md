# ZCS Python Core Library

This repository contains the core python library developed by Madness Lab Team at Zucchetti Centro Sistemi.

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
from zcs.core.exception import ZcsException
```

```python
from zcs.core.logger import ZcsLogging
```

## Local development

See [Local Development](./docs/LOCAL_DEVELOPMENT.md).

## Support

[Claudio Cavina](mailto:c.cavina@zcscompany.com)  
[Michele Mondelli](mailto:m.mondelli@zcscompany.com)
