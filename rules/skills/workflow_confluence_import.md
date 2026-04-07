# Workflow: Confluence 文档导入

## 元数据

- **类型**: Workflow
- **适用场景**: Confluence ↔ Repo 双向文档同步；将 Confluence 页面导出为 Markdown，放入 `projects/<name>/docs/` 作为 AI context
- **创建日期**: 2026-04-07
- **更新日期**: 2026-04-08
- **工具依赖**: `tools/sync_docs_to_confluence.py`（Push）、`tools/pull_from_confluence.py`（Pull）、`tools/convert_confluence_docs.py`（批量初始导入）、`html2text`、`requests`

---

将 Confluence 文档导出为 Markdown 并放入 `projects/<name>/docs/` 的标准操作流程。

---

## 方法一：单页面导出（推荐，少量文档）

**适用**：一次导出 1-5 个页面，格式复杂（有表格、代码块）。

### 步骤

```bash
# 前置：安装 pandoc
sudo apt install pandoc   # Linux
brew install pandoc       # macOS

# 步骤 1：在 Confluence 页面点击 ··· → Export → Word (.docx) 下载
# 步骤 2：用 pandoc 转换
pandoc input.docx -t markdown-raw_html --wrap=none -o output.md

# 步骤 3：人工检查输出，清理多余的格式标记
# 步骤 4：按文档类型放入对应目录
#   PRD/设计文档  → projects/marvin/docs/prd/
#   架构/技术规范 → projects/marvin/docs/architecture/
#   SOP/操作手册  → projects/marvin/docs/sops/
#   调研报告      → projects/marvin/docs/research/
```

**命名规范**：`YYYY-MM-DD_<page-title-snake-case>.md`  
例：`2025-10-01_marvin_system_architecture.md`

---

## 方法二：浏览器复制（最快，纯文字页面）

**适用**：文档以文字为主，格式简单，1-2页。

1. Confluence 页面上 `Ctrl+A` 全选 → `Ctrl+C` 复制
2. 粘贴到编辑器，手动整理为 Markdown
3. 保存到对应 `docs/` 子目录

---

## 方法三：REST API 批量导出（多页面）

**适用**：整个 Confluence Space 下有 10+ 页面需要批量导入。

### 前置条件

- Atlassian Personal Access Token（PAT）
- 确认 Confluence 类型：Cloud（`*.atlassian.net`）还是 Server/Data Center（内部 URL）

### 安装工具

```bash
cd /opt/processes/mc_platform/context-infrastructure
# 激活工作区 venv
source /opt/processes/mc_platform/venv/bin/activate
pip install confluence-markdown-exporter
```

### 导出命令

```bash
# Atlassian Cloud
confluence-markdown-exporter \
  --url https://<your-domain>.atlassian.net \
  --token <your-PAT> \
  --space-key <SPACE_KEY> \
  --output projects/marvin/docs/

# Server/Data Center（内部部署）
confluence-markdown-exporter \
  --url https://<internal-confluence-url> \
  --token <your-PAT> \
  --space-key <SPACE_KEY> \
  --output projects/marvin/docs/
```

> **注意**：批量导出后需要手动将文件按类型分类到 `prd/`、`architecture/`、`sops/`、`research/` 子目录，并更新 `projects/marvin/README.md` 的文档索引表。

---

## 导入后的清理检查清单

- [ ] 文件命名符合 `YYYY-MM-DD_<title>.md` 格式
- [ ] 放置在正确的子目录中
- [ ] 检查图片：Confluence 导出的图片通常是附件路径，需要手动处理（截图重新粘贴或删除）
- [ ] 检查内部链接（Confluence 页面链接不可用，改为相对路径或注释说明）
- [ ] 更新 `projects/marvin/README.md` 的文档索引表
- [ ] 在 `context/status.md` 记录本次导入的时间和范围

---

## 从 Repo 推送回 Confluence（自动脚本）

使用 `tools/sync_docs_to_confluence.py` 将 `projects/marvin/docs/` 下的 Markdown
自动推送到 Confluence Cloud Space，维护以下页面层级：

```
<CONFLUENCE_ROOT_TITLE>
├── Architecture  →  docs/architecture/*.md
├── PRD           →  docs/prd/*.md
├── SOPs          →  docs/sops/*.md
└── Research      →  docs/research/*.md
```

