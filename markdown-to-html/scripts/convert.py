#!/usr/bin/env python3
"""
Markdown to HTML converter with VS Code documentation styling.
"""

import argparse
import os
import sys
from pathlib import Path

VSCODE_CSS = """
:root {
    --vscode-bg: #1e1e1e;
    --vscode-bg-light: #ffffff;
    --vscode-text: #d4d4d4;
    --vscode-text-light: #1e1e1e;
    --vscode-accent: #007acc;
    --vscode-border: #3c3c3c;
    --vscode-code-bg: #1e1e1e;
    --vscode-link: #3794ff;
}

[data-theme="light"] {
    --vscode-bg: #ffffff;
    --vscode-text: #1e1e1e;
    --vscode-border: #e0e0e0;
    --vscode-code-bg: #f5f5f5;
}

*, *::before, *::after {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
    line-height: 1.5;
    color: var(--vscode-text);
    background-color: var(--vscode-bg);
    margin: 0;
    padding: 0;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    line-height: 1.25;
}

h1 {
    font-size: 2rem;
    border-bottom: 1px solid var(--vscode-border);
    padding-bottom: 0.5rem;
    margin-top: 0;
}

h2 {
    font-size: 1.5rem;
    border-bottom: 1px solid var(--vscode-border);
    padding-bottom: 0.3rem;
}

h3 { font-size: 1.25rem; }
h4 { font-size: 1rem; }

p {
    margin: 0 0 1rem 0;
}

a {
    color: var(--vscode-link);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

code {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 0.9em;
    background-color: var(--vscode-code-bg);
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

pre {
    background-color: var(--vscode-code-bg);
    border: 1px solid var(--vscode-border);
    border-radius: 4px;
    padding: 1rem;
    overflow-x: auto;
    margin: 1rem 0;
}

pre code {
    background-color: transparent;
    padding: 0;
    border-radius: 0;
    font-size: 13px;
    line-height: 1.45;
}

blockquote {
    margin: 1rem 0;
    padding: 0.5rem 1rem;
    border-left: 4px solid var(--vscode-accent);
    background-color: rgba(0, 122, 204, 0.1);
    color: var(--vscode-text);
}

ul, ol {
    margin: 1rem 0;
    padding-left: 2rem;
}

li {
    margin: 0.25rem 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1rem 0;
}

th, td {
    border: 1px solid var(--vscode-border);
    padding: 0.5rem 1rem;
    text-align: left;
}

th {
    background-color: var(--vscode-code-bg);
    font-weight: 600;
}

hr {
    border: none;
    border-top: 1px solid var(--vscode-border);
    margin: 2rem 0;
}

img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}

.task-list-item {
    list-style-type: none;
    margin-left: -1.5rem;
}

.task-list-item input {
    margin-right: 0.5rem;
}
"""


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="container">
{content}
    </div>
    <script>
        // Theme toggle functionality
        const theme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', theme === 'light' ? 'light' : 'dark');
    </script>
</body>
</html>
"""


def convert_markdown_to_html(markdown_content: str, title: str = "Document") -> str:
    """Convert markdown to HTML with VS Code styling."""
    try:
        import markdown
    except ImportError:
        print("Installing markdown package with uv...")
        import subprocess
        try:
            subprocess.check_call(["uv", "pip", "install", "--system", "markdown"])
        except FileNotFoundError:
            try:
                subprocess.check_call(["pip", "install", "markdown"])
            except:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "--break-system-packages"])
        import markdown

    html_content = markdown.markdown(
        markdown_content,
        extensions=[
            'extra',
            'codehilite',
            'toc',
            'tables',
            'fenced_code'
        ]
    )

    return HTML_TEMPLATE.format(
        title=title,
        css=VSCODE_CSS,
        content=html_content
    )


def process_file(input_path: Path, output_path: Path) -> None:
    """Process a single markdown file."""
    print(f"Converting: {input_path} -> {output_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    title = input_path.stem.replace('-', ' ').replace('_', ' ').title()
    html_content = convert_markdown_to_html(markdown_content, title)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Successfully created: {output_path}")


def process_directory(input_dir: Path, output_dir: Path) -> None:
    """Process all markdown files in a directory."""
    md_files = list(input_dir.glob('*.md'))

    if not md_files:
        print(f"No markdown files found in {input_dir}")
        return

    print(f"Found {len(md_files)} markdown file(s)")

    for md_file in md_files:
        output_file = output_dir / f"{md_file.stem}.html"
        process_file(md_file, output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown files to HTML with VS Code documentation styling"
    )
    parser.add_argument(
        'input',
        nargs='?',
        default=None,
        help="Input markdown file or directory"
    )
    parser.add_argument(
        'output',
        nargs='?',
        default=None,
        help="Output HTML file or directory"
    )
    parser.add_argument(
        '-d', '--dir',
        dest='dir',
        help="Input directory containing markdown files"
    )
    parser.add_argument(
        '-o', '--output',
        dest='out',
        help="Output directory for HTML files"
    )
    parser.add_argument(
        '-t', '--template',
        help="Custom HTML template file"
    )
    parser.add_argument(
        '-c', '--css',
        help="Custom CSS file (overrides default VS Code styling)"
    )

    args = parser.parse_args()

    if args.css and os.path.exists(args.css):
        with open(args.css, 'r') as f:
            global VSCODE_CSS
            VSCODE_CSS = f.read()
        print(f"Using custom CSS: {args.css}")

    if args.dir and args.out:
        input_dir = Path(args.dir)
        output_dir = Path(args.out)
        process_directory(input_dir, output_dir)
    elif args.input is not None and args.output is not None:
        input_path = Path(args.input)
        output_path = Path(args.output)
        if input_path.is_dir():
            process_directory(input_path, output_path)
        else:
            process_file(input_path, output_path)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()