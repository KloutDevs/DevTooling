# DevTooling CLI Testing Documentation

This document outlines the testing strategy for DevTooling CLI, including different types of tests, their coverage, and use cases.

## 🎯 Testing Goals

- Ensure the precise and accurate detection of project types
- Validate the correct inheritance of project detection rules
- Verify the funcionality of the command-line interface
- Guarantee the persistence of correctly configured settings
- Check the proper handling of errors and exceptions

## 📋 Test Types

### 1. Core Tests
#### ProjectDetector (`test_detector.py`)
- [ ] Detection of project type
  - Verification of correct detection of common projects (React, Node, Python, etc.)
  - Validation of project detection priorities
  - Checking handling of empty/invalid directories

- [ ] Detection of multiple technologies
  - Verification of detection of included technologies
  - Validate detection hierarchy
  - Checking inclusion rules

- [ ] Ignore System
  - Verificate ignore patterns for project types
  - Validate inheritance of ignore rules
  - Check special cases

### 2. Features Tests
#### TreeVisualizer (`test_structure.py`)
- [ ] Visualización de estructura
  - Verificar generación correcta del árbol
  - Validar filtrado de directorios
  - Comprobar modos de visualización (automático, manual, completo)

#### ProjectManager (`test_projects.py`)
- [ ] Gestión de carpetas
  - Verificar añadir/remover carpetas
  - Validar escaneo de proyectos
  - Comprobar persistencia de configuración

- [ ] Navegación de proyectos
  - Verificar navegación a proyectos
  - Validar búsqueda por nombre/ruta
  - Comprobar manejo de errores

#### CLI Arguments (`test_cli.py`)
- [ ] Procesamiento de argumentos
  - Verificar parsing de comandos
  - Validar opciones y flags
  - Comprobar manejo de errores

### 3. Utils Tests
#### Configuration (`test_config.py`)
- [ ] Manejo de configuración
  - Verificar carga/guardado de configuración
  - Validar versionado
  - Comprobar inicialización

## 🔍 Metodología

1. **Tests Unitarios**
   - Uso de `pytest` como framework principal
   - Implementación de fixtures para casos comunes
   - Mocking de sistema de archivos cuando sea necesario

2. **Tests de Integración**
   - Verificación de interacción entre componentes
   - Pruebas de flujos completos
   - Validación de casos de uso reales

3. **Tests de Sistema**
   - Pruebas de CLI en diferentes entornos
   - Validación de instalación y configuración
   - Verificación de experiencia de usuario

## 📊 Cobertura

- Objetivo: >80% de cobertura de código
- Foco en componentes críticos (detector, configuración)
- Inclusión de casos edge y errores comunes

## 🚀 Ejecución

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests específicos
pytest tests/test_detector.py
pytest tests/test_structure.py

# Ejecutar con cobertura
pytest --cov=devtooling tests/

## 📝 Convenciones

1. Nombrado de Tests:

```bash
def test_should_detect_react_project():
def test_should_handle_invalid_path():
```

2. Organización

- Un archivo de test por módulo
- Uso de fixtures compartidos
- Documentación clara de casos de prueba

3. Aserciones

- Uso de aserciones descriptivas
- Mensajes claros de error
- Validación completa de estados

## 🔄 Proceso de Testing

1. Verificar casos positivos y negativos
2. Incluir casos edge y situaciones inesperadas
3. Documentar cambios y decisiones
4. Mantener tests actualizados con cambios de código

## 📈 Estado Actual

| Módulo   | Cobertura| Estado          |
|----------|----------|------------------|
| Core     | 98%      | ✅ Completado  |
| Features | 93%      | ✅ Completado   |
| Utils    | ~65%      | 🟡 En Progreso  |

### Últimas Actualizaciones

#### Core Tests - ProjectDetector (✅ Completado)
- Detección de proyecto simple (React, Python, Flask)
- Manejo de rutas inválidas
- Detección de múltiples tecnologías
- Sistema de ignorado de directorios
- Manejo de directorios vacíos
- Prioridades de detección
- Cobertura: 98% del módulo

#### Features Tests - TreeVisualizer (✅ Completado)
- Establecer directorios ignorados
- Validación de configuración
- Selección manual de directorio con questionary
- Manejo de directorios vacíos
- Filtrado de directorios ignorados
- Visualización de estructura completa
- Manejo de directorios permitidos
- Control de profundidad máxima
- Manejo de rutas inválidas
- Cobertura: 93% del módulo

#### Utils Tests - Configuration (🟡 En Progreso)
✅ Tests Exitosos (12/15):
- Carga de configuración
  - Carga de detection_rules.json
  - Carga de projects.json
  - Manejo de archivos faltantes
  - Manejo de JSON inválido
- Guardado de configuración
  - Guardado básico
  - Creación de directorios
  - Manejo de permisos
- Gestión de rutas
  - Configuración en desarrollo
  - Manejo de proyectos inexistentes
  - Carga desde recursos del paquete
  - Creación de directorios anidados
- Versionado
  - Obtención de versión

❌ Tests Fallidos (3/15):
1. Configuración en producción
   - Error: FileNotFoundError en mock_meipass
2. Copia de reglas en producción
   - Error: FileNotFoundError en creación de directorios
3. Fallback a recursos del paquete
   - Error: AttributeError en pkg_resources.open_text

#### 📊 Métricas de Testing:
- Total de Tests: 31
- Tests Pasados: 28
- Tests Fallidos: 3
- Cobertura General: 29%
- Cobertura por Módulos:
  - Core/detector.py: 98%
  - Features/structure.py: 93%
  - Utils/config.py: 90%
  - Utils/logger.py: 34%
  - Utils/updater.py: 36%
  - Utils/file_handler.py: 0%

### Próximos Pasos
1. Corregir Tests de Configuración:
   - Mejorar mocking de sys._MEIPASS
   - Corregir manejo de directorios temporales
   - Actualizar importación de pkg_resources

2. Implementar Tests Pendientes:
   - CLI Arguments (18% cobertura)
   - CLI Handlers (12% cobertura)
   - Project Manager (17% cobertura)
   - Project Navigator (33% cobertura)

3. Iniciar Tests de:
   - file_handler.py (0% cobertura)
   - main.py (0% cobertura)
   - UI Components (0% cobertura)

### Problemas Identificados
1. Mocking de Entorno:
   - Problemas con sys._MEIPASS en tests de producción
   - Dificultades con pkg_resources.open_text

2. Manejo de Archivos:
   - Errores en creación de directorios temporales
   - Problemas con permisos y rutas

3. Cobertura Baja:
   - Módulos CLI sin cobertura suficiente
   - Componentes UI sin tests
   - Utilidades sin tests completos