## Context

美乔发现了 grapeot 的 context-infrastructure repo，想借助它的设计哲学和框架结构，在自己的 Claude Code 工作流中搭建个人 context 基建。最终目标不是复制这个 repo，而是理解其设计哲学，并在日常 AI 交互中实践，逐步积累属于自己的 skills 和 axioms。

### 核心适配挑战

| Repo 原设计 | 你的环境 (Claude Code) |
|---|---|
| AGENTS.md（session 入口） | `CLAUDE.md`（自动加载） |
| rules/SOUL.md + USER.md | CLAUDE.md 中的对应章节 |
| Observer/Reflector (OpenCode cron) | 手动触发 + Claude Code memory 系统 |
| rules/axioms/ | 项目内 `.context/axioms/` 或 Claude Code memory |
| rules/skills/ | 项目内 `.context/skills/` 或 Claude Code custom commands |

---

## Phase 0：哲学沉浸（第 1-3 天，纯阅读，不改代码）

**目标**：理解 "为什么" 再动手。Repo 本身反复强调：axioms 不能复制，只能从自身经历中蒸馏。

### 必读材料（按顺序）

1. **三篇奠基 axiom**——理解整个系统的理论根基：
   - [a05_docs_long_term_memory.md](rules/axioms/a05_docs_long_term_memory.md) — 文档即长期记忆，解释了为什么要建 context 基建
   - [a02_multiplier_not_replacement.md](rules/axioms/a02_multiplier_not_replacement.md) — AI 是能力放大器，不是替代品
   - [a03_ic_to_manager.md](rules/axioms/a03_ic_to_manager.md) — 用 AI 需要管理者思维（招聘/委派/培训/指导/验收）

2. **记忆系统设计文档**——理解三层架构的运作逻辑：
   - [PRD.md](periodic_jobs/ai_heartbeat/docs/PRD.md) — 系统设计：Pull vs Push、稀疏上下文、信息密度
   - [KNOWLEDGE_BASE.md](periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md) — Observer/Reflector 的 SOP：红黄绿优先级、晋升标准

3. **两篇关于飞轮和自我系统化的 axiom**：
   - [a10_rapport_over_raw_intelligence.md](rules/axioms/a10_rapport_over_raw_intelligence.md) — 为什么积累 context 比模型智力更重要
   - [m08_self_systematization.md](rules/axioms/m08_self_systematization.md) — 人+工具+日志+AI = 混合有机体（含过度系统化的警告）

4. **飞轮机制**：
   - [workflow_knowledge_flywheel.md](rules/skills/workflow_knowledge_flywheel.md) — 笨数据 + 笨方法 + 笨模型 = 精炼知识
   - [workflow_cognitive_profile_extraction.md](rules/skills/workflow_cognitive_profile_extraction.md) — axiom 是怎么从原始数据中蒸馏出来的

**Phase 0 完成标志**：能用自己的话说清楚：(a) 什么是 context rot，(b) L3/L1/L2 分层的意义，(c) skill 和 axiom 的区别，(d) 为什么不能直接复制别人的 axiom。

---

## Phase 1：身份基础（第 4 天，~30 分钟，最高 ROI）

**目标**：让 Claude Code 立刻认识你。Repo 的 setup_guide 说得很清楚：填好 USER.md，AI 行为立刻个性化。

### 你的起点

你已经有一份 user profile 在 `~/.claude/projects/-home-meiqiao-projects-creation-system/memory/user_profile.md`，内容包括：称呼、职业（数据工程师）、核心身份（自我探索者/创作者/Builder）、沟通偏好等。这是好的起点。

### 行动

**1a. 在常用项目根目录创建 CLAUDE.md**

结构参考（融合了 repo 的 SOUL.md + USER.md + COMMUNICATION.md）：

```markdown
# CLAUDE.md

## 你是谁（AI 行为准则）
- 真正有用，不是表演有用
- 有观点，先尝试再问人
- 不说废话，不用填充词
- 读文件、搜上下文，先自己解决

## 我是谁
[从现有 user_profile.md 扩展，加入更多细节：技术栈、当前项目、工作节奏]

## 沟通方式
[从 repo 的 COMMUNICATION.md 中挑选适合你的部分]

## 项目结构
[当前项目的目录路由]

## Context 系统
- 决策原则：.context/axioms/
- 可复用工作流：.context/skills/
- 观察记录：.context/memory/observations.md
```

