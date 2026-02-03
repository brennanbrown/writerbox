# WriterBox

<div align="center">
  <img src="https://raw.githubusercontent.com/brennanbrown/writerbox/main/assets/writerbox-logo.png" alt="WriterBox Logo" width="200">
  
  A terminal-based writing collection manager for organizing and browsing your markdown files.
  
  [![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/brennanbrown/writerbox)
</div>

## ✨ Features

- 🎨 **Beautiful TUI** - A gorgeous terminal interface built with Textual
- 📁 **Smart Scanning** - Automatically discovers markdown files with recursive scanning
- 🏷️ **Metadata Support** - Parses YAML frontmatter for categories, tags, and more
- 📖 **Live Preview** - Markdown syntax highlighting in the preview pane
- ⌨️ **Keyboard-First** - Full keyboard navigation with intuitive shortcuts
- 🎯 **Color-Coded** - Visual metadata display with color coding (date, words, time, tags)
- 🔄 **Seamless Editing** - Open files in your favorite editor and return seamlessly
- 📊 **Statistics** - Track total files, words, reading time, and categories
- 🔍 **Sorting Options** - Sort by date, title, or word count

## 🚀 Quick Start

### Installation

```bash
pip install writerbox
```

### Basic Usage

```bash
# Run in current directory
writerbox

# Specify a directory
writerbox --dir ~/my-writings

# Non-recursive scan
writerbox --no-recursive

# Sort by word count
writerbox --sort word_count
```

## 📋 Requirements

- Python 3.9+
- A terminal that supports true color (most modern terminals)
- Your favorite text editor (micro, vim, nano, VS Code, etc.)

## 🎮 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Open file / Toggle category |
| `↑↓` | Navigate up/down |
| `Space` | Toggle category expansion |
| `1-4` | Sort (newest/oldest/title/words) |
| `r` | Refresh file list |
| `?` | Show help |
| `q` or `Ctrl+Q` | Quit |

## 📝 File Format

WriterBox works with markdown files that include YAML frontmatter:

```yaml
---
category: essays
title: My Amazing Essay
tags: [writing, technology, thoughts]
date: 2025-01-15
---

# My Amazing Essay

Your content goes here...
```

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/brennanbrown/writerbox.git
cd writerbox

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run with sample files
writerbox --dir sample_writings

# Run tests
pytest
```

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👋 Attribution

Created by [Brennan Brown](https://brennan.day) • [GitHub](https://github.com/brennanbrown) • [Mastodon](https://mastodon.social/@brennan)

---

<div align="center">
  <sub>Built with ❤️ using Python, Textual, and Rich</sub>
</div>
