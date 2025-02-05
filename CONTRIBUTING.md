# Guía de Contribución

¡Gracias por tu interés en contribuir a DevTooling CLI! Este documento proporciona las pautas y procesos para contribuir al proyecto.

## 🤝 Proceso de Contribución

1. **Fork & Clone**
   - Haz un fork del repositorio
   - Clona tu fork localmente
   ```bash
   git clone https://github.com/TU-USERNAME/devtooling-cli.git
   ```

2. **Configuración**
   - Instala las dependencias necesarias
   ```bash
   pip install -r requirements.txt
   ```
   - Configura el entorno virtual (recomendado)
   ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. **Crear una nueva rama**

```bash	   
git checkout -b feature/nombre-caracteristica
# o
git checkout -b fix/nombre-bug
```

4. **Convenciones de Código**

Sin definir...

5. **Commits**
   - Asegúrate de escribir mensajes de commit detallados y significativos
   - Utiliza el formato 

     ```
    <tipo>[(scope)]: <descripción>
    [cuerpo opcional]
     ```

   - Tipos: feat, fix, docs, style, refactor, test

   - Ejemplo: `feat(git): add .gitignore create functionality`

6. **Testing**

- Añade tests para nuevas características
- Asegúrate de que todos los tests pasan
- Mantén o mejora la cobertura de código


# 📝 Añadiendo Nuevas Características

## Reglas de Detección
Para añadir soporte para un nuevo tipo de proyecto:

1. Actualiza detection_rules.json
2. Añade reglas de ignorar en ignore_rules.json
3. Documenta el nuevo tipo en README.md

## Nuevas Funcionalidades

1. Discute la idea en Issues
2. Sigue la estructura del proyecto
3. Actualiza la documentación
4. Añade tests

# 🐛 Reportando Bugs
1. Usa la plantilla de issues
2. Incluye:
    - Versión del sistema
    - Pasos para reproducir
    - Comportamiento esperado vs actual
    - Logs relevantes

# 📋 Pull Requests

1. Actualiza el CHANGELOG.md
2. Referencia issues relacionados
3. Actualiza la documentación
4. Espera review
5. Responde a feedback

# 🚀 Release Process

1. Versioning semántico (MAJOR.MINOR.PATCH)
2. Actualiza version en setup.py
3. Actualiza CHANGELOG.md
4. Crea tag de versión

# ⚖️ Código de Conducta

* Se respetuoso
* Acepta feedback constructivo
* Enfócate en lo mejor para la comunidad
* Muestra empatía

# 📮 Contacto

- Issues de GitHub
- Discusiones de GitHub
- Email: schmidtnahuel09@gmail.com