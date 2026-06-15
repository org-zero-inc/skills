---
name: sonar-ai-auditor
description: 代码静态扫描与 AI 动态逻辑审计。触发此技能当用户提到「SonarQube」「sonar扫描」「静态扫描」「代码质量扫描」「代码审计」「代码巡检」「Code Review 自动化」「跑sonar」「看下代码质量」「分析代码问题」「查代码缺陷」时。即使用户没有明确说 sonar，只要上下文涉及自动化代码质量分析、静态扫描、发现隐藏bug、审计代码逻辑漏洞，都应触发。注意 — 如果你需要运行一个完整的 SonarQube 扫描流水线（触发 scanner → 拉 API → 生成 HTML 报告），请先使用本技能调用 `scripts/sonar_auditor.py` 脚本完成全流程，脚本会自动处理扫描、数据拉取、报告生成等步骤。
---

# Sonar AI Auditor — 代码静态扫描 + AI 动态逻辑审计

双引擎代码质量分析技能。**静态引擎**通过 SonarQube 扫描代码规范与安全漏洞并生成可视化 HTML 报告；**动态引擎**利用 Agent 自身的 LLM 推理能力模拟运行时数据流，捕获静态工具无法发现的业务逻辑错误、并发问题和状态机缺陷。

---

## 工作流概览

```
用户请求分析代码质量
│
├─ Action 1: 静态扫描 ──→ 触发 sonar-scanner
│                           ├─ 拉取 SonarQube API → JSON
│                           └─ 渲染 HTML 可视化报告
│
└─ Action 2: 动态审计 ──→ 读取目标代码文件
                            └─ 以 LLM 模拟执行，分析运行时逻辑错误
```

---

## Action 1：静态扫描与报告生成

### 前提条件

- 目标项目根目录下有 `sonar-project.properties`（或用户显式提供 `--project-key`）
- 本地安装了 `sonar-scanner` 命令行工具并已加入 PATH
- SonarQube 服务地址默认为 `http://localhost:9000`，可通过环境变量 `SONAR_URL` 覆盖
- 认证 Token 可通过环境变量 `SONAR_TOKEN` 设置

### 运行命令

使用 `uv run` 执行脚本：

```powershell
# 全流程：扫描 → 拉取 → HTML 报告
uv run --with requests python scripts/sonar_auditor.py scan --project-key <KEY>

# 如果项目目录下已有 sonar-project.properties，可省略 --project-key
uv run --with requests python scripts/sonar_auditor.py scan

# 仅拉取已有结果（不重新扫描）
uv run --with requests python scripts/sonar_auditor.py fetch --project-key <KEY>

# 将已有 JSON 转为 HTML
uv run --with requests python scripts/sonar_auditor.py report --input report.json

# 仅获取新增代码（Leak Period）的问题
uv run --with requests python scripts/sonar_auditor.py scan --new-code
uv run --with requests python scripts/sonar_auditor.py fetch --project-key <KEY> --new-code
```

`--project-dir` 指定项目目录时，建议放在子命令之后（如 `scan --project-dir PATH`），以兼容 argparse 的解析顺序。`--new-code` 参数让 SonarQube API 只返回 Leak Period（新增代码）的问题，适用于增量检查场景。

### 输出产物

| 文件 | 说明 |
|------|------|
| `sonar_report_<KEY>.json` | 完整 Issues + Metrics + Quality Gate 数据 |
| `sonar_report_<KEY>.html` | 可视化报告（严重级别分布柱状图 + 指标 + 问题卡片） |

### 脚本路径

脚本位于本 skill 目录下的 `scripts/sonar_auditor.py`，使用 `uv run --with requests python` 执行。由于脚本依赖 `requests` 库但环境中未必预装，通过 `--with requests` 让 uv 自动拉取。

---

## Action 2：AI 动态逻辑审计

### 核心思路

SonarQube 只能发现已知规则模式（空指针、未关闭资源、SQL 注入模板），对**业务语义层面**的运行时错误无能为力。此动作利用 LLM 的代码推理能力，模拟代码在真实运行环境中的执行路径，发现：

| 错误类型 | 说明 |
|---------|------|
| 🎭 业务逻辑漏洞 | 转账负数未校验、越权、状态跳过 |
| 🔄 并发/竞态条件 | 多线程下计数器无锁、Check-then-Act 非原子 |
| 🧩 状态机缺陷 | 不完整的状态转移、缺失的异常状态处理 |
| 🪤 隐式运行时异常 | 特定输入触发的 NPE、资源泄漏路径 |
| 🚪 权限/认证绕过 | 未校验用户身份的 API 入口 |

### 执行步骤

1. **确定目标文件** — 优先级：用户指定 → 静态扫描中 Bug 最多的文件 → 核心业务文件
2. **读取文件内容** — 使用 Read 工具读取完整内容
3. **以 LLM 执行模拟运行时审计**

将以下 Prompt 以你的思考链方式执行（不需要显式调用外部模型，你本身就是 LLM），并按结构化格式输出审计结果：

```
你现在是一名高级代码审计专家。请对以下代码做【模拟运行动态审计】——即假装这段代码运行在高并发、边界输入、网络延迟的真实环境中，找出静态扫描（如 SonarQube）无法发现的隐藏动态逻辑错误。

重点审查：
1. 业务逻辑漏洞：数值边界未校验、越权、状态机不完整
2. 并发问题：竞态条件、死锁、非原子操作
3. 隐式运行时异常：特定分支下才会触发的 NPE、资源泄漏
4. 状态/时间相关：依赖时序的业务逻辑缺陷

代码文件：{file_path}
{code_content}

输出格式（必须严格遵循）：
## 动态审计报告：{file_path}

### 发现的问题（按严重程度排序）

#### [P0] 标题
- **触发场景**：什么输入/并发/时序下触发
- **后果**：崩溃 / 数据不一致 / 安全风险
- **修复建议**：具体代码修改方案

#### [P1] 标题
...

### 总结
风险评级：高 / 中 / 低
需关注的文件数：X 个
```

### 与静态扫描联动

最优工作流是将 **Action 1** 的扫描结果作为 **Action 2** 的输入：

1. 查看 HTML 报告中 "Bug" 类型且严重级别为 BLOCKER/CRITICAL 的文件
2. 对这些文件执行 Action 2 的动态审计
3. 在最终报告中标注哪些问题是静态扫描已覆盖的，哪些是动态审计新增发现的

---

## 输出交付

每次执行后，向用户交付：

| 交付物 | 说明 |
|--------|------|
| 静态 HTML 报告路径 | 给用户的可视化报告 |
| 动态审计结论 | 结构化的文本报告，列出 P0/P1/P2 问题 |
| 综合建议 | 基于两轮分析的对代码质量的总体评估和改进优先级 |

## 完整工作流示例

用户说："帮我分析下项目的代码质量"

```
Step 1: 检查项目根目录是否有 sonar-project.properties
Step 2: 运行 Action 1 全流程扫描
  → uv run --with requests python scripts/sonar_auditor.py scan
Step 3: 读取 HTML 报告，确认 Bug 最多的文件
Step 4: 对核心业务文件执行 Action 2 动态审计
Step 5: 交付最终结果
```

用户说："查一下这个 service 类的逻辑有没有问题"

```
Step 1: 跳过 Action 1（用户指定了具体文件）
Step 2: Action 2: 读取文件内容，执行模拟运行动态审计
Step 3: 交付动态审计报告
```
