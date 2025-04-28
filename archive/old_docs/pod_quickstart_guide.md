# 🧠 Memory Pod GPT – Quickstart Guide

This guide helps you get up and running with a **Memory Pod** powered by:
- Custom GPT with OpenAPI Tool
- GitHub memory (`memory.yaml`)
- YAML-defined tasks (`task.yaml`)
- File retrieval via FastAPI Git Proxy (`GET` or `POST /batch-files`)

---

## ✅ Overview
Memory Pods are purpose-specific GPTs (e.g., DevPod, QAPod) that dynamically retrieve relevant files from a Git repo and complete a scoped task.

---

## 🔗 Setup
### 1. Structure Your Files
Create a task definition and memory map:

#### `task.yaml`
```yaml
task_id: F1.2-generate-tests-batch
pod: DevPod
description: Generate unit tests using agent logic and validator
inputs:
  - src/models/agent/concussion_agent.py
  - src/models/agent/concussion_validator.py
```

#### `memory.yaml`
```yaml
- path: src/models/agent/concussion_agent.py
  repo: stewmckendry/ai-delivery-framework
- path: src/models/agent/concussion_validator.py
  repo: stewmckendry/ai-delivery-framework
```

---

### 2. Prepare the Repo
✅ Ensure the input file paths in `task.yaml` match those in `memory.yaml`.
✅ Confirm files exist in GitHub under the specified paths.

---

## 🧠 Using the Memory Pod GPT
Paste this into your GPT:

```markdown
🎯 POD MISSION: DevPod – Generate unit tests for concussion logic

🧾 TASK YAML:
(paste your `task.yaml`)

📁 MEMORY:
(paste your `memory.yaml`)

📡 TOOL USE:
Use the GitHub File Tool (batch preferred) to retrieve all inputs.
Then analyze the files and perform the task.
```

GPT will:
1. Parse the inputs
2. Retrieve files using `POST /batch-files`
3. Perform reasoning
4. Return output in markdown or code format

---

## 🛠️ Tool Endpoints
### `GET /repos/{owner}/{repo}/contents/{path}`
Single file fetch

### `POST /batch-files`
Preferred for multi-input tasks
```json
{
  "owner": "stewmckendry",
  "repo": "ai-delivery-framework",
  "paths": [
    "src/models/agent/concussion_agent.py",
    "src/models/agent/concussion_validator.py"
  ]
}
```

---

## 📦 Output Example
```python
# test/models/agent/test_concussion_logic.py

def test_parse_input():
    agent = ConcussionAgent()
    result = agent.parse_input("I feel nausea")
    assert "nausea" in result
```

---

## 🔄 Best Practices
- Keep file paths clean and correct
- Include full task + memory in prompt
- Use batch endpoint for multi-file tasks
- Ask GPT to explain its reasoning if unsure

---

Let’s build faster. Smarter. AI-native. 🚀
