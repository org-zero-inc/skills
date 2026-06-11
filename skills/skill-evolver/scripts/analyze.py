#!/usr/bin/env python3
"""Skill Evolver: 分析与复盘脚本"""

import json
import re
import uuid
import argparse
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from record_issue import ISSUES_DIR, list_issues, ensure_issues_dir

SKILL_BASE_DIR = Path(__file__).parent.parent.parent
SESSIONS_DIR = Path(__file__).parent.parent / "sessions"

# --- 问题分类 ---

ISSUE_TYPE_PATTERNS = {
    "trigger": ["没有触发", "未触发", "trigger", "没有调用"],
    "execution": ["行为不符", "不符合预期", "执行失败", "指令不清晰"],
    "boundary": ["边界", "极端情况", "空值", "未处理"],
    "dependency": ["找不到", "路径错误", "缺失", "not found"],
    "compatibility": ["平台差异", "系统不兼容", "跨平台"],
}


def classify_issue(description: str, error_message: Optional[str] = None) -> str:
    text = (description + " " + (error_message or "")).lower()
    scores = {}
    for issue_type, patterns in ISSUE_TYPE_PATTERNS.items():
        score = sum(1 for p in patterns if p.lower() in text)
        scores[issue_type] = score
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "unknown"


def get_type_description(issue_type: str) -> str:
    descriptions = {
        "trigger": "触发类 - Skill 未能正确触发",
        "execution": "执行类 - 指令不够清晰",
        "boundary": "边界类 - 缺少边界情况处理",
        "dependency": "依赖类 - 工具/脚本缺失",
        "compatibility": "兼容类 - 平台差异",
        "unknown": "未知类型",
    }
    return descriptions.get(issue_type, "未知类型")


def suggest_likely_cause(issue: dict, issue_type: str) -> str:
    causes = {
        "trigger": "触发关键词不够明确",
        "execution": "指令描述过于模糊",
        "boundary": "未考虑边界情况",
        "dependency": "工具路径不存在",
        "compatibility": "未考虑平台差异",
        "unknown": "需要更多信息",
    }
    return causes.get(issue_type, "需要更多信息")


def suggest_update(issue_type: str) -> str:
    updates = {
        "trigger": "优化 description 字段",
        "execution": "改进指令表述",
        "boundary": "添加边界处理说明",
        "dependency": "检查脚本路径",
        "compatibility": "添加平台适配",
        "unknown": "详细记录上下文",
    }
    return updates.get(issue_type, "详细记录上下文")


def analyze_issue(issue: dict) -> dict:
    issue_type = classify_issue(issue.get("description") or "", issue.get("error_message") or "")
    issue["issue_type"] = issue_type
    issue["root_cause_analysis"] = {
        "issue_type": issue_type,
        "type_description": get_type_description(issue_type),
        "likely_cause": suggest_likely_cause(issue, issue_type),
        "update_suggestion": suggest_update(issue_type),
    }
    return issue


def analyze_cross_skill_dependencies(skill_name: str) -> dict:
    issues = list_issues(skill_name)
    dependencies = {}
    for issue in issues:
        context = (issue.get("context") or "") + " " + (issue.get("description") or "")
        refs = re.findall(r"skill-[a-z-]+", context.lower())
        if refs:
            dependencies[issue["id"]] = refs
    return {"dependencies": dependencies, "conflicts": [], "insights": []}


def analyze_skill(skill_name: str) -> dict:
    issues = list_issues(skill_name)
    if not issues:
        return {"error": f"Skill {skill_name} 暂无记录的问题"}
    analyzed = [analyze_issue(i) for i in issues]
    type_stats = {}
    for i in analyzed:
        t = i["issue_type"]
        type_stats[t] = type_stats.get(t, 0) + 1
    skill_path = SKILL_BASE_DIR / skill_name / "SKILL.md"
    content = ""
    if skill_path.exists():
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
    cross = analyze_cross_skill_dependencies(skill_name)
    return {
        "skill_name": skill_name,
        "total_issues": len(issues),
        "type_stats": type_stats,
        "issues": analyzed,
        "skill_content": content,
        "skill_path": str(skill_path),
        "cross_skill": cross,
    }