**1b. 同步更新 Claude Code memory**

确保 context-infrastructure 项目目录下的 Claude Code memory 也有你的 profile。

**验证**：新开一个 Claude Code session，问"介绍一下你对我的了解"。

---

## Phase 2：研究框架结构（第 5-7 天，~2 小时）

**目标**：理解 axiom 和 skill 的格式，但不急着创建自己的。

### 行动

**2a. 浏览 axiom 体系**
- 读 [rules/axioms/INDEX.md](rules/axioms/INDEX.md)：注意分类方式（A/T/M/V/X）、触发词机制、核心公理组
- 精读 2-3 个不同类别的 axiom，理解内部结构：核心公理 → 深度推演 → 适用判断表 → 陷阱 → 关联公理
- 标注引起共鸣的 axiom（不是复制，是记下"这个视角对我有启发"）

**2b. 浏览 skill 体系**
- 读 [rules/skills/INDEX.md](rules/skills/INDEX.md)：理解三类（Workflow / API Guide / BestPractice）
- 重点看 BestPractice 类（工具无关，可直接迁移）：
  - [bestpractice_ai_programming_mindset.md](rules/skills/bestpractice_ai_programming_mindset.md) — AI 编程心法
  - [bestpractice_staged_approach.md](rules/skills/bestpractice_staged_approach.md) — 隔离-处理-验证循环
  - [bestpractice_temporal_info_verification.md](rules/skills/bestpractice_temporal_info_verification.md) — 时效信息验证

**2c. 确定 3-5 个值得立刻采用的 skill**

BestPractice 类中带 ✅ 的基本都可以直接用。挑与你日常工作最相关的。

---

## Phase 3：搭建 L3 层（第 8-14 天）

**目标**：在你的工作项目中建立自己的 context 目录结构。

### 行动

**3a. 创建目录结构**

在你最常用的项目目录下：

```
your-project/
  CLAUDE.md                      # Phase 1 已创建
  .context/
    axioms/                      # 你自己的 axiom（初始为空）
      INDEX.md                   # 索引
    skills/                      # 你自己的 skill
      INDEX.md                   # 索引
    memory/
      observations.md            # L1/L2 等价物
```

**3b. 移植适用的 BestPractice skill**

从 Phase 2 筛选的 skill 中，把适合你的复制到 `.context/skills/`，修改为 Claude Code 语境（去掉 OpenCode 相关引用）。

