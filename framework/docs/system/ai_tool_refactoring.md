## 🎯 POD MISSION: Trim and Consolidate OpenAPI Tools for Custom GPT Integration

### Objective
We are preparing the AI-native delivery framework for seamless integration with OpenAI **Custom GPTs**, which currently support a **maximum of 30 OpenAPI operations**. Our current spec has **46 operations**, so we must refactor and consolidate the toolset to stay within limits — without sacrificing clarity, modularity, or GPT usability.

---

## ✅ Mission Goals

1. **Consolidate tools** into logical groups using a param-based model (action, mode, etc.)
2. **Trim or defer** low-priority or internal-only endpoints
3. **Preserve full GPT tool discoverability** (no abstract dispatcher)
4. **Generate updated openapi.json** and compatible FastAPI handlers

---

## 📦 Inputs

- Current openapi.json (46 endpoints)
- Current main.py (FastAPI routes for each tool)
- Agreement on:
  - Critical tools to keep (must-have for Pods)
  - Optional tools to defer
  - Naming conventions (e.g., manage_entry, query, update_metadata)
  - Parameter structure (e.g., action, tool_mode, etc.)

---

## 🔁 Working Style: How We Collaborate

You (GPT Pod) will:

1. **Generate a high-level plan**
   - Propose grouping strategy and endpoint consolidation table
   - Tell me what inputs you need and what assumptions to confirm

2. **Create an implementation backlog**
   - Break down work into small, reviewable steps
   - Track progress and update backlog after each batch

3. **Bundle patches into logical groups**
   - For each batch, generate:
     - Updated OpenAPI chunk (≤1 route or 1 group)
     - Python FastAPI patch (new route handler)
     - Test payload(s) and expected response

4. **Pause between steps** for review and approval

5. **Support integration and testing**
   - Help run sample calls to validate new structure
   - Document all changes for onboarding and system prompts

---

## 🧩 Sample Consolidations

### Memory Tools
| From                                       | To                          | Param Key  |
|--------------------------------------------|------------------------------|-------------|
| /memory/search, /diff, /stats, /validate-files | /memory/query              | mode       |
| /memory/add, /update_entry, /remove | /memory/manage_entry       | action    |

### Task Metadata Tools
| From                                        | To                            | Param Key  |
|---------------------------------------------|--------------------------------|------------|
| /tasks/update_metadata, /clone, /update_changelog/{task_id} | /tasks/manage_metadata       | action   |

### Issue Management
| From                                          | To                            | Param Key   |
|------------------------------------------------|-------------------------------|-------------|
| /system/log_issue_or_enhancement, /fetch_issues_or_enhancements, /update_issue_status | /system/manage_issues | action     |

---

## 📝 Deliverables

- openapi.json with ≤ 30 routes
- New FastAPI route handlers (1 per consolidated group)
- Sample payloads per tool group
- Backlog file (e.g., openapi_refactor_backlog.yaml)
- Optional markdown documentation for onboarding and prompts

---

## 🚀 Let’s Get Started

First action: GPT should respond with:
- Tool grouping plan
- Assumptions to validate
- Inputs needed from me before generating patches

Repo: ai-delivery-framework  
Files: openapi.json, main.py

---

# ✅ Step 1: Proposed Tool Grouping Plan

We’ll group the 46+ routes into functional clusters using a `mode` or `action` parameter to reduce route count without sacrificing GPT discoverability.

---

## 🔁 Consolidation Plan (Initial Draft)

