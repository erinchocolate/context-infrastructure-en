# AI Heartbeat 安装配置记录

> 记录日期：2026-04-08  
> 操作人：dataadmin @ CEW-5CG3392CQZ

---

## 一、系统架构概览

```
crontab (每日 08:00)
    └─► observer.py          # Python 触发脚本
            └─► OpenCodeClient (HTTP Basic Auth)
                    └─► opencode serve (localhost:4096)
                            └─► AI Agent (model: opencode/big-pickle)
                                    └─► 扫描工作空间文件变动
                                    └─► 写入 contexts/memory/OBSERVATIONS.md

crontab (每周日 09:00)
    └─► reflector.py
            └─► (同上链路)
                    └─► 读取 OBSERVATIONS.md → 晋升规则到 rules/ → GC 清理
```

---

## 二、完成的配置工作

### 1. 修复代码占位符

以下文件在原始仓库中均使用 `/path/to/your/workspace` 占位符，已全部替换为实际路径：

| 文件 | 修改内容 |
|---|---|
| `src/v0/observer.py` | `KNOWLEDGE_BASE` 路径、PROMPT 中两处根目录引用 |
| `src/v0/reflector.py` | `KNOWLEDGE_BASE` 路径、PROMPT 中 OBSERVATIONS.md 路径 |
| `docs/KNOWLEDGE_BASE.md` | `ROOT_DIR` 从占位符改为 `/opt/processes/mc_platform/context-infrastructure/` |
| `docs/CRONTAB.md` | 示例 crontab 中的所有占位符路径 |

### 2. 替换模型 ID 占位符

`observer.py` 和 `reflector.py` 中 `--model` 参数的 `default` 和 `choices` 原为 `<your-model-id>`，已改为 `opencode/big-pickle`（OpenCode Zen 免费模型）。

### 3. 创建 .env 配置文件

**位置**：`periodic_jobs/ai_heartbeat/.env`（这是 `opencode_client.py` 实际读取的路径）

```env
OPENCODE_BASE_URL=http://localhost:4096
OPENCODE_USERNAME=opencode
OPENCODE_PASSWORD=<已设置>
OPENCODE_MESSAGE_TIMEOUT=3600
```

> **注意**：原始 `.env.example` 中写的是 `OPENCODE_API_URL`，但代码实际读取的是 `OPENCODE_BASE_URL`——存在命名不匹配的 bug。`.env` 已按代码实际变量名创建。

### 4. 创建 Python 虚拟环境

```bash
cd /opt/processes/mc_platform/context-infrastructure
python3 -m venv .venv
.venv/bin/pip install requests python-dotenv
```

> `uv` 未安装，改用标准 `venv` + `pip`。

### 5. 配置 OpenCode Server 自启动（systemd user service）

**文件**：`~/.config/systemd/user/opencode.service`

```ini
[Unit]
Description=OpenCode Server
After=network.target

[Service]
Type=simple
Environment=OPENCODE_SERVER_PASSWORD=<已设置>
ExecStart=/home/dataadmin/.opencode/bin/opencode serve --port 4096 --hostname 127.0.0.1
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

启动命令：
```bash
systemctl --user daemon-reload
systemctl --user enable opencode  # 开机自启
systemctl --user start opencode   # 立即启动
```

### 6. 设置 Crontab

时区：`TZ=Pacific/Auckland`

```cron
# Observer — 每日 08:00
0 8 * * * cd /opt/processes/mc_platform/context-infrastructure && .venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py >> /tmp/observer.log 2>&1

# Reflector — 每周日 09:00
0 9 * * 0 cd /opt/processes/mc_platform/context-infrastructure && .venv/bin/python periodic_jobs/ai_heartbeat/src/v0/reflector.py >> /tmp/reflector.log 2>&1

# Crontab Monitor — 每日 09:00
0 9 * * * cd /opt/processes/mc_platform/context-infrastructure && .venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/crontab_monitor.py >> /tmp/crontab_monitor.log 2>&1
```

---

## 三、OpenCode Server 运行机制

### 启动方式
```bash
# 带密码的 server 模式（Python 脚本通过 HTTP 调用）
OPENCODE_SERVER_PASSWORD=xxx opencode serve --port 4096 --hostname 127.0.0.1

