"""Tests for edge cases and special file handling."""

import pytest
from pathlib import Path
import tempfile

from writerbox.scanner import WritingFile, FileScanner


@pytest.fixture
def sample_writings_dir():
    """Use the actual sample_writings directory for testing."""
    return Path(__file__).parent.parent / "sample_writings"


class TestEdgeCases:
    """Test various edge cases in file handling."""
    
    def test_no_frontmatter_file(self, sample_writings_dir):
        """Test handling files with no frontmatter."""
        file_path = sample_writings_dir / "no_frontmatter.md"
        writing_file = WritingFile(file_path)
        
        assert writing_file.category == "uncategorized"
        assert writing_file.title == "no_frontmatter"
        assert writing_file.tags == []
        assert writing_file.content.startswith("This file has no YAML frontmatter")
    
    def test_malformed_frontmatter(self, sample_writings_dir):
        """Test handling files with malformed frontmatter."""
        file_path = sample_writings_dir / "malformed_frontmatter.md"
        # Should not raise an exception
        writing_file = WritingFile(file_path)
        
        # Should handle gracefully - either parse what it can or treat as no frontmatter
        assert hasattr(writing_file, 'category')
        assert hasattr(writing_file, 'content')
    
    def test_empty_file(self, sample_writings_dir):
        """Test handling empty files."""
        file_path = sample_writings_dir / "empty_file.md"
        writing_file = WritingFile(file_path)
        
        assert writing_file.category == "drafts"
        assert writing_file.title == "Empty File"
        assert writing_file.content == ""
        assert writing_file.metadata['word_count'] == 0
        assert writing_file.metadata['reading_time'] == 1
    
    def test_only_frontmatter(self, sample_writings_dir):
        """Test files with only frontmatter and no content."""
        file_path = sample_writings_dir / "only_frontmatter.md"
        writing_file = WritingFile(file_path)
        
        assert writing_file.category == "tests"
        assert writing_file.title == "Only Frontmatter"
        assert writing_file.content == ""
    
    def test_no_category_field(self, sample_writings_dir):
        """Test files without category field in frontmatter."""
        file_path = sample_writings_dir / "no_category.md"
        writing_file = WritingFile(file_path)
        
        # Should default to uncategorized
        assert writing_file.category == "uncategorized"
        assert writing_file.title == "No Category Field"
    
    def test_unicode_and_emoji(self, sample_writings_dir):
        """Test handling of unicode and emoji in content and metadata."""
        file_path = sample_writings_dir / "unicode_test_🎨.md"
        writing_file = WritingFile(file_path)
        
        assert writing_file.category == "journal"
        assert "🌟" in writing_file.title
        assert "🎨" in writing_file.tags
        assert "测试" in writing_file.content
        assert "اختبار" in writing_file.content
    
    def test_many_tags(self, sample_writings_dir):
        """Test files with many tags."""
        file_path = sample_writings_dir / "many_tags.md"
        writing_file = WritingFile(file_path)
        
        assert len(writing_file.tags) > 10
        assert "tag1" in writing_file.tags
        assert "very-long-tag-name-that-might-overflow" in writing_file.tags
    
    def test_quotes_in_title(self, sample_writings_dir):
        """Test quotes in title field."""
        file_path = sample_writings_dir / "quote_in_title.md"
        writing_file = WritingFile(file_path)
        
        assert "'" in writing_file.title
        # YAML parser removes outer quotes but keeps inner quotes
        assert writing_file.title == "Poem with 'quotes' in title"
    
    def test_newline_tag_format(self, sample_writings_dir):
        """Test YAML pipe format for tags."""
        file_path = sample_writings_dir / "newline_in_tags.md"
        writing_file = WritingFile(file_path)
        
        assert "first tag" in writing_file.tags
        assert "second tag" in writing_file.tags
        assert "third tag" in writing_file.tags
    
    def test_long_filename(self, sample_writings_dir):
        """Test handling of very long filenames."""
        file_path = sample_writings_dir / "very_long_name_that_might_overflow_the_ui_display_and_test_how_it_handles_long_filenames.md"
        writing_file = WritingFile(file_path)
        
        assert writing_file.filename == file_path.name
        assert len(writing_file.filename) > 80
    
    def test_special_characters_in_filename(self, sample_writings_dir):
        """Test special characters in filenames."""
        file_path = sample_writings_dir / "special-chars_!@#$%^&()_+.md"
        writing_file = WritingFile(file_path)
        
        assert "!" in writing_file.filename
        assert "@" in writing_file.filename
        assert "#" in writing_file.filename
        assert writing_file.category == "tests"
    
    def test_hidden_file_handling(self, sample_writings_dir):
        """Test handling of hidden files (dotfiles)."""
        hidden_file = sample_writings_dir / ".hidden_file.md"
        
        # File should exist
        assert hidden_file.exists()
        
        # Check if scanner includes it
        scanner = FileScanner(sample_writings_dir, recursive=False)
        files = scanner.scan()
        filenames = [f.filename for f in files]
        
        # Currently includes hidden files - this might change based on requirements
        assert ".hidden_file.md" in filenames
    
    def test_long_content(self, sample_writings_dir):
        """Test handling of files with long content."""
        file_path = sample_writings_dir / "long_essay.md"
        writing_file = WritingFile(file_path)
        
        assert writing_file.metadata['word_count'] > 500
        assert writing_file.metadata['reading_time'] > 2
        assert len(writing_file.content) > 2000
    
    def test_nested_directories(self, sample_writings_dir):
        """Test recursive scanning finds nested files."""
        scanner = FileScanner(sample_writings_dir, recursive=True)
        files = scanner.scan()
        
        # Should find nested files
        filenames = [f.filename for f in files]
        assert "nested_file.md" in filenames
        assert "deeper_file.md" in filenames
        
        # Check paths are correct
        nested_file = next(f for f in files if f.filename == "nested_file.md")
        assert "subdir" in str(nested_file.path)
        
        deeper_file = next(f for f in files if f.filename == "deeper_file.md")
        assert "deep/nested" in str(deeper_file.path)
    
    def test_non_recursive_excludes_nested(self, sample_writings_dir):
        """Test non-recursive mode excludes nested files."""
        scanner = FileScanner(sample_writings_dir, recursive=False)
        files = scanner.scan()
        
        # Should not find nested files
        filenames = [f.filename for f in files]
        assert "nested_file.md" not in filenames
        assert "deeper_file.md" not in filenames


