import os
import sys
from colorama import init, Fore, Style
import questionary

# -------------------- Configuración inicial --------------------
init(autoreset=True)
directorios_ignorar = []
proyecto_tipo = None

# -------------------- Lógica de detección de proyectos --------------------
def detectar_tipo_proyecto(ruta):
    detectores = [
        ('svelte', ['svelte.config.js']),
        ('nextjs', ['next.config.js']),
        ('node', ['package.json']),
        ('bun', ['bun.lockb']),
        ('yarn', ['yarn.lock']),
        ('python', ['requirements.txt', 'pyproject.toml', 'setup.py']),
        ('vue', ['vue.config.js']),
        ('react', ['tsconfig.json', 'react.config.js']),
        ('django', ['manage.py']),
        ('flask', ['app.py', 'wsgi.py']),
        ('angular', ['angular.json']),
        ('dotnet', ['*.csproj', '*.sln']),
        ('java', ['pom.xml', 'build.gradle']),
        ('rust', ['Cargo.toml']),
        ('go', ['go.mod'])
    ]

    for tipo, archivos in detectores:
        for archivo in archivos:
            if os.path.exists(os.path.join(ruta, archivo)):
                return tipo
    return 'otro'

def actualizar_ignorados(tipo_proyecto):
    global directorios_ignorar
    reglas = {
        'node': ['node_modules', 'dist', 'build'],
        'svelte': ['.svelte-kit', 'node_modules', 'build'],
        'nextjs': ['.next', 'node_modules'],
        'python': ['__pycache__', 'venv'],
        'vue': ['node_modules', 'dist', '.nuxt'],
        'react': ['node_modules', 'build', '.next'],
        'django': ['db.sqlite3', 'staticfiles'],
        'flask': ['__pycache__', 'venv'],
        'angular': ['node_modules', 'dist', '.nuxt'],
        'dotnet': ['bin', 'obj'],
        'java': ['target', '.gradle'],
        'rust': ['target', '.cargo'],
        'go': ['.git'],
        'otro': []
    }
    directorios_ignorar = reglas.get(tipo_proyecto, [])
# -------------------- Lógica de visualización corregida --------------------
def mostrar_estructura(ruta, prefijo="", es_ultimo=True, permitidos=None, nivel=0):
    if not os.path.exists(ruta):
        return

    nombre = os.path.basename(ruta)
    relativa = os.path.relpath(ruta, os.path.dirname(ruta))

    # Verificar si el directorio debe ser ignorado
    if nombre in directorios_ignorar:
        return

    # Lógica de filtrado
    if permitidos and nivel == 0 and nombre not in permitidos:
        return

    # Mostrar elemento actual
    if os.path.isdir(ruta):
        print(f"{prefijo}{'└── ' if es_ultimo else '├── '}{Fore.CYAN}{nombre}/")
    else:
        print(f"{prefijo}{'└── ' if es_ultimo else '├── '}{Fore.YELLOW}{nombre}")

    # Recursión para directorios
    if os.path.isdir(ruta):
        elementos = sorted(os.listdir(ruta), key=lambda x: (not os.path.isdir(os.path.join(ruta, x)), x))
        elementos = [e for e in elementos if e not in directorios_ignorar]  # Filtrar elementos ignorados
        nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")

        for i, elemento in enumerate(elementos):
            es_ultimo_elemento = i == len(elementos) - 1
            ruta_elemento = os.path.join(ruta, elemento)
            mostrar_estructura(ruta_elemento, nuevo_prefijo, es_ultimo_elemento, permitidos, nivel + 1)
# -------------------- Interfaz interactiva --------------------
def selector_directorios(ruta):
    elementos = os.listdir(ruta)
    seleccionados = questionary.checkbox(
        "Selecciona directorios a mostrar:",
        choices=[{'name': e, 'checked': True} for e in elementos if os.path.isdir(os.path.join(ruta, e))],
        qmark=" ",
        pointer="→"
    ).ask()
    
    return seleccionados if seleccionados else []

def menu():
    global proyecto_tipo
    while True:
        print(f"\n{Fore.MAGENTA}=== Herramientas Klout ===")
        print(f"{Fore.BLUE}1. Modo automático (con filtros)")
        print(f"{Fore.BLUE}2. Selección manual de carpetas")
        print(f"{Fore.BLUE}3. Estructura completa")
        print(f"{Fore.BLUE}4. Salir")
        
        opcion = input(f"{Fore.WHITE}Selecciona una opción: ").strip()
        
        if opcion == "1":
            ruta = input(f"{Fore.WHITE}Ruta del proyecto: ").strip()
            if os.path.exists(ruta):
                proyecto_tipo = detectar_tipo_proyecto(ruta)
                actualizar_ignorados(proyecto_tipo)
                print(f"{Fore.CYAN}[Detectado: {proyecto_tipo.upper()}]")
                mostrar_estructura(ruta, permitidos=[])
            else:
                print(f"{Fore.RED}✖ Ruta inválida")
                
        elif opcion == "2":
            ruta = input(f"{Fore.WHITE}Ruta del proyecto: ").strip()
            if os.path.exists(ruta):
                permitidos = selector_directorios(ruta)
                print("")
                if permitidos:
                    print(f"{Fore.CYAN}┌── {os.path.basename(ruta)}/")
                    for i, dir in enumerate(permitidos):
                        es_ultimo = i == len(permitidos) - 1
                        mostrar_estructura(
                            os.path.join(ruta, dir),
                            prefijo="│   " if not es_ultimo else "    ",
                            es_ultimo=es_ultimo,
                            permitidos=permitidos
                        )
                else:
                    print(f"{Fore.RED}No se seleccionaron directorios para mostrar")
            else:
                print(f"{Fore.RED}✖ Ruta inválida")
                
        elif opcion == "3":
            ruta = input(f"{Fore.WHITE}Ruta del proyecto: ").strip()
            if os.path.exists(ruta):
                mostrar_estructura(ruta, permitidos=None)
            else:
                print(f"{Fore.RED}✖ Ruta inválida")
                
        elif opcion == "4":
            print(f"{Fore.GREEN}¡Hasta luego!")
            sys.exit()
            
        else:
            print(f"{Fore.RED}✖ Opción inválida")

if __name__ == "__main__":
    menu()