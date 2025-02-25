from devtooling.ui.menu import Menu
from devtooling.utils.logger import setup_logging
from devtooling.features.cli.arguments import parse_args, process_args

def main():
    setup_logging()
    
    # Parse command line arguments
    args = parse_args()
    
    # Process arguments if any command was specified
    exit_code = process_args(args)
    
    # If no command was specified or process_args returns None,
    # launch interactive mode
    if exit_code is None:
        menu = Menu()
        menu.show()
    else:
        return exit_code

if __name__ == "__main__":
    main()