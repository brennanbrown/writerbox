---
title: This has malformed frontmatter
category: fiction
tags: [test, edge-case
date: invalid-date-format
---

This file has malformed YAML frontmatter. The tags array is not closed properly and the date is invalid.

WriterBox should handle this gracefully and not crash. It should either:
1. Skip the malformed parts and use what it can
2. Treat the entire file as having no frontmatter
3. Show an error but continue running

The exact behavior depends on how robust the frontmatter parsing is. This is an important edge case to test.
