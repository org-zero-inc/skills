"""doc-convert: 文档格式转换工具"""

import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ENV_VARS = {
    "Chrome": "CHROME_EXECUTABLE",
    "Edge": "EDGE_EXECUTABLE",
    "Firefox": "FIREFOX_EXECUTABLE",
}


def detect_browser() -> tuple[str, str] | None:
    for name, var in ENV_VARS.items():
        path = os.environ.get(var, "")
        if path and Path(path).is_file():
            return name, path
    return None


def html_to_pdf(html_file: Path, pdf_file: Path, browser_name: str, browser_exe: str) -> None:
    html_uri = html_file.as_uri()
    if browser_name == "Firefox":
        cmd = [browser_exe, "--headless", f"--print-to-pdf={pdf_file}", html_uri]
    else:
        cmd = [browser_exe, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf_file}", html_uri]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        if pdf_file.exists():
            break
        time.sleep(0.5)
    else:
        print(f"PDF 生成失败: {pdf_file}", file=sys.stderr)
        print(f"已保留中间 HTML 文件: {html_file}", file=sys.stderr)
        sys.exit(1)
    time.sleep(0.3)
    try:
        html_file.unlink(missing_ok=True)
    except OSError:
        pass


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="文档格式转换工具")
    parser.add_argument("-i", required=True, help="输入文件路径")
    parser.add_argument("-o", required=True, help="输出文件路径")
    args = parser.parse_args()

    in_file = Path(args.i).resolve()
    out_file = Path(args.o).resolve()

    if not in_file.exists():
        sys.exit(f"输入文件不存在: {in_file}")

    if in_file.suffix.lower() == ".pdf":
        sys.exit("不支持 PDF 作为输入格式")

    if not shutil.which("pandoc"):
        sys.exit("未找到 pandoc，请先安装")

    out_ext = out_file.suffix.lower()

    print(f"转换: {in_file.name} -> {out_file.name}")

    if out_ext == ".pdf":
        html_file = Path(tempfile.gettempdir()) / f"pandoc-convert-{in_file.stem}.html"
        result = subprocess.run(["pandoc", str(in_file), "-o", str(html_file), "-s"])
        if result.returncode != 0 or not html_file.exists():
            sys.exit("pandoc 转换失败")
        browser_info = detect_browser()
        if not browser_info:
            vars_str = "、".join(ENV_VARS.values())
            sys.exit(f"请设置浏览器路径环境变量，如 {vars_str}")
        html_to_pdf(html_file, out_file, *browser_info)
    else:
        cmd = ["pandoc", str(in_file), "-o", str(out_file)]
        if out_ext in (".html", ".htm"):
            cmd.append("-s")
        result = subprocess.run(cmd)
        if result.returncode != 0 or not out_file.exists():
            sys.exit("pandoc 转换失败")

    print(f"完成: {out_file}")


if __name__ == "__main__":
    main()
