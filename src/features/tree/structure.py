import os
from typing import List, Optional
from rich.console import Console
import questionary
import logging

class TreeVisualizer:
    def __init__(self):
        self.console = Console()
        self.logger = logging.getLogger('devtooling')
        self.ignored_dirs = []

    def set_ignored_dirs(self, dirs: List[str]):
        """Set the ignored directories for the tree visualizer."""
        self.ignored_dirs = dirs

    def select_directories(self, path: str) -> List[str]:
        """Allows the user to select directories to show."""
        try:
            elements = [d for d in os.listdir(path) 
                        if os.path.isdir(os.path.join(path, d))]
            
            selecteds = questionary.checkbox(
                "Select directories to show:",
                choices=[{'name': e, 'checked': True} for e in elements],
                qmark=" ",
                pointer="→"
            ).ask()
            
            self.logger.debug(f"Directories selected: {selecteds}")
            return selecteds if selecteds else []
            
        except Exception as e:
            self.logger.error(f"Error selecting directories: {str(e)}")
            raise

    def show_structure(
        self,
        path: str,
        prefix: str = "",
        is_last: bool = True,
        allowed: Optional[List[str]] = None,
        level: int = 0,
        show_all: bool = False
    ):
        """Shows the directory structure recursively."""
        try:
            if not os.path.exists(path):
                self.logger.warning(f"Path does not exist: {path}")
                return

            name = os.path.basename(path)

            # If we are in the root level and there are allowed directories
            if level == 0 and allowed:
                # Show only the root
                self.console.print(f"{prefix}[cyan]{name}/[/cyan]")

                # Process only the allowed directories
                items = [d for d in allowed if os.path.isdir(os.path.join(path, d))]
                items.sort()

                # Show each allowed directory
                for idx, item in enumerate(items):
                    is_last_item = idx == len(items) - 1
                    item_path = os.path.join(path, item)
                    self.show_structure(
                        item_path,
                        prefix + "    ",
                        is_last_item,
                        None,
                        level + 1,
                        show_all
                    )
                return

            # Verify if should be ignored
            if not show_all and any(ignore_dir in name for ignore_dir in self.ignored_dirs):
                return

            # Show current element (for non-root levels)
            if level > 0:
                if os.path.isdir(path):
                    self.console.print(
                        f"{prefix}{'└── ' if is_last else '├── '}[cyan]{name}/[/cyan]"
                    )
                else:
                    self.console.print(
                        f"{prefix}{'└── ' if is_last else '├── '}[yellow]{name}[/yellow]"
                    )

            # Process subdirectories
            if os.path.isdir(path):
                # Sort elements (directories first)
                items = sorted(
                    os.listdir(path),
                    key=lambda x: (not os.path.isdir(os.path.join(path, x)), x)
                )

                # Filter ignored elements
                if not show_all:
                    items = [i for i in items if i not in self.ignored_dirs]

                # New prefix for subdirectories
                new_prefix = prefix + ("    " if is_last else "│   ")

                # Show each element
                for idx, item in enumerate(items):
                    is_last_item = idx == len(items) - 1
                    item_path = os.path.join(path, item)
                    self.show_structure(
                        item_path,
                        new_prefix,
                        is_last_item,
                        None,
                        level + 1,
                        show_all
                    )

        except Exception as e:
            self.logger.error(f"Error showing structure: {str(e)}")
            raise