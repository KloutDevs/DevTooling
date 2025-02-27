import pytest
import os
import json
import tempfile
import appdirs
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from devtooling.utils.config import load_config, save_config, get_version, get_config_path

class TestConfig:
    @pytest.fixture
    def temp_dir(self):
        """Fixture que proporciona un directorio temporal"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Limpiar después de las pruebas
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)

    def test_should_load_detection_rules(self):
        """Test: Debería cargar correctamente las reglas de detección"""
        # Act
        config = load_config('detection_rules.json')
        
        # Assert
        assert 'rules' in config
        assert isinstance(config['rules'], list)
        assert len(config['rules']) > 0
        
        # Verificar estructura de una regla
        rule = config['rules'][0]
        assert 'fileType' in rule
        assert 'files' in rule
        assert 'priority' in rule

    def test_should_load_projects_config(self):
        """Test: Debería cargar correctamente la configuración de proyectos"""
        # Act
        config = load_config('projects.json')
        
        # Assert
        assert 'folders' in config
        assert 'projects' in config
        assert isinstance(config['folders'], list)
        assert isinstance(config['projects'], dict)

    def test_should_save_config(self, temp_dir):
        """Test: Debería guardar correctamente la configuración"""
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
        """Test: Debería manejar correctamente archivos de configuración faltantes"""
        # Arrange
        non_existent_file = 'non_existent_custom.json'  # No usar projects.json que tiene manejo especial
        
        # Act & Assert
        with pytest.raises((FileNotFoundError, ImportError)):  # Permitir ImportError por pkg_resources
            load_config(non_existent_file)

    def test_should_handle_invalid_json(self, temp_dir):
        """Test: Debería manejar correctamente JSON inválido"""
        # Arrange
        filename = 'invalid_custom.json'  # No usar projects.json
        invalid_json_path = os.path.join(temp_dir, filename)
        with open(invalid_json_path, 'w') as f:
            f.write('invalid json content')

        # Act & Assert
        with pytest.raises(json.JSONDecodeError):
            load_config(filename, config_dir=temp_dir)

    def test_should_get_version(self):
        """Test: Debería obtener correctamente la versión"""
        # Act
        version = get_version()
        
        # Assert
        assert isinstance(version, str)
        assert version.count('.') == 2  # Format: X.Y.Z
        
    def test_should_create_config_dir_if_not_exists(self, temp_dir):
        """Test: Debería crear el directorio de configuración si no existe"""
        # Arrange
        config_dir = os.path.join(temp_dir, 'config')
        test_config = {'key': 'value'}
        
        # Act
        save_config('test.json', test_config, config_dir=config_dir)
        
        # Assert
        assert os.path.exists(config_dir)
        assert os.path.exists(os.path.join(config_dir, 'test.json'))

    def test_should_handle_permission_error(self):
        """Test: Debería manejar correctamente errores de permisos"""
        # Arrange
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = PermissionError()
            
            # Act & Assert
            with pytest.raises(PermissionError):
                save_config('test.json', {'key': 'value'})
                
    def test_should_get_config_path_in_development(self):
        """Test: Debería obtener la ruta de configuración en entorno de desarrollo"""
        # Act
        config_path = get_config_path()

        # Assert
        assert os.path.exists(config_path)
        assert os.path.basename(os.path.dirname(config_path)) == 'devtooling'
        assert os.path.basename(config_path) == 'config'

    @patch('sys.frozen', True, create=True)
    @patch('sys._MEIPASS', new='mock_meipass', create=True)
    @patch('appdirs.user_config_dir')
    def test_should_get_config_path_in_production(self, mock_user_config_dir):
        """Test: Debería obtener la ruta de configuración en entorno de producción"""
        # Arrange
        expected_dir = '/mock/config/dir'
        mock_user_config_dir.return_value = expected_dir
        
        # Act
        with patch('os.makedirs') as mock_makedirs:
            config_path = get_config_path()
        
        # Assert
        assert config_path == expected_dir
        mock_makedirs.assert_called_with(expected_dir, exist_ok=True)

    def test_should_handle_projects_config_not_exists(self, temp_dir):
        """Test: Debería crear projects.json si no existe"""
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
        """Test: Debería cargar desde recursos del paquete si el archivo no existe"""
        # Arrange
        mock_file = mock_open(read_data='{"test": "data"}')()
        mock_open_text.return_value = mock_file

        # Act
        config = load_config('custom.json', config_dir=temp_dir)

        # Assert
        assert config == {"test": "data"}
        mock_open_text.assert_called_once()

    def test_should_handle_config_dir_creation(self, temp_dir):
        """Test: Debería crear el directorio de configuración si no existe"""
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
    @patch('shutil.copy2')
    @patch('appdirs.user_config_dir')
    def test_should_copy_detection_rules_in_production(self, mock_user_config_dir, mock_copy, temp_dir):
        """Test: Debería copiar detection_rules.json en producción"""
        # Arrange
        config_dir = os.path.join(temp_dir, 'config')
        mock_user_config_dir.return_value = config_dir
        
        # Act
        with patch('os.makedirs') as mock_makedirs:
            with patch('os.path.exists', return_value=False):
                get_config_path()
        
        # Assert
        mock_copy.assert_called()
        assert 'detection_rules.json' in mock_copy.call_args[0][1]
        
    @patch('pkg_resources.open_text')
    def test_should_fallback_to_package_resources(self, mock_open_text):
        """Test: Debería usar recursos del paquete como fallback"""
        # Arrange
        mock_file = MagicMock()
        mock_file.read.return_value = '{"test": "data"}'
        mock_open_text.return_value = mock_file
        
        # Act
        with patch('os.path.exists', return_value=False):
            config = load_config('test.json')
        
        # Assert
        assert config == {"test": "data"}
        mock_open_text.assert_called_once()