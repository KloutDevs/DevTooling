import argparse
from typing import Optional
from ...utils.config import get_version
from .handlers import handle_structure_command

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='DevTooling CLI - A tool for project analysis and management',
        prog='devtool',
        usage="""
  DevTooling CLI - Project Analysis Tool

  Interactive mode:
    devtool

  Command line mode:
    devtool structure [--mode MODE] [PATH]
    
  Examples:
    devtool structure --mode automatic ./my-project
    devtool structure --mode manual .
    devtool structure --mode complete /path/to/project
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

    return parser.parse_args()

def process_args(args) -> Optional[int]:
    """Process parsed arguments and execute corresponding commands."""
    if args.command == 'structure':
        handle_structure_command(args)
        return 0
    
    # If no command specified, return None to launch interactive mode
    return None