import questionary
import time
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from src.core import ProjectDetector
from ..features.tree.structure import TreeVisualizer
from .banner import Banner
from ..utils.config import get_version

class Menu:
    def __init__(self):
        self.console = Console()
        self.detector = ProjectDetector()
        self.visualizer = TreeVisualizer()
        self.banner = Banner()
        self.logger = logging.getLogger('devtooling')

    def show_progress(self, message: str):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(f"[cyan]{message}[/cyan]", total=None)
            time.sleep(1)
            progress.update(task, completed=True)
            
    def show_structure_menu(self):
        while True:
            self.banner.show()
            opcion = questionary.select(
                "Select an option:",
                choices=[
                    "1. Automatic mode (with filters)",
                    "2. Manual folder selection",
                    "3. Complete structure",
                    "← Back to main menu"
                ],
                qmark="→",
                pointer="❯"
            ).ask()

            if not opcion:
                continue

            if opcion.startswith("←"):
                break

            opcion = opcion[0]

            try:
                if opcion == "1":
                    self.automatic_mode()
                elif opcion == "2":
                    self.manual_mode()
                elif opcion == "3":
                    self.complete_mode()
                
                # Wait for user input before continuing
                input("\nPress Enter to continue...")
                
            except Exception as e:
                self.logger.error(f"Error: {str(e)}")
                self.console.print(f"[red]Error: {str(e)}[/red]")
                time.sleep(2)

    def show_project_info(self, project_type: str, ignored_dirs: list):
        info_panel = Panel(
            f"[cyan]Project Type:[/cyan] [yellow]{project_type.upper()}[/yellow]\n"
            f"[cyan]Ignoring:[/cyan] [yellow]{', '.join(ignored_dirs)}[/yellow]",
            title="[blue]Project Information[/blue]",
            border_style="cyan"
        )
        self.console.print(info_panel)

    def automatic_mode(self):
        try:
            projectPath = questionary.path(
                "Project path:",
                only_directories=True
            ).ask()

            if not projectPath:
                return

            self.logger.info(f"Analyzing project in: {projectPath}")
            self.show_progress("Analyzing project")

            project_type = self.detector.detect_project_type(projectPath)
            ignored_dirs = self.detector.get_ignored_dirs(projectPath)

            self.show_project_info(project_type, ignored_dirs)

            # Set ignored directories in visualizer
            self.visualizer.set_ignored_dirs(ignored_dirs)

            self.show_progress("Generating structure")
            self.visualizer.show_structure(projectPath)

        except Exception as e:
            self.logger.error(f"Error in automatic mode: {str(e)}")
            raise

    def manual_mode(self):
        try:
            projectPath = questionary.path(
                "Project path:",
                only_directories=True
            ).ask()
            
            if not projectPath:
                return
            
            self.logger.info(f"Manual mode in: {projectPath}")
            allowedDirs = self.visualizer.select_directories(projectPath)
            
            if allowedDirs:
                self.show_progress("Generating view")
                self.visualizer.show_structure(projectPath, allowed=allowedDirs)
            
        except Exception as e:
            self.logger.error(f"Error in manual mode: {str(e)}")
            raise

    def complete_mode(self):
        try:
            projectPath = questionary.path(
                "Project path:",
                only_directories=True
            ).ask()
            
            if not projectPath:
                return
            
            self.logger.info(f"Showing complete structure of: {projectPath}")
            self.show_progress("Generating complete structure")
            self.visualizer.show_structure(projectPath, show_all=True)
            
        except Exception as e:
            self.logger.error(f"Error in complete mode: {str(e)}")
            raise

    def show(self):
        while True:
            try:
                self.banner.show()
                opcion = questionary.select(
                    "\nSelect an option:",
                    choices=[
                        "1. Structure view",
                        "Exit"
                    ],
                    qmark="→",
                    pointer="❯"
                ).ask()

                if not opcion:
                    continue
                
                if opcion == "Exit":
                    self.logger.info("Program finished by user")
                    self.console.print("\n[green]Thanks for using DevTooling CLI![/green]")
                    break
                elif opcion.startswith("1"):
                    self.show_structure_menu()

            except KeyboardInterrupt:
                self.logger.info("Program interrupted by user")
                continue
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                self.console.print(f"[red]Error: {str(e)}[/red]")
                time.sleep(1)
                continue