# 🧠 Task-Centric Memory for Hermes Agent

> **Transform your AI agent's memory from a chaotic timeline into an organized, task-oriented project manager.**

![Hermes](https://img.shields.io/badge/Hermes-Agent-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Why This Skill?

By default, AI agents store memory linearly (chronologically). As conversations grow, the agent becomes:
1.  **Slow:** Searching through thousands of lines of history.
2.  **Confused:** Mixing up different projects (e.g., confusing "Coding" tasks with "Stock Analysis").
3.  **Expensive:** Loading raw history consumes more context tokens.

**Task-Centric Memory** solves this by:
*   ✅ **Organizing by Project:** Automatically creating "buckets" for different topics.
*   ✅ **Smart Compression:** keeping details for active tasks, summarizing completed ones.
*   ✅ **Instant Retrieval:** finding answers in milliseconds using a structured JSON index.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **🔍 Auto-Categorization** | No setup required. The agent detects your topic (Coding, Finance, Writing) and creates folders dynamically. |
| **📂 Hierarchical Structure** | Memory is organized: `Category -> Task -> Status`. |
| **📉 Tiered Compression** | **Active Tasks:** Full details preserved. **Completed Tasks:** Compressed into high-density summaries to save context. |
| **⚡ Sub-second Search** | Queries the lightweight JSON index instead of scanning full conversation history. |
| **🛠️ Zero-Config** | Just install. The background script (`indexer.py`) handles everything. |

---

## 📦 Installation

1.  **Download** this repository or copy the skill files.
2.  **Place** the `task-centric-memory` folder into your Hermes skills directory:
    *   macOS/Linux: `~/.hermes/skills/`
    *   Windows: `%USERPROFILE%\.hermes\skills\`
3.  **Restart** your Hermes agent.

---

## 🧠 How It Works (For Agents)

When loaded, this skill instructs the agent to:
1.  **Intercept** the start of a new topic.
2.  **Run** `indexer.py --action add` to log the task in `~/.hermes/task-index.json`.
3.  **Update** status to `Completed` when the task is finished, triggering compression.
4.  **Search** the index first when asked questions, bypassing slow history scanning.

### Example Index Structure
```json
{
  "categories": {
    "project_x": {
      "display_name": "Project X Development",
      "tasks": [
        {
          "id": "task_FixBug_260417",
          "name": "Fix API Timeout Bug",
          "status": "In-Progress",
          "summary": "Investigating connection pooling issue..."
        }
      ]
    }
  }
}
```

---

## 📜 License
MIT License — Free to use and modify.

---
*Created by 阿许 (Ah Xu) & 九张机 (Jiu Zhang Ji)*