### 首次配置（仅一次）

**1. 获取 Atlassian API Token**
- 登录 https://id.atlassian.com/manage-profile/security/api-tokens
- 点击 "Create API token"，命名为 "context-infrastructure-sync"

**2. 配置 .env**

```bash
cp .env.example .env
# 填写以下变量：
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_EMAIL=your@email.com
CONFLUENCE_API_TOKEN=<从上一步复制的 token>
CONFLUENCE_SPACE_KEY=<目标 Space 的 Key，在 Space Settings 中查看>
CONFLUENCE_ROOT_TITLE=Project Marvin - AI Context  # 可选，有默认值
```

**3. 安装依赖**

```bash
source /opt/processes/mc_platform/venv/bin/activate
pip install md2cf mistune requests html2text
```

### 日常使用

```bash
# 干跑：预览哪些页面会被创建/更新，不实际修改 Confluence
python tools/sync_docs_to_confluence.py --dry-run

# 正式推送
python tools/sync_docs_to_confluence.py
```

**幂等性**：脚本维护 `tools/.confluence_page_map.json`（gitignored）记录
`本地路径 → Confluence page_id` 的映射。首次推送创建页面，后续运行按 page_id
更新，不会重复创建。

### 注意事项

- 页面标题由文件名自动生成（下划线→空格，Title Case），推送后不要在 Confluence
  手动修改标题，否则下次推送会找不到原页面（ID 仍在 page map 中，更新不受影响）
- `context/meetings/`、`context/decisions/` 等动态记录不在推送范围内，仍需手动同步
- 如果某次推送失败（网络超时等），重新运行即可，已成功的页面不会重复处理

---

## 从 Confluence 拉回 Repo（Pull）

使用 `tools/pull_from_confluence.py` 将 Confluence 上被修改过的页面同步回本地 Markdown 文件。

**前提**：必须先运行过 Push，本地存在 `tools/.confluence_page_map.json`。

### 工作原理

- 读取 `tools/.confluence_page_map.json`（本地路径 → Confluence page_id）
- 调用 `GET /wiki/rest/api/content/{id}?expand=body.export_view,version`
- 对比版本号缓存 `tools/.confluence_pull_versions.json`，版本相同则跳过
- HTML → Markdown（`html2text`），写回本地文件，添加 `> Last updated:` 头
- 更新版本缓存（gitignored）

### 日常使用

```bash
# 干跑：预览哪些文件会被更新
python tools/pull_from_confluence.py --dry-run

# 正式拉取（覆盖本地文件）
python tools/pull_from_confluence.py

# 强制拉取（忽略版本缓存，全量覆盖）
python tools/pull_from_confluence.py --force
```

### 注意事项

- **Confluence 优先**：有冲突时 Confluence 内容覆盖本地，无合并逻辑
- **只处理 page_map 中已有的页面**：Confluence 上新建的页面需先 Push 建立映射
- **幂等**：重复运行只更新有版本变化的页面

---

## Diagram 处理策略

**已定策略（2026-04-08）**：Diagram 在 Confluence 上手动维护（图片或宏），不参与自动同步。

| 内容类型 | Push（repo → Confluence） | Pull（Confluence → repo） |
|---|---|---|
| 文字内容 | ✅ 自动同步 | ✅ 自动同步 |
| Mermaid 代码块 | 作为普通代码块上传 | 被 Confluence 版本覆盖（消失）|
| Confluence 图片/宏 | 不处理 | `html2text` 忽略图片 |

Repo 中的 Mermaid 图表在首次 Pull 后消失；之后 diagram 只在 Confluence 里维护，无需特殊合并逻辑。

---

## 推荐的双向同步节奏

1. Repo 里修改文档 → `python tools/sync_docs_to_confluence.py` Push 到 Confluence
2. 有人在 Confluence 上改了文字 → `python tools/pull_from_confluence.py` 拉回 repo
3. 可配合 cron 每天自动 Pull：
   ```
   0 8 * * * cd /opt/processes/mc_platform/context-infrastructure && /opt/processes/mc_platform/venv/bin/python tools/pull_from_confluence.py >> /var/log/confluence_pull.log 2>&1
   ```

---

*此 Skill 存放于 `rules/skills/workflow_confluence_import.md`。*