| Group Name           | New Endpoint             | Method | Param Key | Existing Routes to Merge                                                                 |
|----------------------|--------------------------|--------|-----------|------------------------------------------------------------------------------------------|
| Memory Management    | `/memory/manage`         | POST   | action    | `/memory/add`, `/memory/index`, `/memory/diff`, `/memory/validate-files`, `/memory/remove` |
| Memory Query         | `/memory/query`          | POST   | mode      | `/memory/search`, `/memory/stats`, `/memory/similarity` (if any)                        |
| Task Metadata Ops    | `/tasks/manage_metadata` | POST   | action    | `/tasks/update_metadata`, `/tasks/clone`, `/tasks/update_changelog/{task_id}`           |
| Chain of Thought     | `/tasks/chain_of_thought`| POST/GET | action   | `/tasks/append_chain_of_thought`, `/tasks/fetch_chain_of_thought`                       |
| Reasoning Trace      | `/tasks/reasoning_trace` | GET    | full flag | `/tasks/fetch_reasoning_trace`                                                          |
| Issue Management     | `/system/manage_issues`  | POST/GET | action   | `/system/log_issue_or_enhancement`, `/system/fetch_issues_or_enhancements`, `/system/update_issue_status` |
| Project Setup        | `/project/init`          | POST   | —         | `/project/init_project`                                                                 |
| Metrics              | `/metrics/manage`        | POST   | action    | `/metrics/summary`, `/metrics/export`                                                   |
| GitHub Files         | `/files/fetch`           | POST   | batch     | `/getFile`, `/batch-files`                                                              |
| Git Operations       | `/git/ops`               | POST   | action    | `/git/rollback_commit` (future: `/list_commits`, etc.)                                  |
| Task Lifecycle       | `/tasks/lifecycle`       | POST   | action    | `/tasks/start`, `/tasks/complete`, `/tasks/next`, `/tasks/activate`, `/tasks/reopen`, `/tasks/scale_out`, `/tasks/create` |
| Handoff Ops          | `/tasks/handoff`         | POST   | action    | `/tasks/append_handoff_note/{task_id}`, `/tasks/fetch_handoff_note`, `/tasks/auto_generate_handoff/{task_id}`, `/tasks/auto_handoff` |
| Output Commit        | `/tasks/output`          | POST   | —         | `/tasks/commit_and_log_output`                                                          |
| Audit Tools          | `/audit/manage`          | POST   | action    | `/audit/validate_changelog`                                                             |
| System Utilities     | `/system/utilities`      | POST   | mode      | `/system/guide`, `/actions/list`                                                        |
| Task Details         | `/tasks/details/{task_id}`| GET   | —         | `/tasks/{task_id}`                                                                      |

📊 **Total Resulting Routes:** ~16–18 (well under 30!)

- Tools remain GPT-discoverable via `x-gpt-action` blocks at the operation level.

---

## 📌 Assumptions to Validate

- ✅ Discoverability is critical — we’ll avoid opaque dispatcher routes and preserve semantic clarity.
- ✅ You're okay with consolidating by functional cluster using action or mode logic inside handlers.
- ✅ Legacy routes may be deprecated — no need to maintain backwards compatibility.
- ⚠️ For dynamic path routes (like `/{task_id}`), `task_id` will move to the body unless critical to remain in the URL.

---

## 📥 Inputs Needed From You

- ✅ List of **must-keep** routes (if any should be exempt from consolidation)
- ✅ Preferred naming style for the `action` or `mode` parameter
- ⛳ List of any Pods or tools using **hardcoded legacy paths** (to coordinate updates)

---

## ⏭️ Next Steps

Once confirmed, I will:

1. Generate `openapi_refactor_backlog.yaml`
2. Start with **Batch 1**: `memory/manage` + FastAPI patch + OpenAPI update

**Ready to proceed?**

---

# ✅ Step 1: Proposed Tool Grouping Plan

We’ll group the 46+ routes into functional clusters using a `mode` or `action` parameter to reduce route count without sacrificing GPT discoverability.

---

## 🔁 Consolidation Plan (Initial Draft)

