import pytest
import tempfile
import shutil
from pathlib import Path
from devtooling.core.detector import ProjectDetector

class TestProjectDetector:
    @pytest.fixture
    def detector(self):
        """Fixture providing an instance of ProjectDetector"""
        return ProjectDetector()
    
    @pytest.fixture
    def temp_dir(self):
        """Fixture providing a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def create_file(self, base_path, file_path):
        """
        Improved helper to create test files
        Automatically creates necessary directories
        """
        full_path = Path(base_path) / file_path
        # Create parent directories if none exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        # Create file
        full_path.write_text('test content')
        return str(full_path)

    def test_should_detect_react_project(self, detector, temp_dir):
        """Test: Should correctly detect a React project"""
        # Arrange
        self.create_file(temp_dir, 'package.json')
        self.create_file(temp_dir, 'src/App.jsx')
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Print for debug
        print(f"\nDetected project type: {project_type}")
        print(f"All detected types: {detector._detect_all_types(temp_dir)}")
        
        # Assert
        assert project_type == 'react'
    
    def test_should_detect_python_project(self, detector, temp_dir):
        """Test: It should detect a Python project correctly"""
        # Arrange
        self.create_file(temp_dir, 'requirements.txt')
        self.create_file(temp_dir, 'setup.py')
        # Do not create specific Flask files
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Assert
        assert project_type == 'python'
        
    def test_should_detect_flask_project(self, detector, temp_dir):
        """Test: Should successfully detect a Flask project"""
        # Arrange
        self.create_file(temp_dir, 'requirements.txt')
        self.create_file(temp_dir, 'app.py')
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Assert
        assert project_type == 'flask'

    def test_should_handle_invalid_path(self, detector):
        """Test: Should handle invalid routes correctly"""
        # Act
        project_type = detector.detect_project_type('/path/that/does/not/exist')
        
        # Assert
        assert project_type == 'other'
        
    def test_should_detect_multiple_technologies(self, detector, temp_dir):
        """Test: Should identify multiple technologies and respect priorities"""
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
        """Test: Should get directories to ignore correctly"""
        # Arrange
        self.create_file(temp_dir, 'package.json')
        self.create_file(temp_dir, 'next.config.js')
        
        # Act
        ignored_dirs = detector.get_ignored_dirs(temp_dir)
        
        # Assert
        assert 'node_modules' in ignored_dirs
        assert '.next' in ignored_dirs

    def test_should_handle_empty_directory(self, detector, temp_dir):
        """Test: Should handle empty directories correctly"""
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Assert
        assert project_type == 'other'

    def test_should_respect_detection_priorities(self, detector, temp_dir):
        """Test: Should respect detection priorities"""
        # Arrange
        self.create_file(temp_dir, 'angular.json')  # Priority 1
        self.create_file(temp_dir, 'src/App.jsx')   # React - Priority 2
        self.create_file(temp_dir, 'requirements.txt')  # Python - Priority 3
        self.create_file(temp_dir, 'package.json')  # Node - Priority 4
        
        # Act
        project_type = detector.detect_project_type(temp_dir)
        
        # Assert
        assert project_type == 'angular'