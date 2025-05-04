import pytest
import os
from pathlib import Path
import tempfile
import shutil
from unittest.mock import patch
from devtooling.features.tree.structure import TreeVisualizer

class TestTreeVisualizer:
    @pytest.fixture
    def visualizer(self):
        """Fixture providing an instance of TreeVisualizer"""
        return TreeVisualizer()
    
    @pytest.fixture
    def temp_dir(self):
        """Fixture providing a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
        
    def create_directory_structure(self, base_path):
        """Helper to create a test directory structure"""
        # Create directories
        dirs = ['src', 'src/components', 'src/utils', 'node_modules', 'public']
        for _dir in dirs:
            Path(base_path).joinpath(_dir).mkdir(parents=True, exist_ok=True)
            
        # Create files
        files = [
            'src/index.js',
            'src/components/App.jsx',
            'src/utils/helpers.js',
            'public/index.html',
            'package.json',
            '.gitignore'
        ]
        for file in files:
            Path(base_path).joinpath(file).write_text('test content')

    def test_should_set_ignored_dirs(self, visualizer):
        """Test: Should correctly set the directories to ignore"""
        # Arrange
        ignored = ['node_modules', 'build', 'dist']
        
        # Act
        visualizer.set_ignored_dirs(ignored)
        
        # Assert
        assert visualizer.ignored_dirs == ignored
        
    @patch('questionary.checkbox')
    def test_should_select_directories(self, mock_checkbox, visualizer, temp_dir):
        """Test: Should allow selecting directories correctly"""
        # Arrange
        self.create_directory_structure(temp_dir)
        mock_response = ['src', 'public']
        mock_checkbox.return_value.ask.return_value = mock_response

        # Act
        selected = visualizer.select_directories(temp_dir)

        # Assert
        assert selected == mock_response

    def test_should_show_structure_with_ignored_dirs(self, visualizer, temp_dir):
        """Test: Should show the structure respecting ignored directories"""
        # Arrange
        self.create_directory_structure(temp_dir)
        visualizer.set_ignored_dirs(['node_modules'])
        
        # Act
        with patch('rich.console.Console.print') as mock_print:
            visualizer.show_structure(temp_dir)
            
        # Assert
        prints = [call[0][0] for call in mock_print.call_args_list]
        assert any('node_modules' not in str(p) for p in prints)
        assert any('src' in str(p) for p in prints)
        assert any('public' in str(p) for p in prints)

    def test_should_show_complete_structure(self, visualizer, temp_dir):
        """Test: Should show the full structure when show_all is"""
        # Arrange
        self.create_directory_structure(temp_dir)
        visualizer.set_ignored_dirs(['node_modules'])
        
        # Act
        with patch('rich.console.Console.print') as mock_print:
            visualizer.show_structure(temp_dir, show_all=True)
            
        # Assert
        prints = [call[0][0] for call in mock_print.call_args_list]
        assert any('node_modules' in str(p) for p in prints)
        assert any('src' in str(p) for p in prints)
        assert any('public' in str(p) for p in prints)

    def test_should_handle_invalid_path(self, visualizer):
        """Test: Should handle invalid routes correctly"""
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            visualizer.show_structure('/path/that/does/not/exist')
        assert "Path does not exist" in str(exc_info.value)

    def test_should_show_structure_with_allowed_dirs(self, visualizer, temp_dir):
        """Test: Should show only allowed directories"""
        # Arrange
        self.create_directory_structure(temp_dir)
        allowed = ['src', 'public']
        
        # Act
        with patch('rich.console.Console.print') as mock_print:
            visualizer.show_structure(temp_dir, allowed=allowed)
            
        # Assert
        prints = [call[0][0] for call in mock_print.call_args_list]
        assert any('src' in str(p) for p in prints)
        assert any('public' in str(p) for p in prints)
        assert all('node_modules' not in str(p) for p in prints)

    def test_should_respect_max_depth(self, visualizer, temp_dir):
        """Test: Should respect the maximum viewing depth"""
        # Arrange
        deep_path = os.path.join(temp_dir, 'level1', 'level2', 'level3')
        os.makedirs(deep_path)
        
        # Act
        with patch('rich.console.Console.print') as mock_print:
            visualizer.show_structure(temp_dir, max_level=1)
            
        # Assert
        prints = [call[0][0] for call in mock_print.call_args_list]
        assert any('level1' in str(p) for p in prints)
        assert not any('level3' in str(p) for p in prints)

    def test_should_handle_empty_allowed_dirs(self, visualizer, temp_dir):
        """Test: Should correctly handle an empty list of allowed directories"""
        # Arrange
        self.create_directory_structure(temp_dir)
        
        # Act
        with patch('rich.console.Console.print') as mock_print:
            visualizer.show_structure(temp_dir, allowed=[])
            
        # Assert
        prints = [call[0][0] for call in mock_print.call_args_list]
        assert len(prints) > 0  # Should show at least the root directory