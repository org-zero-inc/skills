#!/usr/bin/env python3
"""Surface Scan: 纯表面检查，确认 Skill 结构完整性"""

import json
import argparse
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent.parent


def get_skills():
    return sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists())


def check_yaml(skill_path):
    """检查 YAML frontmatter 基本完整性"""
    skill_md = skill_path / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return [{
            "id": "yaml-missing",
            "severity": "error",
            "message": "SKILL.md 缺少 YAML frontmatter（--- ... ---）",
            "suggestion": "添加 name 和 description 字段",
        }]
    front = m.group(1)
    findings = []
    if not re.search(r"^name\s*:", front, re.MULTILINE):
        findings.append({"id": "yaml-no-name", "severity": "error", "message": "YAML 缺少 name 字段", "suggestion": "添加 name: <skill-name>"})
    if not re.search(r"^description\s*:", front, re.MULTILINE):
        findings.append({"id": "yaml-no-desc", "severity": "error", "message": "YAML 缺少 description 字段，LLM 无法触发", "suggestion": "添加 description 字段"})
    return findings


def check_referenced_files(skill_path):
    """检查 SKILL.md 中引用的文件是否存在"""
    skill_md = skill_path / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    refs = re.findall(r"`([^`]+(?:\.py|\.md|\.yaml|\.json|\.sh|\.ps1))`", text)
    findings = []
    for ref in refs:
        target = skill_path / ref
        if not target.exists():
            findings.append({
                "id": "ref-missing",
                "severity": "warning",
                "message": f"SKILL.md 引用了 `{ref}` 但文件不存在",
                "suggestion": f"创建 {ref} 或移除引用",
            })
    return findings


ALL_CHECKS = [check_yaml, check_referenced_files]


def audit_skill(skill_name):
    skill_path = SKILLS_DIR / skill_name
    if not (skill_path / "SKILL.md").exists():
        return {"skill": skill_name, "error": f"未找到 SKILL.md，无法评审"}

    findings = []
    for check in ALL_CHECKS:
        try:
            findings.extend(check(skill_path))
        except Exception as e:
            findings.append({"id": "check-error", "severity": "error", "message": f"检查异常: {e}", "suggestion": ""})

    return {"skill": skill_name, "total_findings": len(findings), "findings": findings}


def print_report(result):
    if "error" in result:
        print(f"🔴 {result['error']}")
        return
    print(f"\n{'='*50}")
    print(f"📋 表面检查: {result['skill']}")
    print(f"{'='*50}")
    if result["total_findings"] == 0:
        print("\n🟢 结构完整性通过，可以进入深度评审")
        return
    print(f"\n发现 {result['total_findings']} 个问题:\n")
    for f in result["findings"]:
        icon = {"error": "🔴", "warning": "🟡", "info": "🔔"}.get(f["severity"], "⚪")
        print(f"  {icon} [{f['id']}] {f['message']}")
        print(f"     💡 {f['suggestion']}\n")


def main():
    parser = argparse.ArgumentParser(description="Skill 表面检查工具")
    parser.add_argument("--skill", "-s", help="目标 Skill 名称")
    parser.add_argument("--all", "-a", action="store_true", help="检查所有 Skill")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text")
    args = parser.parse_args()

    skills = get_skills()
    if args.all:
        results = [audit_skill(s.name) for s in skills]
    elif args.skill:
        results = [audit_skill(args.skill)]
    else:
        print("可用 Skill:")
        for s in skills:
            print(f"  - {s.name}")
        print("\n使用 --skill <name> 或 --all")
        return

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print_report(r)


if __name__ == "__main__":
    main()
