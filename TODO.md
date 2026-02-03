# WriterBox TODO List

## ✅ Completed (v0.1.0-alpha)

### Project Setup
- [x] Initialize Python project structure
- [x] Set up pyproject.toml with dependencies
- [x] Initialize git repository

### Core Features Implementation

#### 1. File Discovery & Parsing
- [x] Implement directory scanning for .md files
- [x] Add recursive directory scanning option
- [x] Create YAML frontmatter parser
- [x] Extract file metadata (word count, character count, etc.)
- [x] Handle missing/malformed frontmatter gracefully

#### 2. Display & Organization
- [x] Set up Textual TUI framework
- [x] Create main application layout
- [x] Implement categorical grouping
- [x] Design file entry display format
- [x] Add ASCII art decorations
- [x] Implement sorting options
- [x] Add markdown syntax highlighting
- [x] Create responsive layout
- [x] Add color-coded metadata display

#### 3. Navigation & Interaction
- [x] Add keyboard navigation
- [x] Implement file opening functionality
- [x] Add help menu
- [x] Create startup screen
- [x] Fix Enter key behavior for categories/files

#### 4. Configuration
- [x] Implement command-line argument parsing
- [x] Add environment variable support for editor

### Testing
- [x] Write unit tests for file parsing

### Documentation
- [x] Create README.md
- [x] Write CHANGELOG.md

## 🚧 In Progress

### Testing
- [ ] Add integration tests for TUI
- [ ] Test cross-platform compatibility
- [ ] Performance testing with large directories

## 📋 TODO List

### Core Features
- [ ] Create search and filter features
- [ ] Add tag management system
- [ ] Implement export functionality (PDF, HTML, etc.)
- [ ] Add file templates
- [ ] Create plugin system

### Configuration
- [ ] Create config file system
- [ ] Create default configuration
- [ ] Add theme customization

### User Experience
- [ ] Add file bookmarks/favorites
- [ ] Implement recent files tracking
- [ ] Add file duplication/renaming
- [ ] Create batch operations
- [ ] Add dark/light theme toggle

### Advanced Features
- [ ] Full-text search across all files
- [ ] Link checking between files
- [ ] Word count goals/tracking
- [ ] Writing streaks
- [ ] Backup/sync system

### Documentation
- [ ] Write detailed user guide
- [ ] Document API
- [ ] Create contributing guidelines
- [ ] Add troubleshooting section

### Distribution
- [ ] Set up PyPI packaging
- [ ] Create installation scripts
- [ ] Write release notes
- [ ] Create homebrew formula
- [ ] Add snap package

### Development Tools
- [ ] Set up pre-commit hooks
- [ ] Add CI/CD pipeline
- [ ] Create development documentation
- [ ] Add performance profiling

## 🎯 Next Priority

1. **Search and Filter** - Find files quickly by name, tag, or content
2. **Configuration System** - Customizable settings and themes
3. **Integration Tests** - Ensure reliability across platforms
4. **PyPI Release** - Make it easily installable

---

*Last updated: 2025-02-02*
