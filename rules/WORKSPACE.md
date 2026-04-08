# WORKSPACE.md - 目录路由速查

目标：让 AI 每轮 session 都能快速知道"去哪里找/放什么"。**找任何文件前先查这里。**

## 路由规则

### 项目与代码
- **持续进行的项目上下文**（文档、会议记录、决策、状态）：`projects/<project>/`
- 写代码 / 跑脚本 / 一次性项目：`adhoc_jobs/<project>/`
- 工具脚本（邮件、语义搜索、分享报告等）：`tools/`
- 定时任务：`periodic_jobs/

### 知识与记录
- 通用调研报告：`contexts/survey_sessions/`
- 思考 / 复盘 / 方法论：`contexts/thought_review/`
- 每日日志：`contexts/daily_records/`

### 系统与规则
- 可复用技术方案 / Skill：`rules/skills/`
- 核心公理（Axioms）：`rules/axioms/`
- 记忆系统：`contexts/memory/` + `periodic_jobs/ai_heartbeat/`
- GitHub Copilot session 入口：`.github/copilot-instructions.md`（等价于 CLAUDE.md）

## 命名规则
- 目录和文件名：小写 + 下划线 (snake_case)
- 临时项目：`tmp_<name>/`
- **带日期的文档统一格式：`YYYYMMDD_<name>.md`**
  - 例：`20260408_auto_trigger_chunking_on_table_change.md`
  - 适用范围：meetings、decisions、adhoc_jobs 下所有带时间戳的文档
  - 日期取文档创建当天，不用分隔符（不用 `2026-04-08` 或 `2026_04_08`）

## Python 环境
- 根目录 `.venv/` 为工作区级环境，用 `uv pip install` 管理依赖
- 需要隔离时在 `adhoc_jobs/<project>/.venv/` 建独立环境

## 工具索引

| 文件 | 用途 |
|---|---|
| `tools/convert_confluence_docs.py` | Confluence .doc → Markdown 批量转换脚本（配合 `rules/skills/workflow_confluence_import.md`） |
| `tools/opencode_job.py` | 调用 OpenCode agent 的工具脚本 |
| `tools/semantic_search/` | 语义搜索工具（见 `rules/skills/semantic_search.md`） |

## 快速查询

<!-- 随着项目增长，在这里添加活跃项目的快捷路由 -->
<!-- 格式：- `project-name` -> `projects/project_name/` (说明) -->
- `marvin` → `projects/marvin/` （Contact Energy 内部 RAG 信息检索工具）
