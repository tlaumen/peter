"""
Data models for the peter todo application.
"""
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Question:
    """Data class representing a question with priority."""
    question: str
    priority: int

@dataclass
class Answer:
    """Data class representing an answer to a question with priority."""
    question: str
    answer: str
    priority: int
