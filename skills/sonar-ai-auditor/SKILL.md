---
name: sonar-ai-auditor
description: |
  代码静态扫描与 AI 动态逻辑审计。以 Git Diff 为锚点，对版本变更代码执行增量审计：
  SonarQube 拉取变更文件的静态问题，LLM 对变更代码做动态语义审计（业务逻辑/并发/状态机/权限绕过），
  交叉去重后生成综合报告（MD + HTML）。
  触发词：SonarQube、sonar扫描、静态扫描、代码质量扫描、代码审计、代码巡检、
  Code Review 自动化、跑sonar、看下代码质量、分析代码问题、查代码缺陷、
  AI审计、增量扫描、动态审计、code audit。
  即使用户没有明确说 sonar，只要上下文涉及自动化代码质量分析、静态扫描、
  发现隐藏bug、审计代码逻辑漏洞，都应触发。
---

# Sonar AI Auditor — 增量代码审计（静态 + 动态双引擎）

以 Git Diff 驱动的增量代码审计技能。**SonarQube 静态引擎**拉取变更文件中的规则匹配问题，**LLM 动态引擎**对变更代码模拟运行时执行，捕获业务逻辑漏洞、并发竞态、状态机缺陷等静态工具无法发现的问题，交叉去重后生成综合报告。

---

## 工作流概览

```
用户输入: code_dir, source_branch, target_branch
                    │
                    ▼
        ┌───────────────────────┐
        │  Phase 1: Git Diff    │  定位变更文件与代码
        └───────────┬───────────┘
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
┌─────────────────┐  ┌──────────────────────┐
│ Phase 2a: Sonar │  │ Phase 2b: LLM        │
│ 增量静态扫描     │  │ 动态语义审计          │
│ (可退化跳过)     │  │                      │
└────────┬────────┘  └──────────┬───────────┘
         │                      │
         └──────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │  Phase 3: 交叉去重    │
        │  双引擎确认/独有标注   │
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │  Phase 4: 报告生成    │
        │  MD + HTML            │
        └───────────────────────┘
```

---

## 参数收集

执行前必须确认以下参数（如用户未提供，需主动询问）：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--code-dir` | 是 | Git 仓库的根目录路径 |
| `--source-branch` | 是 | 基准分支（如 `main`、`develop`） |
| `--target-branch` | 是 | 目标分支（如 `feat/xxx`、`fix/xxx`） |
| `--project-key` | 否 | SonarQube 项目 key，有 sonar-project.properties 时可省略 |
| `--output-dir` | 否 | 输出目录，默认 `~/sonar-ai-audit-output/` |
| `--format` | 否 | 报告格式 `md`/`html`/`both`，默认 `both` |
| `--skip-sonar` | 否 | 跳过 Sonar 扫描，仅 LLM 审计 |
| `--files` | 否 | 指定审计文件列表（逗号分隔），跳过 git diff |

---

## Phase 1：Git Diff 引擎

### 执行命令

在 `code_dir` 下执行：

```powershell
# 变更文件列表
git diff --name-only {source_branch}..{target_branch}

# 带上下文的 diff（10 行上下文）
git diff -U10 {source_branch}..{target_branch}

# 行数统计
git diff --stat {source_branch}..{target_branch}

# 提交日志
git log --oneline {source_branch}..{target_branch}
```

### 产出

- `changed_files`：变更文件列表，按类型分类：
  - **新增 (A)**：新创建的文件
  - **修改 (M)**：内容变更的文件
  - **删除 (D)**：被删除的文件
  - **重命名 (R)**：被重命名的文件
- `diff_content`：完整 diff 内容
- `diff_stat`：行数统计（+X / -Y）
- `commit_log`：提交历史

### 文件过滤

排除以下文件（不纳入审计）：
- 二进制文件：`.class`、`.jar`、`.png`、`.jpg`、`.gif`、`.svg`、`.ico`
- 构建产物：`node_modules/`、`dist/`、`build/`、`target/`、`.venv/`
- 配置/资源：`.properties`（非 sonar-project.properties）、`.xml`（非 pom.xml）、`.yml`/`.yaml`（非代码）

### 大仓库优化

变更文件 > 30 个时，按模块分组（controller/service/dao/model/config/util/common），后续各 Phase 逐模块处理。

### 如果用户指定了 --files

跳过 git diff，直接使用用户指定的文件列表。

---

## Phase 2a：SonarQube 增量扫描

### 前提条件

- SonarQube 服务可用（`SONAR_URL` + `SONAR_TOKEN` 环境变量，或 sonar-project.properties 中配置）
- 如果 `--skip-sonar` 被指定，直接跳过此 Phase

### 执行策略

**不重新触发 sonar-scanner**，只从 API 拉取已有结果中与变更文件交叉的问题：

1. 调用 SonarQube API `/api/issues/search` 拉取项目所有 open issues
2. 用 `changed_files` 过滤，只保留变更文件中的问题
3. 同时拉取 `sinceLeakPeriod=true` 获取新增代码（Leak Period）的问题
4. 合并去重

### API 调用

使用脚本：

```powershell
# 拉取全量 issues
uv run --with requests python scripts/sonar_auditor.py fetch --project-key <KEY> --output-dir <OUTPUT_DIR>

