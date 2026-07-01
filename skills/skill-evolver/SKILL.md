---
name: skill-evolver
description: |
  Skill 进化助手。会话复盘 → 记录问题 → 分析根因 → 经验提取 → 自动更新 Skill。
  触发："/evolve"、"复盘"、"记录这个问题"、"保存这次修复"、"更新这个Skill"、分析 Skill 问题时。
---

# Skill Evolver

自动分析调试过程中的问题，提取经验并更新目标 Skill。

## 工作流程

### 1. 会话复盘

分析本次会话的 Skill 调用情况，识别：
- 调用了哪些 Skill
- 哪些调用遇到了问题
- 问题的上下文和错误信息

### 2. 记录问题

将问题记录到 `issues/{skill_name}/` 目录下，每个问题一个 JSON 文件：

```json
{
  "id": "8位UUID",
  "timestamp": "ISO时间",
  "skill_name": "skill名称",
  "issue_type": "error | warning | behavior | missing",
  "description": "问题描述",
  "error_message": "原始错误信息（可选）",
  "context": "触发条件/上下文",
  "solution": "解决方案",
  "root_cause": "根因分析（可选）",
  "prevention": "预防措施（可选）",
  "status": "pending"
}
```

同时更新 `issues/{skill_name}/issues.json` 索引和 `issues/summary.json` 全局统计。

### 3. 分析根因

对每个问题进行分类和根因分析：

| 问题类型 | 识别特征 | 常见根因 | 更新建议 |
|---------|---------|---------|---------|
| trigger | 未触发、没调用 | 触发关键词不够明确 | 优化 description 字段 |
| execution | 行为不符、执行失败 | 指令描述过于模糊 | 改进指令表述 |
| boundary | 边界、极端情况、空值未处理 | 未考虑边界情况 | 添加边界处理说明 |
| dependency | 找不到、路径错误、缺失 | 工具/脚本缺失 | 检查脚本路径 |
| compatibility | 平台差异、系统不兼容 | 未考虑平台差异 | 添加平台适配 |

同时分析跨 Skill 依赖关系：检查问题上下文中是否引用了其他 Skill，识别潜在的触发冲突。

### 4. 经验提取

从所有已记录的问题中提取结构化经验，保存到 `issues/{skill_name}/evolution.json`：

```json
{
  "skill_name": "skill名称",
  "version": "1.0.0",
  "last_updated": "ISO时间",
  "experiences": [
    {
      "id": "对应问题ID",
      "pattern": "触发模式摘要",
      "problem": "问题描述",
      "solution": "解决方案",
      "context": "上下文",
      "issue_type": "问题类型",
      "root_cause": "根因",
      "validated": false
    }
  ],
  "cross_skill_insights": [
    {
      "skills": ["skill-a", "skill-b"],
      "insight": "依赖关系说明",
      "recommendation": "建议"
    }
  ]
}
```

### 5. 智能缝合

将提取的经验缝合到目标 Skill 的 SKILL.md 中：

1. **备份**：先复制 SKILL.md 到 `issues/{skill_name}/backups/SKILL.md.{时间戳}`
2. **description 增强**：对 trigger 类问题，将新的触发模式追加到 description 字段
3. **body 增强**：对其他类型问题，在 SKILL.md 末尾添加或更新「经验沉淀」章节：

```markdown
## 经验沉淀 (Evolution)

### 执行优化
- {解决方案1}
- {解决方案2}

### 边界处理
- {上下文}: {解决方案}
```

4. **预览确认**：缝合前先向用户展示变更预览，确认后再写入

## 会话复盘模式

当用户请求会话复盘时（而非针对单个问题）：

1. 收集本次会话调用的 Skill 列表和遇到的问题
2. 生成复盘报告，包含：
   - Skill 使用统计（调用次数、涉及 Skill 数、Top Skills）
   - 问题统计（总数、按类型分布）
   - 优化建议（如：某 Skill 被频繁调用考虑优化触发条件、多个 Skill 有重叠考虑合并）
3. 保存到 `sessions/{session_id}.json` 并更新 `sessions/index.json`

## 注意事项

- 大幅修改前先备份 SKILL.md 到 `issues/{skill_name}/backups/`
- 记录问题时尽量保留原始错误信息
- 缝合前务必预览变更，经用户确认后写入
- `issues/` 目录保存历史问题数据，是经验沉淀的基础
