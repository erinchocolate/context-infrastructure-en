# Workflow: RST → Markdown 文档转换

## 元数据

- **类型**: Workflow
- **适用场景**: 将 Sphinx RST 格式的文档批量转换为 Markdown，导入到 Marvin 项目的 guidelines 或任何 Markdown-native 上下文
- **创建日期**: 2026-04-13
- **工具路径**: `03 refined/tools/rst_to_markdown.py`
- **工具依赖**: Python 3.8+（纯标准库，无需第三方包）

---

## 脚本功能

`rst_to_markdown.py` 是一个纯 Python 状态机转换器，覆盖以下 RST 构型：

| RST 构型 | Markdown 输出 | 说明 |
|---|---|---|
| 标题（下划线 `= - ~ ^`） | `# ## ###` | 按首次出现顺序动态确定层级 |
| `.. code-block:: lang` | ` ```lang ``` ` | 保留语言标注 |
| `.. note::` / `.. warning::` | `> **Note:** ...` blockquote | 支持 note/warning/tip/important/caution |
| `:code:\`text\`` | `` `text` `` | 行内 inline code |
| `:ref:\`label\`` | 纯文本 label | 跨文档引用无法解析，保留文字 |
| `` `text <url>`_ `` | `[text](url)` | 外链转 Markdown 链接 |
| Simple tables（`===`） | GFM pipe table | 多行单元格内容拼接为一行 |
| Grid tables（`+--+`） | GFM pipe table | 合并多行单元格 |
| `.. image:: path` | `![alt](path)` | 提取 `:alt:` 选项 |
| `.. uml::` | ` ```plantuml ``` ` | 保留 UML 体 |
| `.. _label:` 锚点 | 丢弃 | 跨文档锚点无意义 |
| `.. toctree::` / `.. contents::` | 丢弃 | 导航指令对 MD 无意义 |
| `#.` 自动编号列表 | `1. 2. 3.` | 按序展开 |

---

## 使用方法

```bash
cd /opt/processes/mc_platform/context-infrastructure

# 单文件转换
python3 "03 refined/tools/rst_to_markdown.py" input.rst output.md

# 批量转换（将 shell glob 展开后传入）
python3 "03 refined/tools/rst_to_markdown.py" \
  --batch /path/to/docs/*.rst \
  --output-dir "projects/marvin/02 trusted/guidelines"
```

---

## 典型工作流：导入新的 RST 标准文档

### 步骤

1. **确认源文件位置**

   Data Platform 文档源码位于：
   ```
   /opt/processes/documentation/docs/src/standards/
   ```

2. **运行批量转换**

   ```bash
   cd /opt/processes/mc_platform/context-infrastructure
   python3 "03 refined/tools/rst_to_markdown.py" \
     --batch /opt/processes/documentation/docs/src/standards/<name>.rst \
     --output-dir "projects/marvin/02 trusted/guidelines"
   ```

3. **检查输出质量**

   重点看：
   - 标题层级是否正确（h1 对应文档标题，h2 对应主节，h3 对应子节）
   - 代码块是否有语言标注（SQL / Python 应保留）
   - 大型表格的多行单元格是否拼接合理
   - `:ref:` 引用是否退化为可读文字

4. **必要时手动修正**

   以下情况需要手动处理：
   - `.. image::` 的图片路径（相对路径在新位置失效，可替换为绝对路径或注释掉）
   - `.. uml::` 生成的 plantuml 块（如果渲染环境不支持，可删除）
   - 超复杂表格（多列 + 多行 + 内嵌列表）可考虑手动重写为定义列表格式

5. **更新 WORKSPACE.md**（如新增了文档类别）

---

## 已转换的标准文档

存放路径：`projects/guidelines/`

### 2026-04-13 首批

| 文件 | 内容 |
|---|---|
| `tables.md` | Delta Lake 表结构标准（主键、外键、分区、DDL） |
| `sql_standards.md` | SQL 编写规范（标识符、缩进、对齐、ANSI） |
| `transformation.md` | 数据转换作业标准（幂等性、调度、血缘、参数） |
| `spark_standards.md` | PySpark 编码规范 |
| `python_standards.md` | Python 编写规范 |
| `lineage_standards.md` | 血缘框架使用指南（常量定义、事件记录） |
| `databricks_standards.md` | Databricks 标准（计算类型选择、Airflow 算子） |
| `databricks_apps.md` | Databricks Apps 使用规范 |
| `vector_search.md` | Vector Search 标准（端点、索引、代码示例） |

### 2026-04-15 新增

| 文件 | RST 来源 | 内容 |
|---|---|---|
| `design.md` | `standards/design.rst` | 设计标准（Canvas、数据产品设计、模板、影响评估） |
| `data_quality.md` | `standards/data_quality.rst` | 数据质量框架（维度、检查语法、transform 集成） |
| `local_dab_development.md` | `user_guides/development_process/local_dab_development.rst` | 本地 DAB 开发与测试流程 |

---

## 注意事项

- **图片路径**：转换后的 `![](./assets/xxx.svg)` 路径相对于原始 RST 文件，新位置下可能失效。如需展示，手动修正路径或移除图片行。
- **`:ref:` 跨文档链接**：所有 `:ref:\`...\`` 都退化为纯文字。如果目标文档也已转换，可手动替换为相对 MD 链接。
- **多行表格单元格**：RST simple table 中多行内容拼接为一行，保留了信息但格式有损。如原文有项目列表在单元格内（如 PROCESS_TYPE 的枚举值），它们会被展平为空格分隔的文字。
- **Python 环境**：脚本使用纯标准库，任意 Python 3.8+ 环境直接运行，无需激活 venv 或安装依赖。