class TestSorting:
    """Test sorting functionality with various file types."""
    
    def test_sort_by_date_with_edge_cases(self, sample_writings_dir):
        """Test sorting by date handles various date formats."""
        scanner = FileScanner(sample_writings_dir, recursive=True)
        files = scanner.scan()
        
        # Files with invalid dates should still be sortable
        sorted_files = sorted(files, key=lambda f: f.metadata['modified'])
        assert len(sorted_files) == len(files)
    
    def test_sort_by_title_with_special_chars(self, sample_writings_dir):
        """Test sorting by title with special characters."""
        scanner = FileScanner(sample_writings_dir, recursive=True)
        files = scanner.scan()
        
        # Sort by title should handle unicode and special chars
        sorted_files = sorted(files, key=lambda f: f.title.lower())
        assert len(sorted_files) == len(files)
    
    def test_sort_by_word_count_with_empty_files(self, sample_writings_dir):
        """Test sorting by word count with empty files."""
        scanner = FileScanner(sample_writings_dir, recursive=True)
        files = scanner.scan()
        
        # Empty files should have 0 words and sort correctly
        sorted_files = sorted(files, key=lambda f: f.metadata['word_count'])
        assert len(sorted_files) == len(files)
        
        # First file should have 0 or minimal words
        assert sorted_files[0].metadata['word_count'] >= 0
