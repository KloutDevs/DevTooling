<p align="center">
<img  src="https://i.imgur.com/OmX4SND.png" width="150px"/>
</p>
<p align="center">
    <img src="https://img.shields.io/pypi/v/devtooling-cli?label=Version&labelColor=gray&color=blue">
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

### Stage 1: Initial Development 

- [X] **Smart Project Detection**
  - [X] Automatic project type detection
  - [X] Support for multiple frameworks and technologies
  - [X] System of detection based on configurable rules

- [X] **Project Management**
  - [X] Watch folders for automatic project detection
  - [X] Low-level and deep scanning modes
  - [X] Quick project navigation
  - [X] Project type classification
  - [X] Project listing and organization

- [X] **Visualization of Structure**
  - [X] Interactive directory tree
  - [X] Smart filtering of files and folders
  - [X] Customizable visualization

### Stage 2: Integration with Git

- [ ] View repository status: View remaining changes, modified files, and untracked files.

- [ ] Manage branches: Create, delete, and switch between branches.

- [ ] View commit history: Visualize commit history and filter by date, author, file, or message.

- [ ] Generate .gitignore automatically: Generate a .gitignore file based on the current repository.

- [ ] Contribution statistics: View fully detailed statistics about contributions to the repository.

- [ ] Pull request statistics: View statistics about pull requests, including the number of open pull requests, closed pull requests, and merged pull requests.

- [ ] Initialice a new repository tool: Tool for creating new repositories.

### Stage 3: Dependencies Scanning

- [ ] Detect outdated dependencies: Detect outdated dependencies in the project and suggest updates.

- [ ] Detect vulnerabilities: Inspect the project for known vulnerabilities and suggest remediation. Integrated with tools like Snyk, OWASP, Dependency Check and GitHub Advisory Database.

- [ ] Analyze dependency sizes: Analyze the size of dependencies of the project and identify those that are large or unnecessary.

- [ ] Visualize dependency tree: Visualize the dependency tree of the project and identify potential issues.

### Stage 4: Code Analysis

- [ ] Count lines per language: Statistics about lines of code per programming language.

- [ ] Detect duplicated code: Identify duplicated code in the project and suggest ways to optimize it.

- [ ] Analyze complexity: Analyze the complexity of the project and identify potential issues.

- [ ] Suggestions for improvements: Suggest improvements to the project based on standards and best practices.

- [ ] Call Graph Analysis: Search for a function, find all places where it is called, and display execution paths. Generate diagrams with stack traces showing possible call chains.

### Stage 5: Management of Scripts

- [ ] Detect available scripts: Identify available scripts in the project and suggest ways to execute them.

- [ ] Integrated execution: Execute scripts directly from the command line.

- [ ] Customizable shortcuts: Create custom shortcuts for commonly used scripts.

- [ ] Concurrent task management: Monitor and manage multiple tasks running in parallel.

  

### Stage 6: Development Tools

- [ ] Generate components from templates: Create new components from pre-defined templates.

- [ ] Validate project structure: Check the adherence to conventions and best practices.

- [ ] Manage configurations: Edit and update common configuration files.

- [ ] Customizable templates: Create and manage custom templates for project generation.

  

### Stage 7: Docker Integration

- [ ] Analyze configurations: Detect and analyze configuration files for Docker.

- [ ] Optimize Dockerfiles: Suggest improvements to improve the efficiency of Dockerfiles

- [ ] Containers management: Commands for managing Docker containers.

- [ ] Validate best practices: Ensure configurations meet safety and security standards.

### Stage 8: Testing and Quality

- [ ] Run tests: Integration with testing frameworks for run tests easily and generate reports.

- [ ] Coverage reports: Show which parts of the code are covered by tests.

- [ ] Integration with linters: Identify and fix issues with code quality.

- [ ] Quality metrics: Resume of key metrics as bugs, vulnerabilities, and technical debts.


### Stage 9: Documentation

- [ ] Automatic documentation generation: Automatic generation of documentation from comments and code.

- [ ] Update README: Facilitate the creation and maintenance of full README files.

- [ ] Diagrams and visualizations: Generate diagrams and visualizations to better understand complex systems.

- [ ] Documentation templates: Offer customizable templates of documentation for differents types of projects.

  

### Stage 10: Manage of the environment

- [ ] Environment management:  Centralize and manage sensitive variables.

- [ ] Configuration validation: Check for consistency and detect inconsistencies.

- [ ] Environment comparison: Identify differences between configurations.

- [ ] Configuration templates: Facilitate the creation of standard configuration files.


## 🛠️ Installation

### Option 1: Using the Executable (Outdated)

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

venv\Scripts\activate  # Windows

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

#Define the rules to detect project types and their dependencies,
#and the files and directories to ignore based on the project type.

config/detection_rules.json

```

## 🤝 Contributing

The contributions are welcome. Please read the contribution guide before starting.

## 🧪 Testing

### Coverage Status
[![Coverage Status](https://img.shields.io/badge/Coverage-93%25-success)](https://github.com/KloutDevs/DevTooling)

| Module          | Coverage | Status     |
|----------------|----------|------------|
| Core           | 98%      | ✅ Complete |
| Features       | 93%      | ✅ Complete |
| Utils          | ~65%     | 🟡 In Progress |

### Test Suite Structure
```python
tests/
├── core/
│   └── test_detector.py       # Project type detection tests
├── features/
│   ├── test_structure.py      # Directory visualization tests
│   └── test_projects.py       # Project management tests
└── utils/
    ├── test_config.py         # Configuration handling tests
    └── test_logger.py         # Logging system tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/core/test_detector.py

# Run with coverage report
pytest --cov=devtooling tests/
```

### Test Documentation
For detailed information about testing patterns and implementation, please refer to our [Testing Documentation](https://github.com/KloutDevs/DevTooling/blob/master/docs/TESTING.md).

### Contributing to Tests

When adding new features, please ensure:

* Write tests for new functionality
* Maintain or improve current coverage
* Follow existing test patterns
* Update test documentation

For more details about contributing to tests, see our [Contributing Guidelines](https://github.com/KloutDevs/DevTooling/blob/master/docs/CONTRIBUTING.md).

## 📜 License

MIT License.

## 🔄 Project Status  

Developed with ❤️ by [KloutDevs](https://github.com/KloutDevs).