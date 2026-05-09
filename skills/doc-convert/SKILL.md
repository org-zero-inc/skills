---
name: doc-convert
description: Document format conversion tool supporting mutual conversion between common formats such as Markdown, HTML, DOCX, PDF, PPTX, and TXT. Uses Pandoc for format conversion, with PDF output auto-detecting LaTeX engine (pdflatex/xelatex/lualatex) or browser (Edge/Chrome/Firefox) Headless mode. Triggers this skill when users mention "document conversion", "md to html", "md to pdf", "md to docx", "docx to md", "html to md", "convert md to webpage", "convert docx to md", "document format conversion", "markdown to word", "word to markdown", "markdown to pdf", "html to pdf", "docx to pdf". Even if the user doesn't specify an exact format, this skill should trigger whenever document format conversion is involved.
---

# Document Format Conversion

Uses Pandoc to convert between common document formats. The script automatically identifies input/output formats based on file extensions. Cross-platform unified Python script (Windows/Linux/macOS).

## Prerequisites

- **Pandoc** must be installed. Run `pandoc --version` to check. If not installed:
  - Windows: `scoop install pandoc`
  - macOS: `brew install pandoc`
  - Linux: `sudo apt install pandoc` or `sudo dnf install pandoc`

- **PDF output** has two paths (script auto-detects, preferring LaTeX engine):
  1. **LaTeX engine** (preferred): Detects `pdflatex` > `xelatex` > `lualatex`, generates PDF directly via Pandoc's `--pdf-engine`
  2. **Browser Headless** (fallback): Detects in order `Edge` > `Chrome` > `Firefox`, renders HTML to PDF

## Supported Conversion Paths

| Source Format | →HTML | →PDF | →DOCX | →MD | →PPTX | →TXT |
|---------------|-------|------|-------|-----|-------|------|
| MD            | ✅    | ✅   | ✅    | —   | ✅    | ✅   |
| HTML          | —     | ✅   | ✅    | ✅  | —     | ✅   |
| DOCX          | ✅    | ✅   | —     | ✅  | —     | ✅   |
| ODT           | ✅    | ✅   | ✅    | ✅  | —     | ✅   |
| TXT           | ✅    | ✅   | ✅    | ✅  | —     | —    |

Extension mapping: `.md/.markdown`→Markdown, `.html/.htm`→HTML, `.docx`→DOCX, `.odt`→ODT, `.pdf`→PDF, `.pptx`→PPTX, `.txt`→Plain text, `.tex`→LaTeX, `.rst`→reStructuredText, `.org`→Org-mode, `.epub`→EPUB

## Core Workflow

### 1. Determine Input and Output

The user provides an input file path, optionally specifying an output file path. The script identifies formats based on extensions:

- If the user only provides an input file, **default output format**:
  - `.md` → `.html` (GitHub style)
  - `.docx` → `.md`
  - `.html` → `.md`
  - Others → `.html`

- If the user explicitly specifies an output file (e.g., `output.pdf`), the target format is determined by the output extension

### 2. Execute Conversion

Use `uv run python` to call `scripts/convert.py` in the skill directory:

```bash
uv run python "<skill-dir>/scripts/convert.py" --in-file "<input-file>" [--out-file "<output-file>"] [--title "<title>"] [--toc] [--no-preview]
```

**Parameter Description:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--in-file` | Yes | Input file path |
| `--out-file` | No | Output file path, auto-inferred from input by default |
| `--title` | No | Document title, defaults to filename |
| `--toc` | No | Generate Table of Contents |
| `--no-preview` | No | Do not auto-open preview (preview opens automatically after conversion by default) |

### 3. PDF Output Engine Detection Logic

When the target format is PDF, the script auto-detects available engines in the following order:

```
1. pdflatex  ─┐
2. xelatex   ─┤ LaTeX engine (Pandoc --pdf-engine direct generation)
3. lualatex  ─┘
4. Edge      ─┐
5. Chrome    ─┤ Browser Headless (HTML → PDF two-step conversion)
6. Firefox   ─┘
```

- **LaTeX engine**: Generates PDF directly via Pandoc's `--pdf-engine` parameter, higher output quality (supports math formulas, vector graphics), no intermediate HTML needed
- **Browser Headless**: First converts content to temporary HTML with GitHub CSS, then calls the browser to render as PDF
  - Edge/Chrome uses `--headless --disable-gpu --no-pdf-header-footer --print-to-pdf` parameters
  - Firefox uses `--headless --print-to-pdf` parameters

### 4. Format-Specific Handling

**→ HTML:**
- Automatically applies GitHub-style CSS (stylesheet at `scripts/css/github.css`)
- Centered layout, max width 980px, left/right padding 45px

**→ PDF (LaTeX engine):**
- Pandoc directly invokes LaTeX engine to compile output
- Native support for math formulas, syntax highlighting, etc.

**→ PDF (Browser fallback, two-step conversion):**
1. First generates HTML with GitHub CSS via Pandoc (temporary file)
2. Then calls Browser Headless to render HTML to PDF
- Automatically adds print styles (`scripts/css/print.css`): prevents headings/tables/code blocks from being split across pages
- Removes headers and footers (Edge/Chrome supports `--no-pdf-header-footer`)
- Temporary HTML file is automatically cleaned up after PDF generation

### 5. Typical Usage

```bash
# MD → HTML (default)
uv run python scripts/convert.py --in-file report.md

# MD → PDF (auto-detect LaTeX or browser engine)
uv run python scripts/convert.py --in-file report.md --out-file report.pdf

# MD → DOCX
uv run python scripts/convert.py --in-file report.md --out-file report.docx

# MD → PPTX
uv run python scripts/convert.py --in-file slides.md --out-file slides.pptx

# DOCX → MD
uv run python scripts/convert.py --in-file document.docx

# HTML → MD
uv run python scripts/convert.py --in-file page.html

# With table of contents
uv run python scripts/convert.py --in-file report.md --out-file report.pdf --toc

# Without auto-opening preview
uv run python scripts/convert.py --in-file report.md --no-preview
```

## Batch Conversion

```bash
# Convert all md files in directory to pdf (Bash / PowerShell)
# Bash:
for f in *.md; do
    uv run python scripts/convert.py --in-file "$f" --out-file "${f%.md}.pdf" --no-preview
done

# PowerShell:
Get-ChildItem -Filter "*.md" | ForEach-Object {
    uv run python scripts/convert.py --in-file $_.FullName --out-file ($_.FullName -replace '\.md$', '.pdf') --no-preview
}
```

## Error Handling

| Issue | Script Behavior |
|-------|-----------------|
| Pandoc not installed | Error with installation command hint |
| No LaTeX engine and no browser (PDF needed) | Error, prompting to install a LaTeX engine or browser |
| Input file does not exist | Error and exit |
| Unsupported format | Error with supported format list |
| Input and output files are the same | Error and exit |
| PDF generation timeout (15 seconds) | Error, intermediate HTML file preserved |
