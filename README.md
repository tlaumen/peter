# Peter - CLI Todo Manager

A simple CLI tool for managing daily todos using prompt-toolkit.

## Features

- Interactive command-line interface using prompt-toolkit
- Configuration via `.peter` markdown file
- Daily todo management with markdown output
- Automatic handling of empty responses
- Priority management for todos

## Installation

### Using pip
```bash
pip install -e .
```

### Using uvx (recommended)
```bash
uvx peter
```

## Usage

1. Run the tool to create a default `.peter` config file:
```bash
python -m peter
```

2. Edit the `.peter` file to customize your daily questions with priorities:
```markdown
# Daily Todo Questions

- What are your top 3 priorities for today? [priority:3]
- What potential obstacles might you face? [priority:2]
- What progress have you made on your priorities? [priority:3]
- What adjustments do you need to make? [priority:2]
- What did you accomplish today? [priority:1]
- What are you looking forward to tomorrow? [priority:1]
```

3. Run the tool again to answer your questions:
```bash
python -m peter
```

4. Your answers will be saved to `peter.md` in markdown format with priority information.

## Files

- `.peter` - Configuration file with your daily questions (created automatically)
- `peter.md` - Output file with your daily todos (created automatically)

## Example Output

```markdown
# Daily Todos

## 2026-01-02

- **Question**: What are your top 3 priorities for today?
  - **Answer**: Complete project proposal, review team feedback, prepare presentation
  - **Priority**: 3

- **Question**: What did you accomplish today?
  - **Answer**: nothing
  - **Priority**: 1
```

## Requirements

- Python 3.11+
- prompt-toolkit