# 注意：直接运行 `opencode`（交互模式）不需要密码，两者互相独立
```

### 身份认证
- Server 模式使用 **HTTP Basic Auth**
- Username：`opencode`（默认）
- Password：由 `OPENCODE_SERVER_PASSWORD` 环境变量控制
- Python 脚本从 `.env` 读取后用 `Authorization: Basic <base64>` 头传递

### 模型账号（OpenCode Zen）
- 在交互模式下运行 `/connect` → 选择 OpenCode Zen → 浏览器授权
- 认证信息存储在 `~/.local/share/opencode/auth.json`
- 当前已绑定的 API Key：`sk-JtJ5E55j...`

### 可用免费模型（OpenCode Zen）
| 模型 ID | 说明 |
|---|---|
| `opencode/big-pickle` | 当前默认，免费期训练数据 |
| `opencode/gpt-5-nano` | 免费，无数据收集 |
| `opencode/qwen3.6-plus-free` | 限时免费 |

---

## 四、Debug 发现的问题

### 问题 1：`.env` 文件路径错误

**现象**：运行 `observer.py` 报 `ValueError: OPENCODE_PASSWORD not found`

**原因**：`.env` 被创建在 `src/v0/.env`，但 `opencode_client.py` 按以下优先级查找：
```python
project_env_path = module_dir.parent.parent / ".env"  # → ai_heartbeat/.env  ✅ 优先
legacy_env_path  = module_dir.parent / ".env"          # → src/.env
```

**修复**：将 `.env` 复制到 `periodic_jobs/ai_heartbeat/.env`

---

### 问题 2：Agent 名称已废弃

**现象**：API 调用返回空响应，`observer.py` 输出 `Server returned 200 with empty response body`，OBSERVATIONS.md 无新内容

**排查**：查看 `journalctl --user -u opencode` 服务日志，发现：
```
Agent not found: "OpenCode-Builder". Available agents: build, explore, general, plan
```

**原因**：原始代码写的是 `agent="OpenCode-Builder"`，但 OpenCode v1.4.0 已将该 agent 重命名。可用名称为：`build`、`explore`、`general`、`plan`

**修复**：修改 `opencode_client.py` 中 `send_message()` 的默认参数：
```python
# Before
def send_message(self, ..., agent="OpenCode-Builder"):
# After
def send_message(self, ..., agent="build"):
```

---

### 问题 3：`.env.example` 变量名与代码不匹配（未修复，记录备用）

`.env.example` 中记录的是 `OPENCODE_API_URL`，但 `opencode_client.py` 实际读取的是 `OPENCODE_BASE_URL`。这是原始仓库的文档 bug，不影响运行（`.env` 已按正确变量名创建）。

---

## 五、当前状态

| 组件 | 状态 |
|---|---|
| OpenCode v1.4.0 | ✅ 已安装 (`~/.opencode/bin/opencode`) |
| OpenCode Zen 账号 | ✅ 已绑定 |
| systemd user service | ✅ 已启用，`active (running)` on port 4096 |
| Python `.venv` + 依赖 | ✅ 已创建 |
| Crontab | ✅ 已设置（Auckland 时区） |
| 端对端测试 | ⏳ 进行中（Agent 正在运行，等待写入 `OBSERVATIONS.md`） |

---

## 六、手动运行命令参考

```bash
# 运行 Observer（今日，保留 session 用于检查）
cd /opt/processes/mc_platform/context-infrastructure
.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py 2026-04-08 --no-delete

# 运行 Observer（指定日期，使用更快的模型）
.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py 2026-04-08 --model opencode/gpt-5-nano

# 运行 Reflector（每周手动触发）
.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/reflector.py

# 检查 OBSERVATIONS.md 输出
cat contexts/memory/OBSERVATIONS.md

# 检查 OpenCode server 状态
systemctl --user status opencode

# 查看 server 日志（用于 debug）
journalctl --user -u opencode -n 50 --no-pager

# 查看 crontab
crontab -l
```
