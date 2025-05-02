# 🧩 Current Tasks Toolset (Inventory Review)

You have **20 tools** covering all key stages of the task lifecycle.

---

## 🔍 Query & Status

| Tool                                 | Description                                |
|--------------------------------------|--------------------------------------------|
| `GET /tasks/list`                    | List tasks with filters (status, pod owner, category) |
| `GET /tasks/{task_id}`              | Retrieve metadata for a specific task      |
| `GET /tasks/fetch_chain_of_thought` | Fetch chain of thought log                 |
| `GET /tasks/fetch_reasoning_trace`  | Fetch reasoning trace, optionally full trace |

---

## 🔄 Lifecycle Transitions

| Tool                         | Description                                     |
|------------------------------|-------------------------------------------------|
| `POST /tasks/create`         | Create a new task from a template               |
| `POST /tasks/activate`       | Mark a task as “planned”                        |
| `POST /tasks/start`          | Start a task and log prompt used               |
| `POST /tasks/reopen`         | Reopen a completed task                         |
| `POST /tasks/next`           | Retrieve the next available task               |
| `POST /tasks/complete`       | Complete a task and log final output           |
| `POST /tasks/scale_out`      | Create scaled-out clone to extend context      |

---

## 📦 Metadata + Collaboration

| Tool                                      | Description                                      |
|-------------------------------------------|--------------------------------------------------|
| `PATCH /tasks/update_metadata`            | Update metadata fields (status, inputs, etc.)    |
| `PATCH /tasks/update_metadata/{task_id}`  | Same, but scoped                                 |
| `POST /tasks/clone`                       | Clone a task with modified metadata              |
| `POST /tasks/append_chain_of_thought`     | Append reasoning notes                           |
| `POST /tasks/commit_and_log_output`       | Commit a task output and log                     |
| `POST /tasks/update_changelog/{task_id}`  | Update changelog with reasoning/logs             |

---

## 🤝 Handoff Coordination

| Tool                                 | Description                                    |
|--------------------------------------|------------------------------------------------|
| `POST /tasks/append_handoff_note`    | Append a handoff note to a task                |
| `POST /tasks/fetch_handoff_note`     | Retrieve the latest handoff note               |
| `POST /tasks/auto_generate_handoff`  | Generate a handoff note for a completed task   |
| `POST /tasks/auto_handoff`           | Chain two tasks together manually              |

---

## ✅ What’s Working Well

- Robust lifecycle management  
- Strong ReAct-style reasoning trace support  
- Handoff model (handoff notes + auto handoff)  
- Support for scaling and multi-pod use  

---

## 🧠 Opportunities & Gaps

### 1. 🔗 Task Chaining Logic (High Priority)
- ✅ You store `depends_on` and `handoff_from`
- ❌ No tools use these fields to:
  - Suggest next logical task
  - Auto-activate chained successors

**🔧 Add:**
- `POST /tasks/fetch_next_linked_task`
- Auto-trigger activation on dependent task when upstream completes

---

### 2. 🧭 Navigation & Filtering UX
- ❌ Cannot list tasks by phase, pod, or task chain

**🔧 Add:**
- `GET /tasks/list_phases` and/or `GET /tasks/graph`
- `GET /tasks/dependencies/{task_id}` for lineage

---

### 3. 🧩 Prompt + Output Transparency
- ❌ No endpoint to fetch all task artifacts

**🔧 Add:**
- `GET /tasks/artifacts/{task_id}` → includes prompt, outputs, reasoning

---

### 4. 🧪 Reasoning UX Gaps
- ✅ Tools exist for reasoning trace
- ❌ No summaries or scoring

**🔧 Add:**
- `/tasks/reasoning_summary` for impact/uniqueness analysis

---

### 5. 🔁 Cross-Pod Dispatch
- ❌ No way to route task directly to another pod's queue

**🔧 Add:**
- `handoff_to` support in `/start` or `/complete`
- Enhance `/tasks/auto_handoff` to handle pod-level dispatch

---

## 🛠 Recommended Enhancements (Prioritized)

| Priority | Task                                                                 |
|----------|----------------------------------------------------------------------|
| 🔼 High  | Add `fetch_next_linked_task` + auto-activate next based on `depends_on` |
| 🔼 High  | Update `/complete` to activate downstream tasks automatically        |
| 🔼 High  | Add `GET /tasks/artifacts/{task_id}`                                 |
| 🟡 Medium | Add `/graph` or `/dependencies/{task_id}`                           |
| 🟡 Medium | Add `/list_phases`                                                  |
| 🟢 Future | Add `/tasks/reasoning_summary` for analytical insights              |
| 🟢 Future | Extend `auto_handoff` for pod routing                               |

---

