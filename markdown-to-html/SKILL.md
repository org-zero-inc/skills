---
name: markdown-to-html
description: |
  Convert markdown files to HTML with VS Code documentation styling.
  Use this skill when the user wants to transform markdown documents into standalone HTML files
  that match the visual style of code.visualstudio.com documentation. Triggers when user mentions:
  - "convert markdown to html"
  - "markdown to html"
  - "create html from markdown"
  - "generate html documentation"
  - any request to transform .md files into .html with specific styling
---

# Markdown to HTML Converter

This skill converts markdown files to HTML with embedded VS Code documentation styling.

## When to Use

Use this skill whenever the user wants to:
- Convert markdown files to HTML documents
- Create standalone HTML from markdown
- Generate documentation in VS Code docs style
- Transform .md files to .html with proper styling

## Requirements

- Python 3.8+ with `uv` package manager
- Required packages: `markdown`, `jinja2`

## Usage

### Single File Conversion

```bash
uv run python scripts/convert.py input.md output.html
```

### Batch Conversion

```bash
uv run python scripts/convert.py --dir input_folder --output output_folder
```

### Options

- `--dir, -d`: Directory containing markdown files
- `--output, -o`: Output directory for HTML files
- `--template, -t`: Custom HTML template (optional)
- `--css, -c`: Path to custom CSS file (optional, defaults to embedded VS Code style)

## Output

The converter produces standalone HTML files with:
- Embedded CSS matching VS Code documentation style
- Proper semantic HTML structure
- Responsive design
- Code block syntax highlighting
- Dark/light theme support

## Examples

**Input (example.md):**
```markdown
# Hello World

This is a paragraph with **bold** and *italic* text.

## Code Example

```python
def hello():
    print("Hello, World!")
```
```

**Output:** HTML file with VS Code docs styling applied.

## Troubleshooting

- If conversion fails, ensure markdown file has valid syntax
- Check that output directory exists and is writable
- For large files, conversion may take a few seconds