#!/usr/bin/env python3
"""
Universal Task-Centric Memory Indexer
Dynamically manages memory categories and task states.
"""
import os
import re
import json
import sys
import argparse
from datetime import datetime

# Universal default path
INDEX_PATH = os.path.join(os.path.expanduser("~"), ".hermes", "task-index.json")

def load_index():
    """Loads the index or creates a default empty structure if missing."""
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If corrupted, backup and reset
            backup = INDEX_PATH + ".bak"
            if os.path.exists(INDEX_PATH):
                os.replace(INDEX_PATH, backup)
            return {"categories": {}}
    return {"categories": {}}

def save_index(data):
    """Saves the index with a backup."""
    # Ensure directory exists
    try:
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
        
        backup = INDEX_PATH + ".bak"
        if os.path.exists(INDEX_PATH):
            with open(INDEX_PATH, 'r') as src, open(backup, 'w') as dst:
                dst.write(src.read())
        
        with open(INDEX_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"ERROR: Failed to save index -> {str(e)}", file=sys.stderr)
        sys.exit(1)

def generate_id(name):
    """Generates a unique task ID. Supports Chinese, letters, and digits."""
    # Keep letters, digits, and Chinese characters (\u4e00-\u9fff)
    clean = re.sub(r'[^\w\u4e00-\u9fff]', '', name)[:6]
    if not clean:
        clean = "task"
    date_str = datetime.now().strftime("%y%m%d")
    return f"{clean}_{date_str}"

def add_task(category, name, summary, keywords, data):
    """Adds a task, auto-creating category if needed."""
    cats = data.get("categories", {})
    
    # If category doesn't exist, create it
    if category not in cats:
        cats[category] = {"display_name": category, "tasks": []}
    
    cat_data = cats[category]
    
    # Check for duplicate task names in this category
    for t in cat_data.get("tasks", []):
        if t["name"] == name:
            return {"status": "exists", "id": t["id"], "message": "Task already exists in this category."}
    
    # Create new task
    task_id = generate_id(name)
    new_task = {
        "id": task_id,
        "name": name,
        "status": "In-Progress",
        "summary": summary,
        "keywords": keywords,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    cat_data["tasks"].append(new_task)
    return {"status": "success", "id": task_id, "message": "Task added."}

def update_task(identifier, status, summary, data):
    """Updates a task by ID or Name across ALL categories."""
    cats = data.get("categories", {})
    found = False
    
    for cat_key, cat_val in cats.items():
        for task in cat_val.get("tasks", []):
            if task["id"] == identifier or task["name"] == identifier:
                task["status"] = status
                task["summary"] = summary
                task["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                found = True
                break
        if found: break
    
    if found:
        return {"status": "success", "message": "Task updated."}
    else:
        return {"status": "error", "message": f"Task '{identifier}' not found."}

def search_tasks(query, data):
    """Searches for tasks across all categories."""
    results = []
    query = query.lower()
    cats = data.get("categories", {})
    
    for cat_key, cat_val in cats.items():
        display_name = cat_val.get("display_name", cat_key)
        for task in cat_val.get("tasks", []):
            # Check name, summary, and keywords
            if (query in task["name"].lower() or 
                query in task["summary"].lower() or 
                any(query in k.lower() for k in task.get("keywords", []))):
                results.append({
                    "category": display_name,
                    "task_name": task["name"],
                    "status": task["status"],
                    "summary": task["summary"]
                })
    return {"status": "success", "results": results}

def main():
    parser = argparse.ArgumentParser(description="Task-Centric Memory Indexer")
    parser.add_argument("--action", required=True, choices=["add", "update", "search"])
    parser.add_argument("--category", default="general", help="Category key (e.g. 'finance', 'coding')")
    parser.add_argument("--display_name", default="", help="Display name for new category")
    parser.add_argument("--name", default="", help="Task name")
    parser.add_argument("--summary", default="", help="Task summary/status update")
    parser.add_argument("--keywords", default="", help="Comma separated tags")
    parser.add_argument("--id", default="", help="Task ID for updates")
    parser.add_argument("--status", default="In-Progress", help="In-Progress or Completed")
    parser.add_argument("--query", default="", help="Search query")

    args = parser.parse_args()
    data = load_index()

    if args.action == "add":
        kw_list = [k.strip() for k in args.keywords.split(",") if k.strip()]
        res = add_task(args.category, args.name, args.summary, kw_list, data)
    elif args.action == "update":
        res = update_task(args.id or args.name, args.status, args.summary, data)
    elif args.action == "search":
        res = search_tasks(args.query, data)
    else:
        res = {"status": "error", "message": "Unknown action"}
    
    save_index(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