| Group Name           | New Endpoint             | Method | Param Key | Existing Routes to Merge                                                                 |
|----------------------|--------------------------|--------|-----------|------------------------------------------------------------------------------------------|
| Memory Management    | `/memory/manage`         | POST   | action    | `/memory/add`, `/memory/index`, `/memory/diff`, `/memory/validate-files`, `/memory/remove` |
| Memory Query         | `/memory/query`          | POST   | mode      | `/memory/search`, `/memory/stats`, `/memory/similarity` (if any)                        |
| Task Metadata Ops    | `/tasks/manage_metadata` | POST   | action    | `/tasks/update_metadata`, `/tasks/clone`, `/tasks/update_changelog/{task_id}`           |
| Chain of Thought     | `/tasks/chain_of_thought`| POST/GET | action   | `/tasks/append_chain_of_thought`, `/tasks/fetch_chain_of_thought`                       |
| Reasoning Trace      | `/tasks/reasoning_trace` | GET    | full flag | `/tasks/fetch_reasoning_trace`                                                          |
| Issue Management     | `/system/manage_issues`  | POST/GET | action   | `/system/log_issue_or_enhancement`, `/system/fetch_issues_or_enhancements`, `/system/update_issue_status` |
| Project Setup        | `/project/init`          | POST   | —         | `/project/init_project`                                                                 |
| Metrics              | `/metrics/manage`        | POST   | action    | `/metrics/summary`, `/metrics/export`                                                   |
| GitHub Files         | `/files/fetch`           | POST   | batch     | `/getFile`, `/batch-files`                                                              |
| Git Operations       | `/git/ops`               | POST   | action    | `/git/rollback_commit` (future: `/list_commits`, etc.)                                  |
| Task Lifecycle       | `/tasks/lifecycle`       | POST   | action    | `/tasks/start`, `/tasks/complete`, `/tasks/next`, `/tasks/activate`, `/tasks/reopen`, `/tasks/scale_out`, `/tasks/create` |
| Handoff Ops          | `/tasks/handoff`         | POST   | action    | `/tasks/append_handoff_note/{task_id}`, `/tasks/fetch_handoff_note`, `/tasks/auto_generate_handoff/{task_id}`, `/tasks/auto_handoff` |
| Output Commit        | `/tasks/output`          | POST   | —         | `/tasks/commit_and_log_output`                                                          |
| Audit Tools          | `/audit/manage`          | POST   | action    | `/audit/validate_changelog`                                                             |
| System Utilities     | `/system/utilities`      | POST   | mode      | `/system/guide`, `/actions/list`                                                        |
| Task Details         | `/tasks/details/{task_id}`| GET   | —         | `/tasks/{task_id}`                                                                      |

📊 **Total Resulting Routes:** ~16–18 (well under 30!)

- Tools remain GPT-discoverable via `x-gpt-action` blocks at the operation level.

---

## 📌 Assumptions to Validate

- ✅ Discoverability is critical — we’ll avoid opaque dispatcher routes and preserve semantic clarity.
- ✅ You're okay with consolidating by functional cluster using action or mode logic inside handlers.
- ✅ Legacy routes may be deprecated — no need to maintain backwards compatibility.
- ⚠️ For dynamic path routes (like `/{task_id}`), `task_id` will move to the body unless critical to remain in the URL.

---

## 📥 Inputs Needed From You

- ✅ List of **must-keep** routes (if any should be exempt from consolidation)
- ✅ Preferred naming style for the `action` or `mode` parameter
- ⛳ List of any Pods or tools using **hardcoded legacy paths** (to coordinate updates)

---

## ⏭️ Next Steps

Once confirmed, I will:

1. Generate `openapi_refactor_backlog.yaml`
2. Start with **Batch 1**: `memory/manage` + FastAPI patch + OpenAPI update

**Ready to proceed?**

---

# 📦 Consolidation Impact Assessment: `/memory/manage`

This assessment outlines the plan and implications for merging the following four routes into a single consolidated endpoint:

- `/memory/add`
- `/memory/index`
- `/memory/diff`
- `/memory/validate-files`

---

## 🧠 Comparison Summary: Inputs and Outputs

### ✅ Common Payload Elements
All four actions share:
- `repo_name` (required)
- JSON request/response format
- Specific fields like `files` or `base_paths` depending on action

---

## 🗂️ Per-Action Request & Response Breakdown

| Action   | Input Payload Fields                        | Output Fields                                   |
|----------|---------------------------------------------|-------------------------------------------------|
| add      | `repo_name`, `files` (with metadata)        | `message`, `memory_index`                       |
| index    | `repo_name`, `base_paths` (optional)        | `message`                                       |
| diff     | `repo_name`, `base_paths` (required)        | `message`, `missing_files`                      |
| validate | `repo_name`, `files` (list of file paths)   | `validated_files` (exists_in_memory + github)   |

---

## 📊 Field Overlap and Uniqueness

| Field       | add | index | diff | validate | Common?   |
|-------------|-----|-------|------|----------|-----------|
| repo_name   | ✅  | ✅    | ✅   | ✅       | ✅        |
| files       | ✅  | ❌    | ❌   | ✅       | Partial   |
| base_paths  | ❌  | ✅    | ✅   | ❌       | Partial   |
| action (new)| 🔄  | 🔄    | 🔄   | 🔄       | ✅ (new)  |

---

## 🔁 Action-to-Route Mapping

| Action   | Replaces Route              | Assumed Function Name       |
|----------|-----------------------------|-----------------------------|
| add      | `/memory/add`               | `add_to_memory`             |
| index    | `/memory/index`             | `index_memory`              |
| diff     | `/memory/diff`              | `diff_memory_files`         |
| validate | `/memory/validate-files`    | `validate_memory_file_exists`|

