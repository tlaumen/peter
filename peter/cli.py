# Main CLI interface using prompt-toolkit
import os
import sys
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from .config import load_config, create_default_config
from .todo_manager import process_todos
from .models import Question

def main():
    """Main entry point for the peter CLI tool."""
    try:
        # Check if .peter config exists, create default if not
        config_file = ".peter"
        if not os.path.exists(config_file):
            print("No .peter config found. Creating default configuration...")
            create_default_config(config_file)
            print("Default .peter config created. Please edit it with your questions and run peter again.")
            return 0
        
        # Load configuration
        questions = load_config(config_file)
        if not questions:
            raise ValueError("No questions found in .peter file. Please add questions and try again.")
        
        # Process todos
        process_todos(questions)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    sys.exit(main())
