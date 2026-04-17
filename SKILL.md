---
name: task-centric-memory
description: Universal Task-Centric Memory System - Dynamically categorizes, indexes, and compresses conversation memory based on task status.
---

# Task-Centric Memory System (任务核心记忆)

## 🌍 Overview
A universal memory management skill that transforms the AI's linear conversation history into a structured, task-oriented index.
Instead of a chaotic timeline, this skill organizes memory into **Task Buckets** grouped by **Business Domains** (automatically detected).

## 🧠 Core Logic (For Agent)

### 1. Auto-Classification (Zero-Config)
Do NOT assume any fixed categories. Analyze the user's input to detect the domain (e.g., "Coding", "Finance", "Marketing", "Personal").
- If the domain exists in the index -> Add task there.
- If the domain is new -> **Automatically create** a new domain bucket in the JSON index.

### 2. Task Lifecycle & Compression
- **🔴 In-Progress**: Keep raw details, errors, and intermediate steps in the summary. DO NOT compress.
- **🟢 Completed**: Compress into a high-density summary (Result + Key Data + File Paths). Purge noise.

### 3. Tool Usage
Use `execute_code` to run `references/indexer.py`.
- `add`: Add a new task or update an existing one.
- `search`: Find tasks by keywords.

## 📂 Index Structure (JSON)
Stored at `~/.hermes/task-index.json` by default.

```json
{
  "coding_project": {
    "display_name": "Coding Project",
    "tasks": [
      { "id": "task_...", "name": "...", "status": "In-Progress", "summary": "..." }
    ]
  },
  "finance_analysis": {
    "display_name": "Finance Analysis",
    "tasks": [
      { "id": "task_...", "name": "...", "status": "Completed", "summary": "..." }
    ]
  }
}
```

## ⚠️ Instructions
1. Always load this skill when handling complex, multi-turn requests.
2. When the user asks "What was the status of X?" -> Call `search`.
3. When a task finishes -> Call `update` with status "Completed".