# 拉取新增代码 issues
uv run --with requests python scripts/sonar_auditor.py fetch --project-key <KEY> --new-code --output-dir <OUTPUT_DIR>
```

### 变更文件过滤

拉取全量 issues 后，在脚本中用 `changed_files` 列表过滤：
- 提取每个 issue 的 `component` 字段中的文件路径
- 只保留路径在 `changed_files` 中的 issue

### 退化策略

当以下任一条件满足时，Phase 2a 输出为空，自动退化：
- SonarQube 连接失败
- `SONAR_TOKEN` 未设置
- 项目 key 不存在
- `--skip-sonar` 被指定

退化时打印提示：`🟡 SonarQube 不可用，退化为纯 LLM 动态审计模式`

---

## Phase 2b：LLM 动态语义审计（核心）

### 检测的 5 类漏洞

| 漏洞类型 | 检测方式 | 示例 |
|---------|---------|------|
| 🎭 业务逻辑漏洞 | 模拟边界输入执行 | 转账金额负数未校验、订单状态非法跳转 |
| 🔄 并发/竞态条件 | 模拟多线程交叉执行 | Check-then-Act 非原子、共享变量无锁 |
| 🧩 状态机缺陷 | 遍历状态转移图 | "待支付"直接到"已完成"，缺失异常状态处理 |
| 🪤 隐式运行时异常 | 追踪特定输入路径 | 某分支下 NPE、资源泄漏路径 |
| 🚪 权限/认证绕过 | 模拟未认证请求 | API 入口缺权限校验、越权访问 |

### 执行步骤

对 `changed_files` 中每个代码文件（排除已过滤的文件类型）：

1. **读取文件完整内容** — 使用 Read 工具
2. **读取相关上下文** — 如果文件 import 了其他变更文件中的类/函数，也读取（最多 3 层依赖）
3. **执行 LLM 模拟运行时审计** — 以思考链方式执行以下 Prompt

### 审计 Prompt（通用）

```
你现在是一名高级代码审计专家。请对以下变更代码做【模拟运行动态审计】——
即假装这段代码运行在高并发、边界输入、网络延迟的真实环境中，
找出静态扫描工具（如 SonarQube）无法发现的隐藏动态逻辑错误。

## 变更上下文
- 文件：{file_path}
- 变更类型：{A/M/D}
- Diff 片段：
{diff_hunk_for_this_file}

## 完整代码
{code_content}

## 审计重点
1. 🎭 业务逻辑漏洞：数值边界未校验、越权访问、状态机不完整
2. 🔄 并发问题：竞态条件、死锁、非原子操作、共享变量无锁
3. 🧩 状态机缺陷：缺失的状态转移、异常状态未处理
4. 🪤 隐式运行时异常：特定分支/输入下才触发的 NPE、资源泄漏
5. 🚪 权限/认证绕过：未校验用户身份的 API 入口、越权

## 输出格式（必须严格遵循）
### 动态审计：{file_path}

#### [P0] 问题标题
- **漏洞类型**：🎭业务逻辑 / 🔄并发 / 🧩状态机 / 🪤运行时异常 / 🚪权限绕过
- **触发场景**：什么输入/并发/时序下触发
- **PoC 构造思路**：如何构造输入/请求来触发此漏洞（具体步骤）
- **后果**：崩溃 / 数据不一致 / 安全风险 / 资损
- **修复建议**：具体代码修改方案

#### [P1] 问题标题
...

