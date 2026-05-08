"""doc-convert: 使用 Pandoc 实现文档格式互转

支持 Markdown、HTML、DOCX、PDF、PPTX、TXT 等常见格式互转。
PDF 输出自动检测 LaTeX 引擎（pdflatex/xelatex/lualatex），
回退到浏览器 Headless 模式（Edge/Chrome/Firefox）。

用法:
    uv run python convert.py --in-file <输入文件> [--out-file <输出文件>] [--title <标题>] [--toc] [--no-preview]
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CSS_DIR = SCRIPT_DIR / "css"

FORMAT_MAP = {
    ".md": "markdown",
    ".markdown": "markdown",
    ".html": "html",
    ".htm": "html",
    ".docx": "docx",
    ".odt": "odt",
    ".txt": "plain",
    ".tex": "latex",
    ".rst": "rst",
    ".org": "org",
    ".epub": "epub",
}

READER_EXTS = list(FORMAT_MAP.keys())
WRITER_EXTS = [
    ".html",
    ".htm",
    ".pdf",
    ".docx",
    ".odt",
    ".txt",
    ".md",
    ".tex",
    ".rst",
    ".pptx",
    ".epub",
]

LATEX_ENGINE_ORDER = ["pdflatex", "xelatex", "lualatex"]

BROWSER_PATHS = {
    "Windows": {
        "Edge": [
            os.path.join(
                os.environ.get("ProgramFiles(x86)", ""),
                "Microsoft",
                "Edge",
                "Application",
                "msedge.exe",
            ),
            os.path.join(
                os.environ.get("ProgramFiles", ""),
                "Microsoft",
                "Edge",
                "Application",
                "msedge.exe",
            ),
            os.path.join(
                os.environ.get("LOCALAPPDATA", ""),
                "Microsoft",
                "Edge",
                "Application",
                "msedge.exe",
            ),
        ],
        "Chrome": [
            os.path.join(
                os.environ.get("ProgramFiles(x86)", ""),
                "Google",
                "Chrome",
                "Application",
                "chrome.exe",
            ),
            os.path.join(
                os.environ.get("ProgramFiles", ""),
                "Google",
                "Chrome",
                "Application",
                "chrome.exe",
            ),
            os.path.join(
                os.environ.get("LOCALAPPDATA", ""),
                "Google",
                "Chrome",
                "Application",
                "chrome.exe",
            ),
        ],
        "Firefox": [
            os.path.join(
                os.environ.get("ProgramFiles", ""), "Mozilla Firefox", "firefox.exe"
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", ""),
                "Mozilla Firefox",
                "firefox.exe",
            ),
            os.path.join(
                os.environ.get("LOCALAPPDATA", ""), "Mozilla Firefox", "firefox.exe"
            ),
        ],
    },
    "Darwin": {
        "Edge": ["/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"],
        "Chrome": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
        "Firefox": ["/Applications/Firefox.app/Contents/MacOS/firefox"],
    },
    "Linux": {
        "Edge": ["/usr/bin/microsoft-edge", "/usr/bin/microsoft-edge-stable"],
        "Chrome": [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ],
        "Firefox": ["/usr/bin/firefox", "/usr/bin/firefox-esr"],
    },
}


def _cyan(text):
    return f"\033[36m{text}\033[0m"


def _green(text):
    return f"\033[32m{text}\033[0m"


def _gray(text):
    return f"\033[90m{text}\033[0m"


def _yellow(text):
    return f"\033[33m{text}\033[0m"


def _red(text):
    return f"\033[31m{text}\033[0m"


def detect_latex_engine():
    for cmd in LATEX_ENGINE_ORDER:
        if shutil.which(cmd):
            return cmd
    return None


def detect_browser():
    os_name = platform.system()
    browser_map = BROWSER_PATHS.get(os_name, {})
    for name in ["Edge", "Chrome", "Firefox"]:
        for path in browser_map.get(name, []):
            if path and Path(path).is_file():
                return name, path
        if os_name == "Linux" and name in browser_map:
            resolved = shutil.which(name.lower().replace("edge", "microsoft-edge"))
            if resolved:
                return name, resolved
    return None


def infer_out_file(in_file, in_ext):
    in_path = Path(in_file)
    parent = in_path.parent
    stem = in_path.stem
    if in_ext in (".md", ".markdown"):
        return str(parent / f"{stem}.html")
    elif in_ext in (".docx", ".html", ".htm"):
        return str(parent / f"{stem}.md")
    else:
        return str(parent / f"{stem}.html")


def format_label(ext):
    labels = {
        ".html": "HTML",
        ".htm": "HTML",
        ".pdf": "PDF",
        ".docx": "DOCX",
        ".pptx": "PPTX",
        ".odt": "ODT",
        ".epub": "EPUB",
        ".md": "MARKDOWN",
        ".txt": "TXT",
    }
    return labels.get(ext, ext.lstrip(".").upper())


def to_format_name(ext):
    special = {".pptx": "pptx", ".md": "markdown"}
    return special.get(ext, FORMAT_MAP.get(ext, ext.lstrip(".")))


def build_pandoc_args(
    in_file, from_fmt, to_fmt, out_file, latex_engine, toc, need_html_style
):
    args = [str(in_file), "-f", from_fmt, "-t", to_fmt, "-o", str(out_file)]

    if latex_engine:
        args.append(f"--pdf-engine={latex_engine}")

    if toc:
        args.append("--toc")

    if need_html_style:
        args.extend(["-s", "--metadata", f"pagetitle={Path(in_file).stem}"])
        github_css = CSS_DIR / "github.css"
        if github_css.exists():
            args.extend(["-H", str(github_css)])

    return args


def html_to_pdf(html_file, pdf_file, browser_name, browser_exe):
    html_uri = Path(html_file).as_uri()

    if browser_name == "Firefox":
        print(_gray("  使用 Firefox Headless 生成 PDF..."))
        subprocess.run(
            [browser_exe, "--headless", f"--print-to-pdf={pdf_file}", html_uri],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        print(_gray(f"  使用 {browser_name} Headless 生成 PDF..."))
        subprocess.run(
            [
                browser_exe,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_file}",
                html_uri,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    for _ in range(30):
        if Path(pdf_file).exists():
            break
        import time

        time.sleep(0.5)
    else:
        print(_red(f"PDF 生成失败: {pdf_file}"), file=sys.stderr)
        print(_yellow(f"已保留中间 HTML 文件: {html_file}"), file=sys.stderr)
        sys.exit(1)

    import time

    time.sleep(0.5)
    try:
        os.remove(html_file)
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(description="doc-convert: 文档格式转换工具")
    parser.add_argument("--in-file", required=True, help="输入文件路径")
    parser.add_argument(
        "--out-file", default="", help="输出文件路径（默认根据输入自动推断）"
    )
    parser.add_argument("--title", default="", help="文档标题（默认取文件名）")
    parser.add_argument("--toc", action="store_true", help="生成目录")
    parser.add_argument("--no-preview", action="store_true", help="不自动打开预览")
    args = parser.parse_args()

    in_file = Path(args.in_file).resolve()
    if not in_file.exists():
        print(_red(f"输入文件不存在: {in_file}"), file=sys.stderr)
        sys.exit(1)

    if not shutil.which("pandoc"):
        print(_red("未找到 pandoc，请先安装:"), file=sys.stderr)
        print("  Windows: scoop install pandoc", file=sys.stderr)
        print("  macOS:   brew install pandoc", file=sys.stderr)
        print("  Linux:   sudo apt install pandoc", file=sys.stderr)
        sys.exit(1)

    in_ext = in_file.suffix.lower()
    if in_ext not in READER_EXTS:
        print(_red(f"不支持的输入格式: {in_ext}"), file=sys.stderr)
        print(f"支持: {', '.join(READER_EXTS)}", file=sys.stderr)
        sys.exit(1)

    out_file = args.out_file
    if not out_file:
        out_file = infer_out_file(in_file, in_ext)
    out_file = Path(out_file).resolve()

    out_ext = out_file.suffix.lower()
    if out_ext not in WRITER_EXTS:
        print(_red(f"不支持的输出格式: {out_ext}"), file=sys.stderr)
        print(f"支持: {', '.join(WRITER_EXTS)}", file=sys.stderr)
        sys.exit(1)

    if in_file == out_file:
        print(_red("输入和输出文件不能相同"), file=sys.stderr)
        sys.exit(1)

    is_to_pdf = out_ext == ".pdf"
    is_to_html = out_ext in (".html", ".htm")
    need_html_style = is_to_html or is_to_pdf

    latex_engine = None
    html_file = None
    print_css_file = None

    if is_to_pdf:
        latex_engine = detect_latex_engine()

        if need_html_style and not latex_engine:
            print_css_file = CSS_DIR / "print.css"
            tmp_dir = tempfile.gettempdir()
            html_file = Path(tmp_dir) / f"pandoc-convert-{in_file.stem}.html"

        if latex_engine:
            pandoc_out_file = out_file
            pandoc_out_ext = ".pdf"
        else:
            pandoc_out_file = html_file
            pandoc_out_ext = ".html"
    else:
        pandoc_out_file = out_file
        pandoc_out_ext = out_ext

    from_fmt = FORMAT_MAP.get(in_ext, in_ext.lstrip("."))
    to_fmt = to_format_name(pandoc_out_ext)

    pandoc_args = build_pandoc_args(
        in_file,
        from_fmt,
        to_fmt,
        pandoc_out_file,
        latex_engine,
        args.toc,
        need_html_style,
    )

    if print_css_file and print_css_file.exists():
        pandoc_args.extend(["-H", str(print_css_file)])

    in_label = from_fmt.upper()
    out_label = format_label(out_ext)

    print()
    print(_cyan(f"pandoc-convert: {in_label} -> {out_label}"))
    print(_gray(f"  输入: {in_file}"))
    print(_gray(f"  输出: {out_file}"))
    if is_to_pdf:
        if latex_engine:
            print(_gray(f"  引擎: LaTeX ({latex_engine})"))
        else:
            print(_gray(f"  中间: {html_file} (临时)"))
    print()

    result = subprocess.run(["pandoc"] + pandoc_args)
    if result.returncode != 0:
        print(_red(f"pandoc 转换失败，退出码: {result.returncode}"), file=sys.stderr)
        sys.exit(result.returncode)

    if not pandoc_out_file.exists():
        print(_red(f"中间文件未生成: {pandoc_out_file}"), file=sys.stderr)
        sys.exit(1)

    if is_to_pdf and not latex_engine:
        browser_info = detect_browser()
        if not browser_info:
            print(
                _red("未找到可用的浏览器 (Edge/Chrome/Firefox)，无法生成 PDF。"),
                file=sys.stderr,
            )
            print(
                _yellow("请安装浏览器或 LaTeX 引擎 (pdflatex/xelatex/lualatex)"),
                file=sys.stderr,
            )
            print(_yellow(f"已保留中间 HTML 文件: {html_file}"), file=sys.stderr)
            sys.exit(1)
        browser_name, browser_exe = browser_info
        html_to_pdf(html_file, out_file, browser_name, browser_exe)

    if not out_file.exists():
        print(_red(f"输出文件未生成: {out_file}"), file=sys.stderr)
        sys.exit(1)

    size = out_file.stat().st_size
    if size > 1048576:
        size_str = f"{size / 1048576:.1f} MB"
    elif size > 1024:
        size_str = f"{size / 1024:.1f} KB"
    else:
        size_str = f"{size} B"

    print(_green(f"转换完成! {out_label} ({size_str}) -> {out_file}"))

    if not args.no_preview:
        try:
            webbrowser.open(str(out_file))
            print(_gray("已打开预览"))
        except Exception:
            print(_yellow(f"无法自动打开，请手动查看: {out_file}"))


if __name__ == "__main__":
    main()
