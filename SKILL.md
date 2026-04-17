---
name: task-centric-memory
description: Universal Task-Centric Memory System - Dynamically categorizes, indexes, and compresses conversation memory based on task status.
---

# Task-Centric Memory System (强制工具调用协议)

## ⚠️ 强制工作流 (MANDATORY WORKFLOW)
每当用户**开启新话题**、**切换任务领域**或**提出复杂需求**时，你**必须**调用 `execute_code` 运行 `references/indexer.py`。

### 1. 新任务自动登记 (ON NEW TOPIC)
当检测到用户开始一个新任务时，**必须**执行 `add`：
```bash
python3 ~/.hermes/skills/task-centric-memory/references/indexer.py \
  --action add \
  --category "<英文小写领域名>" \
  --name "<简短任务名>" \
  --summary "<当前任务目标>" \
  --keywords "<关键词1>,<关键词2>"
```
> ⚠️ **如果路径不存在**：请运行 `find ~/.hermes -name "indexer.py"` 定位脚本路径。
> 💡 **执行后**：必须将返回的 JSON 结果简要反馈给用户（例如："✅ 已将任务 [xxx] 记录到记忆索引，ID 为 [task_id]，后续可随时查询。"）。
**示例**：用户说"帮我修一下失忆脚本"。
* `--category`: `devops`
* `--name`: `修复防失忆脚本`
* `--summary`: `修改 recover_session.py，使用 ended_at IS NOT NULL 逻辑`

### 2. 任务完成压缩 (ON COMPLETION)
任务结束时，**必须**执行 `update`：
```bash
python3 ~/.hermes/skills/task-centric-memory/references/indexer.py \
  --action update \
  --id <任务ID> \
  --status Completed \
  --summary "<精简后的最终结论或结果>"
```
> 💡 **ID 来源**：ID 来自之前 `add` 命令的返回值，或执行 `search` 后提取结果中的 `id` 字段。
> ⚠️ **重名处理**：若存在重名任务（可能在不同分类下），脚本会更新找到的第一个。**强烈建议优先使用 ID 更新**以确保精准。

### 3. 优先检索索引 (ON QUERY)
当用户问及历史任务细节时（如"我们上次怎么修那个 bug 的？"），**第一步必须是搜索引**：
```bash
python3 ~/.hermes/skills/task-centric-memory/references/indexer.py \
  --action search \
  --query "<关键词>"
```
**禁止**直接搜索原始聊天记录文件。只有索引无结果时，才回退到 `session_search`。

## 📁 脚本路径
* `~/.hermes/skills/task-centric-memory/references/indexer.py`
* `~/.hermes/task-index.json`

> 💻 **跨平台说明**：脚本使用 Python 标准路径库，在 **Windows** 下 `~` 会被自动解析为用户目录，命令格式可直接运行。
## ⚠️ Instructions
1. Always load this skill when handling complex, multi-turn requests.
2. When the user asks "What was the status of X?" -> Call `search`.
3. When a task finishes -> Call `update` with status "Completed".
