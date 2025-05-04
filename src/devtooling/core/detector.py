import os
import glob
from typing import Set, List, Dict, Any
import logging
from devtooling.utils.config import load_config

class ProjectDetector:
    def __init__(self):
        self.logger = logging.getLogger('devtooling')
        self.detection_rules = load_config('detection_rules.json')['rules']

    def _has_file(self, path: str, files: List[str]) -> bool:
        """Verify if any of the files or directories exist in the path."""
        for file in files:
            file_path = os.path.join(path, file)
            # Verify if it's a pattern with wildcard
            if '*' in file:
                pattern = os.path.join(path, file)
                if any(True for _ in glob.glob(pattern)):
                    return True
            # Verify both files and directories
            elif os.path.exists(file_path):
                return True
        return False

    def detect_project_type(self, path: str) -> str:
        """Detect the main project type."""
        self.logger.debug(f"Detecting project type in: {path}")
        
        # Debug print
        print(f"\nChecking path: {path}")
        detected_types = self._detect_all_types(path)
        print(f"Detected types: {detected_types}")
    
        
        # Order rules by priority
        sorted_rules = sorted(self.detection_rules, key=lambda x: x['priority'])
        detected_types = self._detect_all_types(path)
        
        if not detected_types:
            self.logger.debug("Not detected any specific project type")
            return 'other'
        
        # Return the type with the highest priority
        for rule in sorted_rules:
            if rule['fileType'] in detected_types:
                self.logger.debug(f"Project types detected: {', '.join(detected_types)}")
                return rule['fileType']

    def _detect_all_types(self, path: str) -> Set[str]:
        """Detect all project technologies present."""
        detected_types = set()
        
        for rule in self.detection_rules:
            if self._has_file(path, rule['files']):
                detected_types.add(rule['fileType'])
                # Add technologies included
                if 'include' in rule:
                    detected_types.update(rule['include'])
                    self.logger.debug(f"Technologies included detected: {rule['include']}")
        
        return detected_types

    def get_ignored_dirs(self, path: str) -> List[str]:
        """Get the list of directories to ignore based on detected types."""
        ignored_dirs = set()
        detected_types = self._detect_all_types(path)
        
        # Collect directories to ignore from all detected types
        for rule in self.detection_rules:
            if rule['fileType'] in detected_types:
                if 'ignore' in rule:
                    ignored_dirs.update(rule['ignore'])
                
                # Add rules for included technologies
                for included_type in rule.get('include', []):
                    for r in self.detection_rules:
                        if r['fileType'] == included_type and 'ignore' in r:
                            ignored_dirs.update(r['ignore'])
        
        self.logger.debug(f"Directories to ignore: {list(ignored_dirs)}")
        return list(ignored_dirs)