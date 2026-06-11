#!/usr/bin/env python3
"""
Skill Evolver: 问题记录脚本
用于记录调试过程中遇到的问题和解决方案
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
import argparse
import sys

ISSUES_DIR = Path(__file__).parent.parent / "issues"


def ensure_issues_dir(skill_name: str) -> Path:
    """确保问题存储目录存在"""
    skill_dir = ISSUES_DIR / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    return skill_dir


def load_issues(skill_name: str) -> list:
    """加载已存在的问题列表"""
    issues_file = ensure_issues_dir(skill_name) / "issues.json"
    if issues_file.exists():
        with open(issues_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_issues(skill_name: str, issues: list):
    """保存问题列表"""
    issues_file = ensure_issues_dir(skill_name) / "issues.json"
    with open(issues_file, "w", encoding="utf-8") as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)


def record_issue(
    skill_name: str,
    issue_type: str,
    description: str,
    solution: str,
    error_message: Optional[str] = None,
    context: Optional[str] = None,
    root_cause: Optional[str] = None,
    prevention: Optional[str] = None,
) -> dict:
    """记录一个问题"""
    issue_id = str(uuid.uuid4())[:8]
    issue = {
        "id": issue_id,
        "timestamp": datetime.now().isoformat(),
        "skill_name": skill_name,
        "issue_type": issue_type,
        "description": description,
        "error_message": error_message,
        "context": context,
        "solution": solution,
        "root_cause": root_cause,
        "prevention": prevention,
        "files_modified": [],
        "status": "pending",
    }

    # 保存单个问题详情
    issue_file = ensure_issues_dir(skill_name) / f"{issue_id}.json"
    with open(issue_file, "w", encoding="utf-8") as f:
        json.dump(issue, f, ensure_ascii=False, indent=2)

    # 更新问题列表
    issues = load_issues(skill_name)
    issues.append({"id": issue_id, "timestamp": issue["timestamp"], "status": "pending"})
    save_issues(skill_name, issues)

    # 更新全局汇总
    update_summary(skill_name, issue_type, "added")

    return issue


def update_summary(skill_name: str, issue_type: str, action: str):
    """更新全局汇总统计"""
    summary_file = ISSUES_DIR / "summary.json"
    summary = {}
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            summary = json.load(f)

    if skill_name not in summary:
        summary[skill_name] = {"total": 0, "by_type": {}}

    summary[skill_name]["total"] += 1 if action == "added" else -1

    if issue_type not in summary[skill_name]["by_type"]:
        summary[skill_name]["by_type"][issue_type] = 0
    summary[skill_name]["by_type"][issue_type] += 1 if action == "added" else -1

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def list_issues(skill_name: str) -> list:
    """列出指定Skill的所有问题"""
    issues = load_issues(skill_name)
    result = []
    for item in issues:
        issue_file = ensure_issues_dir(skill_name) / f"{item['id']}.json"
        if issue_file.exists():
            with open(issue_file, "r", encoding="utf-8") as f:
                detail = json.load(f)
                result.append(detail)
    return result


def print_issue(issue: dict):
    """格式化打印问题"""
    print(f"\n{'='*60}")
    print(f"ID: {issue['id']}")
    print(f"时间: {issue['timestamp']}")
    print(f"类型: {issue['issue_type']}")
    print(f"状态: {issue['status']}")
    print(f"\n问题描述:")
    print(f"  {issue['description']}")
    if issue.get("error_message"):
        print(f"\n错误信息:")
        print(f"  {issue['error_message']}")
    if issue.get("solution"):
        print(f"\n解决方案:")
        print(f"  {issue['solution']}")
    if issue.get("root_cause"):
        print(f"\n根因分析:")
        print(f"  {issue['root_cause']}")


def main():
    parser = argparse.ArgumentParser(description="Skill 问题记录工具")
    parser.add_argument("--skill", "-s", help="Skill名称")
    parser.add_argument("--issue", "-i", help="问题描述")
    parser.add_argument("--type", "-t", default="error", choices=["error", "warning", "behavior", "missing"], help="问题类型")
    parser.add_argument("--solution", help="解决方案")
    parser.add_argument("--error", "-e", help="错误信息")
    parser.add_argument("--context", "-c", help="上下文/触发条件")
    parser.add_argument("--root-cause", help="根因分析")
    parser.add_argument("--prevention", help="预防措施")
    parser.add_argument("--list", "-l", action="store_true", help="列出问题")
    parser.add_argument("--detail", "-d", help="查看指定问题的详情")

    args = parser.parse_args()

    if args.list:
        if not args.skill:
            print("错误: --list 需要指定 --skill")
            sys.exit(1)
        issues = list_issues(args.skill)
        if not issues:
            print(f"Skill '{args.skill}' 暂无记录的问题")
        else:
            print(f"\n{'='*60}")
            print(f"Skill '{args.skill}' 的问题列表 (共 {len(issues)} 个)")
            print("=" * 60)
            for issue in issues:
                print_issue(issue)

    elif args.detail:
        if not args.skill:
            print("错误: --detail 需要指定 --skill")
            sys.exit(1)
        issue_file = ensure_issues_dir(args.skill) / f"{args.detail}.json"
        if issue_file.exists():
            with open(issue_file, "r", encoding="utf-8") as f:
                issue = json.load(f)
                print_issue(issue)
        else:
            print(f"未找到问题: {args.detail}")

    elif args.issue:
        if not args.skill:
            print("错误: --issue 需要指定 --skill")
            sys.exit(1)
        if not args.solution:
            print("错误: --issue 需要指定 --solution")
            sys.exit(1)

        issue = record_issue(
            skill_name=args.skill,
            issue_type=args.type,
            description=args.issue,
            solution=args.solution,
            error_message=args.error,
            context=args.context,
            root_cause=args.root_cause,
            prevention=args.prevention,
        )
        print(f"\n问题已记录: {issue['id']}")
        print_issue(issue)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()