import os
import platform
import subprocess

def build():
    # Determine the platform-specific separator
    is_windows = platform.system() == "Windows"
    separator = ";" if is_windows else ":"
    
    # Base command
    cmd = [
        "pyinstaller",
        "--name=devtool",
        "--onefile",
        "--clean",
        f"--add-data=config{separator}config",
        "--hidden-import=rich",
        "--hidden-import=questionary",
        "--collect-all=pyfiglet",
    ]
    
    # Add icon according the platform
    #if is_windows:
    #    cmd.append("--icon=assets/icon.ico")
    #else:
    #    cmd.append("--icon=assets/icon.png")
    
    # Add the main file
    cmd.append("src/main.py")
    
    # Execute the command
    subprocess.run(cmd)

if __name__ == "__main__":
    build()