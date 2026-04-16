# Skill: PR Code Review 工作流

## 元数据

- **类型**: Workflow
- **适用场景**: 对 `data_platform` 仓库的 PR/branch 进行 AI 辅助代码审查
- **输出位置**: `context-infrastructure/01 raw/YYYYMMDD_pr_review_<branch>.md`
- **依赖脚本**: `context-infrastructure/03 refined/tools/pr_review.sh`
- **依赖 Skill**: `workflow_parallel_subagents.md`
- **创建日期**: 2026-04-14
- **最后更新**: 2026-04-14

---

## 触发词

当用户说以下任意内容时，激活此 skill：

- "帮我 review 这个 PR"
- "review 一下 `<branch名>` 这个 branch"
- "我同事做了 XXX 改动，帮我看看"
- "code review"、"PR review"

---

## 核心原则

1. **先识别，再询问**：先自动分析代码改动，再询问用户是否有项目文档可补充参考，而不是一开始就让用户提供所有信息
2. **Guidelines 驱动**：所有 review 意见必须有 guidelines 出处，不能凭空提建议
3. **分级严重性**：问题按 Critical / Major / Minor 分级，帮用户快速判断优先级
4. **可操作，不说教**：每条问题必须给出具体修改建议，而不仅仅指出问题

---

## 工作流程

### Phase 1：拉取 Diff

**向用户确认 branch 名后，运行：**

```bash
bash "/opt/processes/mc_platform/context-infrastructure/03 refined/tools/pr_review.sh" \
    --branch <branch_name> \
    [--base master] \
    [--repo /opt/processes/data_platform]
```

从脚本输出中提取：
- Changed files 列表及类型
- Commit 摘要（了解改动意图）
- Full diff（供后续分析）

如果脚本报错（branch 不存在），提示用户检查 branch 名，并列出脚本返回的候选 branch。

---

### Phase 2：自动匹配 Guidelines

根据 changed files 的类型和文件路径，**自动**决定需要参考哪些 guidelines。

**文件类型 → Guidelines 映射：**

| 条件 | 参考文件 |
|------|---------|
| 包含 `.py` 文件 | `projects/guidelines/python_standards.md` |
| 包含 `.sql` 文件 | `projects/guidelines/sql_standards.md` |
| 包含 Databricks bundle/DAB 配置（`.yml`）或 notebooks | `projects/guidelines/databricks_standards.md` |
| 改动涉及 Delta 表、schema、`CREATE TABLE`、`LOCATION` | `projects/guidelines/tables.md` |
| 改动涉及 transformation pipeline、ETL 流程 | `projects/guidelines/transformation.md` |
| 改动涉及 lineage 框架调用 | `projects/guidelines/lineage_standards.md` |
| 改动涉及 vector search、embedding、chunk | `projects/guidelines/vector_search.md` |
| 改动涉及 Databricks Apps | `projects/guidelines/databricks_apps.md` |
| 改动涉及 Spark 代码（`spark.`, `DataFrame`, `pyspark`) | `projects/guidelines/spark_standards.md` |

**所有 guidelines 文件路径前缀：**
`/opt/processes/mc_platform/context-infrastructure/projects/guidelines/`

列出匹配到的 guidelines，读取其内容（留存在 context 中备用）。

---

### Phase 3：询问项目文档

向用户展示代码改动摘要（1-2 句话描述改动主题），然后询问：

> 以上改动涉及 **[改动主题]**。
>
> 如果在 `context-infrastructure/projects/` 下有相关的 requirement、plan 或 design 文档，请提供路径；如果没有，直接跳过这一步。

若用户提供了路径（如 `projects/my_project/01 raw/chunking_design.md`），读取这些文档，在 Phase 4 中增加一个维度的分析。

---

### Phase 4：并行 Review（参考 `workflow_parallel_subagents.md`）

**评估是否值得并行**：
- 如果改动很小（< 50 行 / 单个简单文件），直接串行分析，不需要并行
- 如果改动较大（多文件、多模块），启动并行 sub-agents

**并行分割（代码任务，overlap ≤ 20%）：**

**Sub-agent A — 代码质量与准确性**
分析内容：
- 逻辑正确性（算法、边界情况、数据类型处理）
- 错误处理：是否处理了异常情况？
- 性能：是否有明显的低效操作（如在循环中执行全表扫描）？
- 可读性：命名、函数拆分、注释
- 安全性：是否有注入、敏感数据暴露等问题（OWASP Top 10）
- 测试覆盖：是否有单元测试，是否覆盖核心路径