# 🎯 Enhancement: `/tasks/artifacts/{task_id}`

## ✅ Goal

Provide a **single endpoint** to fetch all artifacts related to a task. This enables comprehensive inspection, smoother context loading, and handoff reuse.

---

## 📦 What It Fetches

- `prompt_used.txt` – Prompt used to start the task
- `outputs` – All output files listed in `task.yaml.outputs`
- `reasoning_trace.yaml` – Summary of task reasoning
- `chain_of_thought.yaml` – Iterative GPT or human logs
- `handoff_notes.yaml` – Context passed to or from other tasks

---

## 🔍 Why It Matters

| Benefit                  | Purpose                                                  |
|--------------------------|----------------------------------------------------------|
| 🔍 Human inspection      | See the full trace and output of any task                |
| 📦 GPT context loading   | Load prompt + trace + outputs in one call                |
| 🔁 Reuse consistency     | Ensure handoffs reuse complete and aligned information   |

---

## 🛠 Patch Plan

- **Route**: `GET /tasks/artifacts/{task_id}`
- **Input**: `task_id`, `repo_name`
- **Output (example)**:
```json
{
  "task_id": "1.3",
  "prompt_used": "...", 
  "outputs": {
    "main.py": "...",
    "report.md": "..."
  },
  "reasoning_trace": "...",
  "chain_of_thought": "...",
  "handoff_notes": [
    {
      "from_pod": "DevPod",
      "to_pod": "QAPod",
      "reason": "Initial delivery",
      "notes": "Ready for testing"
    }
  ]
}
```

## 🛠 Implementation Notes for `/tasks/artifacts/{task_id}`

### 🧰 Functions to Use
- **`fetch_yaml_from_github()`** – Load `task.yaml`, `handoff_notes.yaml`, `chain_of_thought.yaml`, `reasoning_trace.yaml`
- **`safe_get_contents()`** – Retrieve file contents reliably with retry logic (for `prompt_used.txt` and outputs)

### ✅ Validation Logic
- Parse `task.yaml.outputs` to determine which files to fetch under `/project/outputs/{task_id}/`
- Only return outputs that exist in the repo
- If any artifact is missing (e.g., no handoff yet), return `null` or `"Not available"` for that section

---

## 🧠 Future Ideas

| Feature                  | Description |
|--------------------------|-------------|
| `format=zip` query param | Allow download of all artifacts as a ZIP archive |
| `artifacts_summary.md`  | Generate a clean markdown summary for sharing with humans or linking in handoffs |

These enhancements would help streamline delivery audits, handoffs, and cross-Pod collaboration.

---

## 🔗 GET /tasks/dependencies/{task_id}

### 🎯 Goal
Return a full list of upstream and downstream task dependencies for a given task ID, enabling:
- Visualization of task chains
- Detection of blockers or prerequisites
- DAG-based task planning and orchestration

---

### 🧠 Behavior

For a given `task_id`, return the following structure:

```json
{
  "task_id": "1.3_define_architecture",
  "upstream": ["1.1_capture_project_goals", "1.2_define_user_flows"],
  "downstream": ["1.4_build_data_flow", "1.5_write_api_spec"]
}
```
---

## 🧠 `/tasks/reasoning_summary`

### 🎯 Purpose
Provide a compact summary of reasoning effectiveness across all tasks, helping users understand quality, depth, and improvement areas at a glance.

---

### ✅ What It Returns

A project-wide table of reasoning metrics per task:

| task_id                   | thought_quality | recall_used | novel_insight | total_thoughts | improvement_opportunities |
|---------------------------|------------------|--------------|----------------|----------------|-----------------------------|
| 1.1_project_goals         | 4                | ✅           | ✅             | 6              | Clarify assumptions         |
| 2.2_feature_patch         | 3                | ❌           | ✅             | 3              | Include test rationale      |

Metrics are parsed from each task’s `reasoning_trace.yaml`.

---

### 🔄 Why It’s Needed

- `/tasks/fetch_reasoning_trace` shows full trace or per-task summary — but not rollups.
- This new endpoint supports audits, dashboards, and GPT-level reasoning improvement.

---

### ✅ Implementation Recommendation

**Route**: `GET /tasks/reasoning_summary`

**Returns**: List of all task IDs with parsed reasoning metrics.

---

### 🛠 Implementation Notes

- Load all `reasoning_trace.yaml` files from the repo
- Extract key fields: `thought_quality`, `recall_used`, `novel_insight`, etc.
- Format as summary table
- Handle missing/invalid fields gracefully

---

### ✅ Why Not Overload `/fetch_reasoning_trace`?

- Keeps tool responsibilities minimal and discoverable
- Plays well with `/metrics/summary`
- Future-proof for advanced analysis and batch reporting
