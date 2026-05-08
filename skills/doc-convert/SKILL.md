---
name: doc-convert
description: 文档格式转换工具，支持 Markdown、HTML、DOCX、PDF、PPTX、TXT 等常见格式互转。使用 Pandoc 处理格式转换，PDF 输出自动检测 LaTeX 引擎（pdflatex/xelatex/lualatex）或浏览器（Edge/Chrome/Firefox）Headless 模式。当用户提到"文档转换"、"md转html"、"md转pdf"、"md转docx"、"docx转md"、"html转md"、"把md转成网页"、"把docx转md"、"文档格式转换"、"markdown转word"、"word转markdown"、"markdown转pdf"、"html转pdf"、"docx转pdf"时触发此技能。即使用户没有明确说具体格式，只要涉及文档格式之间的转换，都应触发。
---

# 文档格式转换

使用 Pandoc 实现常见文档格式之间的互相转换，脚本根据文件扩展名自动识别输入/输出格式。跨平台统一使用 Python 脚本（Windows/Linux/macOS）。

## 前置条件

- **Pandoc** 必须已安装。运行 `pandoc --version` 检查，如果未安装：
  - Windows: `scoop install pandoc`
  - macOS: `brew install pandoc`
  - Linux: `sudo apt install pandoc` 或 `sudo dnf install pandoc`

- **PDF 输出**有两种路径（脚本自动检测，优先使用 LaTeX 引擎）：
  1. **LaTeX 引擎**（优先）：检测 `pdflatex` > `xelatex` > `lualatex`，通过 Pandoc 的 `--pdf-engine` 直接生成 PDF
  2. **浏览器 Headless**（回退）：按 `Edge` > `Chrome` > `Firefox` 顺序检测，将 HTML 渲染为 PDF

## 支持的转换路径

| 源格式 | →HTML | →PDF | →DOCX | →MD | →PPTX | →TXT |
|--------|-------|------|-------|-----|-------|------|
| MD     | ✅    | ✅   | ✅    | —   | ✅    | ✅   |
| HTML   | —     | ✅   | ✅    | ✅  | —     | ✅   |
| DOCX   | ✅    | ✅   | —     | ✅  | —     | ✅   |
| ODT    | ✅    | ✅   | ✅    | ✅  | —     | ✅   |
| TXT    | ✅    | ✅   | ✅    | ✅  | —     | —    |

扩展名映射：`.md/.markdown`→Markdown, `.html/.htm`→HTML, `.docx`→DOCX, `.odt`→ODT, `.pdf`→PDF, `.pptx`→PPTX, `.txt`→纯文本, `.tex`→LaTeX, `.rst`→reStructuredText, `.org`→Org-mode, `.epub`→EPUB

## 核心流程

### 1. 确定输入和输出

用户提供输入文件路径，可选指定输出文件路径。脚本根据扩展名自动识别格式：

- 如果用户只提供输入文件，**默认输出格式**：
  - `.md` → `.html`（GitHub 风格）
  - `.docx` → `.md`
  - `.html` → `.md`
  - 其他 → `.html`

- 如果用户明确指定输出文件（如 `output.pdf`），则按输出扩展名确定目标格式

### 2. 执行转换

使用 `uv run python` 调用 skill 目录下的 `scripts/convert.py`：

```bash
uv run python "<skill-dir>/scripts/convert.py" --in-file "<输入文件>" [--out-file "<输出文件>"] [--title "<标题>"] [--toc] [--no-preview]
```

**参数说明：**

| 参数 | 必需 | 说明 |
|------|------|------|
| `--in-file` | 是 | 输入文件路径 |
| `--out-file` | 否 | 输出文件路径，默认根据输入自动推断 |
| `--title` | 否 | 文档标题，默认取文件名 |
| `--toc` | 否 | 生成目录（Table of Contents） |
| `--no-preview` | 否 | 不自动打开预览（转换完成后默认自动打开） |

### 3. PDF 输出引擎检测逻辑

当目标格式为 PDF 时，脚本按以下顺序自动检测可用引擎：

```
1. pdflatex  ─┐
2. xelatex   ─┤ LaTeX 引擎（Pandoc --pdf-engine 直接生成）
3. lualatex  ─┘
4. Edge      ─┐
5. Chrome    ─┤ 浏览器 Headless（HTML → PDF 两步转换）
6. Firefox   ─┘
```

- **LaTeX 引擎**：直接通过 Pandoc 的 `--pdf-engine` 参数生成 PDF，输出质量更高（支持数学公式、矢量图形），无需中间 HTML
- **浏览器 Headless**：先将内容转为带 GitHub CSS 的临时 HTML，再调用浏览器渲染为 PDF
  - Edge/Chrome 使用 `--headless --disable-gpu --no-pdf-header-footer --print-to-pdf` 参数
  - Firefox 使用 `--headless --print-to-pdf` 参数

### 4. 格式特殊处理

**→ HTML：**
- 自动应用 GitHub 风格 CSS（样式文件在 `scripts/css/github.css`）
- 居中布局，最大宽度 980px，左右 padding 45px

**→ PDF（LaTeX 引擎）：**
- Pandoc 直接调用 LaTeX 引擎编译输出
- 数学公式、代码高亮等原生支持

**→ PDF（浏览器回退，两步转换）：**
1. 先通过 Pandoc 生成带 GitHub CSS 的 HTML（临时文件）
2. 再调用浏览器 Headless 将 HTML 渲染为 PDF
- 自动添加打印样式（`scripts/css/print.css`）：避免标题/表格/代码块被分页截断
- 移除页眉页脚（Edge/Chrome 支持 `--no-pdf-header-footer`）
- 临时 HTML 文件在 PDF 生成后自动清理

### 5. 典型用法

```bash
# MD → HTML（默认）
uv run python scripts/convert.py --in-file report.md

# MD → PDF（自动检测 LaTeX 或浏览器引擎）
uv run python scripts/convert.py --in-file report.md --out-file report.pdf

# MD → DOCX
uv run python scripts/convert.py --in-file report.md --out-file report.docx

# MD → PPTX
uv run python scripts/convert.py --in-file slides.md --out-file slides.pptx

# DOCX → MD
uv run python scripts/convert.py --in-file document.docx

# HTML → MD
uv run python scripts/convert.py --in-file page.html

# 带目录
uv run python scripts/convert.py --in-file report.md --out-file report.pdf --toc

# 不自动打开预览
uv run python scripts/convert.py --in-file report.md --no-preview
```

## 批量转换

```bash
# 目录下所有 md 转 pdf（Bash / PowerShell 通用）
# Bash:
for f in *.md; do
    uv run python scripts/convert.py --in-file "$f" --out-file "${f%.md}.pdf" --no-preview
done

# PowerShell:
Get-ChildItem -Filter "*.md" | ForEach-Object {
    uv run python scripts/convert.py --in-file $_.FullName --out-file ($_.FullName -replace '\.md$', '.pdf') --no-preview
}
```

## 错误处理

| 问题 | 脚本行为 |
|------|----------|
| Pandoc 未安装 | 报错并提示安装命令 |
| 无 LaTeX 引擎也无浏览器（需要 PDF） | 报错，提示安装 LaTeX 引擎或浏览器 |
| 输入文件不存在 | 报错退出 |
| 不支持的格式 | 报错并列出支持的格式列表 |
| 输入输出文件相同 | 报错退出 |
| PDF 生成超时（15秒） | 报错，保留中间 HTML 文件 |
