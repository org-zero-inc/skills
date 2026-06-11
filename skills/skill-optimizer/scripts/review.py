#!/usr/bin/env python3
"""结构化评审报告生成工具"""

import json
import argparse
from pathlib import Path

REPORT_TEMPLATE = """# 📋 Skill 设计质量评审报告

**Skill**: {skill_name}
**日期**: {date}
**总评**: {overall}

---

## 逐维度评级

{dimension_summary}

---

## 详细发现

{findings_detail}

---

## 交叉问题

{cross_cutting}

---

## 改进优先级

{priorities}

---
*由 skill-optimizer 自动生成*
"""


def load_findings(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def rating_icon(rating):
    return {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(rating, "⚪")


def generate_report(skill_name, data):
    date = data.get("date", "N/A")
    dimensions = data.get("dimensions", [])
    findings = data.get("findings", [])
    cross_cutting = data.get("cross_cutting", [])
    priorities = data.get("priorities", [])

    overall = data.get("overall", "N/A")

    # Dimension summary table
    rows = []
    for d in dimensions:
        icon = rating_icon(d.get("rating", ""))
        rows.append(f"| {d['name']} | {icon} {d.get('rating', 'N/A')} | {d.get('summary', '')} |")
    dim_table = "| 维度 | 评级 | 概要 |\n|------|------|------|\n" + "\n".join(rows)

    # Detailed findings
    detail_lines = []
    for f in findings:
        icon = rating_icon(f.get("rating", ""))
        detail_lines.append(f"### {f['dimension']} {icon}\n")
        for item in f.get("items", []):
            loc = f"`{item.get('location', '')}`" if item.get("location") else ""
            detail_lines.append(f"- **{item.get('title', '')}** {loc}")
            detail_lines.append(f"  - {item.get('detail', '')}")
            if item.get("suggestion"):
                detail_lines.append(f"  - 💡 {item['suggestion']}")
            detail_lines.append("")
    findings_detail = "\n".join(detail_lines)

    cross_lines = [f"- {c}" for c in cross_cutting] if cross_cutting else ["无显著交叉问题"]
    cross_section = "\n".join(cross_lines)

    prio_lines = [f"{i+1}. **{p.get('priority', '')}** — {p.get('item', '')} ({p.get('dimension', '')})" for i, p in enumerate(priorities)] if priorities else ["无"]
    prio_section = "\n".join(prio_lines)

    return REPORT_TEMPLATE.format(
        skill_name=skill_name,
        date=date,
        overall=overall,
        dimension_summary=dim_table,
        findings_detail=findings_detail,
        cross_cutting=cross_section,
        priorities=prio_section,
    )


def main():
    parser = argparse.ArgumentParser(description="Skill 评审报告生成器")
    parser.add_argument("--skill", "-s", required=True, help="Skill 名称")
    parser.add_argument("--findings", "-f", required=True, help="评审发现 JSON 文件路径")
    parser.add_argument("--output", "-o", help="输出路径（默认 stdout）")
    args = parser.parse_args()

    data = load_findings(args.findings)
    report = generate_report(args.skill, data)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"🟢 报告已保存到 {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
