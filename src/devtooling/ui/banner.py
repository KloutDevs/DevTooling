import os
import time
import logging
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
import pyfiglet
from devtooling.utils.config import get_version

class Banner:
    def __init__(self):
        self.console = Console()
        self.logger = logging.getLogger('devtooling')

    def _clear_screen(self):
        """Limpia la pantalla."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _create_banner_text(self) -> str:
        """Crea el texto del banner."""
        try:
            # Now we use an ASCII art banner instead of pyfiglet
            return """
 ____              _____           _ _             
|  _ \  _____   _|_   _|__   ___ | (_)_ __   __ _ 
| | | |/ _ \ \ / / | |/ _ \ / _ \| | | '_ \ / _` |
| |_| |  __/\ V /  | | (_) | (_) | | | | | | (_| |
|____/ \___| \_/   |_|\___/ \___/|_|_|_| |_|\__, |
                                            |___/ 
"""
        except Exception as e:
            self.logger.error(f"Error creating banner: {str(e)}")
            return "DevTooling CLI"  # Fallback simple

    def show(self):
        """Shows the banner with animation."""
        try:
            self._clear_screen()
            self.console.print("\n")
            
            # Create banner
            banner_text = self._create_banner_text()
            
            # Create panel decorative
            panel = Panel(
                f"[magenta]{banner_text}[/magenta]",
                border_style="cyan",
                padding=(1, 2),
                title=f"[yellow]v{get_version()}[/yellow]",
                subtitle="[blue]By KloutDevs[/blue]"
            )
            
            # Show with animation
            with Live(panel, refresh_per_second=4):
                time.sleep(1)
            
            self.console.print("\n")
            
        except Exception as e:
            self.logger.error(f"Error showing banner: {str(e)}")
            # Show fallback in case of error
            self.console.print("\n[bold magenta]DevTooling CLI[/bold magenta]\n")