import json
from typing import Dict, Any

def load_config(filename: str) -> Dict[str, Any]:
    with open(f'config/{filename}', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_version() -> str:
    return "0.2.0"