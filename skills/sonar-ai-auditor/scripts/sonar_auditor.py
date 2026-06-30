#!/usr/bin/env python3
"""
sonar_auditor.py — SonarQube 静态扫描 + AI 动态审计 CLI 工具

用法:
  uv run --with requests python scripts/sonar_auditor.py scan --project-key <KEY> [--sonar-url <URL>] [--token <TOKEN>]
  uv run --with requests python scripts/sonar_auditor.py fetch --project-key <KEY> [--changed-files <FILES>] [--new-code]
  uv run --with requests python scripts/sonar_auditor.py report --input <JSON_PATH> --output <HTML_PATH>
  uv run --with requests python scripts/sonar_auditor.py filter --input <JSON_PATH> --changed-files <FILES> --output <JSON_PATH>

子命令:
  scan    运行本地 sonar-scanner → 拉取 API → 生成 HTML 报告（全流程）
  fetch   仅从 SonarQube API 拉取 Issues，保存为 JSON
  filter  对已有 JSON 按变更文件过滤，输出增量 JSON
  report  将已有的 JSON 结果转换为 HTML 报告
"""

import argparse
import html
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

SONAR_URL_ENV = "SONAR_URL"
SONAR_TOKEN_ENV = "SONAR_TOKEN"
DEFAULT_SONAR_URL = "http://localhost:9000"

SKIP_EXTENSIONS: Set[str] = {
    ".class", ".jar", ".war", ".ear", ".png", ".jpg", ".jpeg", ".gif",
    ".svg", ".ico", ".bmp", ".tiff", ".woff", ".woff2", ".ttf", ".eot",
    ".mp3", ".mp4", ".avi", ".mov", ".zip", ".tar", ".gz", ".rar",
}

SKIP_DIRS: Set[str] = {
    "node_modules", "dist", "build", "target", ".venv", "venv",
    "__pycache__", ".git", ".idea", ".vscode", "vendor",
}


def _should_skip_file(filepath: str) -> bool:
    _, ext = os.path.splitext(filepath)
    if ext.lower() in SKIP_EXTENSIONS:
        return True
    parts = filepath.replace("\\", "/").split("/")
    for d in parts:
        if d in SKIP_DIRS:
            return True
    return False


# ── HTTP 工具（零外部依赖） ──────────────────────────────────────────

def api_get(url: str, token: Optional[str] = None) -> Dict[str, Any]:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} from {url}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"无法连接 {url}: {e.reason}") from e


# ── SonarQube API 调用 ──────────────────────────────────────────────

def fetch_issues(
    sonar_url: str,
    project_key: str,
    token: Optional[str] = None,
    max_per_page: int = 100,
    new_code_only: bool = False,
) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    page = 1
    while True:
        params = {
            "projectKeys": project_key,
            "resolved": "false",
            "ps": str(max_per_page),
            "p": str(page),
            "additionalFields": "rules,users",
        }
        if new_code_only:
            params["sinceLeakPeriod"] = "true"
        encoded = urllib.parse.urlencode(params)
        url = f"{sonar_url.rstrip('/')}/api/issues/search?{encoded}"
        data = api_get(url, token=token)
        issues.extend(data.get("issues", []))
        total = data.get("total", 0)
        if page * max_per_page >= total:
            break
        page += 1
    return issues


def fetch_metrics(
    sonar_url: str,
    project_key: str,
    token: Optional[str] = None,
    metric_keys: str = "bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,ncloc",
    new_code_only: bool = False,
) -> Dict[str, Any]:
    params: Dict[str, str] = {
        "component": project_key,
        "metricKeys": metric_keys,
    }
    if new_code_only:
        params["period"] = "1"
    encoded = urllib.parse.urlencode(params)
    url = f"{sonar_url.rstrip('/')}/api/measures/component?{encoded}"
    data = api_get(url, token=token)
    measures: Dict[str, str] = {}
    for m in data.get("component", {}).get("measures", []):
        measures[m["metric"]] = m.get("value", "N/A")
    return measures


