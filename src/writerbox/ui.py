"""Textual UI for WriterBox."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Footer, Header, Static, Tree
from textual import events
from rich.text import Text
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from writerbox.scanner import FileScanner, WritingFile

# Optional imports for markdown highlighting
try:
    import markdown
    from rich.console import Console
    from rich.markdown import Markdown as RichMarkdown
    from rich.syntax import Syntax
    from io import StringIO
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False


class StartupScreen(ModalScreen):
    """Startup screen with welcome message and instructions."""
    
    BINDINGS = [
        Binding("escape", "dismiss", "Continue"),
        Binding("enter", "dismiss", "Continue"),
        Binding("space", "dismiss", "Continue"),
    ]
    
    def compose(self) -> ComposeResult:
        with Container(id="startup-container"):
            yield Static(
                "╭─────────────────────────────────────────────────────────────╮\n"
                "│                                                             │\n"
                "│  ⭘  WriterBox v0.1.0                                        │\n"
                "│  A Terminal-Based Writing Collection Manager                │\n"
                "│                                                             │\n"
                "╰─────────────────────────────────────────────────────────────╯\n"
                "\n"
                "╭─ Welcome! ──────────────────────────────────────────────────╮\n"
                "│                                                             │\n"
                "│  WriterBox helps you organize and browse your markdown      │\n"
                "│  writing collection with a beautiful terminal interface.     │\n"
                "│                                                             │\n"
                "│  Features:                                                  │\n"
                "│  • Organize files by category                               │\n"
                "│  • Preview markdown with syntax highlighting                │\n"
                "│  • Sort by date, title, or word count                       │\n"
                "│  • Open files in your preferred editor                      │\n"
                "│  • Color-coded metadata for easy scanning                   │\n"
                "│                                                             │\n"
                "╰─────────────────────────────────────────────────────────────╯\n"
                "\n"
                "╭─ Keyboard Shortcuts ───────────────────────────────────────╮\n"
                "│                                                             │\n"
                "│  Enter        • Open file / Toggle category                 │\n"
                "│  Arrow Keys  • Navigate up/down/left/right                  │\n"
                "│  Space       • Toggle category expansion                    │\n"
                "│  1-4         • Sort by (date/newest, date/oldest, title,    │\n"
                "│               word count)                                   │\n"
                "│  r           • Refresh file list                            │\n"
                "│  ?           • Show help screen                             │\n"
                "│  q or Ctrl+Q • Quit the application                        │\n"
                "│                                                             │\n"
                "╰─────────────────────────────────────────────────────────────╯\n"
                "\n"
                "╭─ Get Started ───────────────────────────────────────────────╮\n"
                "│                                                             │\n"
                "│  • Files need YAML frontmatter with a 'category' field      │\n"
                "│  • Categories are automatically grouped                    │\n"
                "│  • Press Enter on any file to open it in your editor        │\n"
                "│                                                             │\n"
                "│  Repository: https://github.com/brennanbrown/writerbox      │\n"
                "│                                                             │\n"
                "╰─────────────────────────────────────────────────────────────╯\n"
                "\n"
                "Press Enter, Space, or Escape to continue...",
                id="startup-content"
            )
    
    CSS = """
    #startup-container {
        background: #24283b;
        border: solid #5fcfd0;
        width: 80;
        height: 35;
        padding: 1;
    }
    
    #startup-content {
        text-align: center;
        color: #c0caf5;
    }
    """


class HelpScreen(ModalScreen):
    """Help screen with keyboard shortcuts."""
    
    BINDINGS = [("escape", "dismiss", "Close")]
    
    def compose(self) -> ComposeResult:
        with Container(id="help-container"):
            yield Static(
                "╔════════════════════════════════════════════════════════════════╗\n"
                "║  ✨ WriterBox Help ✨                                          ║\n"
                "╚════════════════════════════════════════════════════════════════╝\n"
                "\n"
                "╭─ Navigation ──────────────────────────────────────────────────╮\n"
                "│  ↑/↓        - Navigate up/down                               │\n"
                "│  Enter      - Open selected file in editor                  │\n"
                "│  Space/Tab  - Expand/collapse category                      │\n"
                "│  Home/End   - Jump to top/bottom                            │\n"
                "╰───────────────────────────────────────────────────────────────╯\n"
                "\n"
                "╭─ Actions ──────────────────────────────────────────────────────╮\n"
                "│  r          - Refresh file list                             │\n"
                "│  q          - Quit WriterBox                                │\n"
                "│  ?          - Show this help                                │\n"
                "│  /          - Search files (not implemented yet)            │\n"
                "╰───────────────────────────────────────────────────────────────╯\n"
                "\n"
                "╭─ Sorting ──────────────────────────────────────────────────────╮\n"
                "│  1          - Sort by date (newest first)                   │\n"
                "│  2          - Sort by date (oldest first)                   │\n"
                "│  3          - Sort by title (A-Z)                           │\n"
                "│  4          - Sort by word count (longest first)            │\n"
                "│  --sort     - Set initial sort via CLI                     │\n"
                "╰───────────────────────────────────────────────────────────────╯\n"
                "\n"
                "╭─ Tips ─────────────────────────────────────────────────────────╮\n"
                "│  • Files need YAML frontmatter with 'category' field         │\n"
                "│  • Editor is auto-detected from $EDITOR or common editors   │\n"
                "│  • Files are indented (no arrows), categories expand       │\n"
                "│  • Categories have emoji icons and can be expanded        │\n"
                "╰───────────────────────────────────────────────────────────────╯\n"
                "\n"
                "Press [Escape] to close",
                id="help-content"
            )
    
    CSS = """
    #help-container {
        background: #24283b;
        border: solid #5fcfd0;
        width: 60;
        height: 25;
        padding: 1;
    }
    
    #help-content {
        text-align: left;
    }
    """


class WriterBoxTree(Tree):
    """Custom Tree widget with enhanced Enter key behavior."""
    
    def action_select_cursor(self) -> None:
        """Handle Enter key - toggle category or open file."""
        if self.cursor_node:
            # Check if this is a file node (has WritingFile data)
            if hasattr(self.cursor_node, 'data') and isinstance(self.cursor_node.data, WritingFile):
                # This is a file, trigger the open file action
                self.app.action_open_file()
            else:
                # This is a category, toggle expansion
                if self.cursor_node.is_expanded:
                    self.cursor_node.collapse()
                else:
                    self.cursor_node.expand()
    
    def action_toggle_node(self) -> None:
        """Handle Space key - toggle expansion for any node."""
        if self.cursor_node:
            if self.cursor_node.is_expanded:
                self.cursor_node.collapse()
            else:
                self.cursor_node.expand()


class WriterBoxUI(App):
    """Main WriterBox application."""
    
    BINDINGS = [
        Binding("enter", "open_file", "Open"),
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("?", "help", "Help"),
        Binding("escape", "escape", "Escape"),
        Binding("1", "sort_date_desc", "Newest"),
        Binding("2", "sort_date_asc", "Oldest"),
        Binding("3", "sort_title", "Title"),
        Binding("4", "sort_word_count", "Words"),
        Binding("ctrl+q", "quit", "Quit", priority=True),
    ]
    
    CSS = """
    /* Main app styles */
    Screen {
        background: #1a1b26;
    }
    
    /* Header styles */
    Header {
        background: #24283b;
        color: #c0caf5;
        text-align: center;
        content-align: center middle;
    }
    
    /* Tree styles */
    Tree {
        background: #24283b;
        border: solid #414868;
        color: #c0caf5;
        width: 1fr;
        height: 1fr;
    }
    
    Tree .tree-node--label {
        color: #c0caf5;
    }
    
    Tree .file-node .tree-node--label {
        color: #9ca0af;
    }
    
    #file-content {
        background: #24283b;
        border: solid #414868;
        color: #c0caf5;
        width: 1fr;
        height: 1fr;
        text-style: none;
        scrollbar-background: #414868;
        scrollbar-color: #565f89;
    }
    
    #file-content-inner {
        padding: 1;
    }
    
    #content-header {
        background: #414868;
        color: #c0caf5;
        padding: 0 1;
        height: 1;
        text-align: center;
    }
    
    /* Footer styles */
    #footer-box {
        background: #24283b;
        color: #9aa5ce;
        padding: 0 1;
        height: 1;
        text-align: center;
        text-style: italic;
    }
    
    /* Container styles */
    #main-container {
        height: 100%;
    }
    
    #content-area {
        height: 1fr;
    }
    
    /* Help content */
    #help-content {
        text-align: left;
    }
    
    .category-poetry {
        color: #5fcfd0;
    }
    
    .category-essays {
        color: #c678dd;
    }
    
    .category-journal {
        color: #98c379;
    }
    
    .category-drafts {
        color: #abb2bf;
    }
    
    .category-fiction {
        color: #e06c75;
    }
    
    .category-uncategorized {
        color: #9aa5ce;
    }
    
    .file-entry {
        color: #c0caf5;
    }
    
    .file-entry:hover {
        background: #414868;
    }
    
    .metadata {
        color: #565f89;
        text-style: italic;
    }
    
    .tags {
        color: #e0af68;
    }
    
    .tree-node--selected {
        background: #414868;
        border-left: solid #5fcfd0;
    }
    
    .tree-node--cursor .tree-node__label {
        text-style: bold;
    }
    
    Tree {
        background: #1a1b26;
    }
    
    TextArea {
        background: #24283b;
        border: solid #414868;
        color: #c0caf5;
    }
    """
    
    def __init__(self, directory: Path, recursive: bool = True, sort: str = "date_desc", show_startup: bool = False):
        super().__init__()
        self.directory = directory
        self.recursive = recursive
        self.sort = sort
        self.files: List[WritingFile] = []
        self.categories: Dict[str, List[WritingFile]] = {}
        self.current_file: WritingFile | None = None
        self.show_startup = show_startup
        
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # Set the title
        self.title = f"WriterBox v0.1.0 — by brennan.day • {self.directory.name}"
        
        # Load files
        self.load_files()
        
        # Show startup screen on first launch
        if self.show_startup:
            self.push_screen(StartupScreen())
        
    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        
        with Container(id="main-container"):
            # Main content area
            with Container(id="content-area"):
                with Horizontal():
                    # File tree
                    yield WriterBoxTree("Files", id="file-tree")
                    
                    # Content viewer
                    with Vertical():
                        yield Static("Select a file to view its content", id="content-header")
                        with ScrollableContainer(id="file-content"):
                            yield Static("", id="file-content-inner")
            
            # Footer with status - will be updated in load_files
            yield Static("", id="footer-box")
        
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # Set the title
        self.title = f"WriterBox v0.1.0 — by brennan.day • {self.directory.name}"
        
        # Load files
        self.load_files()
        
        # Show startup screen on first launch
        if hasattr(self, 'show_startup') and self.show_startup:
            self.push_screen(StartupScreen())
        
    def get_category_icon(self, category: str) -> str:
        """Get the icon for a category."""
        icons = {
            "poetry": "📝",
            "essays": "📚",
            "journal": "✍️",
            "drafts": "💭",
            "fiction": "📖",
            "uncategorized": "📄",
        }
        return icons.get(category.lower(), "📄")
        
    def load_files(self) -> None:
        """Load and display files."""
        scanner = FileScanner(self.directory, self.recursive)
        self.files = scanner.scan()
        self.categories = scanner.group_by_category(self.files)
        
        # Apply sorting to files within each category
        for category in self.categories:
            self.categories[category] = self.sort_files(self.categories[category])
        
        # Update footer with single line format
        footer = self.query_one("#footer-box", Static)
        total_files = len(self.files)
        total_categories = len(self.categories)
        total_words = sum(f.metadata['word_count'] for f in self.files)
        total_reading_time = sum(f.metadata['reading_time'] for f in self.files)
        
        sort_display = {
            "date_desc": "Newest",
            "date_asc": "Oldest", 
            "title": "Title",
            "word_count": "Words"
        }
        
        footer_text = (
            f"Files: {total_files} | "
            f"Categories: {total_categories} | "
            f"Words: {total_words:,} | "
            f"Time: {total_reading_time:.0f} min | "
            f"Sort: {sort_display.get(self.sort, self.sort)} | "
            "Shortcuts: Enter=Open q=Quit r=Refresh ?=Help 1-4=Sort"
        )
        footer.update(footer_text)
        
        # Populate the tree
        tree = self.query_one("#file-tree", Tree)
        tree.clear()
        
        if not self.files:
            # Empty state
            empty_node = tree.root.add("No files found")
            return
        
        for category, files in sorted(self.categories.items()):
            # Get category icon
            icon = self.get_category_icon(category)
            
            # Add category node with simple label
            category_label = f"{icon} {category.title()} ({len(files)} files)"
            category_node = tree.root.add(category_label)
            
            # Add files as leaf nodes (not expandable)
            for file in files:
                # Format file label with metadata
                file_label = self.format_file_label_simple(file)
                # Create the node and set its data
                file_node = category_node.add_leaf(file_label)
                file_node.data = file
                
        tree.root.expand()
        # Don't refresh to avoid clearing selection
        
    def sort_files(self, files: List[WritingFile]) -> List[WritingFile]:
        """Sort files based on the current sort method."""
        if self.sort == "date_desc":
            return sorted(files, key=lambda f: f.metadata['modified'], reverse=True)
        elif self.sort == "date_asc":
            return sorted(files, key=lambda f: f.metadata['modified'])
        elif self.sort == "title":
            return sorted(files, key=lambda f: f.title.lower())
        elif self.sort == "word_count":
            return sorted(files, key=lambda f: f.metadata['word_count'], reverse=True)
        else:
            # Default to date_desc
            return sorted(files, key=lambda f: f.metadata['modified'], reverse=True)
        
    def format_file_label_simple(self, file: WritingFile) -> str:
        """Format a file label for tree display with Rich text styling."""
        # Create a Rich Text object with styling
        text = Text()
        
        # Add filename (default color)
        text.append("  ")
        text.append(file.filename, style="default")
        text.append(" • ")
        
        # Add date in red
        text.append(file.metadata['modified'].strftime('%b %d'), style="red")
        text.append(" • ")
        
        # Add word count in orange/yellow
        text.append(f"{file.metadata['word_count']} words", style="yellow")
        text.append(" • ")
        
        # Add reading time in green
        reading_time = file.metadata['reading_time']
        if reading_time < 1:
            text.append("<1 min", style="green")
        elif reading_time == 1:
            text.append("~1 min", style="green")
        else:
            text.append(f"~{reading_time} min", style="green")
        
        # Add tags in light blue if they exist
        if file.tags:
            for tag in file.tags:
                text.append(f" #{tag}", style="bright_blue")
        
        return text
        
    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        """Called when a tree node is highlighted (cursor moves)."""
        # Only display content if this is a file node (has WritingFile data)
        if hasattr(event.node, 'data') and isinstance(event.node.data, WritingFile):
            self.display_file_content(event.node.data)
        # Don't do anything for category nodes - don't clear the content
            
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Called when a tree node is selected."""
        # Only display content if this is a file node (has WritingFile data)
        if hasattr(event.node, 'data') and isinstance(event.node.data, WritingFile):
            self.display_file_content(event.node.data)
        # Don't do anything for category nodes
            
    def display_file_content(self, file: WritingFile) -> None:
        """Display the content of a file with optional markdown highlighting."""
        content_widget = self.query_one("#file-content-inner", Static)
        header = self.query_one("#content-header", Static)
        
        if MARKDOWN_AVAILABLE:
            # Use Rich's Markdown component directly in Static
            content_widget.update(RichMarkdown(file.content, code_theme="monokai"))
        else:
            # Fallback to plain text
            content_widget.update(file.content)
        
        # Update header
        icon = self.get_category_icon(file.category)
        header.update(f"{icon} {file.filename} ({file.category})")
        self.current_file = file
        
    def get_editor(self) -> str:
        """Get the preferred text editor."""
        # Check environment variables
        editor = os.environ.get("EDITOR")
        if editor:
            return editor
            
        # Fallback to common editors
        editors = ["micro", "nano", "vim", "vi", "code"]
        for ed in editors:
            if subprocess.run(["which", ed], capture_output=True).returncode == 0:
                return ed
                
        return "nano"  # Default fallback
        
    def action_open_file(self) -> None:
        """Open the currently selected file in the preferred editor."""
        # Get the currently selected tree node
        tree = self.query_one("#file-tree", WriterBoxTree)
        
        if tree.cursor_node:
            # Check if this is a file node (has WritingFile data)
            if hasattr(tree.cursor_node, 'data') and isinstance(tree.cursor_node.data, WritingFile):
                # This is a file node, open it
                file_to_open = tree.cursor_node.data
                editor = self.get_editor()
                file_path = str(file_to_open.path)
                
                try:
                    # Use suspend as a context manager for proper terminal handling
                    with self.suspend():
                        # Simple, clean command without extra flags
                        os.system(f'{editor} "{file_path}"')
                except Exception as e:
                    # If anything fails, show the command to run manually
                    self.notify(f"Error: {e}. Run manually: {editor} {file_path}", severity="error")
                    return
                
                # Refresh the file list when returning
                self.load_files()
                self.notify(f"Returned from {editor}", severity="information")
            else:
                # This shouldn't happen since the Tree handles categories
                pass
        else:
            self.notify("No file selected", severity="warning")
                
    def action_refresh(self) -> None:
        """Refresh the file list."""
        self.load_files()
        self.notify("File list refreshed", severity="information")
        
    def action_sort_date_desc(self) -> None:
        """Sort by date (newest first)."""
        self.sort = "date_desc"
        self.load_files()
        self.notify("Sorted by date (newest first)", severity="information")
        
    def action_sort_date_asc(self) -> None:
        """Sort by date (oldest first)."""
        self.sort = "date_asc"
        self.load_files()
        self.notify("Sorted by date (oldest first)", severity="information")
        
    def action_sort_title(self) -> None:
        """Sort by title (A-Z)."""
        self.sort = "title"
        self.load_files()
        self.notify("Sorted by title (A-Z)", severity="information")
        
    def action_sort_word_count(self) -> None:
        """Sort by word count (longest first)."""
        self.sort = "word_count"
        self.load_files()
        self.notify("Sorted by word count (longest first)", severity="information")
        
    def action_help(self) -> None:
        """Show the help screen."""
        self.push_screen(HelpScreen())
        
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
        
    def action_escape(self) -> None:
        """Handle escape key."""
        # If help is shown, close it
        if self.screen_stack:
            self.pop_screen()
        else:
            # Otherwise, quit
            self.exit()


def run_ui(directory: Path, recursive: bool = True, sort: str = "date_desc") -> None:
    """Run the WriterBox UI."""
    app = WriterBoxUI(directory, recursive, sort)
    app.run()