def generate_report(analysis: dict) -> str:
    if "error" in analysis:
        return analysis["error"]
    report = f"{'='*60}\nSkill 优化分析报告: {analysis['skill_name']}\n{'='*60}\n问题统计: {analysis['total_issues']} 个\n"
    for t, c in sorted(analysis["type_stats"].items(), key=lambda x: -x[1]):
        report += f"  - {t}: {c} 个\n"
    if analysis["cross_skill"]["dependencies"]:
        report += f"跨 Skill 依赖: {len(analysis['cross_skill']['dependencies'])} 个\n"
    return report


# --- 会话复盘 ---


def ensure_sessions_dir() -> Path:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    return SESSIONS_DIR


def analyze_skill_usage(skills: list[str]) -> dict:
    skill_counts = Counter(skills)
    return {
        "total_invocations": len(skills),
        "unique_skills": len(skill_counts),
        "top_skills": dict(skill_counts.most_common(5)),
    }


def analyze_issues(issues: list[dict]) -> dict:
    if not issues:
        return {"total": 0, "by_type": {}}
    type_counts = Counter(i.get("issue_type", "unknown") for i in issues)
    return {"total": len(issues), "by_type": dict(type_counts)}


def update_sessions_index(session_id: str, review: dict):
    index_file = ensure_sessions_dir() / "index.json"
    index = []
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)
    index.insert(0, {
        "id": session_id,
        "timestamp": review["timestamp"],
        "skills_count": len(review["invoked_skills"]),
        "issues_count": len(review["issues_encountered"]),
    })
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index[:50], f, ensure_ascii=False, indent=2)


def create_session_review(
    invoked_skills: list[str],
    issues_encountered: list[dict],
    session_summary: str = "",
    recommendations: list[str] = None,
) -> dict:
    session_id = str(uuid.uuid4())[:8]
    review = {
        "id": session_id,
        "timestamp": datetime.now().isoformat(),
        "invoked_skills": invoked_skills,
        "issues_encountered": issues_encountered,
        "session_summary": session_summary,
        "recommendations": recommendations or [],
        "skill_stats": analyze_skill_usage(invoked_skills),
        "issues_stats": analyze_issues(issues_encountered),
    }
    session_file = ensure_sessions_dir() / f"{session_id}.json"
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(review, f, ensure_ascii=False, indent=2)
    update_sessions_index(session_id, review)
    return review


def list_sessions(limit: int = 10) -> list:
    index_file = ensure_sessions_dir() / "index.json"
    if not index_file.exists():
        return []
    with open(index_file, "r", encoding="utf-8") as f:
        index = json.load(f)
    return index[:limit]


