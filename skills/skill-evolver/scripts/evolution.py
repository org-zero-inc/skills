#!/usr/bin/env python3
"""
Skill Evolver: 经验提取与缝合脚本
将问题记录转化为结构化经验，自动缝合到 Skill 文件
"""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
import argparse
import sys

sys.path.insert(0, str(Path(__file__).parent))
from record_issue import ISSUES_DIR, list_issues, ensure_issues_dir
from analyze import classify_issue, analyze_skill

SKILL_BASE_DIR = Path(__file__).parent.parent.parent


def load_evolution(skill_name: str) -> dict:
    """加载现有经验数据"""
    evolution_file = ensure_issues_dir(skill_name) / "evolution.json"
    if evolution_file.exists():
        with open(evolution_file, "r", encoding="utf-8") as f:
            return json.load(f)

    return {
        "skill_name": skill_name,
        "version": "1.0.0",
        "last_updated": datetime.now().isoformat(),
        "experiences": [],
        "cross_skill_insights": [],
    }


def save_evolution(skill_name: str, evolution: dict):
    """保存经验数据"""
    evolution["last_updated"] = datetime.now().isoformat()
    evolution_file = ensure_issues_dir(skill_name) / "evolution.json"
    with open(evolution_file, "w", encoding="utf-8") as f:
        json.dump(evolution, f, ensure_ascii=False, indent=2)


def extract_experience(issue: dict) -> dict:
    """从问题中提取经验"""
    return {
        "id": issue.get("id"),
        "pattern": extract_trigger_pattern(issue),
        "problem": issue.get("description") or "",
        "solution": issue.get("solution") or "",
        "context": issue.get("context") or "",
        "issue_type": issue.get("issue_type") or "unknown",
        "root_cause": issue.get("root_cause") or "",
        "validated": issue.get("status") == "applied",
        "extracted_at": datetime.now().isoformat(),
    }


def extract_trigger_pattern(issue: dict) -> str:
    """提取触发模式"""
    desc = issue.get("description") or ""
    patterns = []

    trigger_keywords = [
        r"触发词[：:]\s*([^\n,，]+)",
        r"关键词[：:]\s*([^\n,，]+)",
        r"用户说[：:]\s*['\"]([^'\"]+)['\"]",
        r"phrase[：:]\s*([^\n,，]+)",
    ]

    for pattern in trigger_keywords:
        match = re.search(pattern, desc, re.IGNORECASE)
        if match:
            patterns.append(match.group(1).strip())

    if not patterns:
        patterns = [f"当遇到 '{desc[:50]}...' 时"]

    return patterns[0]


def extract_all_experiences(skill_name: str) -> list:
    """提取所有经验"""
    issues = list_issues(skill_name)
    experiences = []

    for issue in issues:
        if issue.get("status") in ["applied", "pending"]:
            exp = extract_experience(issue)
            experiences.append(exp)

    return experiences


def generate_cross_skill_insights(skill_name: str) -> list:
    """生成跨 Skill 洞察"""
    insights = []

    issues = list_issues(skill_name)
    skill_dependencies = {}

    for issue in issues:
        context = issue.get("context") or ""
        dep_matches = re.findall(r"skill-[a-z-]+", context.lower())
        if dep_matches:
            skill_dependencies[skill_name] = list(set(dep_matches))

    for skill, deps in skill_dependencies.items():
        if deps:
            insights.append({
                "skills": [skill] + deps,
                "insight": f"{skill} 与 {', '.join(deps)} 存在依赖关系",
                "recommendation": f"确保两个 Skill 的触发条件不会冲突",
            })

    return insights


def stitch_to_description(skill_content: str, experiences: list) -> str:
    """将经验缝合到 description"""
    trigger_experiences = [e for e in experiences if e["issue_type"] == "trigger"]

    if not trigger_experiences:
        return skill_content

    trigger_patterns = [e["pattern"] for e in trigger_experiences[:3]]

    desc_pattern = r'(description:\s*[|>]?\s*)"([^"]+)"'
    match = re.search(desc_pattern, skill_content, re.MULTILINE | re.DOTALL)

    if match:
        current_desc = match.group(2)
        current_desc = current_desc.rstrip()

        new_triggers = "\n  ".join(trigger_patterns)
        current_desc += f"\n  增强触发: {new_triggers}"

        skill_content = skill_content.replace(
            match.group(0), f'{match.group(1)}"{current_desc}"'
        )

    return skill_content


def stitch_to_body(skill_content: str, experiences: list) -> str:
    """将经验缝合到 body"""
    other_experiences = [e for e in experiences if e["issue_type"] != "trigger"]

    if not other_experiences:
        return skill_content

    evolution_section = "\n\n## 经验沉淀 (Evolution)\n\n"

    execution_exp = [e for e in other_experiences if e["issue_type"] == "execution"]
    if execution_exp:
        evolution_section += "### 执行优化\n"
        for exp in execution_exp[:3]:
            evolution_section += f"- {exp['solution']}\n"
        evolution_section += "\n"

    boundary_exp = [e for e in other_experiences if e["issue_type"] == "boundary"]
    if boundary_exp:
        evolution_section += "### 边界处理\n"
        for exp in boundary_exp[:3]:
            evolution_section += f"- {exp['context']}: {exp['solution']}\n"
        evolution_section += "\n"

    if "## 经验沉淀" in skill_content:
        pattern = r"(\n## 经验沉淀.*?)(?=\n## |\Z)"
        skill_content = re.sub(pattern, evolution_section, skill_content, flags=re.DOTALL)
    else:
        skill_content += evolution_section

    return skill_content


