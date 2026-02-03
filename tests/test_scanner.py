"""Tests for the file scanner module."""

import pytest
from pathlib import Path
from datetime import datetime
import tempfile
import os

from writerbox.scanner import WritingFile, FileScanner


@pytest.fixture
def temp_dir():
    """Create a temporary directory with test markdown files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_path = Path(tmpdir)
        
        # Create test files with different frontmatter
        test_files = {
            "poem1.md": """---
category: poetry
title: Spring Sonnet
tags: [nature, spring]
---

Roses are red,
Violets are blue,
Spring is here,
And so are you.
""",
            "essay1.md": """---
category: essays
title: On Technology
date: 2024-01-15
tags: technology
---

Technology is changing our world...
""",
            "no_frontmatter.md": """Just a plain markdown file.
No frontmatter here.
""",
        }
        
        for filename, content in test_files.items():
            (dir_path / filename).write_text(content)
            
        # Create a subdirectory with another file
        subdir = dir_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.md").write_text("""---
category: drafts
title: Nested Idea
---

A nested file.
""")
        
        yield dir_path


def test_writing_file_load(temp_dir):
    """Test WritingFile loads and parses correctly."""
    file_path = temp_dir / "poem1.md"
    writing_file = WritingFile(file_path)
    
    assert writing_file.category == "poetry"
    assert writing_file.title == "Spring Sonnet"
    assert writing_file.tags == ["nature", "spring"]
    assert writing_file.metadata["word_count"] == 13
    assert writing_file.metadata["reading_time"] == 1


def test_writing_file_no_frontmatter(temp_dir):
    """Test WritingFile handles missing frontmatter."""
    file_path = temp_dir / "no_frontmatter.md"
    writing_file = WritingFile(file_path)
    
    assert writing_file.category == "uncategorized"
    assert writing_file.title == "no_frontmatter"
    assert writing_file.tags == []


def test_filescanner_non_recursive(temp_dir):
    """Test FileScanner in non-recursive mode."""
    scanner = FileScanner(temp_dir, recursive=False)
    files = scanner.scan()
    
    # Should only find files in root directory
    assert len(files) == 3
    filenames = [f.filename for f in files]
    assert "poem1.md" in filenames
    assert "essay1.md" in filenames
    assert "no_frontmatter.md" in filenames
    assert "nested.md" not in filenames


def test_filescanner_recursive(temp_dir):
    """Test FileScanner in recursive mode."""
    scanner = FileScanner(temp_dir, recursive=True)
    files = scanner.scan()
    
    # Should find all files including nested
    assert len(files) == 4
    filenames = [f.filename for f in files]
    assert "nested.md" in filenames


def test_group_by_category(temp_dir):
    """Test grouping files by category."""
    scanner = FileScanner(temp_dir, recursive=True)
    files = scanner.scan()
    categories = scanner.group_by_category(files)
    
    assert "poetry" in categories
    assert "essays" in categories
    assert "drafts" in categories
    assert "uncategorized" in categories
    
    assert len(categories["poetry"]) == 1
    assert len(categories["essays"]) == 1
    assert len(categories["drafts"]) == 1
    assert len(categories["uncategorized"]) == 1
