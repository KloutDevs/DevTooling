import pytest
import os
import json
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from devtooling.utils.config import load_config, save_config, get_version, get_config_path


class TestConfig:

    @pytest.fixture
    def temp_dir(self):
        """Fixture providing a temporary directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Clean up after testing
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)

    def test_should_load_detection_rules(self):
        """Test: Should load detection rules correctly"""
        # Act
        config = load_config('detection_rules.json')
        
        # Assert
        assert 'rules' in config
        assert isinstance(config['rules'], list)
        assert len(config['rules']) > 0
        
        # Check the structure of a rule
        rule = config['rules'][0]
        assert 'fileType' in rule
        assert 'files' in rule
        assert 'priority' in rule

    def test_should_load_projects_config(self):
        """Test: Should successfully load project settings"""
        # Act
        config = load_config('projects.json')
        
        # Assert
        assert 'folders' in config
        assert 'projects' in config
        assert isinstance(config['folders'], list)
        assert isinstance(config['projects'], dict)

    def test_should_save_config(self, temp_dir):
        """Test: Should save the configuration correctly"""
        # Arrange
        config_path = os.path.join(temp_dir, 'test_config.json')
        test_config = {
            'test_key': 'test_value',
            'nested': {'key': 'value'}
        }
        
        # Act
        save_config('test_config.json', test_config, config_dir=temp_dir)
        
        # Assert
        assert os.path.exists(config_path)
        with open(config_path, 'r') as f:
            saved_config = json.load(f)
        assert saved_config == test_config

    def test_should_handle_missing_config(self):
        """Test: Should handle missing configuration files correctly"""
        # Arrange
        non_existent_file = 'non_existent_custom.json'  # Do not use projects.json that has special handling
        
        # Act & Assert
        with pytest.raises((FileNotFoundError, ImportError)):
            load_config(non_existent_file)

    def test_should_handle_invalid_json(self, temp_dir):
        """Test: Should handle invalid JSON correctly"""
        # Arrange
        filename = 'invalid_custom.json'  # Don't use projects.json
        invalid_json_path = os.path.join(temp_dir, filename)
        with open(invalid_json_path, 'w') as f:
            f.write('invalid json content')

        # Act & Assert
        with pytest.raises(json.JSONDecodeError):
            load_config(filename, config_dir=temp_dir)

    def test_should_get_version(self):
        """Test: Should get the version correctly"""
        # Act
        version = get_version()
        
        # Assert
        assert isinstance(version, str)
        assert version.count('.') == 2  # Format: X.Y.Z
        
    def test_should_create_config_dir_if_not_exists(self, temp_dir):
        """Test: Should create the configuration directory if it does not exist"""
        # Arrange
        config_dir = os.path.join(temp_dir, 'config')
        test_config = {'key': 'value'}
        
        # Act
        save_config('test.json', test_config, config_dir=config_dir)
        
        # Assert
        assert os.path.exists(config_dir)
        assert os.path.exists(os.path.join(config_dir, 'test.json'))

    def test_should_handle_permission_error(self):
        """Test: Should handle permission errors correctly"""
        # Arrange
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = PermissionError()
            
            # Act & Assert
            with pytest.raises(PermissionError):
                save_config('test.json', {'key': 'value'})
                
    def test_should_get_config_path_in_development(self):
        """Test: Should get the configuration path in development environment"""
        # Act
        config_path = get_config_path()

        # Assert
        assert os.path.exists(config_path)
        assert os.path.basename(os.path.dirname(config_path)) == 'devtooling'
        assert os.path.basename(config_path) == 'config'

    @patch('sys.frozen', True, create=True) # Simulates an compiled app
    @patch('sys._MEIPASS', new='mock_meipass', create=True) # Simultes the PyInstaller dyr
    @patch('os.makedirs') #  Prevents actual directory creation
    @patch('os.path.exists') # Controls which files "exist"
    @patch('shutil.copy2') # Prevents real copies of files
    @patch('appdirs.user_config_dir') # Simulates user’s config dir
    @patch('builtins.open', new_callable=mock_open) # Prevents actual file operations
    def test_should_get_config_path_in_production(
        self, 
        mock_open,
        mock_user_config_dir, 
        mock_copy2, 
        mock_exists, 
        mock_makedirs
    ):
        """Test: Should get config path in production environment without error."""
        # Arrange
        expected_dir = '/mock/config/dir'
        mock_user_config_dir.return_value = expected_dir

        # Simulate that the config directory exists
        mock_exists.side_effect = lambda path: not (
            'detection_rules.json' in path or 
            'projects.json' in path
        )

        # Prevent actual file operations
        mock_copy2.return_value = None
        mock_open.return_value.write.return_value = None

        # Act
        config_path = get_config_path()

        # Assert
        assert config_path == expected_dir
        mock_makedirs.assert_called_with(expected_dir, exist_ok=True)

        # Verify copy2 was called with correct paths
        expected_src = os.path.join('mock_meipass', 'config', 'detection_rules.json')
        expected_dst = os.path.join(expected_dir, 'detection_rules.json')
        mock_copy2.assert_called_with(expected_src, expected_dst)

        # Verify projects.json was created
        expected_projects_path = os.path.join(expected_dir, 'projects.json')
        mock_open.assert_called_with(expected_projects_path, 'w', encoding='utf-8')

    def test_should_handle_projects_config_not_exists(self, temp_dir):
        """Test: Should create projects.json if it does not exist"""
        # Arrange
        config_dir = os.path.join(temp_dir, 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        # Act
        with patch('devtooling.utils.config.get_config_path', return_value=config_dir):
            config = load_config('projects.json')
        
        # Assert
        assert config == {"folders": [], "projects": {}}
        assert os.path.exists(os.path.join(config_dir, 'projects.json'))

    @patch('importlib.resources.open_text')
    def test_should_load_from_package_resources(self, mock_open_text, temp_dir):
        """Test: Should load from package resources if file does not exist"""
        # Arrange
        mock_file = mock_open(read_data='{"test": "data"}')()
        mock_open_text.return_value = mock_file

        # Act
        config = load_config('custom.json', config_dir=temp_dir)

        # Assert
        assert config == {"test": "data"}
        mock_open_text.assert_called_once()

    def test_should_handle_config_dir_creation(self, temp_dir):
        """Test: Should create the configuration directory if it does not exist"""
        # Arrange
        nested_config_dir = os.path.join(temp_dir, 'deep', 'nested', 'config')
        test_config = {'key': 'value'}

        # Act
        save_config('test.json', test_config, config_dir=nested_config_dir)

        # Assert
        assert os.path.exists(nested_config_dir)
        assert os.path.exists(os.path.join(nested_config_dir, 'test.json'))

    @patch('sys.frozen', True, create=True)
    @patch('sys._MEIPASS', new='mock_meipass', create=True)
    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('shutil.copy2')
    @patch('appdirs.user_config_dir')
    @patch('builtins.open', new_callable=mock_open)
    def test_should_copy_detection_rules_in_production(
        self,
        mock_open,
        mock_user_config_dir,
        mock_copy2,
        mock_exists,
        mock_makedirs
    ):
        """Test: Verify that configuration files are copied correctly in production"""
        # Arrange
        config_dir = '/mock/config/dir'
        mock_user_config_dir.return_value = config_dir

        # Pretend that files do not initially exist
        mock_exists.side_effect = lambda path: False

        # Configure the open mock to prevent actual file operations
        mock_open.return_value.write.return_value = None

        # Act
        result_path = get_config_path()

        # Assert
        assert result_path == config_dir

        # Verify that the directory has been created
        mock_makedirs.assert_called_with(config_dir, exist_ok=True)

        # Verify that you copied detection_rules.json
        expected_rules_src = os.path.join('mock_meipass', 'config', 'detection_rules.json')
        expected_rules_dst = os.path.join(config_dir, 'detection_rules.json')
        mock_copy2.assert_any_call(expected_rules_src, expected_rules_dst)

        # Verify that you created projects.json
        expected_projects_path = os.path.join(config_dir, 'projects.json')
        mock_open.assert_called_with(expected_projects_path, 'w', encoding='utf-8')

        # Verify that the correct content was written in projects.json
        mock_open.return_value.write.assert_called()
        
    @patch('devtooling.utils.config.importlib_resources.open_text')  # Use the alias defined in config.py
    def test_should_fallback_to_package_resources(self, mock_open_text):
        """Test: Should fallback to package resources when config file does not exist."""
        # Arrange
        mock_content = '{"test": "data"}'
        mock_file = MagicMock()
        mock_file.__enter__.return_value = MagicMock()
        mock_file.__enter__.return_value.read.return_value = mock_content
        mock_open_text.return_value = mock_file

        # Act
        with patch('os.path.exists', return_value=False):
            config = load_config('test.json')

        # Assert
        assert config == {"test": "data"}
        mock_open_text.assert_called_once_with(
            'devtooling.config',
            'test.json',
            encoding='utf-8'
        )