def fetch_quality_gate(
    sonar_url: str,
    project_key: str,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    params = urllib.parse.urlencode({"projectKey": project_key})
    url = f"{sonar_url.rstrip('/')}/api/qualitygates/project_status?{params}"
    return api_get(url, token=token)


# ── 增量过滤 ────────────────────────────────────────────────────────

def filter_issues_by_files(
    issues: List[Dict[str, Any]],
    changed_files: Set[str],
) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for iss in issues:
        component = iss.get("component", "")
        file_path = component.split(":")[-1] if ":" in component else component
        if file_path in changed_files:
            filtered.append(iss)
            continue
        for cf in changed_files:
            if file_path.endswith(cf) or cf.endswith(file_path):
                filtered.append(iss)
                break
    return filtered


def parse_changed_files(files_str: str) -> Set[str]:
    result: Set[str] = set()
    for f in files_str.split(","):
        f = f.strip().strip("'\"")
        if f and not _should_skip_file(f):
            result.add(f)
    return result


# ── 本地 sonar-scanner ──────────────────────────────────────────────

def run_sonar_scanner(project_dir: Optional[str] = None) -> None:
    cwd = project_dir or os.getcwd()
    props_path = os.path.join(cwd, "sonar-project.properties")
    if not os.path.isfile(props_path):
        print("⚠️  未找到 sonar-project.properties，Scanner 将使用默认配置")

    use_shell = sys.platform == "win32"
    scanner_cmd = "sonar-scanner"
    if sys.platform == "win32":
        scanner_cmd = "sonar-scanner.cmd"
        try:
            subprocess.run(
                ["where.exe", "sonar-scanner"],
                capture_output=True, text=True, check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "未找到 sonar-scanner 命令，请确保已安装并加入 PATH。"
                "下载地址: https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/"
            )
    else:
        import shutil
        if not shutil.which("sonar-scanner"):
            raise RuntimeError("未找到 sonar-scanner 命令，请确保已安装并加入 PATH。")

    try:
        subprocess.run(
            [scanner_cmd] if not use_shell else scanner_cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
            shell=use_shell,
        )
    except subprocess.CalledProcessError as e:
        print(f"⚠️  sonar-scanner 返回非零退出码 {e.returncode}")
        print(e.stdout)
        print(e.stderr)
        raise


# ── 严重级别映射 ────────────────────────────────────────────────────

SEVERITY_ORDER = {"BLOCKER": 0, "CRITICAL": 1, "MAJOR": 2, "MINOR": 3, "INFO": 4}
SEVERITY_COLORS = {
    "BLOCKER": "#ff4444",
    "CRITICAL": "#ff6b6b",
    "MAJOR": "#f59e0b",
    "MINOR": "#60a5fa",
    "INFO": "#8a8578",
}
TYPE_LABELS = {
    "BUG": "[x] Bug",
    "VULNERABILITY": "[/] 漏洞",
    "CODE_SMELL": "[~] 坏味道",
    "SECURITY_HOTSPOT": "[!] 安全热点",
}

UA_BG = "#0a0a0a"
UA_SURFACE = "#141414"
UA_BORDER = "#1a1a1a"
UA_ACCENT = "#d4a574"
UA_ACCENT_GLOW = "rgba(212, 165, 116, .15)"
UA_TEXT = "#e8e2d8"
UA_TEXT_MUTED = "#8a8578"
UA_GRAD_COOL = "#c9867a"
UA_GRAD_MID = "#b8865c"
UA_GRAD_WARM = "#d4a574"


# ── HTML 报告生成 ───────────────────────────────────────────────────

def generate_html_report(
    issues: List[Dict[str, Any]],
    project_key: str,
    output_path: str,
    metrics: Optional[Dict[str, str]] = None,
    quality_gate: Optional[Dict[str, Any]] = None,
    source_branch: str = "",
    target_branch: str = "",
    is_incremental: bool = False,
    llm_findings: Optional[List[Dict[str, Any]]] = None,
) -> str:
    issues.sort(key=lambda i: SEVERITY_ORDER.get(i.get("severity", "INFO"), 99))

    total = len(issues)
    by_severity: Dict[str, int] = {}
    by_type: Dict[str, int] = {}
    for iss in issues:
        s = iss.get("severity", "INFO")
        t = iss.get("type", "CODE_SMELL")
        by_severity[s] = by_severity.get(s, 0) + 1
        by_type[t] = by_type.get(t, 0) + 1

    qg_status = ""
    qg_color = UA_ACCENT
    if quality_gate:
        qs = quality_gate.get("projectStatus", {}).get("status", "NONE")
        if qs == "OK":
            qg_status = "[OK] 通过"
            qg_color = "#22c55e"
        elif qs == "ERROR":
            qg_status = "[FAIL] 未通过"
            qg_color = "#ff4444"
        else:
            qg_status = f"[WARN] {qs}"
            qg_color = "#f59e0b"

    severity_labels = {
        "BLOCKER": "阻断",
        "CRITICAL": "严重",
        "MAJOR": "主要",
        "MINOR": "次要",
        "INFO": "提示",
    }
    max_sv = max(by_severity.values()) if by_severity else 1

    issue_cards = ""
    for iss in issues:
        sev = iss.get("severity", "INFO")
        sv_color = SEVERITY_COLORS.get(sev, UA_TEXT_MUTED)
        msg = html.escape(iss.get("message", ""))
        comp = html.escape(iss.get("component", "").split(":")[-1])
        line = iss.get("line") or iss.get("textRange", {}).get("startLine", "?")
        rule = html.escape(iss.get("rule", ""))
        itype = iss.get("type", "CODE_SMELL")
        itype_label = TYPE_LABELS.get(itype, itype)
        effort = iss.get("effort", "")
        author = html.escape(iss.get("author", ""))
        creation_date = iss.get("creationDate", "").split("T")[0] if iss.get("creationDate") else ""

        issue_cards += f"""
        <div class="issue-card" style="border-left-color:{sv_color};">
            <div class="issue-header">
                <span class="severity-badge" style="background:{sv_color};">{sev}</span>
                <span class="type-badge">{itype_label}</span>
                <span class="issue-date">{creation_date}</span>
            </div>
            <div class="issue-message">{msg}</div>
            <div class="issue-meta">
                <span class="meta-item">&#9679; {comp}:{line}</span>
                <span class="meta-item">&#9881; <code>{rule}</code></span>
                {f'<span class="meta-item">&#9201; {effort}</span>' if effort else ''}
                {f'<span class="meta-item">&#9998; {author}</span>' if author else ''}
            </div>
        </div>"""

    bar_chart_svg = _generate_bar_chart(by_severity, severity_labels, max_sv, total)

    llm_section = ""
    if llm_findings:
        llm_cards = ""
        for finding in llm_findings:
            priority = finding.get("priority", "P2")
            p_color = "#ff4444" if priority == "P0" else "#f59e0b" if priority == "P1" else "#60a5fa"
            title = html.escape(finding.get("title", ""))
            vuln_type = html.escape(finding.get("vuln_type", ""))
            trigger = html.escape(finding.get("trigger", ""))
            poc = html.escape(finding.get("poc", ""))
            consequence = html.escape(finding.get("consequence", ""))
            fix = html.escape(finding.get("fix", ""))
            file_path = html.escape(finding.get("file", ""))
            line_no = finding.get("line", "?")

            llm_cards += f"""
            <div class="issue-card" style="border-left-color:{p_color};">
                <div class="issue-header">
                    <span class="severity-badge" style="background:{p_color};">{priority}</span>
                    <span class="type-badge">🔴 动态审计</span>
                    <span class="type-badge">{vuln_type}</span>
                </div>
                <div class="issue-message">{title}</div>
                <div class="issue-meta">
                    <span class="meta-item">&#9679; {file_path}:{line_no}</span>
                </div>
                <div class="finding-detail">
                    <div class="detail-row"><strong>触发场景：</strong>{trigger}</div>
                    <div class="detail-row"><strong>PoC 构造思路：</strong>{poc}</div>
                    <div class="detail-row"><strong>后果：</strong>{consequence}</div>
                    <div class="detail-row"><strong>修复建议：</strong>{fix}</div>
                </div>
            </div>"""

        llm_total = len(llm_findings)
        llm_p0 = sum(1 for f in llm_findings if f.get("priority") == "P0")
        llm_p1 = sum(1 for f in llm_findings if f.get("priority") == "P1")
        llm_p2 = sum(1 for f in llm_findings if f.get("priority") == "P2")
        llm_section = f"""
        <div class="issues-section">
            <h2>LLM 动态语义审计 &mdash; {llm_total} 项发现（P0: {llm_p0}, P1: {llm_p1}, P2: {llm_p2}）</h2>
            {llm_cards}
        </div>"""

    branch_info = f"{source_branch} → {target_branch}" if source_branch and target_branch else project_key
    mode_label = "增量" if is_incremental else "全量"
    title_text = f"增量代码审计报告" if is_incremental else "SonarQube 静态扫描报告"

    def _metric_row(label: str, key: str) -> str:
        val = metrics.get(key, "N/A") if metrics else "N/A"
        return f"<tr><td>{label}</td><td><strong>{html.escape(str(val))}</strong></td></tr>" if val != "N/A" else ""

    metrics_rows = ""
    if metrics:
        for label, key in [("Bug 数", "bugs"), ("漏洞数", "vulnerabilities"), ("坏味道", "code_smells"),
                            ("代码行数", "ncloc"), ("重复率", "duplicated_lines_density"), ("覆盖率", "coverage")]:
            metrics_rows += _metric_row(label, key)

    grain_svg = "%3Csvg%20viewBox%3D%270%200%20256%20256%27%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%3E%3Cfilter%20id%3D%27noise%27%3E%3CfeTurbulence%20type%3D%27fractalNoise%27%20baseFrequency%3D%270.9%27%20numOctaves%3D%274%27%20stitchTiles%3D%27stitch%27%2F%3E%3C%2Ffilter%3E%3Crect%20width%3D%27100%25%27%20height%3D%27100%25%27%20filter%3D%27url(%23noise)%27%2F%3E%3C%2Fsvg%3E"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_text} - {html.escape(branch_info)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&amp;family=Inter:wght@400;600&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<style>
:root {{
    --bg:        {UA_BG};
    --surface:   {UA_SURFACE};
    --border:    {UA_BORDER};
    --accent:    {UA_ACCENT};
    --accent-glow: {UA_ACCENT_GLOW};
    --text:      {UA_TEXT};
    --text-muted:{UA_TEXT_MUTED};
    --grad-cool: {UA_GRAD_COOL};
    --grad-mid:  {UA_GRAD_MID};
    --grad-warm: {UA_GRAD_WARM};
    --font-heading: 'DM Serif Display', Georgia, 'Times New Roman', serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-code: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    font-family: var(--font-body);
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}}
body::before {{
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 9999;
    opacity: .03;
    background-image: url("data:image/svg+xml,{grain_svg}");
}}
.header {{
    background: linear-gradient(135deg, var(--grad-cool), var(--grad-mid), var(--grad-warm));
    padding: 40px 48px;
    position: relative;
}}
.header::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(10,10,10,.6);
    pointer-events: none;
}}
.header-content {{
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}}
.header h1 {{
    font-family: var(--font-heading);
    font-size: 28px;
    font-weight: 400;
    color: var(--text);
    letter-spacing: -0.3px;
}}
.header .subtitle {{
    color: rgba(232,226,216,.7);
    font-size: 14px;
    margin-top: 4px;
}}
.mode-badge {{
    display: inline-block;
    padding: 4px 14px;
    border-radius: 100px;
    font-family: var(--font-code);
    font-size: 12px;
    font-weight: 500;
    color: var(--text);
    background: rgba(212,165,116,.2);
    border: 1px solid rgba(212,165,116,.3);
    margin-left: 12px;
}}
.container {{ max-width:1200px; margin:0 auto; padding:32px 24px; }}
.summary-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; margin-bottom:28px; }}
.summary-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    transition: border-color .3s ease, box-shadow .3s ease;
}}
.summary-card:hover {{
    border-color: rgba(212,165,116,.25);
    box-shadow: 0 0 24px var(--accent-glow);
}}
.summary-card .num {{
    font-family: var(--font-heading);
    font-size: 32px;
    font-weight: 400;
    line-height: 1.2;
}}
.summary-card .num.BLOCKER {{ color: {SEVERITY_COLORS['BLOCKER']}; }}
.summary-card .num.CRITICAL {{ color: {SEVERITY_COLORS['CRITICAL']}; }}
.summary-card .num.MAJOR {{ color: {SEVERITY_COLORS['MAJOR']}; }}
.summary-card .num.MINOR {{ color: {SEVERITY_COLORS['MINOR']}; }}
.summary-card .num.INFO {{ color: {SEVERITY_COLORS['INFO']}; }}
.summary-card .num.TOTAL {{ color: var(--accent); }}
.summary-card .num.LLM {{ color: #c9867a; }}
.summary-card .label {{ color: var(--text-muted); font-size: 12px; margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; }}
.charts {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:28px; }}
@media (max-width:768px) {{ .charts {{ grid-template-columns:1fr; }} }}
.chart-box {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
}}
.chart-box h3 {{ font-family: var(--font-heading); font-size: 16px; font-weight: 400; color: var(--text); margin-bottom: 16px; }}
.metrics-table {{ width:100%; border-collapse:collapse; font-size: 14px; }}
.metrics-table td {{ padding:10px 12px; border-bottom:1px solid var(--border); }}
.metrics-table td:last-child {{ text-align:right; font-family: var(--font-code); color: var(--accent); }}
.metrics-table tr:last-child td {{ border-bottom: none; }}
.quality-gate {{
    display: inline-block;
    padding: 6px 18px;
    border-radius: 100px;
    font-family: var(--font-code);
    font-size: 13px;
    font-weight: 500;
    color: #fff;
    background: {qg_color};
    border: 1px solid rgba(255,255,255,.1);
}}
.issues-section h2 {{ font-family: var(--font-heading); font-size: 18px; font-weight: 400; margin-bottom: 16px; color: var(--text); }}
.issue-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
    transition: border-color .3s ease, box-shadow .3s ease;
}}
.issue-card:hover {{
    border-color: rgba(212,165,116,.25);
    border-left-color: inherit;
    box-shadow: 0 0 20px var(--accent-glow);
}}
.issue-header {{ display:flex; align-items:center; gap:8px; margin-bottom:8px; }}
.severity-badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 100px;
    font-family: var(--font-code);
    font-size: 11px;
    font-weight: 500;
    color: #fff;
    letter-spacing: 0.3px;
    border: 1px solid rgba(255,255,255,.08);
}}
.type-badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 100px;
    font-family: var(--font-code);
    font-size: 11px;
    background: rgba(255,255,255,.03);
    color: var(--text-muted);
    border: 1px solid rgba(138,133,120,.25);
}}
.issue-date {{ margin-left:auto; font-size:12px; color: var(--text-muted); font-family: var(--font-code); }}
.issue-message {{ font-size:15px; margin-bottom:8px; line-height:1.5; color: var(--text); }}
.issue-meta {{ display:flex; flex-wrap:wrap; gap:14px; font-size:13px; color: var(--text-muted); }}
.issue-meta code {{ font-family: var(--font-code); background: rgba(255,255,255,.03); padding:1px 6px; border-radius:4px; font-size:12px; border: 1px solid rgba(138,133,120,.15); color: var(--text-muted); }}
.finding-detail {{ margin-top:10px; padding:10px 14px; background: rgba(255,255,255,.02); border-radius:8px; font-size:13px; line-height:1.6; }}
.detail-row {{ margin-bottom:6px; }}
.detail-row:last-child {{ margin-bottom:0; }}
.detail-row strong {{ color: var(--accent); }}
.footer {{ text-align:center; padding:32px; color: var(--text-muted); font-size:12px; font-family: var(--font-code); opacity: .6; }}
.empty-state {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 48px;
    text-align: center;
    color: var(--text-muted);
    font-size: 16px;
}}
.divider {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 28px 0;
}}
</style>
</head>
<body>
<div class="header">
    <div class="header-content">
        <div>
            <h1>{title_text}<span class="mode-badge">{mode_label}</span></h1>
            <div class="subtitle">{html.escape(branch_info)} &middot; {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
        </div>
        <div class="quality-gate">质量门禁: {qg_status}</div>
    </div>
</div>
<div class="container">
    <div class="summary-grid">
        <div class="summary-card"><div class="num TOTAL">{total}</div><div class="label">Sonar 问题</div></div>
        {''.join(f'<div class="summary-card"><div class="num {s}">{by_severity.get(s,0)}</div><div class="label">{severity_labels.get(s,s)}</div></div>' for s in ["BLOCKER","CRITICAL","MAJOR","MINOR","INFO"])}
        {"<div class=\"summary-card\"><div class=\"num LLM\">" + str(len(llm_findings) if llm_findings else 0) + "</div><div class=\"label\">LLM 发现</div></div>" if llm_findings else ""}
    </div>
    <div class="charts">
        <div class="chart-box">
            <h3>严重级别分布</h3>
            {bar_chart_svg}
        </div>
        <div class="chart-box">
            <h3>项目指标</h3>
            <table class="metrics-table">
                {metrics_rows if metrics_rows else '<tr><td style="color:var(--text-muted);text-align:center;">暂无指标数据</td></tr>'}
            </table>
        </div>
    </div>
    <div class="issues-section">
        <h2>SonarQube 静态扫描 &mdash; {total} 项</h2>
        {issue_cards if issue_cards else '<div class="empty-state">变更文件中未发现 SonarQube 问题</div>'}
    </div>
    {f'<hr class="divider">{llm_section}' if llm_section else ''}
</div>
<div class="footer">Sonar AI Auditor Skill 自动生成 &middot; {mode_label}模式</div>
</body>
</html>"""

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_path


def _generate_bar_chart(
    by_severity: Dict[str, int],
    labels: Dict[str, str],
    max_val: int,
    total: int,
) -> str:
    if not by_severity or max_val == 0:
        return '<div style="color:var(--text-muted);text-align:center;">暂无数据</div>'

    bar_height = 20
    gap = 8
    label_width = 60
    chart_width = 400
    padding_left = label_width + 8
    padding_right = 50
    svg_w = padding_left + chart_width + padding_right
    svg_h = len([k for k in ["BLOCKER","CRITICAL","MAJOR","MINOR","INFO"] if k in by_severity or True]) * (bar_height + gap) + 10

    svg = f'<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" font-family="Inter,-apple-system,BlinkMacSystemFont,sans-serif" font-size="12">'
    y = 5
    for sev in ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]:
        count = by_severity.get(sev, 0)
        color = SEVERITY_COLORS.get(sev, UA_TEXT_MUTED)
        svg += f'<text x="{label_width}" y="{y + 14}" text-anchor="end" fill="{UA_TEXT_MUTED}">{labels.get(sev,sev)}</text>'
        if count > 0:
            bar_w = int((count / max_val) * chart_width) if max_val else 0
            if bar_w < 4:
                bar_w = 4
            svg += f'<rect x="{padding_left}" y="{y}" width="{bar_w}" height="{bar_height}" rx="4" fill="{color}" opacity=".85"/>'
            svg += f'<text x="{padding_left + bar_w + 6}" y="{y + 14}" fill="{UA_TEXT}" font-weight="600">{count}</text>'
        else:
            svg += f'<text x="{padding_left + 4}" y="{y + 14}" fill="rgba(138,133,120,.4)">0</text>'
        y += bar_height + gap
    svg += "</svg>"
    return svg


# ── 从 sonar-project.properties 读取 project key ────────────────────

def read_sonar_props(project_dir: Optional[str] = None) -> Dict[str, str]:
    result: Dict[str, str] = {}
    props_path = os.path.join(project_dir or os.getcwd(), "sonar-project.properties")
    if not os.path.isfile(props_path):
        return result
    with open(props_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, _, val = line.partition("=")
                result[key.strip()] = val.strip()
    return result


# ── CLI ─────────────────────────────────────────────────────────────

def cmd_scan(args: argparse.Namespace) -> None:
    props = read_sonar_props(project_dir=args.project_dir)
    project_key = args.project_key or props.get("sonar.projectKey")
    if not project_key:
        print("🔴 错误：未指定 --project-key，且无法从 sonar-project.properties 自动检测")
        sys.exit(1)

    sonar_url = args.sonar_url or os.environ.get(SONAR_URL_ENV) or props.get("sonar.host.url", DEFAULT_SONAR_URL)
    token = args.token or os.environ.get(SONAR_TOKEN_ENV) or props.get("sonar.token")
    output_dir = args.output_dir or os.getcwd()

    print("⏳ [1/4] 运行 sonar-scanner ...")
    run_sonar_scanner(project_dir=args.project_dir)

    new_code = getattr(args, "new_code", False)
    label = "（仅新增代码）" if new_code else ""

    print(f"📡 [2/4] 从 {sonar_url} 拉取分析结果{label} ...")
    issues = fetch_issues(sonar_url, project_key, token=token, new_code_only=new_code)

    print(f"📊 [3/4] 拉取项目指标{label} ...")
    metrics = fetch_metrics(sonar_url, project_key, token=token, new_code_only=new_code)
    qg = fetch_quality_gate(sonar_url, project_key, token=token)

    changed_files: Optional[Set[str]] = None
    if getattr(args, "changed_files", None):
        changed_files = parse_changed_files(args.changed_files)
        issues = filter_issues_by_files(issues, changed_files)
        print(f"   过滤后保留 {len(issues)} 个变更文件中的问题")

    json_path = os.path.join(output_dir, f"sonar_report_{project_key}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"project": project_key, "issues": issues, "metrics": metrics, "quality_gate": qg}, f, ensure_ascii=False, indent=2)
    print(f"💾   JSON 已保存: {json_path}")

    print("📄 [4/4] 生成 HTML 报告 ...")
    html_path = os.path.join(output_dir, f"sonar_report_{project_key}.html")
    generate_html_report(
        issues, project_key, html_path, metrics=metrics, quality_gate=qg,
        source_branch=getattr(args, "source_branch", ""),
        target_branch=getattr(args, "target_branch", ""),
        is_incremental=bool(changed_files),
    )

    print(f"🟢 全流程完成！共发现 {len(issues)} 个问题")
    print(f"   HTML 报告: {html_path}")
    print(f"   JSON 数据: {json_path}")


def cmd_fetch(args: argparse.Namespace) -> None:
    props = read_sonar_props(project_dir=getattr(args, "project_dir", None))
    project_key = args.project_key
    sonar_url = args.sonar_url or os.environ.get(SONAR_URL_ENV) or props.get("sonar.host.url", DEFAULT_SONAR_URL)
    token = args.token or os.environ.get(SONAR_TOKEN_ENV) or props.get("sonar.token")
    output_dir = args.output_dir or os.getcwd()

    new_code = getattr(args, "new_code", False)
    label = "（仅新增代码）" if new_code else ""

    print(f"📡 从 {sonar_url} 拉取 {project_key} 的分析结果{label} ...")
    issues = fetch_issues(sonar_url, project_key, token=token, new_code_only=new_code)
    metrics = fetch_metrics(sonar_url, project_key, token=token, new_code_only=new_code)
    qg = fetch_quality_gate(sonar_url, project_key, token=token)

    if getattr(args, "changed_files", None):
        changed_files = parse_changed_files(args.changed_files)
        original_count = len(issues)
        issues = filter_issues_by_files(issues, changed_files)
        print(f"   变更文件过滤: {original_count} → {len(issues)} 个问题")

    json_path = os.path.join(output_dir, f"sonar_report_{project_key}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"project": project_key, "issues": issues, "metrics": metrics, "quality_gate": qg}, f, ensure_ascii=False, indent=2)
    print(f"✅ 已拉取 {len(issues)} 个问题，JSON 保存至: {json_path}")


def cmd_filter(args: argparse.Namespace) -> None:
    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    issues = data.get("issues", [])
    changed_files = parse_changed_files(args.changed_files)
    original_count = len(issues)
    filtered = filter_issues_by_files(issues, changed_files)

    data["issues"] = filtered
    output_path = args.output or args.input
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 过滤完成: {original_count} → {len(filtered)} 个问题，保存至: {output_path}")


def cmd_report(args: argparse.Namespace) -> None:
    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)
    issues = data.get("issues", [])
    project_key = data.get("project", args.input)
    metrics = data.get("metrics")
    qg = data.get("quality_gate")
    llm_findings = data.get("llm_findings")
    output = args.output or args.input.rsplit(".", 1)[0] + ".html"
    generate_html_report(
        issues, project_key, output, metrics=metrics, quality_gate=qg,
        source_branch=data.get("source_branch", ""),
        target_branch=data.get("target_branch", ""),
        is_incremental=data.get("is_incremental", False),
        llm_findings=llm_findings,
    )
    print(f"✅ HTML 报告已生成: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="SonarQube 静态扫描 + AI 动态审计 CLI 工具")
    parser.add_argument("--sonar-url", help=f"SonarQube 服务地址（默认 {DEFAULT_SONAR_URL}，也支持环境变量 {SONAR_URL_ENV}）")
    parser.add_argument("--token", help=f"SonarQube Token（也支持环境变量 {SONAR_TOKEN_ENV}）")
    parser.add_argument("--output-dir", "-o", help="输出目录（默认当前目录）")
    parser.add_argument("--project-dir", help="项目目录（默认当前目录）")

    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="全流程：运行 sonar-scanner + 拉取 API + 生成 HTML")
    p_scan.add_argument("--project-key", "-k", help="项目 Key（不指定则从 sonar-project.properties 自动检测）")
    p_scan.add_argument("--project-dir", help="项目目录（默认当前目录）")
    p_scan.add_argument("--new-code", action="store_true", help="仅获取新增代码（Leak Period）的问题")
    p_scan.add_argument("--changed-files", help="变更文件列表（逗号分隔），仅输出这些文件的问题")
    p_scan.add_argument("--source-branch", help="源分支名称（用于报告标题）")
    p_scan.add_argument("--target-branch", help="目标分支名称（用于报告标题）")
    p_scan.set_defaults(func=cmd_scan)

    p_fetch = sub.add_parser("fetch", help="仅从 SonarQube API 拉取 Issues 并保存为 JSON")
    p_fetch.add_argument("--project-key", "-k", required=True, help="项目 Key")
    p_fetch.add_argument("--new-code", action="store_true", help="仅获取新增代码（Leak Period）的问题")
    p_fetch.add_argument("--project-dir", help="项目目录（默认当前目录）")
    p_fetch.add_argument("--changed-files", help="变更文件列表（逗号分隔），仅输出这些文件的问题")
    p_fetch.set_defaults(func=cmd_fetch)

    p_filter = sub.add_parser("filter", help="对已有 JSON 按变更文件过滤")
    p_filter.add_argument("--input", "-i", required=True, help="输入的 JSON 文件路径")
    p_filter.add_argument("--changed-files", required=True, help="变更文件列表（逗号分隔）")
    p_filter.add_argument("--output", "-o", help="输出的 JSON 文件路径（默认覆盖输入）")
    p_filter.set_defaults(func=cmd_filter)

    p_report = sub.add_parser("report", help="将已有的 JSON 结果转换为 HTML 报告")
    p_report.add_argument("--input", "-i", required=True, help="输入的 JSON 文件路径")
    p_report.add_argument("--output", "-o", help="输出的 HTML 文件路径（默认同目录）")
    p_report.set_defaults(func=cmd_report)

    parsed = parser.parse_args()
    parsed.func(parsed)


if __name__ == "__main__":
    main()
