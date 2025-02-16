from src.ui.menu import Menu
from src.utils.logger import setup_logging

def main():
    setup_logging()
    menu = Menu()
    menu.show()

if __name__ == "__main__":
    main()