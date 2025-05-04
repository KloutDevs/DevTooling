# DevTooling CLI Testing Documentation

This document outlines the testing strategy for DevTooling CLI, including different types of tests, their coverage, and use cases.

## 🎯 Testing Goals

- Ensure the precise and accurate detection of project types
- Validate the correct inheritance of project detection rules
- Verify the funcionality of the command-line interface
- Guarantee the persistence of correctly configured settings
- Check the proper handling of errors and exceptions

## 📋 Test Types

### 1. Core Tests
#### ProjectDetector (`test_detector.py`)
- [X] Detection of project type
  - Verification of correct detection of common projects (React, Node, Python, etc.)
  - Validation of project detection priorities
  - Checking handling of empty/invalid directories

- [X] Detection of multiple technologies
  - Verification of detection of included technologies
  - Validate detection hierarchy
  - Checking inclusion rules

- [X] Ignore System
  - Verificate ignore patterns for project types
  - Validate inheritance of ignore rules
  - Check special cases

### 2. Features Tests
#### TreeVisualizer (`test_structure.py`)
- [X] Structure Visualization
  - Verify correct tree generation
  - Validate directory filtering
  - Check visualization modes (automatic, manual, complete)

#### ProjectManager (`test_projects.py`)
- [] Folder Management
  - Verify add/remove folders
  - Validate project scanning
  - Check configuration persistence

- [ ] Project Navigation
  - Verify project navigation
  - Validate search by name/path
  - Check error handling

#### CLI Arguments (`test_cli.py`)
- [ ] Argument Processing
  - Verify command parsing
  - Validate options and flags
  - Check error handling

### 3. Utils Tests
#### Configuration (`test_config.py`)
- [X] Configuration Management
  - Configuration Loading
    - Load detection_rules.json
    - Load projects.json
    - Handle missing files
    - Handle invalid JSON
  - Configuration Saving
    - Basic save operations
    - Directory creation
    - Permission handling
  - Path Management
    - Development environment configuration
    - Production environment configuration
    - Handle non-existent projects
    - Package resource loading
    - Nested directory creation
  - Production Environment
    - Mock MEIPASS handling
    - Rules copying in production
    - Package resource fallback

#### Logger (`test_logger.py`)
- [ ] Logging System
  - Verify log configuration
  - Test log levels
  - Check file handlers

#### File Handler (`test_file_handler.py`)
- [ ] File Operations
  - Test directory creation
  - Test file listing
  - Test file size calculations

## 🔍 Testing Methodology

1. **Unit Tests** ✅
   - Using `pytest` as main framework
   - Implementation of fixtures for common cases
   - File system mocking when necessary

2. **Integration Tests** 🟡
   - Component interaction verification
   - Complete flow testing
   - Real use case validation

3. **System Tests** 🟡
   - CLI testing in different environments
   - Installation and configuration validation
   - User experience verification

## 📊 Coverage Status

| Module          | Coverage | Status     | Previous |
|----------------|----------|------------|----------|
| Core           | 98%      | ✅ Complete | 98%     |
| Features/Tree  | 93%      | ✅ Complete | 93%     |
| Utils/Config   | 88%      | ✅ Complete | 65%     |
| CLI Arguments  | 18%      | 🟡 Progress | 0%      |
| Project Manager| 17%      | 🟡 Progress | 0%      |
| UI Components  | 0%       | ❌ Pending  | 0%      |

## 🚀 Test Execution

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_detector.py
pytest tests/test_structure.py

# Run with coverage
pytest --cov=devtooling tests/

# Generate coverage report
pytest --cov=devtooling tests/ --cov-report=html
```

## 📝 Test Conventions

1. Test Naming:

```bash
def test_should_detect_react_project():
def test_should_handle_invalid_path():
def test_should_fallback_to_package_resources():
```

2. Organization

- One test file per module
- Shared fixtures usage
- Clear test case documentation

```bash
tests/
├── core/
│   └── test_detector.py
├── features/
│   ├── cli/
│   │   ├── test_arguments.py
│   │   └── test_handlers.py
│   ├── projects/
│   │   └── test_manager.py
│   └── tree/
│       └── test_structure.py
└── utils/
    ├── test_config.py
    ├── test_logger.py
    └── test_file_handler.py
```

3. Assertions

- Use descriptive assertions
- Clear error messages
- Complete state validation

### Latest Updates

#### Completed Components ✅
1. **Core Tests - ProjectDetector (98%)**
   - Project type detection (React, Python, Flask)
   - Invalid path handling
   - Multiple technology detection
   - Directory ignore system
   - Empty directory handling
   - Detection priorities

2. **Features Tests - TreeVisualizer (93%)**
   - Directory ignore configuration
   - Manual directory selection
   - Directory filtering
   - Complete structure visualization
   - Directory depth control
   - Invalid path handling

3. **Utils Tests - Configuration (88%)**
   - Configuration loading/saving
   - Version management
   - Development environment handling
   - Production environment configuration
   - Package resource fallback

#### In Progress Components 🟡
1. **CLI Arguments (18%)**
   - Basic command parsing
   - Initial flag validation
   - Error handling foundation

2. **Project Manager (17%)**
   - Folder management basics
   - Initial scanning implementation
   - Navigation groundwork

3. **Logger System (34%)**
   - Basic configuration testing
   - Initial file handling
   - Log level validation

#### Pending Implementation ❌
1. **File Handler (0%)**
   - Directory operations
   - File listing functionality
   - Size calculations

2. **UI Components (0%)**
   - Menu system
   - Banner display
   - User interaction

#### 📊 Métricas de Testing:
- Total de Tests: 31
- Tests Pasados: 31 (100%)
- Tests Fallidos: 0 (0%)
- Cobertura General: 29%
- Cobertura por Módulos:
  - Core/detector.py: 98%
  - Features/structure.py: 93%
  - Utils/config.py: 88%
  - Utils/logger.py: 34%
  - Utils/updater.py: 36%
  - Utils/file_handler.py: 0%
  - UI Components: 0%

### Next Steps
1. **High Priority**
   - Complete CLI argument tests
   - Implement project manager tests
   - Add file handler tests

2. **Medium Priority**
   - Add UI component tests
   - Finish logger test suite
   - Implement system tests

3. **Low Priority**
   - Add performance tests
   - Implement stress tests
   - Enhance documentation

### ⚠️ Known Issues
1. **Environment Mocking**
   - sys._MEIPASS simulation in production tests
   - Package resources handling improvements needed

2. **File Operations**
   - Temporary directory management
   - Permission handling refinement
   - Path resolution in different environments

3. **Coverage Gaps**
   - Complete UI testing implementation
   - Expand CLI handler coverage
   - Utility module test completion