---

## 🧠 GPT Discoverability

In `openapi.json`, add:

```json
"x-gpt-action": {
  "name": "Manage Memory Files",
  "instructions": "Use this to add, index, diff, or validate memory entries. Set `action` to one of: add, index, diff, validate.",
  "summary_keywords": ["memory", "add", "index", "diff", "validate"]
}
```

---

# 🧩 Proposed Consolidation Plan for `/memory/*` Routes

This plan merges multiple memory-related endpoints into streamlined, semantically grouped routes while preserving clarity, discoverability, and GPT compatibility.

---

## 🔁 Group 1: `/memory/manage` ✅ (Already Done)

| Legacy Route              | Action Param |
|---------------------------|--------------|
| `/memory/add`             | `add`        |
| `/memory/index`           | `index`      |
| `/memory/diff`            | `diff`       |
| `/memory/validate-files`  | `validate`   |

**✅ Status:** Completed

---

## 🧠 Group 2: `/memory/query` (📦 Batch 2 Target)

| Legacy Route             | Mode Param |
|--------------------------|------------|
| `/memory/search`         | `search`   |
| `/memory/list_entries`   | `list`     |
| `/memory/stats`          | `stats`    |

### New Endpoint: `/memory/query`
- **Param:** `mode`: `search` | `list` | `stats`
- **Structure:** `repo_name` is always required; other fields depend on mode

| Mode   | Additional Params             | Output Example                               |
|--------|-------------------------------|----------------------------------------------|
| search | `keyword`                     | `matches[]`                                  |
| list   | `pod_owner`, `tag`, `type`    | `results[]`, `total`                         |
| stats  | *(none)*                      | `total_entries`, `by_pod_owner`, etc.        |

---

## 🛠 Group 3: `/memory/manage_entry` (📦 Batch 3 Target)

| Legacy Route              | Action Param |
|---------------------------|--------------|
| `/memory/update_entry`    | `update`     |
| `/memory/remove`          | `remove`     |

### New Endpoint: `/memory/manage_entry`
- **Param:** `action`: `update` | `remove`
- **Field Notes:**
  - `update`: Requires `path` + one or more fields (`description`, `tags`, `owner`)
  - `remove`: Requires `path`

---

## 🧭 Consolidated Endpoint Summary

| New Route              | Param Key | Supported Modes / Actions       | Replaces Routes                                 |
|------------------------|-----------|----------------------------------|-------------------------------------------------|
| `/memory/manage`       | `action`  | `add`, `index`, `diff`, `validate` | ✅ Done: `/add`, `/index`, `/diff`, `/validate` |
| `/memory/query`        | `mode`    | `search`, `list`, `stats`         | `/search`, `/list_entries`, `/stats`           |
| `/memory/manage_entry` | `action`  | `update`, `remove`                | `/update_entry`, `/remove`                     |

---

Would you like to proceed with `/memory/query` as Batch 2?

---

# 🧠 Batch 2: Updated Impact Assessment — `/memory/query`

## 🎯 Goal
Consolidate memory query tools into a single discoverable and extendable endpoint: `/memory/query`.

### ✅ Legacy Tools to Consolidate

| Existing Route         | New Mode Value | Purpose                                   |
|------------------------|----------------|-------------------------------------------|
| `/memory/search`       | `search`       | Keyword-based search in memory index      |
| `/memory/list_entries` | `list`         | List entries with optional filters        |
| `/memory/stats`        | `stats`        | Return memory index diagnostics           |

---

## 🗂️ Field Comparison by Mode

| Mode   | Required Fields     | Optional Fields               | Response Keys                                  |
|--------|----------------------|-------------------------------|------------------------------------------------|
| search | `repo_name`, `keyword` | —                             | `matches`                                      |
| list   | `repo_name`           | `pod_owner`, `tag`, `file_type` | `total`, `results[]`                          |
| stats  | `repo_name`           | —                             | `total_entries`, `missing_metadata`, `by_pod_owner` |

---

### 📦 Next Steps
- Define FastAPI route: `POST /memory/query`
- Use `mode` parameter to switch logic paths
- Update OpenAPI schema with x-gpt-action per mode
- Return consistent JSON structures with mode-specific fields

---

# 🧠 Batch 3: Impact Assessment — `/memory/manage_entry`

