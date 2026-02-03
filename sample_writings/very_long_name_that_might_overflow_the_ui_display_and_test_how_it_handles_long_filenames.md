---
category: tests
title: Very Long Filename Test
tags: [ui, edge-case, filename]
---

This file has an extremely long filename to test how the UI handles it.

Long filenames can cause display issues in terminal applications, especially with limited width. WriterBox should either:
1. Truncate the filename with ellipsis
2. Wrap the filename to multiple lines
3. Show the filename in a scrolling view

This is an important edge case for ensuring the UI remains usable with various filename lengths.
