#!/usr/bin/env python3
"""Test script for WriterBox UI."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from writerbox.ui import run_ui

if __name__ == "__main__":
    sample_dir = Path(__file__).parent / "sample_writings"
    run_ui(sample_dir)
