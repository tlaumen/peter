# Configuration handling for .peter files
import os
import re
from typing import List, Dict, Any

def load_config(config_file: str) -> List[Dict[str, Any]]:
    """
    Load questions with priorities from .peter config file.
    
    Args:
        config_file (str): Path to the .peter file
        
    Returns:
        List[Dict[str, Any]]: List of question dictionaries with priority
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse markdown content to extract questions and priorities
        lines = content.strip().split('\n')
        questions = []
        
        for line in lines:
            line = line.strip()
            # Match lines that start with - or * followed by whitespace
            if line.startswith('- ') or line.startswith('* '):
                # Extract question and check for priority
                question_text = line[2:].strip()
                
                # Look for priority in the format: "Question text [priority:3]"
                priority = 3  # Default priority
                if '[priority:' in question_text:
                    # Extract priority from the question text
                    import re
                    priority_match = re.search(r'\[priority:(\d+)\]', question_text)
                    if priority_match:
                        priority = int(priority_match.group(1))
                        # Remove priority from question text
                        question_text = re.sub(r'\[priority:\d+\]', '', question_text).strip()
                
                if question_text:  # Only add non-empty questions
                    questions.append({
                        'question': question_text,
                        'priority': priority
                    })
        
        return questions
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file {config_file} not found")
    except Exception as e:
        raise Exception(f"Error reading config file: {e}")

def create_default_config(config_file: str):
    """
    Create a default .peter config file.
    
    Args:
        config_file (str): Path where to create the config file
    """
    default_content = """# Daily Todo Questions

- What are your top 3 priorities for today? [priority:3]
- What potential obstacles might you face? [priority:2]
- What progress have you made on your priorities? [priority:3]
- What adjustments do you need to make? [priority:2]
- What did you accomplish today? [priority:1]
- What are you looking forward to tomorrow? [priority:1]
"""
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(default_content)
    
    print(f"Created default config file: {config_file}")

def validate_config(questions: List[Dict[str, Any]]) -> bool:
    """
    Validate that the config contains valid questions.
    
    Args:
        questions (List[Dict[str, Any]]): List of question dictionaries to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not questions:
        return False
    for q in questions:
        if not isinstance(q, dict) or 'question' not in q or 'priority' not in q:
            return False
        if not isinstance(q['question'], str) or not q['question'].strip():
            return False
        if not isinstance(q['priority'], int) or q['priority'] < 1:
            return False
    return True