def get_session(session_id: str) -> Optional[dict]:
    session_file = ensure_sessions_dir() / f"{session_id}.json"
    if not session_file.exists():
        return None
    with open(session_file, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_review_report(review: dict) -> str:
    report = f"\n{'='*60}\n会话复盘报告: {review['id']}\n{'='*60}\n"
    report += f"\n📅 时间: {review['timestamp']}"
    report += f"\n\n📊 Skill 使用统计\n{'='*40}"
    report += f"\n  调用次数: {review['skill_stats']['total_invocations']}"
    report += f"\n  涉及 Skill: {review['skill_stats']['unique_skills']} 个\n"
    report += "\n  Top Skills:\n"
    for skill, count in review["skill_stats"]["top_skills"].items():
        report += f"    • {skill}: {count} 次\n"
    issues_stats = review["issues_stats"]
    report += f"\n🐛 问题统计\n{'='*40}\n  问题总数: {issues_stats['total']}\n"
    if issues_stats["by_type"]:
        report += "  按类型分布:\n"
        for issue_type, count in issues_stats["by_type"].items():
            report += f"    • {issue_type}: {count} 个\n"
    if review.get("issues_encountered"):
        report += f"\n📄 问题详情\n{'='*40}\n"
        for issue in review["issues_encountered"]:
            report += f"\n  [{issue.get('skill_name') or 'unknown'}] {issue.get('issue_type') or 'unknown'}\n    {(issue.get('description') or '')[:80]}"
    if review.get("recommendations"):
        report += f"\n🔔 优化建议\n{'='*40}\n"
        for i, rec in enumerate(review["recommendations"], 1):
            report += f"  {i}. {rec}\n"
    if review.get("session_summary"):
        report += f"\n📝 会话总结\n{'='*40}\n  {review['session_summary']}\n"
    return report


def quick_review(skills: list[str], issues: list[dict] = None) -> dict:
    review = {
        "invoked_skills": skills,
        "issues_encountered": issues or [],
        "skill_stats": analyze_skill_usage(skills),
        "issues_stats": analyze_issues(issues or []),
    }
    recommendations = []
    skill_stats = review["skill_stats"]
    issues_stats = review["issues_stats"]
    if skill_stats["unique_skills"] > 5:
        recommendations.append(f"本次会话使用了 {skill_stats['unique_skills']} 个 Skill，考虑是否有 Skill 功能重叠")
    if issues_stats["total"] > 0:
        recommendations.append(f"遇到 {issues_stats['total']} 个问题，建议记录并分析根因")
    most_used = skill_stats["top_skills"]
    if most_used:
        top_skill = max(most_used, key=most_used.get)
        if most_used[top_skill] > 3:
            recommendations.append(f"'{top_skill}' 被频繁调用({most_used[top_skill]}次)，考虑优化其触发条件")
    review["recommendations"] = recommendations
    return review


# --- CLI 入口 ---


def main():
    parser = argparse.ArgumentParser(description="Skill 分析与复盘工具")
    parser.add_argument("--skill", "-s", help="分析指定 Skill 的问题")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--skills", help="会话复盘：传入调用的 Skill 列表（逗号分隔）")
    parser.add_argument("--issues", help="会话复盘：传入问题列表（JSON 格式）")
    parser.add_argument("--summary", help="会话复盘：会话总结")
    parser.add_argument("--list", "-l", action="store_true", help="列出历史会话复盘")
    parser.add_argument("--session", help="查看指定会话复盘详情")
    parser.add_argument("--auto", "-a", action="store_true", help="自动模式（保存复盘记录）")
    args = parser.parse_args()

    # 报告模式
    if args.skill:
        result = analyze_skill(args.skill)
        if args.format == "json":
            print(json.dumps({k: v for k, v in result.items() if k != "skill_content"}, ensure_ascii=False, indent=2))
        else:
            print(generate_report(result))
        return

    # 复盘模式
    if args.list:
        sessions = list_sessions()
        if not sessions:
            print("暂无会话复盘记录")
        else:
            print(f"\n{'='*60}\n历史会话复盘 (共 {len(sessions)} 条)\n{'='*60}")
            for session in sessions:
                print(f"\n[{session['id']}] {session['timestamp'][:19]}")
                print(f"  Skills: {session['skills_count']} | Issues: {session['issues_count']}")
        return

    if args.session:
        review = get_session(args.session)
        if not review:
            print(f"未找到复盘记录: {args.session}")
        else:
            print(generate_review_report(review))
        return

    if args.skills:
        skills = [s.strip() for s in args.skills.split(",")]
        issues = []
        if args.issues:
            try:
                issues = json.loads(args.issues)
            except json.JSONDecodeError:
                print("警告: issues 格式错误，将被忽略")
        if args.auto:
            review = create_session_review(skills, issues, args.summary or "")
            print(generate_review_report(review))
        else:
            quick = quick_review(skills, issues)
            print(f"\n📊 快速复盘\n  调用 Skill: {quick['skill_stats']['unique_skills']} 个\n  问题数量: {quick['issues_stats']['total']}")
            if quick["recommendations"]:
                print(f"\n🔔 建议:")
                for rec in quick["recommendations"]:
                    print(f"  • {rec}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
