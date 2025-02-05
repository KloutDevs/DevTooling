import os
import sys
import json
from colorama import init, Fore, Style
import questionary

# -------------------- Configuración inicial --------------------
init(autoreset=True)
directorios_ignorar = []
proyecto_tipo = None
# -------------------- Carga de reglas de detección --------------------
def cargar_reglas_deteccion():
    try:
        with open('detection_rules.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['rules']
    except FileNotFoundError:
        print(f"{Fore.RED}Error: No se encontró el archivo detection_rules.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: El archivo detection_rules.json tiene un formato inválido")
        sys.exit(1)
# -------------------- Carga de reglas de ignorados --------------------
def cargar_reglas_ignorar():
    try:
        with open('ignore_rules.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['rules']
    except FileNotFoundError:
        print(f"{Fore.RED}Error: No se encontró el archivo ignore_rules.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: El archivo ignore_rules.json tiene un formato inválido")
        sys.exit(1)
# -------------------- Lógica de detección de proyectos --------------------
def detectar_tipo_proyecto(ruta):
    # Definimos una función auxiliar para verificar archivos
    def tiene_archivo(archivos):
        return any(os.path.exists(os.path.join(ruta, archivo)) for archivo in archivos)

    # Cargamos las reglas desde el archivo JSON
    reglas_deteccion = cargar_reglas_deteccion()

    # Ordenamos las reglas por prioridad
    reglas_deteccion.sort(key=lambda x: x['prioridad'])

    # Detectamos todos los tipos que aplican
    tipos_detectados = set()
    
    for regla in reglas_deteccion:
        if tiene_archivo(regla['archivos']):
            tipos_detectados.add(regla['tipo'])
            # Agregamos las tecnologías implicadas
            if 'implica' in regla:
                tipos_detectados.update(regla['implica'])

    if not tipos_detectados:
        return 'otro'
    
    # Retornamos el tipo principal (el de mayor prioridad)
    for regla in reglas_deteccion:
        if regla['tipo'] in tipos_detectados:
            return regla['tipo']
        
def actualizar_ignorados(ruta):
    global directorios_ignorar
    reglas = cargar_reglas_ignorar()
    
    # Obtenemos todos los tipos detectados
    def detectar_todos_tipos(ruta):
        def tiene_archivo(archivos):
            return any(os.path.exists(os.path.join(ruta, archivo)) for archivo in archivos)

        reglas_deteccion = cargar_reglas_deteccion()
        tipos_detectados = set()
        
        for regla in reglas_deteccion:
            if tiene_archivo(regla['archivos']):
                tipos_detectados.add(regla['tipo'])
                # Agregamos las tecnologías implicadas
                if 'implica' in regla:
                    tipos_detectados.update(regla['implica'])
        
        return tipos_detectados

    # Detectamos todos los tipos presentes en el proyecto
    tipos_detectados = detectar_todos_tipos(ruta)
    
    # Acumulamos todos los directorios a ignorar basados en los tipos detectados
    directorios_ignorar = set()
    for tipo in tipos_detectados:
        if tipo in reglas:
            directorios_ignorar.update(reglas[tipo])
    
    # Convertimos el set de vuelta a lista
    directorios_ignorar = list(directorios_ignorar)
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
                actualizar_ignorados(ruta)  # Ahora pasamos la ruta en lugar del tipo
                print(f"{Fore.CYAN}[Tipo de Proyecto detectado: {proyecto_tipo.upper()}]")
                print(f"{Fore.CYAN}[Ignorando: {', '.join(directorios_ignorar)}]")  # Añadimos esto para ver qué se ignora
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