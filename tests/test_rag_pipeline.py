import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from chatbot.rag_pipeline import extract_student_name


def test_extracts_name_after_about():
    assert extract_student_name("Tell me about Alice Smith") == "Alice Smith"


def test_extracts_name_with_what_is():
    assert extract_student_name("What is Bob Johnson's discipline?") == "Bob Johnson"


def test_returns_none_for_general_question():
    assert extract_student_name("Hello, what can you do?") is None


def test_handles_extra_whitespace():
    assert extract_student_name("show me   diana   prince") == "Diana Prince"