## 🎯 Objective
Consolidate the following memory entry modification routes into a single endpoint:

| Original Route           | New Action | Function Name         |
|--------------------------|------------|------------------------|
| `/memory/update_entry`   | `update`   | `handle_update_entry` |
| `/memory/remove`         | `remove`   | `handle_remove_entry` |

---

## 🧩 Field Comparison

| Field       | `update_entry` | `remove` | Common? | Notes                            |
|-------------|----------------|----------|---------|----------------------------------|
| `repo_name` | ✅              | ✅        | ✅       | Always required                  |
| `path`      | ✅              | ✅        | ✅       | Path of the file to modify       |
| `description` | ✅            | ❌        | ✴️       | Optional — only for update       |
| `tags`      | ✅              | ❌        | ✴️       | Optional — only for update       |
| `pod_owner` | ✅              | ❌        | ✴️       | Optional — only for update       |

---

## 📌 Endpoint Design

- **Route:** `POST /memory/manage_entry`
- **Param:** `action` with enum: `update` | `remove`
- **Behavior:** 
  - `update`: modifies metadata fields of a given path
  - `remove`: deletes the entry from memory.yaml

---

## ✅ Benefits

- Simplifies the API surface
- Ensures consistent schema and validation logic
- Enhances GPT tool discoverability through unified `x-gpt-action` blocks

---

🧠 **`/tasks/` Consolidation Plan**

We’ll group routes by functional intent, preserving discoverability with `action` or `mode` where needed.  
The goal is to reduce from ~25 routes to ~6–8 multi-mode endpoints.

---

✅ **Group 1: `/tasks/manage_metadata` (Batch 4A)**  
**Original Route** | **Action**  
--- | ---  
`/tasks/update_metadata` | `update_metadata`  
`/tasks/update_changelog/{task_id}` | `update_changelog`  
`/tasks/clone` | `clone`  

**New endpoint**: `/tasks/manage_metadata`  
**Param**: `action` (string), plus `task_id` in body  

---

✅ **Group 2: `/tasks/lifecycle`**  
**Original Route** | **Action**  
--- | ---  
`/tasks/start` | `start`  
`/tasks/complete` | `complete`  
`/tasks/reopen` | `reopen`  
`/tasks/next` | `next`  
`/tasks/create` | `create`  
`/tasks/scale_out` | `scale_out`  

**New endpoint**: `/tasks/lifecycle`  
**Param**: `action` (string), possibly with `task_id`  

---

✅ **Group 3: `/tasks/handoff`**  
**Original Route** | **Action**  
--- | ---  
`/tasks/append_handoff_note/{task_id}` | `append`  
`/tasks/fetch_handoff_note` | `fetch`  
`/tasks/auto_generate_handoff/{task_id}` | `generate_auto`  
`/tasks/auto_handoff` | `execute_auto`  

**New endpoint**: `/tasks/handoff`  
**Param**: `action` (string), `task_id` in body  

---

✅ **Group 4: `/tasks/chain_of_thought`**  
**Original Route** | **Action**  
--- | ---  
`/tasks/append_chain_of_thought` | `append`  
`/tasks/fetch_chain_of_thought` | `fetch`  

**New endpoint**: `/tasks/chain_of_thought`  
**Param**: `action` (string)  

---

✅ **Group 5: `/tasks/reasoning`**  
**Original Route** | **Action**  
--- | ---  
`/tasks/fetch_reasoning_trace` | `trace`  
`/tasks/reasoning_summary` | `summary`  

**New endpoint**: `/tasks/reasoning`  
**Param**: `action` (string)  

---

✅ **Group 6: `/tasks/query`**  
**Original Route** | **Mode / ID**  
--- | ---  
`/tasks/list` | `list`  
`/tasks/list_phases` | `list_phases`  
`/tasks/graph` | `graph`  
`/tasks/dependencies/{task_id}` | `dependencies`  
`/tasks/{task_id}` | `get_details`  

**New endpoint**: `/tasks/query`  
**Param**: `mode` (string), task-specific actions go in body  

---

✅ **Group 7: `/tasks/artifacts`**  
**Original Route** | **Notes**  
--- | ---  
`/tasks/artifacts/{task_id}` | Standalone  

This could remain standalone or be bundled into `/tasks/query` as `mode=artifacts`.

---

🧭 **Summary Table**

