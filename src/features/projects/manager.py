import os
import json
from typing import Dict, List, Optional
import logging
from ...utils.config import load_config, save_config
from ...core.detector import ProjectDetector

class ProjectManager:
    def __init__(self):
        self.logger = logging.getLogger('devtooling')
        self.detector = ProjectDetector()
        self.config = self._load_projects_config()

    def _load_projects_config(self) -> Dict:
        """Load projects configuration."""
        try:
            return load_config('projects.json')
        except FileNotFoundError:
            # Create default config if not exists
            default_config = {"folders": [], "projects": {}}
            save_config('projects.json', default_config)
            return default_config

    def _save_config(self):
        """Save current configuration."""
        save_config('projects.json', self.config)

    def add_folder(self, path: str, low_level: bool = False) -> bool:
        """
        Add a folder to watch for projects.
        
        Args:
            path: Path to add
            low_level: If True, only scan root and one level deep
        """
        try:
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                self.logger.error(f"Path does not exist: {abs_path}")
                return False

            # Verificar si el path ya existe
            for folder in self.config["folders"]:
                if folder["path"] == abs_path:
                    return False

            # Store the scanning mode with the folder
            self.config["folders"].append({
                "path": abs_path,
                "low_level": low_level
            })
            self._save_config()
            self.refresh_folder(abs_path, low_level)
            return True
        except Exception as e:
            self.logger.error(f"Error adding folder: {str(e)}")
            return False

    def remove_folder(self, path: str) -> bool:
        """Remove a folder from watched folders."""
        try:
            abs_path = os.path.abspath(path)
            # Buscar la configuración de la carpeta
            for folder in self.config["folders"]:
                if folder["path"] == abs_path:
                    self.config["folders"].remove(folder)
                    # Remove projects from this folder
                    self.config["projects"] = {
                        k: v for k, v in self.config["projects"].items()
                        if not k.startswith(abs_path)
                    }
                    self._save_config()
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error removing folder: {str(e)}")
            return False

    def list_folders(self) -> List[Dict]:
        """List all watched folders with their configurations."""
        return self.config["folders"]


    def refresh_folder(self, folder_path: Optional[str] = None, low_level: Optional[bool] = None):
        """
        Refresh projects in specified folder or all folders.
        
        Args:
            folder_path: Specific folder to refresh, or None for all folders
            low_level: Override scanning mode for this refresh
        """
        try:
            projects_found = 0
    
            if folder_path:
                abs_path = os.path.abspath(folder_path)
                folders = [{"path": abs_path, "low_level": low_level if low_level is not None else False}]
                # Limpiar proyectos existentes de esta carpeta
                self.config["projects"] = {
                    k: v for k, v in self.config["projects"].items()
                    if not k.startswith(abs_path)
                }
            else:
                folders = self.config["folders"]
                # Limpiar todos los proyectos para un refresh completo
                self.config["projects"] = {}
    
            for folder_config in folders:
                folder = folder_config["path"]
                is_low_level = low_level if low_level is not None else folder_config.get("low_level", False)
                
                self.logger.info(f"Scanning folder: {folder} (low-level: {is_low_level})")
                
                # Analyze root directory
                project_type = self.detector.detect_project_type(folder)
                if project_type != 'otro':
                    projects_found += 1
                    self.logger.info(f"Found {project_type} project in: {folder}")
                    self.config["projects"][folder] = {
                        "name": os.path.basename(folder),
                        "type": project_type,
                        "path": folder
                    }
    
                # First level scan
                for item in os.listdir(folder):
                    item_path = os.path.join(folder, item)
                    if os.path.isdir(item_path) and not item.startswith('.'):
                        # Analyze first level directory
                        project_type = self.detector.detect_project_type(item_path)
                        if project_type != 'otro':
                            projects_found += 1
                            self.logger.info(f"Found {project_type} project in: {item_path}")
                            self.config["projects"][item_path] = {
                                "name": item,
                                "type": project_type,
                                "path": item_path
                            }
                        
                        # If not low_level, scan one level deeper
                        if not is_low_level:
                            for subitem in os.listdir(item_path):
                                subitem_path = os.path.join(item_path, subitem)
                                if os.path.isdir(subitem_path) and not subitem.startswith('.'):
                                    project_type = self.detector.detect_project_type(subitem_path)
                                    if project_type != 'otro':
                                        projects_found += 1
                                        self.logger.info(f"Found {project_type} project in: {subitem_path}")
                                        self.config["projects"][subitem_path] = {
                                            "name": subitem,
                                            "type": project_type,
                                            "path": subitem_path
                                        }
    
            self._save_config()
            return projects_found
    
        except Exception as e:
            self.logger.error(f"Error refreshing folders: {str(e)}")
            return 0

    def get_project_path(self, identifier: str) -> Optional[str]:
        """Get project path by name or path."""
        # Check if it's a direct path
        if identifier in self.config["projects"]:
            return identifier
            
        # Search by project name
        for project_info in self.config["projects"].values():
            if project_info["name"] == identifier:
                return project_info["path"]
                
        return None