import subprocess
import pkg_resources
import requests
from typing import Optional, Tuple
import logging

logger = logging.getLogger('devtooling')

def check_latest_version() -> Tuple[str, Optional[str]]:
    """
    Checks for the latest version on PyPI.
    Returns (current_version, latest_version) or (current_version, None) if can't check
    """
    try:
        current = pkg_resources.get_distribution('devtooling-cli').version
        response = requests.get('https://pypi.org/pypi/devtooling-cli/json')
        latest = response.json()['info']['version']
        return current, latest if latest != current else None
    except Exception as e:
        logger.error(f"Error checking latest version: {str(e)}")
        return current, None

def update_package() -> bool:
    """Updates the package using pip."""
    try:
        result = subprocess.run(
            ['pip', 'install', '--upgrade', 'devtooling-cli'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error updating package: {str(e)}")
        return False