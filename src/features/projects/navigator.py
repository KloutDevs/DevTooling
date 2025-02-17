import os
import subprocess
import platform
import logging

class ProjectNavigator:
    def __init__(self):
        self.logger = logging.getLogger('devtooling')

    def navigate_to(self, path: str) -> bool:
        """Navigate to specified project path."""
        try:
            if not os.path.exists(path):
                self.logger.error(f"Path does not exist: {path}")
                return False

            # Different approach depending on OS
            system = platform.system().lower()
            
            if system == 'windows':
                # In Windows, use start cmd in the specified location
                os.system(f'start cmd /k "cd /d {path}"')
            else:
                # In Unix, use the default shell
                shell = os.environ.get('SHELL', '/bin/bash')
                subprocess.run([shell, '-c', f'cd "{path}" && {shell}'])
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error navigating to path: {str(e)}")
            return False