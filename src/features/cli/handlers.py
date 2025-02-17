from ...core.detector import ProjectDetector
from ..tree.structure import TreeVisualizer
import logging

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