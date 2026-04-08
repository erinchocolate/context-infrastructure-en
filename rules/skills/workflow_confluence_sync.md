# Workflow: Confluence 文档双向同步

## 元数据

- **类型**: Workflow
- **适用场景**: Confluence ↔ Repo 文档双向同步；将 Confluence 导出文件转换为 Markdown；将本地 Markdown 推送到 Confluence
- **创建日期**: 2026-04-09
- **更新日期**: 2026-04-09
- **工具路径**: `tools/confluence/`
- **工具依赖**: `html2text`, `requests`, `python-dotenv`, `mistune`, `md2cf`

---

## 工具一览

所有脚本位于 `context-infrastructure/tools/confluence/`，使用工作区 venv 运行：

```bash
source /opt/processes/mc_platform/venv/bin/activate
cd /opt/processes/mc_platform/context-infrastructure
```

| 脚本 | 用途 |
|------|------|
| `sync_docs_to_confluence.py` | Push：将 `projects/marvin/docs/` 下的 Markdown 推送到 Confluence（新建或更新） |
| `pull_from_confluence.py` | Pull：从 Confluence 拉取页面到本地，按版本号跳过未变更页面 |
| `convert_confluence_docs.py` | Convert：将 Confluence 导出的 `.doc`/`.docx` 文件批量转换为 Markdown，并按类型分类 |

状态文件（存放于 `tools/confluence/`，已 gitignore）：
- `.confluence_page_map.json` — 本地路径 → Confluence page ID 的映射（由 push 脚本写入）
- `.confluence_pull_versions.json` — 每个页面上次 pull 时的版本号（由 pull 脚本写入）

---

## 环境配置

在 `context-infrastructure/.env` 中设置（参考 `.env.example`）：

```bash
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_EMAIL=your@email.com
CONFLUENCE_API_TOKEN=<token from id.atlassian.com>
CONFLUENCE_SPACE_KEY=MARVIN
CONFLUENCE_ROOT_TITLE=Project Marvin - AI Context  # 可选，默认值即此
```

---

## 使用方法

### 1. Push：本地 Markdown → Confluence

将 `projects/marvin/docs/` 下所有 Markdown 文件推送到 Confluence。首次运行自动创建页面，后续运行更新已有页面。

```bash
# Dry run（只打印计划，不实际推送）
python tools/confluence/sync_docs_to_confluence.py --dry-run

# 实际推送
python tools/confluence/sync_docs_to_confluence.py
```

**目录结构映射**（在 Confluence 中自动创建层级）：
```
Root page (CONFLUENCE_ROOT_TITLE)
├── Architecture  ← docs/architecture/*.md
├── Design        ← docs/design/*.md
├── SOPs          ← docs/sops/*.md
└── Research      ← docs/research/*.md
```

Push 完成后 `.confluence_page_map.json` 会自动更新，保存 page ID 映射供后续增量更新使用。

---

### 2. Pull：Confluence → 本地 Markdown

从 Confluence 拉取页面内容更新本地文件。通过版本号缓存实现幂等（未变更的页面自动跳过）。

```bash
# Dry run
python tools/confluence/pull_from_confluence.py --dry-run

# 实际拉取（只更新 Confluence 版本比本地新的页面）
python tools/confluence/pull_from_confluence.py

# 强制覆盖所有页面
python tools/confluence/pull_from_confluence.py --force
```

**前置条件**：需要先执行过至少一次 push，否则 `.confluence_page_map.json` 不存在，pull 会报错。

---

### 3. Convert：批量转换 Confluence 导出文件

将从 Confluence 页面导出的 `.doc`（MIME/HTML 格式）批量转换为 Markdown，并按内容类型自动分类。

```bash
# 默认：转换 projects/marvin/docs/*.doc，输出到同目录的子文件夹
python tools/confluence/convert_confluence_docs.py

# 指定输入/输出目录
python tools/confluence/convert_confluence_docs.py \
  --input-dir projects/marvin/context \
  --output-dir projects/marvin/docs
```

**自动分类规则**（基于文件名关键词）：
- `architecture/`：system overview、architecture、chatbot、loading、rag、vector、codebase
- `prd/`：prerequisites、requirements
- `sops/`：how-to、common changes、setup、configuration、optimisation
- `research/`：evaluation、mlflow、dab，以及默认 fallback

**导出文件获取方式**：Confluence 页面 → `···` → `Export` → `Word (.doc)`

---

## 典型工作流

### 场景 A：初次同步（已有 Confluence 文档 → Repo）

```bash
# 步骤 1：从 Confluence 导出 .doc 文件到 projects/marvin/docs/
# 步骤 2：批量转换
python tools/confluence/convert_confluence_docs.py

# 步骤 3：检查转换结果，手动归类未识别的文件

# 步骤 4：Push 回 Confluence，建立 page map
python tools/confluence/sync_docs_to_confluence.py --dry-run
python tools/confluence/sync_docs_to_confluence.py
```

### 场景 B：日常维护（Repo 为主源）

```bash
# 在 repo 中编辑 Markdown → 推送到 Confluence
python tools/confluence/sync_docs_to_confluence.py
```

### 场景 C：日常维护（Confluence 为主源）

```bash
# 从 Confluence 拉取最新内容
python tools/confluence/pull_from_confluence.py
```

---

## 注意事项

- **图表不参与自动同步**：Confluence drawio/diagram 图表需手动维护，脚本不处理图片附件
- **内部链接**：Confluence 的跨页面链接在本地 Markdown 中无效，需手动替换为相对路径
- **文件命名规范**：本地文件建议使用 `YYYY-MM-DD_<title-snake-case>.md` 格式
- **Page map 丢失**：若 `.confluence_page_map.json` 丢失，下次 push 时 Confluence 端会创建重复页面，需手动删除后重建

---

## 依赖安装

```bash
source /opt/processes/mc_platform/venv/bin/activate
pip install html2text requests python-dotenv mistune md2cf
```