### 总结
- 风险评级：🔴 高 / 🟡 中 / 🟢 低
- 发现问题数：X 个（P0: X, P1: X, P2: X）
```

### 语言特化 Prompt 片段

根据文件后缀自动注入额外的检查项：

**Java (.java)**
```
额外检查：
- Spring @Transactional 传播行为是否正确（特别是嵌套调用）
- Spring 依赖注入是否存在循环依赖
- MyBatis Mapper 中 ${} 拼接导致的 SQL 注入
- Stream API 中的异常处理（checked exception in lambda）
- synchronized 和 Lock 的混用
- Spring Security @PreAuthorize 缺失的接口
```

**Python (.py)**
```
额外检查：
- 可变默认参数 def func(arg=[]) 导致的状态共享
- except: 裸异常捕获吞掉所有错误
- is 和 == 的误用（特别是对 int/str 缓存范围外）
- 资源未使用 with 语句（文件/连接泄漏）
- asyncio 中的阻塞调用未用 run_in_executor
- FastAPI/Flask 缺失认证中间件的端点
```

**Go (.go)**
```
额外检查：
- goroutine 泄漏（无退出条件的 channel 接收）
- 未关闭的 channel 导致死锁
- defer 在循环中的行为
- map 并发读写（需 sync.Map 或 mutex）
- context 传播缺失
```

**TypeScript/JavaScript (.ts/.js/.tsx/.jsx)**
```
额外检查：
- undefined 与 null 处理不一致
- async/await 的错误处理缺失
- == 与 === 的使用
- 事件监听器未移除导致内存泄漏
- Promise.all 中单个 rejection 导致全部失败
- React useEffect 依赖数组缺失
```

### 并发控制

变更文件逐个审计，避免 token 爆炸。每个文件审计完成后立即记录结果，不等待所有文件完成。

---

## Phase 3：交叉去重与置信度评估

### 去重逻辑

对 Phase 2a（Sonar）和 Phase 2b（LLM）的发现做交叉比对：

1. **合并问题列表**：将 Sonar issues 和 LLM 发现统一为 `{file, line, type, description}` 格式
2. **匹配规则**：
   - 同一文件 + 同一行附近（±5行）+ 同类漏洞类型 → 视为同一问题
   - Sonar 的 `VULNERABILITY` 对应 LLM 的 `🚪权限绕过` / `🎭业务逻辑`
   - Sonar 的 `BUG` 对应 LLM 的 `🪤运行时异常` / `🔄并发`
3. **标注结果**：

| 情况 | 标注 | 置信度 |
|------|------|--------|
| Sonar 和 LLM 都发现 | 🔵 **双引擎确认** | 最高，基本可确认 |
| 仅 Sonar 发现 | 🟢 静态扫描独有 | 中，可能是规则误报，附提醒 |
| 仅 LLM 发现 | 🔴 动态审计独有 | 中高，这些是 Sonar 漏掉的，需人工复核 |

### 统一分级

所有问题统一按 P0/P1/P2 分级：
- **P0**：双引擎确认的 BLOCKER/CRITICAL，或 LLM 发现的明确安全漏洞
- **P1**：双引擎确认的 MAJOR，或 LLM 发现的业务逻辑缺陷
- **P2**：单引擎发现的 MINOR/INFO，或 LLM 发现的代码质量建议

---

## Phase 4：报告生成

### Markdown 报告

输出到 `{output_dir}/sonar-ai-audit-report.md`，结构如下：

```markdown
# 🔍 增量代码审计报告

## 1. 执行摘要
| 项目 | 值 |
|------|-----|
| 代码目录 | {code_dir} |
| 对比分支 | {source_branch} → {target_branch} |
| 执行时间 | {timestamp} |
| 变更文件数 | X 个（新增 X / 修改 X / 删除 X） |
| 代码行数 | +X / -Y |
| Sonar 问题数 | X 个（BLOCKER: X, CRITICAL: X, MAJOR: X） |
| LLM 发现数 | X 个（P0: X, P1: X, P2: X） |
| 综合风险评级 | 🔴 高 / 🟡 中 / 🟢 低 |

## 2. 变更代码概览

### 2.1 新增文件（X 个）
- `path/to/new_file.java` — 简要说明

### 2.2 修改文件（X 个）
| 文件 | 模块 | 行数 | 说明 |
|------|------|------|------|
| `path/to/file.java` | service | +10/-5 | 核心业务逻辑变更 |

### 2.3 删除文件（X 个）
- `path/to/deleted_file.java` — 影响说明

## 3. SonarQube 静态扫描结果（增量）

### 3.1 按严重级别

#### BLOCKER（X 个）
| 文件 | 行号 | 类型 | 规则 | 描述 |
|------|------|------|------|------|
| `file.java` | 42 | BUG | java:S2259 | 可能的空指针 |

#### CRITICAL（X 个）
...

### 3.2 Sonar 不可用时的提示
> 🟡 SonarQube 不可用，静态扫描部分跳过。仅依赖 LLM 动态审计结果。

## 4. LLM 动态语义审计结果

### 4.1 {file_path}
**风险评级：🔴 高**

