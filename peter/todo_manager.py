# Core todo management logic
import os
import re
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from typing import List, Dict, Any
from .models import Question, Answer, Todo

def process_todos(questions: List[Question]):
    """
    Process todos by asking questions and saving responses.
    
    Args:
        questions (List[Question]): List of Question objects with priority
    """
    # Get current date for filename
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = "peter.md"
    
    # Create styled prompt
    style = Style.from_dict({
        'question': 'bold fg:ansicyan',
        'answer': 'fg:ansigreen',
        'date': 'bold fg:ansiyellow',
    })
    
    print(f"\n📝 Daily Todo Manager - {today}")
    print("=" * 50)
    print("Answer the following questions (press Ctrl+C to cancel):")
    print()
    
    # Collect answers
    answers = []
    for i, question_data in enumerate(questions, 1):
        try:
            question_text = question_data.question
            default_priority = question_data.priority
            
            # Show question
            print(f"Question {i}: {question_text}")
            
            # Prompt for priority with default value
            priority_input = prompt(f"Priority (default {default_priority}): ", style=style)
            
            # Use default priority if empty
            if not priority_input or not priority_input.strip():
                priority = default_priority
            else:
                try:
                    priority = int(priority_input)
                except ValueError:
                    print(f"Invalid priority '{priority_input}', using default {default_priority}")
                    priority = default_priority
            
            # Collect all answers for this question
            answer_number = 1
            while True:
                # Get user answer
                answer = prompt(f"Answer {answer_number}: ", style=style)
                
                # Handle empty input
                if not answer or not answer.strip():
                    answer = "nothing"
                
                # Skip saving todos with "nothing" answers
                if answer.lower().strip() != "nothing":
                    answers.append(Answer(question_text, answer, priority))
                    print(f"✅ Answer {answer_number} saved")
                else:
                    print("ℹ️  Empty answer skipped (no todo created)")
                
                # Ask if user wants to add another answer
                if answer_number > 1:
                    add_more = prompt("Add another answer? (y/n, default n): ", style=style)
                else:
                    add_more = prompt("Add another answer? (y/n, default n): ", style=style)
                
                # Default to yes if empty or invalid input
                if add_more.lower().strip() in ['y', 'yes']:
                    answer_number += 1
                    print()
                    continue
                else:
                    break
            print("\n")
            print('-'*50)
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return
        except Exception as e:
            print(f"Error getting answer: {e}")
            # Skip creating todo for empty answers
            # Continue with default priority and "nothing" as answer
            # But don't add to the answers list
            # answers.append(Answer(question_text, "nothing", default_priority))
    
    # Save to markdown file
    save_todos_to_markdown(answers, today, output_file)
    
    print(f"✅ Todos saved to {output_file}")

def save_todos_to_markdown(answers: List[Answer], date: str, output_file: str):
    """
    Save todos to markdown file.
    
    Args:
        answers (List[Answer]): List of Answer objects
        date (str): Date string
        output_file (str): Output filename
    """
    # Check if file exists and if we need to append or create new
    file_exists = os.path.exists(output_file)
    
    # Create markdown content
    content = []
    
    if not file_exists:
        content.append("# Daily Todos")
        content.append("")
    
    # Add date section
    content.append(f"## {date}")
    content.append("")
    
    # Add questions, answers, and priorities
    for item in answers:
        content.append(f"- **Question**: {item.question}")
        content.append(f"  - **Answer**: {item.answer}")
        content.append(f"  - **Priority**: {item.priority}")
        content.append("")
    
    # Write to file
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"📝 Saved {len(answers)} todos for {date}")

def parse_todos_from_markdown(file_path: str) -> List[Todo]:
    """
    Parse TODO entries from markdown file.
    
    Args:
        file_path (str): Path to the markdown file
        
    Returns:
        List[Todo]: List of Todo objects with their status
    """
    if not os.path.exists(file_path):
        return []
    
    todos = []
    current_date = ""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for date section
        if line.startswith("## "):
            current_date = line[3:].strip()
        elif line.startswith("- **Question**:"):
            # Parse a TODO entry
            question = line[15:].strip()  # Remove "- **Question**: "
            
            # Look for answer and priority in following lines
            answer = "nothing"
            priority = 999 # default
            completed = False
            
            # Check next lines for answer and priority
            j = i + 1
            while j < len(lines) and not lines[j].startswith("- **Question**:") and not lines[j].startswith("## "):
                content_line = lines[j].strip()
                if content_line.startswith("- **Answer**:"):
                    answer = content_line[12:].strip()  # Remove "- **Answer**: "
                elif content_line.startswith("- **Priority**:"):
                    priority = int(content_line[15:].strip())  # Remove "- **Priority**: "
                elif content_line.startswith("- **Completed**:"):
                    completed = content_line[14:].strip().lower() == "true"
                j += 1
            
            todos.append(Todo(question, answer, priority, completed, current_date))
        
        i += 1
    
    return todos

def list_open_todos(todos: List[Todo]) -> List[Todo]:
    """
    Filter and return only open (incomplete) TODOs.
    
    Args:
        todos (List[Todo]): List of all TODO objects
        
    Returns:
        List[Todo]: List of open TODO objects
    """
    # Filter out completed todos AND todos with empty answers ("nothing")
    return [todo for todo in todos if not todo.completed and todo.answer.lower() != "nothing"]

def mark_todo_completed(todos: List[Todo], index: int) -> List[Todo]:
    """
    Mark a specific TODO as completed.
    
    Args:
        todos (List[Todo]): List of all TODO objects
        index (int): Index of the TODO to mark as completed
        
    Returns:
        List[Todo]: Updated list of TODO objects
    """
    if 0 <= index < len(todos):
        todos[index].completed = True
    return todos

def save_todos_to_markdown_with_status(todos: List[Todo], output_file: str):
    """
    Save todos to markdown file with completion status.
    
    Args:
        todos (List[Todo]): List of Todo objects
        output_file (str): Output filename
    """
    # Group todos by date
    dated_todos = {}
    for todo in todos:
        date = todo.date
        if date not in dated_todos:
            dated_todos[date] = []
        dated_todos[date].append(todo)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Daily Todos\n\n")
        
        # Write each date section
        for date in sorted(dated_todos.keys()):
            f.write(f"## {date}\n\n")
            for todo in dated_todos[date]:
                f.write(f"- **Question**: {todo.question}\n")
                f.write(f"  - **Answer**: {todo.answer}\n")
                f.write(f"  - **Priority**: {todo.priority}\n")
                f.write(f"  - **Completed**: {todo.completed}\n\n")
    
    print(f"📝 Updated todos saved to {output_file}")

def create_sample_config():
    """Create a sample .peter file for testing."""
    sample_content = """# Daily Todo Questions

- What are your top 3 priorities for today? [priority:3]
- What potential obstacles might you face? [priority:2]
- What progress have you made on your priorities? [priority:3]
- What adjustments do you need to make? [priority:2]
- What did you accomplish today? [priority:1]
- What are you looking forward to tomorrow? [priority:1]
"""
    
    with open('.peter', 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print("Created sample .peter file")
