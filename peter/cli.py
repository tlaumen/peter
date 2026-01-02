# Main CLI interface using prompt-toolkit
import os
import sys
from datetime import datetime
import click
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog, checkboxlist_dialog
from prompt_toolkit.widgets import Dialog, Button, Box, CheckboxList
from prompt_toolkit.layout import Layout, HSplit, VSplit, FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import FormattedText
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
        
        # Sort todos by priority (1 highest) and then by date (older first)
        open_todos.sort(key=lambda x: (x.priority, x.date))
        
        # Create a simple text-based menu for selecting TODOs
        print("\n📋 Select TODOs to Close:")
        print("=" * 50)
        
        # Display all open todos with numbers
        for i, todo in enumerate(open_todos, 1):
            print(f"{i}. {todo.question}")
            print(f"   Priority: {todo.priority}")
            print(f"   Date: {todo.date}")
            print()
        
        print("Instructions:")
        print("- Enter numbers separated by spaces to select multiple TODOs")
        print("- Press Enter to submit your selection")
        print("- Press Ctrl+C to cancel")
        print()
        
        # Get user selection
        while True:
            try:
                selection_input = input("Enter TODO numbers (space-separated): ").strip()
                
                if not selection_input:
                    print("No selection made. Operation cancelled.")
                    return 0
                
                # Parse the selection
                selected_indices = []
                for num_str in selection_input.split():
                    try:
                        num = int(num_str)
                        if 1 <= num <= len(open_todos):
                            selected_indices.append(num - 1)  # Convert to 0-based index
                        else:
                            print(f"⚠️  Invalid number: {num}. Please enter numbers between 1 and {len(open_todos)}")
                            raise ValueError("Invalid number")
                    except ValueError:
                        print(f"⚠️  '{num_str}' is not a valid number. Please try again.")
                        raise ValueError("Invalid input")
                
                if not selected_indices:
                    print("No valid selections made. Please try again.")
                    continue
                
                # Remove duplicates while preserving order
                seen = set()
                unique_indices = []
                for idx in selected_indices:
                    if idx not in seen:
                        seen.add(idx)
                        unique_indices.append(idx)
                selected_indices = unique_indices
                
                # Get the selected todos
                selected_todos = [open_todos[i] for i in selected_indices]
                
                # Confirm selection
                print(f"\nSelected TODOs to close:")
                for i, todo in enumerate(selected_todos, 1):
                    print(f"  {i}. {todo.question}")
                
                confirm = input(f"\nConfirm closing {len(selected_todos)} TODO(s)? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    break
                elif confirm in ['n', 'no']:
                    print("Operation cancelled.")
                    return 0
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
                    continue
                    
            except ValueError:
                continue
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                return 0
        
        # Mark all selected todos as completed
        for selected_todo in selected_todos:
            # Find index in full todos list
            full_index = todos.index(selected_todo)
            mark_todo_completed(todos, full_index)
        save_todos_to_markdown_with_status(todos, "peter.md")
        print(f"✅ {len(selected_todos)} TODO(s) marked as completed:")
        for todo in selected_todos:
            print(f"   - {todo.question}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    cli()
