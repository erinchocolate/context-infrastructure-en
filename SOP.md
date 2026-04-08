# 每日工作 SOP

> 这份文档是日常工作的操作手册。把它当作"每天需要做什么"的清单，不是理论文档。
>
> 背后的设计哲学：**Context Rot 是 AI 工作流的头号敌人。**
> AI 的上下文窗口有七秒记忆——每次开新会话，之前的理解归零。
> 解法是把每天的工作产出持续写进文件，让知识慢慢沉淀成 axiom 和 skill，再在下一次会话中自动生效。
> 这个飞轮一旦转起来，今天写的东西会让三个月后的工作更精准。

---

## 一、每日流程

### ☀️ 早晨：开始工作前（5 分钟）

1. 打开 Claude Code，给 AI 一句话说清楚今天要做什么：

   > "今天的任务是 [具体目标]。成功标准是 [可验证的结果]。相关文件是 [路径]。"

   **为什么**：AI 编程 70% 的问题出在上下文和成功标准不清楚。这一句话是最高 ROI 的投入。

2. 如果今天开始一个新项目，先更新或创建 `projects/<name>/README.md`

---

### 🔧 工作中：随手维护 Context

**把你本来要告诉同事的话，告诉文件。**

#### 维护项目 README

`projects/<name>/README.md` 是 AI 的项目入口。遇到以下情况时顺手更新：

- 做了重要架构决策
- 完成了一个阶段/里程碑
- 发现了重要约束或坑
- 引入了新工具/依赖
- 当前工作重点改变了

一两句话即可，不需要完美。

#### 新文档放对地方

| 内容 | 存放路径 |
|---|---|
| 会议记录、决策文档 | `contexts/daily_records/YYYYMMDD_<name>.md` |
| 技术调研、竞品分析 | `contexts/survey_sessions/YYYYMMDD_<name>.md` |
| 架构复盘、方法论思考 | `contexts/thought_review/<name>.md` |
| 代码实验、一次性脚本 | `adhoc_jobs/<project>/` |

新目录/项目记得更新 `rules/WORKSPACE.md`。

---

### 🌆 结束工作：每日观察（5 分钟）

**这是整个系统最重要的一步。**

#### 方式 A：手动（推荐，适合公司环境）

在 Claude Code 里粘贴（模板也在 `contexts/memory/PROMPTS.md`）：

```
回顾今天我们的工作。用红黄绿系统总结关键观察，追加到 contexts/memory/OBSERVATIONS.md：

- 🔴 红色：跨项目的方法论或约束洞察（3 个月后仍有复用价值的认知结晶）
- 🟡 黄色：活跃项目的关键决策、进展、遇到的问题
- 🟢 绿色：常规任务完成记录

过滤标准：
- 只记录有认知价值的内容，不机械记录每个操作
- 如果今天没有值得记录的观察，就不写
- 一条观察不超过 2-3 句话
```

#### 方式 B：自动脚本（需要 OpenCode server 运行）

```bash
cd /opt/processes/mc_platform/context-infrastructure
.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py
# 运行时间约 5-15 分钟，等待 "Task complete" 后检查 OBSERVATIONS.md
```

**红黄绿标准**：
- 🔴 红：3 个月后仍有复用价值的跨项目模式。每天能有一条就很好，没有就不写
- 🟡 黄：项目决策和进展，未来几周需要参考
- 🟢 绿：执行记录，1-2 周后会被 Reflector 清理

**写出来的样子**：

```
## 2026-04-08

🔴 调试 OpenCode API 空响应时，优先查 server 日志（journalctl --user -u opencode）
   而非猜测——日志直接暴露了 agent 名称已改版的问题，节省了大量排查时间。

🟡 [context-infrastructure] AI Heartbeat 安装完成，手动触发需在
   context-infrastructure 目录下运行，自动脚本依赖 OpenCode server 在 4096 端口运行。

🟢 完成 observer.py / reflector.py 路径配置，systemd service 和 crontab 已设置。
```

---

## 二、每周流程

### 📅 周末：每周反思（15 分钟）

