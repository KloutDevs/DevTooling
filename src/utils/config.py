import os
import sys
import json
from typing import Dict, Any

def get_config_path() -> str:
    """Get the absolute path to the config directory."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, 'config')
    
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')

def load_config(filename: str) -> Dict[str, Any]:
    """Load a configuration file."""
    config_path = os.path.join(get_config_path(), filename)
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(filename: str, data: Dict[str, Any]):
    """Save configuration to file."""
    config_path = os.path.join(get_config_path(), filename)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_version() -> str:
    return "0.2.1"