def backup_skill(skill_name: str) -> Optional[Path]:
    """备份 Skill 文件"""
    skill_path = SKILL_BASE_DIR / skill_name
    backup_dir = ensure_issues_dir(skill_name) / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"SKILL.md.{timestamp}"

    skill_file = skill_path / "SKILL.md"
    if skill_file.exists():
        shutil.copy2(skill_file, backup_path)
        return backup_path
    return None


def extract_experiences(skill_name: str) -> dict:
    """提取经验"""
    evolution = load_evolution(skill_name)
    experiences = extract_all_experiences(skill_name)
    insights = generate_cross_skill_insights(skill_name)

    evolution["experiences"] = experiences
    evolution["cross_skill_insights"] = insights
    save_evolution(skill_name, evolution)

    return evolution


def stitch_experiences(skill_name: str, dry_run: bool = True) -> dict:
    """缝合经验到 Skill"""
    evolution = load_evolution(skill_name)
    experiences = evolution.get("experiences", [])

    if not experiences:
        return {"success": False, "message": "没有可缝合的经验"}

    skill_path = SKILL_BASE_DIR / skill_name / "SKILL.md"
    if not skill_path.exists():
        return {"success": False, "message": f"Skill 文件不存在: {skill_path}"}

    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    content = stitch_to_description(content, experiences)
    content = stitch_to_body(content, experiences)

    if content == original_content:
        return {"success": False, "message": "没有检测到需要缝合的内容"}

    if not dry_run:
        backup_path = backup_skill(skill_name)
        if backup_path:
            print(f"已备份到: {backup_path}")

        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content)

        for exp in experiences:
            exp["validated"] = True
        save_evolution(skill_name, evolution)

    return {
        "success": True,
        "dry_run": dry_run,
        "skill_name": skill_name,
        "experiences_stitched": len(experiences),
        "changes_preview": content[len(original_content):500] if content != original_content else "",
    }


def auto_evolution(skill_name: str) -> dict:
    """自动模式：一键提取并缝合"""
    print(f"\n{'='*60}")
    print(f"自动进化: {skill_name}")
    print(f"{'='*60}")

    print("\n📦 提取经验...")
    evolution = extract_experiences(skill_name)
    print(f"   提取了 {len(evolution['experiences'])} 条经验")
    print(f"   发现 {len(evolution['cross_skill_insights'])} 条跨 Skill 洞察")

    if not evolution["experiences"]:
        return {"success": False, "message": "没有可用的经验"}

    print("\n🧵 缝合经验到 Skill...")
    result = stitch_experiences(skill_name, dry_run=False)

    if result["success"]:
        print(f"\n🟢 自动进化完成!")
        print(f"   缝合了 {result['experiences_stitched']} 条经验")
    else:
        print(f"\n🟡 {result['message']}")

    return result


def generate_evolution_report(skill_name: str) -> str:
    """生成经验报告"""
    evolution = load_evolution(skill_name)

    report = f"""
{'='*60}
经验沉淀报告: {skill_name}
{'='*60}

📅 最后更新: {evolution.get('last_updated', 'N/A')}
📊 版本: {evolution.get('version', '1.0.0')}

📚 经验列表 ({len(evolution['experiences'])} 条)
{'-'*40}
"""

    for i, exp in enumerate(evolution["experiences"], 1):
        status = "🟢" if exp.get("validated") else "⏳"
        report += f"""
{i}. {status} [{exp['issue_type']}]
   模式: {exp['pattern'][:60]}...
   问题: {exp['problem'][:60]}...
   方案: {exp['solution'][:60]}...
"""

    if evolution.get("cross_skill_insights"):
        report += f"""
🔗 跨 Skill 洞察 ({len(evolution['cross_skill_insights'])} 条)
{'-'*40}
"""
        for insight in evolution["cross_skill_insights"]:
            report += f"""
   Skills: {', '.join(insight['skills'])}
   洞察: {insight['insight']}
   建议: {insight.get('recommendation', 'N/A')}
"""

    return report


def main():
    parser = argparse.ArgumentParser(description="Skill 经验提取与缝合工具")
    parser.add_argument("--skill", "-s", required=True, help="Skill名称")
    parser.add_argument("--extract", "-e", action="store_true", help="提取经验")
    parser.add_argument("--stitch", action="store_true", help="缝合经验")
    parser.add_argument("--auto", "-a", action="store_true", help="自动模式")
    parser.add_argument("--dry-run", "-n", action="store_true", help="预览模式")
    parser.add_argument("--report", "-r", action="store_true", help="生成报告")

    args = parser.parse_args()

    if args.auto:
        result = auto_evolution(args.skill)
        if result["success"]:
            print("\n📄 生成报告:")
            print(generate_evolution_report(args.skill))

    elif args.extract:
        evolution = extract_experiences(args.skill)
        print(f"\n🟢 提取完成!")
        print(f"   经验数量: {len(evolution['experiences'])}")
        print(f"   跨 Skill 洞察: {len(evolution['cross_skill_insights'])}")

    elif args.stitch:
        if args.dry_run:
            print("\n🔍 预览模式\n")
        result = stitch_experiences(args.skill, dry_run=args.dry_run)
        if result["success"]:
            print(f"\n🟢 缝合成功!")
            print(f"   处理了 {result['experiences_stitched']} 条经验")
            if args.dry_run:
                print("\n📝 预览变更:")
                print(result["changes_preview"])
        else:
            print(f"\n🔴 失败: {result['message']}")

    elif args.report:
        print(generate_evolution_report(args.skill))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()