import os
import sys
import json
from typing import Dict, Any
import appdirs
import shutil
import importlib.resources as pkg_resources


def get_config_path() -> str:
    """Get the absolute path to the config directory."""
    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        config_dir = appdirs.user_config_dir("devtooling-cli", "KloutDevs")
        os.makedirs(config_dir, exist_ok=True)
        
        meipass_config = os.path.join(sys._MEIPASS, 'config')
        rules_path = os.path.join(config_dir, 'detection_rules.json')
        projects_path = os.path.join(config_dir, 'projects.json')
        
        # Verify and create config files if they don't exist
        if not os.path.exists(rules_path):
            shutil.copy2(
                os.path.join(meipass_config, 'detection_rules.json'),
                rules_path
            )
        
        if not os.path.exists(projects_path):
            with open(projects_path, 'w', encoding='utf-8') as f:
                json.dump({"folders": [], "projects": {}}, f, indent=2)
        
        return config_dir
    
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')

def load_config(filename: str, config_dir: str = None) -> Dict[str, Any]:
    """
    Load a configuration file.
    
    Args:
        filename: Name of the configuration file
        config_dir: Optional directory to load from (for testing)
    """
    if config_dir:
        config_path = os.path.join(config_dir, filename)
    else:
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
            
        # For others files, try to load from the packaged resources
        with pkg_resources.open_text('devtooling.config', filename, encoding='utf-8') as f:
            return json.load(f)
            
    except Exception as e:
        if filename == 'projects.json':
            default_config = {"folders": [], "projects": {}}
            save_config(filename, default_config)
            return default_config
        raise
    
def save_config(filename: str, data: Dict[str, Any], config_dir: str = None):
    """
    Save configuration to file.
    
    Args:
        filename: Name of the configuration file
        data: Configuration data to save
        config_dir: Optional directory to save to (for testing)
    """
    if config_dir:
        config_path = os.path.join(config_dir, filename)
    else:
        config_path = os.path.join(get_config_path(), filename)
        
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_version() -> str:
    return "0.2.9"