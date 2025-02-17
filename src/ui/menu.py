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
from ..features.projects import ProjectManager, ProjectNavigator
from .banner import Banner
from ..utils.config import get_version

class Menu:
    def __init__(self):
        self.console = Console()
        self.detector = ProjectDetector()
        self.visualizer = TreeVisualizer()
        self.project_manager = ProjectManager()
        self.navigator = ProjectNavigator()
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

    def show_projects_menu(self):
        """Show projects management menu."""
        while True:
            self.banner.show()
            option = questionary.select(
                "Select an option:",
                choices=[
                    "1. Add project folder",
                    "2. Remove project folder",
                    "3. List projects and folders",
                    "4. Refresh folders",
                    "5. Navigate to project",
                    "← Back to main menu"
                ],
                qmark="→",
                pointer="❯"
            ).ask()

            if not option:
                continue

            if option.startswith("←"):
                break

            try:
                if option.startswith("1"):
                    self.add_project_folder()
                elif option.startswith("2"):
                    self.remove_project_folder()
                elif option.startswith("3"):
                    self.list_projects()
                elif option.startswith("4"):
                    self.refresh_folders()
                elif option.startswith("5"):
                    self.navigate_to_project()
                
                input("\nPress Enter to continue...")
                
            except Exception as e:
                self.logger.error(f"Error: {str(e)}")
                self.console.print(f"[red]Error: {str(e)}[/red]")
                time.sleep(2)

    def add_project_folder(self):
        """Add a new project folder."""
        folder_path = questionary.path(
            "Enter folder path:",
            only_directories=True
        ).ask()

        if not folder_path:
            return

        low_level = questionary.confirm(
            "Use low-level scan? (only root and first level)",
            default=False
        ).ask()

        self.console.print(f"[cyan]Adding folder: {folder_path}[/cyan]")
        self.show_progress("Processing")

        if self.project_manager.add_folder(folder_path, low_level):
            projects_found = self.project_manager.refresh_folder(folder_path, low_level)
            self.console.print(f"[green]✓ Folder added successfully[/green]")
            self.console.print(f"[green]Found {projects_found} projects[/green]")
        else:
            self.console.print("[red]Failed to add folder[/red]")

    def remove_project_folder(self):
        """Remove a project folder."""
        folders = self.project_manager.list_folders()
        if not folders:
            self.console.print("[yellow]No folders being watched[/yellow]")
            return

        choices = [f["path"] for f in folders]
        folder_path = questionary.select(
            "Select folder to remove:",
            choices=choices,
            qmark="→",
            pointer="❯"
        ).ask()

        if folder_path:
            self.show_progress("Removing folder")
            if self.project_manager.remove_folder(folder_path):
                self.console.print("[green]✓ Folder removed successfully[/green]")
            else:
                self.console.print("[red]Failed to remove folder[/red]")

    def list_projects(self):
        """List all projects and folders."""
        # Create table for folders
        folders_table = Table(title="[cyan]Watched Folders[/cyan]")
        folders_table.add_column("Path", style="green")
        folders_table.add_column("Scan Mode", style="blue")
        
        folders = self.project_manager.list_folders()
        if folders:
            for folder in folders:
                folders_table.add_row(
                    folder["path"],
                    "Low Level" if folder.get("low_level") else "Deep Scan"
                )
            self.console.print(folders_table)
        else:
            self.console.print("[yellow]No folders being watched[/yellow]")
        
        # Create table for projects
        projects = self.project_manager.config["projects"]
        if projects:
            projects_table = Table(title="[cyan]Detected Projects[/cyan]")
            projects_table.add_column("Name", style="green")
            projects_table.add_column("Type", style="blue")
            projects_table.add_column("Path", style="yellow")
            
            for project in projects.values():
                projects_table.add_row(
                    project["name"],
                    project["type"],
                    project["path"]
                )
            
            self.console.print(projects_table)
        else:
            self.console.print("[yellow]No projects detected yet[/yellow]")

    def refresh_folders(self):
        """Refresh all project folders."""
        low_level = questionary.confirm(
            "Use low-level scan? (only root and first level)",
            default=False
        ).ask()

        self.console.print("[cyan]Refreshing folders...[/cyan]")
        self.show_progress("Scanning projects")
        
        projects_found = self.project_manager.refresh_folder(low_level=low_level)
        self.console.print(f"[green]✓ Folders refreshed successfully[/green]")
        self.console.print(f"[green]Found {projects_found} projects[/green]")

    def navigate_to_project(self):
        """Navigate to a selected project."""
        projects = self.project_manager.config["projects"]
        if not projects:
            self.console.print("[yellow]No projects available[/yellow]")
            return

        choices = [f"{p['name']} ({p['type']})" for p in projects.values()]
        selected = questionary.select(
            "Select project to navigate to:",
            choices=choices,
            qmark="→",
            pointer="❯"
        ).ask()

        if selected:
            project_name = selected.split(" (")[0]
            path = self.project_manager.get_project_path(project_name)
            
            if path:
                self.console.print(f"[cyan]Opening new terminal in: {path}[/cyan]")
                if self.navigator.navigate_to(path):
                    self.console.print(f"[green]✓ Navigation successful[/green]")
                else:
                    self.console.print("[red]Failed to navigate to path[/red]")

    def show(self):
        while True:
            try:
                self.banner.show()
                option = questionary.select(
                    "\nSelect an option:",
                    choices=[
                        "1. Structure view",
                        "2. Projects management",
                        "Exit"
                    ],
                    qmark="→",
                    pointer="❯"
                ).ask()

                if not option:
                    continue
                
                if option == "Exit":
                    self.logger.info("Program finished by user")
                    self.console.print("\n[green]Thanks for using DevTooling CLI![/green]")
                    break
                elif option.startswith("1"):
                    self.show_structure_menu()
                elif option.startswith("2"):
                    self.show_projects_menu()

            except KeyboardInterrupt:
                self.logger.info("Program interrupted by user")
                continue
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                self.console.print(f"[red]Error: {str(e)}[/red]")
                time.sleep(1)
                continue