**3c. 更新 CLAUDE.md 引用 .context/**

让 Claude Code 在每次 session 开始时知道这些文件的存在。

---

## Phase 4：建立观察习惯（第 15-30 天）

**目标**：用手动方式替代 repo 的自动 observer/reflector，开始积累原始素材。

### 核心适配

Repo 的 observer.py 依赖 OpenCode Server API，在 Claude Code 中不可用。但 observer 的本质是："回顾今天的工作，提取有复用价值的认知结晶"。这个过程可以手动触发。

**4a. 每日观察（5 分钟）**

工作结束时，给 Claude Code 一个 prompt：

> "回顾今天我们的工作。用红黄绿系统总结关键观察：红色=跨项目的方法论/约束洞察，黄色=活跃项目的决策/进展，绿色=常规任务完成。追加到 .context/memory/observations.md。"

**红黄绿标准**（来自 repo 的 KNOWLEDGE_BASE.md）：
- 🔴 红：3 个月后仍有复用价值的跨项目模式
- 🟡 黄：未来几周内需要的项目决策/进展
- 🟢 绿：当天任务执行记录，1-2 周后可清理

**4b. 每周反思（15 分钟，周末）**

> "读 .context/memory/observations.md。分析本周红色和高优先黄色条目，识别重复出现的模式。如果有条目满足晋升条件（跨项目通用、多次验证、有明确应用场景），起草为 axiom 或 skill 候选。清理过期绿色条目。"

**4c. 同时利用 Claude Code 原生 memory**

- Claude Code memory (`~/.claude/projects/*/memory/`)：快速的、session 级别的 recall
- `.context/memory/observations.md`：结构化的、带优先级的、为 axiom 蒸馏提供素材的长期记录

两者互补，不冲突。

---

## Phase 5：开始蒸馏 axiom（第 2-3 个月）

**前提**：至少 3-4 周的 observations 积累。

### 行动

**5a. 理解 axiom 的质量标准**

好的 axiom 必须满足（来自 repo 的 cognitive_profile_extraction workflow）：
- **持久性**：跨时间反复出现
- **独特性**：属于你个人的，不是通用常识
- **预测性**：能预测你未来的决策倾向
- **边界性**：有明确的不适用条件

**5b. 蒸馏前 3-5 个 axiom**

> "分析 .context/memory/observations.md 中所有红色和高优先黄色条目。找出 3-5 个反复出现的决策模式。每个模式写出：(1) 一段话的核心陈述，(2) 3+ 条来自观察记录的证据，(3) 至少一个不适用的边界条件。"

**5c. 不需要一开始就写到 repo 的深度**

Repo 里每个 axiom 有 6 个章节（核心/推演/适用判断/陷阱/关联/实践）。你的第一版 axiom 只需要核心陈述 + 证据就够了，深度随时间自然生长。

**5d. 建立 axiom 索引**

创建 `.context/axioms/INDEX.md`，分类方式不必照搬 A/T/M/V/X——用你自己的认知框架分类。

---

## Phase 6：飞轮运转（第 3 个月+）

**目标**：日常工作 → 观察 → 蒸馏 axiom/skill → 改善日常工作，形成闭环。

### 行动

**6a. Skill 积累**：每当你发现自己向 Claude 解释同一个流程第二次，就把它写成 skill。

**6b. 月度系统审查**：
- Axiom 还准确吗？需要基于新证据更新吗？
- 有红色观察积压了好几周没晋升吗？为什么？
- 有 skill 该退役或合并吗？
- CLAUDE.md 太长了吗？需要拆分子文件吗？

**6c. 进阶选项**（等手动流程稳定后再考虑）：
- Claude Code 的 `/schedule` 功能可以创建定时 remote agent，部分自动化 observer
- 语义搜索（当 `.context/` 积累足够内容后）
- 自定义 Claude Code slash commands 封装常用 skill

---

## 实战工作流：公司环境落地指南

### 一次性设置（明天做，约 20 分钟）

**Step 1：在公司电脑上 clone mc-context-infrastructure**

找一个独立于公司 repo 的个人目录：

```bash
cd ~/projects   # 或你偏好的个人目录
git clone <your-mc-context-infrastructure-url>
```

关键点：**这个 repo 不要放在公司 repo 里面**。公司 repo 有自己的 git，两者平行存在。

**Step 2：在公司项目根目录创建轻量 CLAUDE.md**

打开公司 repo 根目录，创建 `CLAUDE.md`：

```markdown
# CLAUDE.md - [公司项目名]

## 上下文系统
我的个人 context 规则在 ~/projects/mc-context-infrastructure/，session 开始时请读：
- ~/projects/mc-context-infrastructure/rules/SOUL.md
- ~/projects/mc-context-infrastructure/rules/USER.md
- ~/projects/mc-context-infrastructure/rules/COMMUNICATION.md
- ~/projects/mc-context-infrastructure/rules/skills/INDEX.md

## 项目说明
[一两句话：这个 repo 是做什么的，技术栈，当前阶段]

## 项目结构
[主要目录和各自职责，帮 Claude 快速定位文件]

