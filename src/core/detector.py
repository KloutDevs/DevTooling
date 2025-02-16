import os
import glob
from typing import Set, List, Dict, Any
import logging
from ..utils.config import load_config

class ProjectDetector:
    def __init__(self):
        self.logger = logging.getLogger('devtooling')
        self.detection_rules = load_config('detection_rules.json')['rules']

    def _has_file(self, path: str, files: List[str]) -> bool:
        """Verifica si alguno de los archivos o directorios existe en la ruta."""
        for file in files:
            file_path = os.path.join(path, file)
            # Verificar si es un patrón con wildcard
            if '*' in file:
                pattern = os.path.join(path, file)
                if any(True for _ in glob.glob(pattern)):
                    return True
            # Verificar tanto archivos como directorios
            elif os.path.exists(file_path):
                return True
        return False

    def detect_project_type(self, path: str) -> str:
        """Detecta el tipo principal de proyecto."""
        self.logger.debug(f"Detectando tipo de proyecto en: {path}")
        
        # Ordenar reglas por prioridad
        sorted_rules = sorted(self.detection_rules, key=lambda x: x['priority'])
        detected_types = self._detect_all_types(path)
        
        if not detected_types:
            self.logger.info("No se detectó ningún tipo específico de proyecto")
            return 'otro'
        
        # Retornar el tipo de mayor prioridad
        for rule in sorted_rules:
            if rule['fileType'] in detected_types:
                self.logger.info(f"Tipos de proyecto detectados: {', '.join(detected_types)}")
                return rule['fileType']

    def _detect_all_types(self, path: str) -> Set[str]:
        """Detecta todos los tipos de tecnologías presentes."""
        detected_types = set()
        
        for rule in self.detection_rules:
            if self._has_file(path, rule['files']):
                detected_types.add(rule['fileType'])
                # Agregar tecnologías incluidas
                if 'include' in rule:
                    detected_types.update(rule['include'])
                    self.logger.debug(f"Tecnologías incluidas detectadas: {rule['include']}")
        
        return detected_types

    def get_ignored_dirs(self, path: str) -> List[str]:
        """Obtiene la lista de directorios a ignorar basado en los tipos detectados."""
        ignored_dirs = set()
        detected_types = self._detect_all_types(path)
        
        # Recolectar directorios a ignorar de todos los tipos detectados
        for rule in self.detection_rules:
            if rule['fileType'] in detected_types:
                if 'ignore' in rule:
                    ignored_dirs.update(rule['ignore'])
                
                # Agregar reglas de tecnologías incluidas
                for included_type in rule.get('include', []):
                    for r in self.detection_rules:
                        if r['fileType'] == included_type and 'ignore' in r:
                            ignored_dirs.update(r['ignore'])
        
        self.logger.debug(f"Directorios a ignorar: {list(ignored_dirs)}")
        return list(ignored_dirs)