**New Endpoint** | **Param Key** | **Routes Merged**  
--- | --- | ---  
`/tasks/manage_metadata` | `action` | `update_metadata`, `update_changelog`, `clone`  
`/tasks/lifecycle` | `action` | `start`, `complete`, `reopen`, `next`, `create`, `scale_out`  
`/tasks/handoff` | `action` | `append_handoff_note`, `fetch_handoff_note`, `auto_generate_handoff`, `auto_handoff`  
`/tasks/chain_of_thought` | `action` | `append_chain_of_thought`, `fetch_chain_of_thought`  
`/tasks/reasoning` | `action` | `fetch_reasoning_trace`, `reasoning_summary`  
`/tasks/query` | `mode` | `list`, `list_phases`, `graph`, `dependencies`, `task_id`, *(optional: artifacts)*  

---

🧠 **Revised Batch 4A: `/tasks/manage_metadata`**

🎯 **Consolidates:**

**Original Route** | **Action**  
--- | ---  
`/tasks/update_metadata` | `update_metadata`  
`/tasks/clone` | `clone`  

---

🧠 **Batch 4B: Impact Assessment — `/tasks/lifecycle`**

🎯 **Goal**  
Unify the following into a single `action`-based route for task lifecycle transitions:

**Original Route** | **Action** | **Summary**  
--- | --- | ---  
`/tasks/start` | `start` | Mark task in progress + log prompt  
`/tasks/complete` | `complete` | Mark done, log outputs & trace  
`/tasks/reopen` | `reopen` | Undo completion, restart task  
`/tasks/next` | `next` | Suggest next available task  
`/tasks/scale_out` | `scale_out` | Fork current task into new one  

---

🧩 **Payload Comparison (by action)**

| **Field**         | **start** | **complete** | **reopen** | **next** | **scale_out** | **Notes**                                  |
|-------------------|-----------|--------------|------------|----------|----------------|---------------------------------------------|
| `repo_name`       | ✅        | ✅           | ✅         | ✅       | ✅             | Required for all                            |
| `task_id`         | ✅        | ✅           | ✅         | ❌       | ✅             | Required for all but `next`                 |
| `prompt_used`     | ✅        | ❌           | ❌         | ❌       | ❌             | Required only for `start`                   |
| `outputs`         | ❌        | ✅           | ❌         | ❌       | ❌             | Required for `complete`                     |
| `reasoning_trace` | ❌        | ✅           | ❌         | ❌       | ❌             | Optional for `complete`                     |
| `handoff_note`    | ❌        | ✅           | ❌         | ❌       | ✅             | Used by `complete` and `scale_out`          |
| `reason`          | ❌        | ❌           | ✅         | ❌       | ✅             | Used in `reopen`, `scale_out`               |
| `pod_owner`       | ❌        | ❌           | ❌         | ✅       | ❌             | Used only for `next`                        |

---

🧠 **Batch 4C: Impact Assessment — `/tasks/handoff`**

🎯 **Goal**  
Unify the following 4 endpoints into a single multi-action endpoint for task handoffs:

**Original Route** | **Action** | **Summary**  
--- | --- | ---  
`/tasks/append_handoff_note/{task_id}` | `append` | Manually append a handoff note to a task  
`/tasks/fetch_handoff_note` | `fetch` | Retrieve latest upstream handoff note  
`/tasks/auto_generate_handoff/{task_id}` | `generate_auto` | Auto-generate a handoff note for a task  
`/tasks/auto_handoff` | `execute_auto` | Automatically log and propagate a full handoff  

---

🧩 **Field Comparison**

| **Field**                  | **append** | **fetch** | **generate_auto** | **execute_auto** | **Notes**                                                  |
|----------------------------|------------|-----------|-------------------|------------------|-------------------------------------------------------------|
| `repo_name`                | ✅         | ✅        | ✅                | ✅               | Required for all                                           |
| `task_id`                  | ✅ (path)  | ✅        | ✅ (path)         | ✅               | Always required                                            |
| `next_task_id`            | ❌         | ❌        | ❌                | ✅               | For downstream chaining                                    |
| `handoff_mode`             | ❌         | ❌        | ❌                | ✅               | Used in `execute_auto` to tag sync/async mode              |
| `from_pod` / `to_pod`      | ✅         | ❌        | *(inferred)*      | ✅               | Manual vs. inferred based on task lineage                  |
| `token_count`, `next_prompt` | ✅     | ❌        | ❌                | ❌               | Used only in `append` or passed in by GPT                 |
| `reference_files`, `notes`, `ways_of_working` | ✅ | ❌ | ❌ | ❌ | Enriched metadata captured during manual handoffs          |

