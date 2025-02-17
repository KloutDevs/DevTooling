
`CHANGELOG.md`:
```markdown
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5] - 2024-02-17

### Added
- Added projects management system
  - Watch folders for projects detection
  - Support for low-level and deep scanning modes
  - Automatic project type detection in watched folders
  - Project navigation feature with new terminal
  - Projects listing with detailed information

- Added command line interface for projects management:
  - `devtool projects --folders-add PATH [--low-level]`
  - `devtool projects --folders-remove PATH`
  - `devtool projects --list`
  - `devtool projects --refresh-folders`
  - `devtool projects --go PROJECT_NAME`
  - `devtool go PROJECT_NAME` (shortcut command)
  
- Added interactive menu for projects management

### Changed
- Enhanced CLI with better command documentation
- Improved project detection efficiency
- Updated menu structure to include projects management


## [0.2.2] - 2024-02-17

### Added
- Added support for arguments on the command line instead of just having a CLI

### Fixed

- Fixed the structure view on manual mode

## [0.2.1] - 2024-02-16

### Added
- Added build script for PyInstaller

### Changed
- Replaced the use of PyFiglet for an simplified ASCII art banner

## [0.2.0] - 2024-02-16

### Added
- Added support for more frameworks and technologies
- Fully organized project structure
- Added logging system

### Changed
- Replaced the ignore_rules.json file with a more flexible configuration in detection_rules.json
- Changed the menu options to allow more functionalities in the future
- Replaced the FileIgnorer file with a more flexible ProjectDetector

### Fixed
- Fixed the detection of simultaneous project types
- Fixed the detection of nested projects
- Fixed the manage of invalid routes
- Fixed the visualization of directory structure (After the CLI was reset before of generate the structure)
- Other minor fixes and improvements

## [0.1.0] - 2024-02-02

### Added
- Base system of project detection
- Visualization of directory structure
- Improved JSON configuration
- Intelligent detection of project types
- Command-line basic interface

### Changed
- Improved the project detection logic
- Optimized the ignore directories system

### Fixed
- Fixed the detection of nested projects
- Fixed the manage of invalid routes

## [0.1.0] - 2024-02-01

### Added
- Initial project structure
- Basic detection system
- JSON Configuration files
- Initial documentation
- Basic CLI interface

### Changed
- Reorganized project structure
- Improved logging system

## Type of changes
- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.