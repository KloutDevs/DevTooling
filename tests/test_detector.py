import os
import pytest
import tempfile
import shutil
from pathlib import Path
from devtooling.core.detector import ProjectDetector

class TestProjectDetector:
    @pytest.fixture
    def detector(self):
        """Fixture que proporciona una instancia de ProjectDetector"""
        return ProjectDetector()
    
    @pytest.fixture
    def temp_dir(self):
        """Fixture que proporciona un directorio temporal para las pruebas"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def create_file(self, base_path, file_path):
        """
        Helper mejorado para crear archivos de prueba
        Crea automáticamente los directorios necesarios
        """
        full_path = Path(base_path) / file_path
        # Crear directorios padre si no existen
        full_path.parent.mkdir(parents=True, exist_ok=True)
        # Crear archivo
        full_path.write_text('test content')
        return str(full_path)

    def test_should_detect_react_project(self, detector, temp_dir):
        """Test: Debería detectar correctamente un proyecto React"""
        # Arrange
        self.create_file(temp_dir, 'package.json')
        self.create_file(temp_dir, 'src/App.jsx')
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Print para debug
        print(f"\nDetected project type: {project_type}")
        print(f"All detected types: {detector._detect_all_types(temp_dir)}")
        
        # Assert
        assert project_type == 'react'
    
    def test_should_detect_python_project(self, detector, temp_dir):
        """Test: Debería detectar correctamente un proyecto Python"""
        # Arrange
        self.create_file(temp_dir, 'requirements.txt')
        self.create_file(temp_dir, 'setup.py')
        # No crear archivos específicos de Flask
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Assert
        assert project_type == 'python'
        
    def test_should_detect_flask_project(self, detector, temp_dir):
        """Test: Debería detectar correctamente un proyecto Flask"""
        # Arrange
        self.create_file(temp_dir, 'requirements.txt')
        self.create_file(temp_dir, 'app.py')
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Assert
        assert project_type == 'flask'

    def test_should_handle_invalid_path(self, detector):
        """Test: Debería manejar correctamente rutas inválidas"""
        # Act
        project_type = detector.detect_project_type('/path/that/does/not/exist')
        
        # Assert
        assert project_type == 'otro'
        
    def test_should_detect_multiple_technologies(self, detector, temp_dir):
        """Test: Debería detectar múltiples tecnologías y respetar prioridades"""
        # Arrange
        self.create_file(temp_dir, 'package.json')
        self.create_file(temp_dir, 'next.config.js')
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        detected_types = detector._detect_all_types(temp_dir)
        
        # Assert
        assert project_type == 'nextjs'
        assert 'node' in detected_types
        assert 'react' in detected_types

    def test_should_get_correct_ignored_dirs(self, detector, temp_dir):
        """Test: Debería obtener los directorios a ignorar correctamente"""
        # Arrange
        self.create_file(temp_dir, 'package.json')
        self.create_file(temp_dir, 'next.config.js')
        
        # Act
        ignored_dirs = detector.get_ignored_dirs(temp_dir)
        
        # Assert
        assert 'node_modules' in ignored_dirs
        assert '.next' in ignored_dirs

    def test_should_handle_empty_directory(self, detector, temp_dir):
        """Test: Debería manejar correctamente directorios vacíos"""
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Assert
        assert project_type == 'otro'

    def test_should_respect_detection_priorities(self, detector, temp_dir):
        """Test: Debería respetar las prioridades de detección"""
        # Arrange
        self.create_file(temp_dir, 'angular.json')  # Priority 1
        self.create_file(temp_dir, 'src/App.jsx')   # React - Priority 2
        self.create_file(temp_dir, 'requirements.txt')  # Python - Priority 3
        self.create_file(temp_dir, 'package.json')  # Node - Priority 4
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Assert
        assert project_type == 'angular'