积累 3 天以上观察后触发。

#### 方式 A：手动

```
读 contexts/memory/OBSERVATIONS.md，分析本周的观察记录：

1. 识别重复出现的模式（尤其是红色和高优先黄色条目）
2. 检查是否有条目满足晋升条件：
   - 跨项目通用（不只适用于某个特定场景）
   - 多次验证（出现过 2 次以上）
   - 有明确应用场景（知道什么时候该用）
3. 满足条件的，起草为 axiom 或 skill 候选（放到对应目录）
4. 清理已过期的绿色条目
5. 合并重复的黄色条目
6. 将反思结果追加到 OBSERVATIONS.md 的"周反思"区域
```

#### 方式 B：自动脚本

```bash
cd /opt/processes/mc_platform/context-infrastructure
.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/reflector.py
```

**晋升标准**——同时满足以下三点才晋升：
1. 跨项目通用（不只适用于某个特定场景）
2. 多次验证（在观察记录里出现过 2 次以上）
3. 有明确应用场景（知道什么时候该用）

**晋升目标文件**：

| 内容类型 | 目标文件 |
|---|---|
| 决策原则、思维框架 | `rules/axioms/<name>.md` + 更新 `INDEX.md` |
| 可复用工作流、操作流程 | `rules/skills/<name>.md` + 更新 `INDEX.md` |
| AI 行为/沟通偏好 | `rules/COMMUNICATION.md` |
| 用户画像更新 | `rules/USER.md` |
| 工作空间路由变更 | `rules/WORKSPACE.md` |

---

## 三、每月流程

### 🗓️ 月度系统健康检查（30 分钟）

```
对整个 context 系统做一次健康检查：

1. 读 rules/axioms/INDEX.md：现有 axiom 还准确吗？需要基于新证据更新吗？
2. 读 rules/skills/INDEX.md：有 skill 该退役或合并吗？
3. 读 contexts/memory/OBSERVATIONS.md：有红色观察积压了好几周没晋升吗？为什么？
4. 读 CLAUDE.md：太长了吗？需要拆分子文件吗？
5. 总结系统健康状况和下一步行动项。
```

---

## 四、关键原则

### Axiom vs Skill

| | Axiom | Skill |
|---|---|---|
| 回答 | 怎么**想** | 怎么**做** |
| 例子 | "AI 是放大器不是替代品" | "深度调研 workflow" |
| 来源 | 只能从自身经历蒸馏，不能复制别人的 | 可移植，需适配 |
| 位置 | `rules/axioms/` | `rules/skills/` |

### 遇到 AI 反复失败怎么办

先诊断三个问题，再换策略：
1. AI 看到足够的上下文了吗？（报错、日志、相关文件）
2. 成功标准说清楚了吗？（"不报错"太模糊，"row count 一致"才具体）
3. 给 AI 验证的方式了吗？

三个都满足了还改不好，才是模型/架构问题。

### 什么时候写 Skill

**每当你需要向 AI 解释同一个流程第二次——写成 skill。**

### 关于数据安全（公司环境）

手动方式（方式 A）内容不离开本机，适合公司环境。
自动脚本（方式 B）会将工作空间内容发送给 OpenCode Zen 的外部服务器，使用前确认符合公司 IT 政策。

### CLAUDE.md 膨胀问题

超过 ~200 行就拆分为子文件引用。Context window 是有限资源，密度比长度重要。

---

## 五、系统文件速查

| 文件 | 作用 |
|---|---|
| `CLAUDE.md` | Session 入口，AI 每次启动必读 |
| `rules/WORKSPACE.md` | 目录路由表，找文件前查这里 |
| `rules/axioms/INDEX.md` | 所有 axiom 的索引 |
| `rules/skills/INDEX.md` | 所有 skill 的索引 |
| `contexts/memory/OBSERVATIONS.md` | 每日观察的积累地 |
| `contexts/memory/PROMPTS.md` | 手动触发观察/反思的 prompt 模板 |
| `periodic_jobs/ai_heartbeat/docs/SETUP_LOG.md` | AI Heartbeat 安装配置记录 |
