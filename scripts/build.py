import os
import platform
import subprocess
import shutil

def build():
    # Determine the platform-specific separator
    is_windows = platform.system() == "Windows"
    separator = ";" if is_windows else ":"
    
    # Create a temporary config directory with default files
    temp_config = "temp_config"
    os.makedirs(temp_config, exist_ok=True)
    
    # Copy detection_rules.json
    shutil.copy2("config/detection_rules.json", f"{temp_config}/detection_rules.json")
    
    # Create default projects.json
    with open(f"{temp_config}/projects.json", "w") as f:
        f.write('{"folders": [], "projects": {}}')
    
    # Base command
    cmd = [
        "pyinstaller",
        "--name=devtool",
        "--onefile",
        "--clean",
        f"--add-data={temp_config}{separator}config",
        "--hidden-import=rich",
        "--hidden-import=questionary",
        "--hidden-import=appdirs",
        "--collect-all=pyfiglet",
    ]
    
    # Add icon according the platform
    #if is_windows:
    #    cmd.append("--icon=assets/icon.ico")
    #else:
    #    cmd.append("--icon=assets/icon.png")
    
    # Add the main file
    cmd.append("src/main.py")
    
    try:
        # Execute the command
        subprocess.run(cmd)
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_config, ignore_errors=True)

if __name__ == "__main__":
    build()