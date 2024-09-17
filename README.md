
<span style="color: magenta; font-size: 20px;">·.•°•.·.✧ ✦ 🧚 ✦</span> 
# Navi-Assistant

Navi is an OpenAI assistant manager which allows you to quickly create assistants with useful tools and query them.

## Features
### Global & Local Assistants
Navi creates a "global" and "local" assistants. The global assistant is a system-wide assistant, whereas local assistants are perticular to a specific directory.  
When using Navi, the global assistant is used by default, when there is not an local Navi configuration in the current directory.  

This lets users create specific assistant configurations for any work/project.

### Easy Assistant Tooling
Navi configurations (both global and local) can be setup with tools to enhance the capability of the assistant. Sets of tools are managed via Github repositories (e.g.: https://github.com/NixonInnes/Navi-Assistant-Tools-Linux).  
Tools are simply added by cloning the repository into the assistants tools directory.  

This lets users create managed sets of tools, that are also shareable.

### Vector File Store Management
Navi can be configured to include specific directories and file extensions to sync with a vector file store associated to the assistant. 

A simple `sync` command lets users keep relevent files up to date for the assistant to search.

## Installation

### Requirements
 - Python 3.12+
 - curl
 - git

 ### via Script
 > TODO: Add some sane mechanism to provide relevent `install.sh` script  
 You can automatically setup Navi using the `install.sh` script:
 ```bash
 curl -fsSL https://raw.githubusercontent.com/NixonInnes/Navi-Assistant/v0.1.2/install.sh | bash
 ```

 ### From a Release
 You can install a specific release by heading to the releases page: https://github.com/NixonInnes/Navi-Assistant/releases

Download the specific release `.whl` file.

Create a virtual environment for Navi:  
```bash
python3 -m venv venv
```

Install the `.whl` into the virtual environment:
```bash
venv/bin/pip install path/to/navi_assistant-<version>-py3-none-any.whl
```

Add a bash script into a local user bin (i.e. `${HOME}/.local/bin`) similar to:
```bash
path/to/venv/bin/python -m navi_assistant "$@"
```

Run the install module:
```bash
path/to/venv/bin/python -m navi_assistant.install
```

### From Source
> TODO: Add better details
- clone repo
- build wheel
- follow "from Release" steps

## Basic Usage
> TODO: Add explanation & example 

### Querying an Assistant
```bash
navi ask ...
```

### Creating a Local Assistant
```bash
navi init
```

### Show Current Navi Configuration
```bash
navi info
```

### Update Navi Configuration
```bash
navi config model gpt-4o-mini
```

### Adding Tools
```bash
navi tools pull NixonInnes/Navi-Assistant-Tools-Linux
```

### Setting Up Files for Upload
```bash
navi files set ---dir src ---dir test ---file-ext py
```

### Syncing files
```bash
navi files sync
```

## Full Documentation
For a full listing of the CLI commands and options, please see: [Docs](docs/index.md)