#### [P0] 竞态条件导致余额不一致
- **漏洞类型**：🔄 并发
- **触发场景**：两个并发请求同时对同一账户转账
- **PoC 构造思路**：
  1. 启动两个线程同时调用 `transfer(accountId, 100)`
  2. 由于 check-balance 和 deduct 非原子，两个线程都通过余额检查
  3. 最终余额为负数
- **后果**：数据不一致，资损
- **修复建议**：使用 `SELECT ... FOR UPDATE` 或分布式锁

#### [P1] ...
...

### 4.2 {another_file}
...

## 5. 交叉分析

### 5.1 🔵 双引擎确认（X 个）
| 问题 | Sonar 规则 | LLM 类型 | 文件:行号 |
|------|-----------|---------|----------|
| SQL 注入 | java:S2077 | 🎭 业务逻辑 | `Mapper.java:28` |

### 5.2 🟢 静态扫描独有（X 个）
| 问题 | Sonar 规则 | 文件:行号 | 提醒 |
|------|-----------|----------|------|
| 未使用的变量 | java:S1481 | `Service.java:15` | 可能是误报 |

### 5.3 🔴 动态审计独有（X 个）
| 问题 | LLM 类型 | 文件:行号 | 需人工复核 |
|------|---------|----------|----------|
| 竞态条件 | 🔄 并发 | `TransferService.java:42` | ✅ 是 |

## 6. 综合风险清单

### P0 — 严重（X 个）
| # | 来源 | 问题 | 文件:行号 | 修复建议 |
|---|------|------|----------|---------|
| 1 | 🔵 双引擎 | SQL 注入 | `Mapper.java:28` | 使用参数化查询 |

### P1 — 高（X 个）
...

### P2 — 中（X 个）
...

## 7. 总结与建议
- 改动总体评估
- 优先处理事项（P0 必须修复后才能合并）
- 建议人工复核的文件列表
- 建议补充的测试用例
```

### HTML 报告

输出到 `{output_dir}/sonar-ai-audit-report.html`，采用 **Understand-Anything** 暖色暗调风格：
- 近黑背景 (#0a0a0a) + 琥珀色强调 (#d4a574)
- DM Serif Display 衬线标题 + Inter 无衬线正文 + JetBrains Mono 等宽代码
- 噪点纹理增加质感
- 与 code-diff-analyzer 报告风格一致

使用脚本生成：

```powershell
uv run --with requests python scripts/sonar_auditor.py report --input {json_path} --output {html_path}
```

---

## 交付物

| 文件 | 说明 |
|------|------|
| `sonar-ai-audit-report.md` | Markdown 综合审计报告 |
| `sonar-ai-audit-report.html` | HTML 可视化报告 |
| `sonar-issues.json` | SonarQube 拉取的原始数据（仅 Sonar 可用时） |

---

## 使用示例

**示例 1：增量审计（最常用）**
```
用户：帮我审计 feat/用户挂失 分支的代码质量
      仓库在 D:\code\my-app，基准分支 develop
```
→ 执行 Phase 1-4 全流程

**示例 2：完整参数**
```
用户：代码审计 --code-dir D:\code\my-app --source-branch develop --target-branch feat/支付优化 --project-key my-app --output-dir D:\reports\0622 --format both
```

**示例 3：跳过 Sonar，仅 LLM 审计**
```
用户：AI审计 D:\code\my-app main feat/重构 --skip-sonar
```

**示例 4：指定文件审计**
```
用户：审计这些文件的逻辑 D:\code\my-app\src\service\TransferService.java,D:\code\my-app\src\controller\PayController.java
```
→ 跳过 git diff，直接对指定文件执行 Phase 2b + Phase 4

**示例 5：快速指令**
```
用户：sonar扫描 D:\code\my-app develop feat/用户挂失
```

---

## 注意事项

1. **只读操作**：本 Skill 仅执行 git diff 和 SonarQube API 读取，不会修改代码
2. **Sonar 退化**：SonarQube 不可用时自动退化为纯 LLM 审计，不影响核心功能
3. **大仓库优化**：变更文件 > 30 个时按模块分组分段分析
4. **人工复核必要**：🔴 动态审计独有的问题需人工复核，LLM 可能存在幻觉
5. **PoC 仅为思路**：LLM 构造的 PoC 是触发思路，非可直接运行的攻击代码
6. **语言支持**：自动根据文件后缀注入语言特化检查项

## 依赖工具

- Git 命令行
- SonarQube API（可选，不可用时退化）
- Python/uv（sonar_auditor.py 脚本）
- PowerShell 7+
