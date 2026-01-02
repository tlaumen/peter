# Main CLI interface using prompt-toolkit
import os
import sys
from datetime import datetime
import click
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog
from .config import load_config, create_default_config
from .todo_manager import process_todos, parse_todos_from_markdown, list_open_todos, mark_todo_completed, save_todos_to_markdown_with_status
from .models import Question, Todo

@click.group()
def cli():
    """Peter - CLI Todo Manager"""
    pass

@cli.command()
def run():
    """Run the todo manager (default behavior)"""
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

@cli.command()
def list():
    """List all open TODOs"""
    try:
        todos = parse_todos_from_markdown("peter.md")
        open_todos = list_open_todos(todos)
        
        # Filter out todos with empty answers ("nothing")
        filtered_todos = [todo for todo in open_todos if todo.answer.lower() != "nothing"]
        
        if not filtered_todos:
            print("✅ No open TODOs found.")
            return 0
        
        print("\n📋 Open TODOs:")
        print("=" * 50)
        for i, todo in enumerate(filtered_todos, 1):
            print(f"{i}. {todo.question}")
            print(f"   Answer: {todo.answer}")
            print(f"   Priority: {todo.priority}")
            print(f"   Date: {todo.date}")
            print()
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        raise

@cli.command()
def status():
    """Show status of all TODOs"""
    try:
        todos = parse_todos_from_markdown("peter.md")
        
        # Filter out todos with empty answers ("nothing") from display
        filtered_todos = [todo for todo in todos if todo.answer.lower() != "nothing"]
        
        if not filtered_todos:
            print("📝 No TODOs found.")
            return 0
        
        print("\n📊 All TODOs:")
        print("=" * 50)
        for i, todo in enumerate(filtered_todos, 1):
            status = "✅ Completed" if todo.completed else "⏳ Open"
            print(f"{i}. [{status}] {todo.question}")
            print(f"   Answer: {todo.answer}")
            print(f"   Priority: {todo.priority}")
            print(f"   Date: {todo.date}")
            print()
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        raise

@cli.command()
def close():
    """Close a TODO item"""
    try:
        todos = parse_todos_from_markdown("peter.md")
        open_todos = list_open_todos(todos)
        
        if not open_todos:
            print("✅ No open TODOs to close.")
            return 0
        
        # Create selection list using prompt-toolkit radiolist
        options = [(todo, f"{todo.question} (Priority: {todo.priority})") for todo in open_todos]
        
        # Use radiolist dialog for selection
        selected_todo = radiolist_dialog(
            title="Select TODO to Close",
            text="Choose a TODO item to mark as completed:",
            values=options
        ).run()
        
        if selected_todo:
            # Find index in full todos list
            full_index = todos.index(selected_todo)
            mark_todo_completed(todos, full_index)
            save_todos_to_markdown_with_status(todos, "peter.md")
            print(f"✅ TODO '{selected_todo.question}' marked as completed.")
        else:
            print("Operation cancelled.")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    cli()