## 代码规范
[公司特有约束：Python 版本、数据库类型、API 风格、命名规则等]
```

**Step 3：在 mc-context-infrastructure 的 WORKSPACE.md 注册公司项目**

打开 `rules/WORKSPACE.md`，在快速查询部分添加：

```
- `company-project` → `adhoc_jobs/company_project_name/` (代码实验、笔记、临时 script)
```

---

### 公司内容放哪里

| 内容类型 | 存放位置 | 命名格式示例 |
|---|---|---|
| 会议记录 | `contexts/daily_records/` | `2026-04-07_sprint_planning.md` |
| 技术调研、竞品分析 | `contexts/survey_sessions/` | `2026-04-07_dbt_vs_spark.md` |
| 复盘、架构思考 | `contexts/thought_review/` | `data_pipeline_design_review.md` |
| 代码实验、临时 script | `adhoc_jobs/<company_project>/` | 自由命名 |
| 项目决策 / 进展 | `contexts/memory/OBSERVATIONS.md` | 🟡 黄色条目 |

**核心原则**：公司代码和敏感数据留在公司 repo，mc-context-infrastructure 只存你自己的认知产出——笔记、洞察、决策记录。没有数据泄漏风险。

---

### 每次写代码的 Session 工作流

#### 开始前（2 分钟）

给 Claude 一句话上下文，模板：

> "今天的任务是 [具体目标]。成功标准是 [可验证的结果]。相关文件是 [路径]。"

为什么要这样做：`bestpractice_ai_programming_mindset.md` 的核心发现是，**AI 编程 70% 的问题出在上下文和成功标准不清楚**，不是模型能力不够。这一句话是最高 ROI 的投入。

例子：
> "今天的任务是给 staging 表加 incremental logic。成功标准是跑 `dbt run --select staging_orders` 不报错，且 row count 与昨天一致。相关文件是 `models/staging/staging_orders.sql`。"

#### 执行中

**遇到复杂改动**：先用语音输入说清楚你想做什么，让 Claude 复述理解，对齐后再开始改代码。对应 A03「委派前先对齐期望」。

**遇到代码改不好（一直 retry 没效果）**：停下来，触发 `bestpractice_ai_debugging_diagnosis.md` 的诊断决策树：

1. Claude 看到足够上下文了吗？（报错信息、日志、相关文件）
2. 成功标准说清楚了吗？（"不报错"太模糊，"row count 一致"才具体）
3. 有没有给 Claude 验证的方式？（贴截图、贴命令输出）

三个都满足了还是改不好，才是真正的模型/架构问题。

**遇到破坏性操作**（删数据、数据库迁移、大规模重构）：触发 `bestpractice_staged_approach.md`——先 dry run 看输出，人工确认，再真正执行。

#### 结束后（5 分钟，Phase 4 的核心）

工作结束，切换到 mc-context-infrastructure 目录，发这个 prompt：

> "回顾今天我们的工作（[今天做了什么，一句话]）。用红黄绿系统总结关键观察，追加到 contexts/memory/OBSERVATIONS.md：
> - 🔴 红：跨项目有复用价值的方法论/约束洞察（3 个月后仍有效）
> - 🟡 黄：公司项目的决策/进展/待跟进事项（未来几周需要）
> - 🟢 绿：今天任务的执行记录（1-2 周后可清理）"

**实际写出来的例子**：

```
🟡 2026-04-07 | [data-pipeline] 决定用 dbt incremental 而不是 full-refresh，
   原因：数据量已超过 full-refresh 可接受时间窗口（>15min）。后续所有大表都走 incremental。
