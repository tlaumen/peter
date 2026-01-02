# Test configuration loading functionality
import os
import tempfile
import pytest
from peter.config import load_config, create_default_config, validate_config
from peter.models import Question

def test_load_config():
    """Test loading questions from .peter file."""
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.peter', delete=False) as f:
        f.write("""# Test Questions

- Test question 1
- Test question 2
- Test question 3
""")
        config_file = f.name
    
    try:
        questions = load_config(config_file)
        assert len(questions) == 3
        assert questions[0].question == "Test question 1"
        assert questions[1].question == "Test question 2"
        assert questions[2].question == "Test question 3"
        assert questions[0].priority == 3  # Default priority
        print("✅ Config loading test passed")
    finally:
        os.unlink(config_file)

def test_load_config_with_stars():
    """Test loading questions that start with * instead of -."""
    # Create a temporary config file with * bullets
    with tempfile.NamedTemporaryFile(mode='w', suffix='.peter', delete=False) as f:
        f.write("""# Test Questions

* Star question 1
* Star question 2
""")
        config_file = f.name
    
    try:
        questions = load_config(config_file)
        assert len(questions) == 2
        assert questions[0].question == "Star question 1"
        assert questions[1].question == "Star question 2"
        assert questions[0].priority == 3  # Default priority
        print("✅ Config with * bullets test passed")
    finally:
        os.unlink(config_file)

def test_create_default_config():
    """Test creating default config file."""
    with tempfile.NamedTemporaryFile(suffix='.peter', delete=False) as f:
        config_file = f.name
    
    try:
        create_default_config(config_file)
        
        # Check that file was created
        assert os.path.exists(config_file)
        
        # Check that it contains expected content
        with open(config_file, 'r') as f:
            content = f.read()
            assert "Daily Todo Questions" in content
            assert "What are your top 3 priorities for today?" in content
            print("✅ Default config creation test passed")
    finally:
        os.unlink(config_file)

def test_validate_config():
    """Test config validation."""
    # Valid config
    valid_questions = [
        Question("Question 1", 3),
        Question("Question 2", 2)
    ]
    assert validate_config(valid_questions) == True
    
    # Empty config
    assert validate_config([]) == False
    
    # Config with invalid structure
    invalid_questions = [
        Question("Question 1", 3),
        "invalid_item"
    ]
    assert validate_config(invalid_questions) == False
    
    # Config with empty question
    invalid_questions = [
        Question("Question 1", 3),
        Question("", 2)
    ]
    assert validate_config(invalid_questions) == False
    
    # Config with invalid priority
    invalid_questions = [
        Question("Question 1", 3),
        Question("Question 2", 0)
    ]
    assert validate_config(invalid_questions) == False
    
    print("✅ Config validation test passed")

if __name__ == "__main__":
    test_load_config()
    test_load_config_with_stars()
    test_create_default_config()
    test_validate_config()
    print("All config tests passed!")
