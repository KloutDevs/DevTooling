import os
import sys
import json
from typing import Dict, Any
import appdirs
import shutil
import importlib.resources as pkg_resources


def get_config_path() -> str:
    """Get the absolute path to the config directory."""
    if hasattr(sys, '_MEIPASS'):
        # Case of packaged application
        config_dir = appdirs.user_config_dir("devtooling-cli", "KloutDevs")
        os.makedirs(config_dir, exist_ok=True)
        
        # Copy the files of _MEIPASS if they don't exist
        meipass_config = os.path.join(sys._MEIPASS, 'config')
        
        # Verify and copy detection_rules.json if it doesn't exist
        if not os.path.exists(os.path.join(config_dir, 'detection_rules.json')):
            shutil.copy2(
                os.path.join(meipass_config, 'detection_rules.json'),
                os.path.join(config_dir, 'detection_rules.json')
            )
        
        # Verify and copy projects.json if it doesn't exist
        projects_path = os.path.join(config_dir, 'projects.json')
        if not os.path.exists(projects_path):
            with open(projects_path, 'w') as f:
                json.dump({"folders": [], "projects": {}}, f, indent=2)
        
        return config_dir
    else:
        # Case of development environment
        # Only up two directories to reach to 'src/devtooling/config'
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')

def load_config(filename: str) -> Dict[str, Any]:
    """Load a configuration file."""
    config_path = os.path.join(get_config_path(), filename)
    
    try:
        # First, try to load from the local file
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # If doesn't exist, create a new one
        if filename == 'projects.json':
            default_config = {"folders": [], "projects": {}}
            save_config(filename, default_config)
            return default_config
            
        # For others files, try to load from the packaged resources (Only in production)
        with pkg_resources.open_text('devtooling.config', filename, encoding='utf-8') as f:
            return json.load(f)
            
    except Exception as e:
        if filename == 'projects.json':
            default_config = {"folders": [], "projects": {}}
            save_config(filename, default_config)
            return default_config
        raise

def save_config(filename: str, data: Dict[str, Any]):
    """Save configuration to file."""
    config_path = os.path.join(get_config_path(), filename)
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_version() -> str:
    return "0.2.7"