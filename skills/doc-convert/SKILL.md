---
name: doc-convert
description: 文档格式转换工具，使用 Pandoc 实现常见格式互转，PDF 输出通过浏览器 Headless 模式打印。当用户提到"文档转换"、"md转html"、"md转pdf"、"md转docx"、"docx转md"、"html转md"等涉及文档格式间转换时触发。
---

# 文档格式转换

## 前置条件

- **Pandoc**：`scoop install pandoc` / `brew install pandoc` / `sudo apt install pandoc`
- **PDF 输出**：需设置浏览器路径环境变量（`CHROME_EXECUTABLE` / `EDGE_EXECUTABLE` / `FIREFOX_EXECUTABLE`）

## 用法

```bash
uv run python scripts/convert.py -i <输入文件> -o <输出文件>
```

| 参数 | 说明 |
|------|------|
| `-i` | 输入文件路径（不支持 .pdf） |
| `-o` | 输出文件路径 |

## 转换逻辑

| 输出格式 | 方式 |
|----------|------|
| `.pdf` | Pandoc 出 HTML (`-s`) → 浏览器 Headless 打印 PDF |
| `.html`/`.htm` | `pandoc -s` 直出 |
| 其他 (`.docx`/`.pptx`/`.md`/`.txt` 等) | `pandoc` 直出 |

## 示例

```bash
uv run python scripts/convert.py -i report.md -o report.html
uv run python scripts/convert.py -i report.md -o report.pdf
uv run python scripts/convert.py -i report.md -o report.docx
uv run python scripts/convert.py -i document.docx -o document.md
```
