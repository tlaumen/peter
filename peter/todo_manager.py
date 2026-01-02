# Core todo management logic
import os
import re
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from typing import List, Dict, Any
from .models import Question, Answer

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
            
            # Get user answer
            answer = prompt("Answer: ", style=style)
            
            # Handle empty input
            if not answer or not answer.strip():
                answer = "nothing"
            
            answers.append(Answer(question_text, answer, priority))
            print()
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return
        except Exception as e:
            print(f"Error getting answer: {e}")
            # Continue with default priority and "nothing" as answer
            answers.append(Answer(question_text, "nothing", default_priority))
    
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