🟢 2026-04-07 | 完成 staging_orders incremental logic，PR #42 已提交等待 review
```

**注意**：红色条目才是最有价值的，是未来 axiom 的原材料。如果某天全是绿色，说明今天没有值得沉淀的新洞察——这很正常，不必强求。

#### 每周末（15 分钟，同样在 mc-context-infrastructure 目录）

> "读 contexts/memory/OBSERVATIONS.md。分析本周红色和高优先黄色条目，识别重复出现的模式。如果有条目满足晋升条件（跨项目通用、多次验证、有明确应用场景），起草为 axiom 或 skill 候选。清理过期绿色条目。"

---

## 需要注意的反模式

1. **不要复制别人的 axiom**：Repo 的 43 条 axiom 是作者个人经历的蒸馏。读它们获取启发，但你的 axiom 必须从你自己的观察中长出来。
2. **不要一次全部搭好**：严格按 phase 推进。Phase 1 的 ROI 远高于 Phase 4-6。
3. **不要过度自动化 reflector**：手动周反思是 feature 不是 bug——这个判断过程本身在训练你的 meta-cognition。
4. **CLAUDE.md 不要无限膨胀**：超过 ~200 行就拆分为子文件引用。Context window 是有限资源（axiom A05 的核心观点）。
5. **不要因为追求完美而不开始**：一个只有 USER.md 的系统已经比没有系统好 10 倍。

---

## 关键文件清单

| 用途 | 文件路径 |
|---|---|
| Repo 入口 & session 路由 | [AGENTS.md](AGENTS.md) |
| 搭建指南 | [setup_guide.md](setup_guide.md) |
| AI 身份模板 | [rules/SOUL.md](rules/SOUL.md) |
| 用户画像模板 | [rules/USER.md](rules/USER.md) |
| 沟通风格指南 | [rules/COMMUNICATION.md](rules/COMMUNICATION.md) |
| 目录路由 | [rules/WORKSPACE.md](rules/WORKSPACE.md) |
| Axiom 索引 | [rules/axioms/INDEX.md](rules/axioms/INDEX.md) |
| Skill 索引 | [rules/skills/INDEX.md](rules/skills/INDEX.md) |
| 记忆系统 PRD | [periodic_jobs/ai_heartbeat/docs/PRD.md](periodic_jobs/ai_heartbeat/docs/PRD.md) |
| Observer/Reflector SOP | [periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md](periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md) |
| 核心 axiom: 文档即记忆 | [rules/axioms/a05_docs_long_term_memory.md](rules/axioms/a05_docs_long_term_memory.md) |
| 核心 axiom: AI 是放大器 | [rules/axioms/a02_multiplier_not_replacement.md](rules/axioms/a02_multiplier_not_replacement.md) |
| Cognitive extraction workflow | [rules/skills/workflow_cognitive_profile_extraction.md](rules/skills/workflow_cognitive_profile_extraction.md) |

---

## 验证方式

- **Phase 1 验证**：新 session 问"介绍你对我的了解"，AI 回答准确反映你的 profile
- **Phase 4 验证**：2 周后 observations.md 有 10+ 条带红黄绿标记的观察
- **Phase 5 验证**：第一个 axiom 有核心陈述 + 3 条来自 observations 的真实证据 + 1 条边界条件
- **Phase 6 验证**：月度审查时，发现 axiom/skill 确实影响了你的日常决策

## Repo 的设计哲学：三层理解

### 第一层：为什么要建 context 基建？

核心问题是 **context rot**（上下文腐烂）。AI 的上下文窗口本质是"七秒记忆的鱼"——切换 session、对话太长、换个任务，之前的理解就消失了。这导致三种失败：
- **空间遗忘**：改文件 A 时看不到文件 B 已有相同功能，重复实现
- **时间自我推翻**：修好的 bug 在几轮迭代后被改回去
- **全局视角缺失**：宁愿重写也不复用已有代码

解法不是更好的 prompt，而是**把短期上下文窗口转化为可持久化、可版本化的长期资产**——这就是 context 基建存在的理由。

### 第二层：和 AI 的关系应该是什么？

**AI 是放大器，不是替代品。** 放大效果与你自身的专业度和判断力成正比。

关键心智转变：从 IC（个人贡献者）到管理者。用 AI 的五大管理支柱：
1. **招聘** → 选对模型（不同任务用不同模型）
2. **委托** → 显式化你的隐含期望（用语音输入降低表达摩擦）
3. **培训** → 建立持久化知识库（CLAUDE.md、文档、context 文件）
4. **指导** → 教方法论，不给答案（让 AI 学会自己钓鱼）
5. **验收** → 定义可测量的成功标准，建立反馈循环

70-80% 完成度不是失败，是 feature——剩下的 30% 是你的品味、判断和标准制定能力的体现。

### 第三层：系统怎么自我演进？

三层记忆架构形成飞轮：

```
L3（全局约束）← 晋升 ← L2（周反思）← 蒸馏 ← L1（日观察）← 日常工作
     ↓                                                        ↑
  每次 session 自动加载 ─────────────────────────────────→ 改善工作质量
```

- **L3**：你是谁、AI 该怎么行为、沟通风格、决策原则（axioms）、可复用流程（skills）
- **L1**：每天从工作中提取的观察（红黄绿优先级）
- **L2**：每周把高价值观察晋升为 L3 规则，清理低价值条目

关键原则：**信息密度 > 信息量**。不是记录一切，而是只保留 3 个月后仍有复用价值的认知结晶。

### Axiom vs Skill 的区别

- **Axiom**（公理）：从个人经历蒸馏的决策原则。比如"AI 是放大器不是替代品"——它指导你**怎么想**
- **Skill**（技能）：可复用的操作流程。比如"深度调研 workflow"——它指导你**怎么做**
