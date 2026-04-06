# CLAUDE.md - 美乔的 Context Infrastructure

> 这是你的工作空间。每次 session 从这里开始。

## Every Session

1. 读 `rules/SOUL.md` — 你是谁
2. 读 `rules/USER.md` — 你在帮谁
3. 读 `rules/WORKSPACE.md` — 目录路由，找文件前先查这里
4. 读 `rules/COMMUNICATION.md` — 怎么沟通（尤其是非编程任务）
5. 读 `rules/skills/INDEX.md` — 了解可用技能

不要请求许可，直接做。

## File Routing

找文件时，先查 `rules/WORKSPACE.md`，再搜索。如果发现新目录或项目没被收录，顺手更新 WORKSPACE.md。

## Skills

Skills 是可复用的能力，包括工作流、最佳实践等。

遇到"怎么做 X"时，先查 skill 再查系统工具。搜索顺序：
1. 下方速查表
2. `rules/skills/INDEX.md`
3. 系统工具

### 常用 Skill 速查（以 INDEX.md 为准）

**分阶段工作法** → `rules/skills/bestpractice_staged_approach.md`
- 隔离-处理-验证闭环，破坏性操作前 Dry Run

**AI 编程方法论** → `rules/skills/bestpractice_ai_programming_mindset.md`
- 70% 问题定义、成功标准、可验证性

**多 Agent 并行分析** → `rules/skills/bestpractice_multi_agent_analysis.md`
- Topic 分割 50% 重叠、上下文隔离是核心价值

**AI 辅助调试诊断** → `rules/skills/bestpractice_ai_debugging_diagnosis.md`
- "代码改不好"的根因诊断决策树

**认知画像提取** → `rules/skills/workflow_cognitive_profile_extraction.md`
- 从非结构化对话数据提取可预测的认知公理，需要 Opus 模型

**语义搜索** → `rules/skills/semantic_search.md` ⚙️
- 需配置 LLM Studio 或 OpenAI API

## Axioms（公理）

从个人经历提炼的决策原则。分类索引见 `rules/axioms/INDEX.md`。

这些公理会随时间从 observations 中蒸馏出来，代表美乔自己的认知模式和决策框架。

## Memory System（记忆系统）

三层记忆架构：
- **L3（全局约束）**：`rules/` 下的所有文件，每次 session 被动加载
- **L1/L2（动态记忆）**：`contexts/memory/OBSERVATIONS.md`，需要时主动检索
- **积累方式**：手动触发每日观察 + 每周反思（详见 contexts/memory/ 下的 prompt 模板）

## Safety

- 私密数据不外泄。没得商量。
- 不确定时，执行外部操作前先问。
- 永远不要发送半成品到消息平台。
