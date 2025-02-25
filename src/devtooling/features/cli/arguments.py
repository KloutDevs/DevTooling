import argparse
from typing import Optional
from devtooling.utils.config import get_version
from devtooling.features.cli.handlers import handle_structure_command, handle_projects_command, handle_go_command

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='DevTooling CLI - A tool for project analysis and management',
        prog='devtool',
        usage="""
  DevTooling CLI - Project Analysis Tool

  Interactive mode:
    devtool

  Command line guide: () optional, [] required

  Structure commands:
    devtool structure --mode [MODE] [PROJECTS_PATH]

    Examples:
      devtool structure --mode automatic ./my-project
      devtool structure --mode manual .
      devtool structure --mode complete /path/to/project

  Projects commands:
    devtool projects --folders-add [PROJECTS_PATH] (--low-level)
    devtool projects --folders-remove [PROJECTS_PATH]
    devtool projects --list
    devtool projects --refresh-folders
    devtool projects --go [PROJECT_NAME]
    
    Examples:
      devtool projects --folders-add ./projects 
      devtool projects --folders-add ./projects --low-level
      devtool projects --folders-remove ./projects
      devtool projects --list
      devtool projects --refresh-folders
      devtool projects --go my-react-project
        """
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {get_version()}'
    )

    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        title='commands'
    )

    # Structure command
    structure_parser = subparsers.add_parser(
        'structure',
        help='Show project structure in different modes',
        description='Show the directory structure of a project with different viewing options'
    )
    
    structure_parser.add_argument(
        '-m', '--mode',
        choices=['automatic', 'manual', 'complete'],
        default='automatic',
        help='''Mode to show structure:
            automatic: show structure with intelligent filters
            manual: manually select directories to show
            complete: show complete structure without filters'''
    )

    structure_parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Project path to analyze (default: current directory)'
    )
    
    # Projects command
    projects_parser = subparsers.add_parser(
        'projects',
        help='Manage project folders and navigation'
    )
    
    projects_parser.add_argument(
        '--folders-add',
        metavar='PATH',
        help='Add a folder to watch for projects'
    )
    
    projects_parser.add_argument(
        '--low-level',
        action='store_true',
        help='Scan only root and first level directories'
    )
    
    projects_parser.add_argument(
        '--folders-remove',
        metavar='PATH',
        help='Remove a folder from watched folders'
    )
    
    projects_parser.add_argument(
        '--list',
        action='store_true',
        help='List all watched folders and projects'
    )
    
    projects_parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all folders and projects from configuration'
    )
    
    projects_parser.add_argument(
        '--refresh-folders',
        action='store_true',
        help='Refresh projects in all watched folders'
    )
    
    projects_parser.add_argument(
        '--go',
        metavar='PROJECT',
        help='Navigate to project by name or path'
    )
    
    # Go command (shortcut for projects --go)
    go_parser = subparsers.add_parser(
        'go',
        help='Navigate to project'
    )
    
    go_parser.add_argument(
        'project',
        help='Project name or path to navigate to'
    )

    return parser.parse_args()

def process_args(args) -> Optional[int]:
    """Process parsed arguments and execute corresponding commands."""
    if args.command == 'structure':
        handle_structure_command(args)
        return 0
    elif args.command == 'projects':
        handle_projects_command(args)
        return 0
    elif args.command == 'go':
        handle_go_command(args)
        return 0
    
    # If no command specified, return None to launch interactive mode
    return None