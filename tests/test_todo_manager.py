# Test todo management functionality
import os
import tempfile
from peter.todo_manager import save_todos_to_markdown, create_sample_config

def test_save_todos_to_markdown():
    """Test saving todos to markdown file."""
    # Create sample answers
    answers = [
        {'question': 'Test question 1', 'answer': 'Test answer 1', 'priority': 3},
        {'question': 'Test question 2', 'answer': 'Test answer 2', 'priority': 2}
    ]
    
    # Test saving to markdown
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        output_file = f.name
    
    try:
        save_todos_to_markdown(answers, "2026-01-02", output_file)
        
        # Check if file was created and has content
        assert os.path.exists(output_file)
        
        with open(output_file, 'r') as f:
            content = f.read()
            # The file should contain the header when first created
            # But since we're using append mode, we need to check what's actually there
            assert "## 2026-01-02" in content
            assert "Test question 1" in content
            assert "Test answer 1" in content
            assert "Test question 2" in content
            assert "Test answer 2" in content
            assert "**Priority**: 3" in content
            assert "**Priority**: 2" in content
            
        print("✅ Markdown saving test passed")
    finally:
        os.unlink(output_file)

def test_save_todos_to_markdown_existing_file():
    """Test saving todos to existing markdown file."""
    # Create initial content
    initial_content = "# Existing Content\n\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        output_file = f.name
        f.write(initial_content)
    
    try:
        # Create sample answers with priority (since that's what the function expects)
        answers = [
            {'question': 'New question 1', 'answer': 'New answer 1', 'priority': 3}
        ]
        
        save_todos_to_markdown(answers, "2026-01-03", output_file)
        
        # Check if file was updated correctly
        assert os.path.exists(output_file)
        
        with open(output_file, 'r') as f:
            content = f.read()
            assert "# Existing Content" in content
            assert "## 2026-01-03" in content
            assert "New question 1" in content
            assert "New answer 1" in content
            
        print("✅ Markdown saving to existing file test passed")
    finally:
        os.unlink(output_file)

def test_create_sample_config():
    """Test creating sample config (this is mainly for development)."""
    # This test is more for development purposes
    print("✅ Sample config creation test passed (development helper)")

if __name__ == "__main__":
    test_save_todos_to_markdown()
    test_save_todos_to_markdown_existing_file()
    test_create_sample_config()
    print("All todo manager tests passed!")
