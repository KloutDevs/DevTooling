from devtooling.features.projects import ProjectManager, ProjectNavigator
from devtooling.core.detector import ProjectDetector
from devtooling.features.tree.structure import TreeVisualizer
from devtooling.utils.updater import check_latest_version, update_package
from rich.table import Table
from rich.console import Console
import logging
import questionary

logger = logging.getLogger('devtooling')

def handle_structure_command(args):
    """Handle the structure command execution."""
    try:
        detector = ProjectDetector()
        visualizer = TreeVisualizer()

        if args.mode == 'automatic':
            logger.info(f"Showing automatic structure for: {args.path}")
            project_type = detector.detect_project_type(args.path)
            ignored_dirs = detector.get_ignored_dirs(args.path)
            visualizer.set_ignored_dirs(ignored_dirs)
            visualizer.show_structure(args.path)
        
        elif args.mode == 'manual':
            logger.info(f"Showing manual structure for: {args.path}")
            allowed_dirs = visualizer.select_directories(args.path)
            if allowed_dirs:
                visualizer.show_structure(args.path, allowed=allowed_dirs, level=0, is_last=True)
        
        elif args.mode == 'complete':
            logger.info(f"Showing complete structure for: {args.path}")
            visualizer.show_structure(args.path, show_all=True)

    except Exception as e:
        logger.error(f"Error handling structure command: {str(e)}")
        raise
    
def handle_projects_command(args):
    """Handle projects command execution."""
    manager = ProjectManager()
    navigator = ProjectNavigator()
    console = Console()

    try:
        if args.folders_add:
            console.print(f"[cyan]Adding folder: {args.folders_add}[/cyan]")
            if manager.add_folder(args.folders_add, args.low_level):
                projects_found = manager.refresh_folder(args.folders_add, args.low_level)
                console.print(f"[green]✓ Folder added successfully[/green]")
                console.print(f"[green]Found {projects_found} projects[/green]")
            else:
                console.print("[red]Failed to add folder[/red]")

        elif args.folders_remove:
            if manager.remove_folder(args.folders_remove):
                console.print("[green]✓ Folder removed successfully[/green]")
            else:
                console.print("[red]Folder not found[/red]")

        elif args.list:
            # Create table for folders
            folders_table = Table(title="[cyan]Watched Folders[/cyan]")
            folders_table.add_column("Path", style="green")
            folders_table.add_column("Scan Mode", style="blue")
            
            folders = manager.list_folders()
            if folders:
                for folder in folders:
                    folders_table.add_row(
                        folder["path"],
                        "Low Level" if folder.get("low_level") else "Deep Scan"
                    )
                console.print(folders_table)
            else:
                console.print("[yellow]No folders being watched[/yellow]")
            
            # Create table for projects
            projects = manager.config["projects"]
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
                
                console.print(projects_table)
            else:
                console.print("[yellow]No projects detected yet[/yellow]")

        elif args.refresh_folders:
            console.print("[cyan]Refreshing folders...[/cyan]")
            projects_found = manager.refresh_folder(low_level=args.low_level)
            console.print(f"[green]✓ Folders refreshed successfully[/green]")
            console.print(f"[green]Found {projects_found} projects[/green]")

        elif args.clear:
            if questionary.confirm("Are you sure you want to clear all folders and projects?").ask():
                manager.clear_config()
                console.print("[green]✓ Configuration cleared successfully[/green]")

        elif args.go:
            path = manager.get_project_path(args.go)
            if path and navigator.navigate_to(path):
                console.print(f"[green]✓ Navigating to: {path}[/green]")
            else:
                console.print("[red]Project not found[/red]")

    except Exception as e:
        logger.error(f"Error in projects command: {str(e)}")
        console.print(f"[red]Error: {str(e)}[/red]")

def handle_go_command(args):
    """Handle go command execution."""
    manager = ProjectManager()
    navigator = ProjectNavigator()
    console = Console()

    path = manager.get_project_path(args.project)
    if path:
        console.print(f"[cyan]Opening new terminal in: {path}[/cyan]")
        if navigator.navigate_to(path):
            console.print(f"[green]✓ Navigation successful[/green]")
        else:
            console.print("[red]Failed to navigate to path[/red]")
    else:
        console.print("[red]Project not found[/red]")
        
def handle_update_command(args):
    """Handle update command execution."""
    console = Console()
    current, latest = check_latest_version()
    
    if not latest:
        console.print("[green]You are already using the latest version![/green]")
        return
        
    console.print(f"[yellow]New version available: {latest}[/yellow]")
    console.print(f"[cyan]Current version: {current}[/cyan]")
    
    if questionary.confirm("Would you like to update now?", default=True).ask():
        console.print("[cyan]Updating package...[/cyan]")
        if update_package():
            console.print("[green]✓ Update successful! Please restart DevTooling.[/green]")
        else:
            console.print("[red]Failed to update package[/red]")