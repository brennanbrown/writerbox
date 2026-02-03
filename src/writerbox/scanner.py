"""File scanning functionality for WriterBox."""

from pathlib import Path
from typing import List, Dict, Any
import frontmatter
from datetime import datetime


class WritingFile:
    """Represents a single writing file with metadata."""
    
    def __init__(self, path: Path):
        self.path = path
        self.filename = path.name
        self.frontmatter = {}
        self.content = ""
        self.metadata = {}
        
        # Load file content and parse frontmatter
        self._load()
        
    def _load(self):
        """Load file and parse frontmatter."""
        try:
            post = frontmatter.load(self.path)
            self.frontmatter = post.metadata
            self.content = post.content
            
        except Exception as e:
            print(f"Error loading {self.path}: {e}")
            # Treat as plain text file if frontmatter parsing fails
            try:
                self.content = self.path.read_text(encoding='utf-8')
                self.frontmatter = {}
            except Exception:
                self.content = ""
                self.frontmatter = {}
        
        # Always extract file metadata, even if frontmatter failed
        try:
            stat = self.path.stat()
            self.metadata = {
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "word_count": len(self.content.split()),
                "char_count": len(self.content),
                "line_count": len(self.content.splitlines()),
            }
            
            # Calculate reading time (assuming 200 words per minute)
            self.metadata["reading_time"] = max(1, self.metadata["word_count"] // 200)
        except Exception as e:
            print(f"Error getting metadata for {self.path}: {e}")
            # Set default metadata if stat fails
            self.metadata = {
                "created": datetime.now(),
                "modified": datetime.now(),
                "word_count": 0,
                "char_count": 0,
                "line_count": 0,
                "reading_time": 1,
            }
            
    @property
    def category(self) -> str:
        """Get the category from frontmatter, with fallback."""
        return self.frontmatter.get("category", "uncategorized")
        
    @property
    def title(self) -> str:
        """Get the title from frontmatter or filename."""
        return self.frontmatter.get("title", self.path.stem)
        
    @property
    def tags(self) -> List[str]:
        """Get tags from frontmatter."""
        tags = self.frontmatter.get("tags", [])
        
        # Handle different tag formats
        if isinstance(tags, str):
            # Handle YAML list format with newlines
            if '\n' in tags:
                # Split by newlines and clean up
                tag_list = []
                for line in tags.split('\n'):
                    line = line.strip()
                    # Remove YAML list markers
                    if line.startswith('- '):
                        line = line[2:]
                    if line:
                        tag_list.append(line)
                return tag_list
            else:
                # Single tag as string
                return [tags]
        elif isinstance(tags, list):
            # List of tags - clean each one
            return [str(tag).strip() for tag in tags if str(tag).strip()]
        
        return []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display."""
        return {
            "path": str(self.path),
            "filename": self.filename,
            "title": self.title,
            "category": self.category,
            "tags": self.tags,
            "created": self.metadata["created"],
            "modified": self.metadata["modified"],
            "word_count": self.metadata["word_count"],
            "char_count": self.metadata["char_count"],
            "line_count": self.metadata["line_count"],
            "reading_time": self.metadata["reading_time"],
        }


class FileScanner:
    """Scans directories for writing files."""
    
    def __init__(self, directory: Path, recursive: bool = True):
        self.directory = directory
        self.recursive = recursive
        
    def scan(self) -> List[WritingFile]:
        """Scan directory for markdown files."""
        files = []
        
        # Find all .md files
        if self.recursive:
            pattern = "**/*.md"
        else:
            pattern = "*.md"
            
        for path in self.directory.glob(pattern):
            if path.is_file():
                files.append(WritingFile(path))
                
        return files
        
    def group_by_category(self, files: List[WritingFile]) -> Dict[str, List[WritingFile]]:
        """Group files by category."""
        categories = {}
        
        for file in files:
            category = file.category
            if category not in categories:
                categories[category] = []
            categories[category].append(file)
            
        return categories
