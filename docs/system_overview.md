# General Flow of the System

[Human Lead] 
    ↓
[List Tasks] → [Pick Task] → [Activate Task] → [Validate Inputs (memory + GitHub)]
    ↓
[Pod Starts Task] 
    ↓
[Optional: Search Memory for Context]
    ↓
[Work: Outputs + Reasoning + Prompt]
    ↓
[Promote Patch (outputs + memory.yaml updated)]
    ↓
[Generate Patch + Create PR]
    ↓
[Human Lead Reviews & Merges]
    ↓
[Memory + Repo Updated 📚]
    ↓
[Pods Get Smarter Next Time 🚀]


# 🧩 How the Core Tools Fit Into the Flow

| **Stage** | **Tool(s)** |
|-----------|-------------|
| **List and pick tasks** | `/tasks/list`, `/tasks/{task_id}` |
| **Activate and validate inputs** | `/tasks/activate`, `/memory/validate-files` |
| **Find supporting context** | `/memory/search` |
| **Produce outputs** | Free-form Pod work |
| **Promote patch** | `/patches/promote`, `/memory/add` |
| **Validate + Generate Patch** | Shell scripts: `generate_patch_from_output.sh`, `create_pr_from_patch.sh` |
| **Merge and grow** | GitHub PR process |

---
