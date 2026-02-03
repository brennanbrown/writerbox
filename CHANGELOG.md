# WriterBox Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha] - 2025-02-02

### Added
- Terminal-based UI for markdown file management using Textual
- YAML frontmatter parsing for metadata extraction
- Categorized file display with expandable tree view
- Keyboard navigation and shortcuts
- File preview with markdown syntax highlighting
- Color-coded metadata (date in red, word count in orange, time in green, tags in blue)
- Sorting functionality (date, title, word count)
- Editor integration with suspend/resume for seamless editing
- Startup screen with welcome message and instructions
- Responsive layout that adapts to terminal size
- File statistics display (files, categories, total words, reading time)
- Help modal with comprehensive keyboard shortcuts
- Category icons and visual hierarchy
- Support for recursive directory scanning
- CLI with multiple options (--dir, --recursive, --sort)

### Fixed
- Fixed Enter key to toggle categories and open files
- Removed dropdown arrows from file nodes
- Fixed "No file selected" notification appearing on category expansion
- Resolved micro editor crashes with proper terminal state management
- Fixed footer formatting to single line
- Resolved startup screen key binding issues

### Technical
- Uses Rich for markdown rendering and syntax highlighting
- Implements proper suspend/resume pattern for external editors
- Custom Tree widget for enhanced file navigation
- Clean separation of concerns between UI, scanner, and CLI modules

## [Unreleased]

### Planned Features
- Search and filtering capabilities
- Configuration system
- Tag management
- Export functionality
- Plugin system

## [0.1.0] - Future Release

### Planned Features
- Terminal-based UI for markdown file management
- YAML frontmatter parsing
- Categorized file display
- Keyboard navigation
- Configuration system
- Search and filtering capabilities