---

🚀 **Proposed Design**

**New Route**:  
`POST /tasks/handoff`  
**Param**: `"action"` with options:  
- `"append"` (manual input)  
- `"fetch"` (lookup from upstream)  
- `"generate_auto"` (GPT-written)  
- `"execute_auto"` (auto-log + propagate)  

---

🧠 **Batch 4D: Impact Assessment — `/tasks/chain_of_thought`**

🎯 **Goal**  
Unify the following two endpoints into a single mode-based route:

**Original Route** | **Action** | **Description**  
--- | --- | ---  
`/tasks/append_chain_of_thought` | `append` | Log a message, issue, or lesson  
`/tasks/fetch_chain_of_thought` | `fetch` | Retrieve all thoughts for a given task  

---

🧩 **Field Comparison**

| **Field**        | **append** | **fetch** | **Notes**                                      |
|------------------|------------|-----------|------------------------------------------------|
| `repo_name`      | ✅         | ✅        | Always required                                |
| `task_id`        | ✅         | ✅        | Always required                                |
| `message`        | ✅         | ❌        | Required for `append`                          |
| `tags`           | optional   | ❌        | Optional tagging for `append`                  |
| `issues`         | optional   | ❌        | List of issues linked to thought               |
| `lessons`        | optional   | ❌        | Lessons learned                                |

---

🔁 **Recommended API Design**

**New Route**:  
`POST /tasks/chain_of_thought`  

**Parameter**: `"action"` with values:  
- `"append"`: add entry to `chain_of_thought.yaml`  
- `"fetch"`: return all entries for a task  

---

🧠 **Batch 4E: Impact Assessment — `/tasks/reasoning_trace`**

🎯 **Goal**  
Unify the following reasoning-focused tools under one route:

**Original Route** | **Action** | **Purpose**  
--- | --- | ---  
`/tasks/fetch_reasoning_trace` | `fetch` | Get final or full reasoning for a single task  
`/tasks/reasoning_summary` | `summary` | Generate reasoning quality metrics across all tasks  

---

🧩 **Field Comparison**

| **Field**     | **fetch** | **summary** | **Notes**                          |
|---------------|-----------|-------------|------------------------------------|
| `repo_name`   | ✅        | ✅          | Required for both                  |
| `task_id`     | ✅        | ❌          | Required for `fetch`               |
| `full`        | ✅        | ❌          | Optional for `fetch`               |

---

🔁 **Recommended API Design**

**New Route**:  
`POST /tasks/reasoning_trace`  

**Param**: `"action"` with values:  
- `"fetch"` – get final or full trace for a specific task  
- `"summary"` – return a quality report across all tasks  

---

🧠 **Batch 6A: Impact Assessment — `/tasks/query`**

🎯 **Goal**  
Consolidate the following 5 metadata routes into one unified query interface:

**Original Route** | **mode Value** | **Purpose**  
--- | --- | ---  
`/tasks/list` | `list` | List tasks (optionally filtered by pod/status/etc.)  
`/tasks/list_phases` | `list_phases` | List tasks grouped by SDLC phase  
`/tasks/graph` | `graph` | Task dependency graph (nodes + edges)  
`/tasks/dependencies/{task}` | `dependencies` | Upstream + downstream dependencies for a task  
`/tasks/{task}` | `get_details` | Full metadata for a specific task  

---

🔁 **Recommended API Design**

**New Route**:  
`POST /tasks/query`  

**Required Param**:  
- `mode`: `list` | `list_phases` | `graph` | `dependencies` | `get_details`  

---

**Input Fields**

| **Field**     | **Type**  | **Used In**               | **Description**                                |
|---------------|-----------|----------------------------|------------------------------------------------|
| `mode`        | string    | all                        | Which query to perform (list, graph, etc.)     |
| `repo_name`   | string    | all                        | GitHub repo to query                           |
| `task_id`     | string    | `get_details`, `dependencies` | Task to look up if querying specific one    |
| `status`      | string    | `list`                     | Optional filter (e.g., `in_progress`)          |
| `pod_owner`   | string    | `list`                     | Optional filter (e.g., `ProductPod`)           |
| `category`    | string    | `list`                     | Optional filter for category                   |

---


