<p align="center">
<img  src="https://i.imgur.com/OmX4SND.png" width="150px"/>
</p>
<p align="center">
    <img src="https://img.shields.io/badge/version-0.2.6-blue?style=flat">
    <img src="https://img.shields.io/pypi/dm/devtooling-clistyle=flat&logo=PyPi">
    <img src="https://img.shields.io/badge/licencia-MIT-green?style=flat">
    <img src="https://img.shields.io/badge/status-alpha-orange?style=flat">
    <img src="https://img.shields.io/badge/Python-3.7%2B-blue?style=flat&logo=python">
</p>

<h1 align="center">DevTooling CLI</h1>
<p align="center">
DevTooling CLI is an advanced command-line tool for project analysis and development management.
</p>
 
<p align="center">
  <img src="https://i.imgur.com/GmYPHOS.gif" width="500">
</p>


## 🚀 Features

  

-  **Smart Project Detection**

- Automatic project type detection

- Support for multiple frameworks and technologies

- System of detection based on configurable rules

  

-  **Project Management**

- Watch folders for automatic project detection

- Low-level and deep scanning modes

- Quick project navigation

- Project type classification

- Project listing and organization

  

-  **Visualization of Structure**

- Interactive directory tree

- Smart filtering of files and folders

- Customizable visualization

  

## 🎯 Roadmap

  

### Stage 1: Dependencies Scanning

- [ ] Detect outdated dependencies

- [ ] Detect vulnerabilities

- [ ] Analyze dependency sizes

- [ ] Visualize dependency tree

  

### Stage 2: Integration with Git

- [ ] View repository status

- [ ] Manage branches

- [ ] View commit history

- [ ] Generate .gitignore automatically

- [ ] Contribution statistics

- [ ] Pull request statistics

- [ ] Initialice a new repository tool

  

### Stage 3: Code Analysis

- [ ] Count lines per language

- [ ] Detect duplicated code

- [ ] Analyze complexity

- [ ] Project statistics

- [ ] Suggestions for improvements

  

### Stage 4: Gestión de Scripts

- [ ] Detect available scripts

- [ ] Integrated execution

- [ ] Customizable shortcuts

- [ ] Concurrent task management

  

### Stage 5: Development Tools

- [ ] Generate components from templates

- [ ] Validate project structure

- [ ] Manage configurations

- [ ] Customizable templates

  

### Stage 6: Docker Integration

- [ ] Analyze configurations

- [ ] Optimize Dockerfiles

- [ ] Containers management

- [ ] Validate best practices

  

### Stage 7: Testing and Quality

- [ ] Run tests

- [ ] Coverage reports

- [ ] Integration with linters

- [ ] Quality metrics

  

### Stage 8: Documentación

- [ ] Automatic documentation generation

- [ ] Update README

- [ ] Diagrams and visualizations

- [ ] Documentation templates

  

### Stage 9: Gestión de Entorno

- [ ] Environment management

- [ ] Configuration validation

- [ ] Environment comparison

- [ ] Configuration templates

  

## 🛠️ Installation

  

### Option 1: Using the Executable (Recommended)

Download the latest release for your operating system:

  
  

```bash

# Windows

Download  devtool.exe  from  the  latest  release

  

# Linux/MacOS

Download  devtool  from  the  latest  release

chmod  +x  devtool  # Make it executable

```

  

### Option 2: Using pip

  

```bash

# Install globally

pip  install  devtooling-cli

  

# Or install in a virtual environment

python  -m  venv  .venv

source  .venv/bin/activate  # Linux/MacOS

.venv\Scripts\activate  # Windows

pip  install  devtooling-cli

```

  

### Option 3: From Source

  

```bash

# Clone the repository

git  clone  https://github.com/KloutDevs/DevTooling.git

cd  DevTooling

  

# Install dependencies

pip  install  -r  requirements.txt

  

# Install the package

pip  install  .

```

  

## 📖 Use

  

### Interactive Mode

  

```bash

# Launch the interactive CLI

devtool

  

# Or if installed from source

python  -m  devtool

```

  

### Command Line Mode

  

*Structure Visualization*

  

```bash

# Show project structure with different modes

devtool  structure  --mode  MODE  PATH

  

# Examples:

devtool  structure  --mode  automatic  ./my-project

devtool  structure  --mode  manual  .

devtool  structure  --mode  complete  /path/to/project

```

  

*Projects Management*

  

```bash

# Add a folder to watch for projects

devtool  projects  --folders-add  PATH

# Add with low-level scanning (only root and first level)

devtool  projects  --folders-add  PATH  --low-level

  

# Remove a watched folder

devtool  projects  --folders-remove  PATH

  

# List all watched folders and detected projects

devtool  projects  --list

  

# Refresh projects in watched folders

devtool  projects  --refresh-folders

  

# Navigate to a project

devtool  projects  --go  PROJECT_NAME

# or use the shortcut

devtool  go  PROJECT_NAME

```

  

## 📝 Configuration

  

The tool will automatically detect your project type and apply appropriate filters. You can customize the detection rules by modifying:

  

```bash

#Define the rules to detect project types and their dependencies, #and the files and directories to ignore based on the project type.

  

config/detection_rules.json

```

  

## 🤝 Contributing

  

The contributions are welcome. Please read the contribution guide before starting.

  

## 📜 License

  

MIT License.

  

## 🔄 Project Status

  

Developed with ❤️ by KloutDevs.