---
name: skill-evolver
description: |
  Skill 进化助手。会话复盘 → 记录问题 → 分析根因 → 经验提取 → 自动更新 Skill。
  触发："/evolve"、"复盘"、"记录这个问题"、"保存这次修复"、"更新这个Skill"、分析 Skill 问题时。
---

# Skill Evolver

自动分析调试过程中的问题，提取经验并更新目标 Skill。

## 工作流程

1. **会话复盘** — 分析本次会话的 Skill 调用情况
2. **记录问题** — 记录调试中遇到的问题和解决方案
3. **分析根因** — 分类问题类型，定位根源
4. **经验提取** — 将问题转化为结构化经验
5. **智能缝合** — 自动更新 SKILL.md

## 命令行

### 记录问题
```
uv run scripts/record_issue.py --skill <name> --issue "问题" --solution "方案"
```

### 分析
```
uv run scripts/analyze.py --skill <name>                    # 分析记录的问题
uv run scripts/analyze.py --skills "<list>"                 # 会话复盘
uv run scripts/analyze.py --skills "<list>" --auto          # 会话复盘并保存
```

### 经验提取与缝合
```
uv run scripts/evolution.py --skill <name> --auto           # 自动：提取 + 缝合
uv run scripts/evolution.py --skill <name> --extract        # 仅提取经验
uv run scripts/evolution.py --skill <name> --stitch -n      # 预览缝合（不写入）
uv run scripts/evolution.py --skill <name> --stitch         # 执行缝合
uv run scripts/evolution.py --skill <name> --report         # 查看经验沉淀报告
```

## 注意事项

- 大幅修改前使用 `--dry-run` / `-n` 预览
- 修改前自动备份到 `issues/<skill>/backups/`
- 记录问题时尽量保留原始错误信息