**Sub-agent B — Guidelines 合规审查**
分析内容：
- 对照匹配到的 guidelines 逐条核查
- 每条 Guideline 的合规状态：✅ 合规 / ⚠️ 部分合规 / ❌ 违规
- 对 ⚠️ 和 ❌ 条目给出具体改动建议

**Sub-agent C（仅当用户提供了项目文档时）— 需求符合度**
分析内容：
- 代码实现是否符合 requirement/design 文档的描述？
- 有哪些需求点未被覆盖到？
- 有哪些实现与设计文档有出入？

---

### Phase 5：生成 Review 报告

将 Phase 4 的结果整合，生成最终 Markdown 报告并保存。

**报告文件路径：**
```
/opt/processes/mc_platform/context-infrastructure/01 raw/<YYYYMMDD>_pr_review_<branch_safe_name>.md
```
（`branch_safe_name` = 将 `/` 替换为 `_`，例如 `ann/cdringest` → `ann_cdringest`）

---

## 报告模板

```markdown
# PR Review: `<branch_name>`

| 字段 | 内容 |
|------|------|
| Branch | `<branch_name>` |
| Base | `master` |
| Review 日期 | YYYY-MM-DD |
| Reviewer | AI (GitHub Copilot) |
| 参考 Guidelines | python_standards, tables（根据实际匹配列出）|
| 项目文档 | `projects/xxx/01 raw/xxx.md`（如有）/ 无 |

---

## 改动摘要

<!-- 用 2-4 句话描述这个 PR 做了什么，改动规模，涉及哪些模块 -->

## Changed Files

| 状态 | 文件 |
|------|------|
| M | `path/to/file.py` |
| A | `path/to/new_file.py` |

---

## 代码质量

### 🔴 Critical（必须修复）

<!-- 影响正确性、安全性、数据完整性的问题 -->

- **[文件名:行号]** 问题描述
  - **建议**: 具体修改方式

### 🟡 Major（建议修复）

<!-- 性能问题、不符合 guidelines 的设计决策 -->

- **[文件名:行号]** 问题描述
  - **建议**: 具体修改方式

### 🟢 Minor（可选优化）

<!-- 可读性、命名、注释等 -->

- **[文件名:行号]** 问题描述
  - **建议**: 具体修改方式

---

## Guidelines 合规检查

### `python_standards.md`

| # | Guideline | 状态 | 说明 |
|---|-----------|------|------|
| 1 | PEP8 代码格式 | ✅ | - |
| 2 | Google docstring 格式 | ❌ | `chunk()` 函数缺少 docstring |

<!-- 按实际匹配到的 guidelines 展开，每个文件一节 -->

---

## 需求符合度

<!-- 仅当 Phase 3 用户提供了项目文档时才包含此节 -->

| 需求点 | 状态 | 说明 |
|--------|------|------|
| 支持按段落切分 | ✅ | 已实现 |
| 支持重叠窗口（overlap） | ⚠️ | 逻辑存在，但 overlap 大小未作边界检查 |
| 最大 chunk size 可配置 | ❌ | 硬编码为 512，未从 config 读取 |

---

## 总体建议

<!-- 3-5 条高层次建议，帮助作者快速了解最重要的改进方向 -->

1. ...
2. ...

---

## 结论

<!-- 一句话总结：Approve / Approve with minor comments / Request changes -->

> **建议**: Request changes — 需要先解决 X 个 Critical 问题后再合并
```

---

## 使用示例

**用户**：帮我 review 一下 ann/cdringest 这个 branch

**Agent 动作**：
1. 运行 `pr_review.sh --branch ann/cdringest`
2. 读取输出，发现改动包含 `.py` 和 `.sql` 文件
3. 自动加载 `python_standards.md`、`sql_standards.md`
4. 向用户展示：「这个 PR 涉及 CDR ingest 流程改动，包含 X 个 Python 文件和 Y 个 SQL 文件。是否有相关的 requirement 或 design 文档？」
5. 用户回复「有，在 `projects/cdr_ingest/01 raw/design.md`」
6. 读取该文档，启动 3 个并行 sub-agent
7. 合并结果，生成报告，保存到 `01 raw/20260414_pr_review_ann_cdringest.md`
