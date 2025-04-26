# 🧠 Memory Management for AI-Native Delivery

---

## What Problem Are We Solving?

You’re 100% right:

- ✅ We already have a Git repository holding everything (tasks, outputs, prompts, traces)
- ✅ GPT Pods can fetch individual files if they know the path
- ⛔️ But Pods don't know what's in the repo unless told explicitly — and ChatGPT can't natively browse Git folders today.

👉 **memory.yaml** is a **directory + metadata index** — a searchable, structured view of project knowledge to help GPT (and humans) navigate growing complexity.

> Think of it as project scaffolding for AI-native teamwork.

---

## 🗺️ What Will Be Inside `memory.yaml`?

For each known file:

- `file_path`: where to find it
- `description`: what it contains (auto or human-enriched)
- `tags`: helpful filters (e.g., `dev`, `research`, `spec`, `test`, `retrospective`)

### Example

```yaml
memory:
  prompts_used_DevPod_2_1_capture_project_goals_prompt_txt:
    file_path: prompts/used/DevPod/2.1_capture_project_goals_prompt.txt
    description: "Prompt to capture high-level project goals in early Discovery phase"
    tags: ["prompt", "devpod", "discovery"]
```

---

## 🏗️ What Does `memory.yaml` Enable?

Without it:

- GPT can only hard-code known paths
- No structured recall
- Scaling = brittle

With it:

- ✅ Pods can search `memory.yaml` to discover past outputs, prompts, thoughts, specs
- ✅ Future tools can retrieve related work before generating new patches
- ✅ Humans can visualize project assets
- ✅ It future-proofs scaling to 100s or 1000s of outputs

---

## 🛠️ How Will It Actually Be Used?

| **User** | **How they use memory.yaml** | **Example** |
|----------|-------------------------------|-------------|
| GPT Pod | - Lookup a file needed for a current task<br>- Suggest similar past outputs<br>- Improve generation quality | "Before writing test plan, fetch memory items tagged 'testplan'" |
| Human Lead | - Browse memory easily<br>- Search for "all patches for feature X" or "all research spikes" | "Show me all DevPod outputs from Discovery phase" |
| Scripts / Tools | - Auto-attach links to PRs<br>- Preload Pod work sessions with context | Auto-populate "related memory" section when launching a Pod |

---

## 🔥 How We Make It Frictionless, Repeatable, Feasible

### Frictionless

- Index automatically via FastAPI (`index_memory`)
- GPT can suggest, Human approves/augments
- Tools like `add_descriptions_to_memory` can semi-automate enrichment

### Repeatable

- Every project has a `memory.yaml`
- Every Pod knows: "Search `memory.yaml` first."

### Feasible (Today’s Limits)

- GPT can't auto-push to Git
- But GPT can generate `memory.yaml` updates
- Human Lead stages updates manually with `promote_patch`

---

# 🔥 Overall Flow After This Patch

| **Step** | **Action** |
|----------|------------|
| 1 | Pod completes task and uses `promote_patch` |
| 2 | FastAPI promotes outputs + updates `memory.yaml` live |
| 3 | Human downloads ZIP |
| 4 | `generate_patch_from_output.sh` unzips outputs + `memory.yaml` |
| 5 | Patch file created with outputs + updated `memory.yaml` |
| 6 | GitHub PR created |
| 7 | AI-native delivery system gets smarter every patch 🚀 |

---

# ✨ Memory Management Roadmap

| Step | Action | Who/What |
|------|--------|----------|
| 1 | Selectively index framework files now, all project files later | `index_memory` tool |
| 2 | Tag entries as `framework`, `project`, or both | during indexing |
| 3 | After each patch, promote updated `memory.yaml` if needed | Human + `promote_patch` |
| 4 | GPT drafts file descriptions, human refines optionally | `add_descriptions_to_memory` tool |
| 5 | Build lightweight retrieval helpers | `fetch_memory_item`, `list_memory_by_tag` |
| 6 | *(Optional later)* add semantic search if needed | `vectorize_memory` |

---

# 🛠️ Memory Tools Overview

| Tool | Purpose | Benefit |
|------|---------|---------|
| `index_memory` | Create initial `memory.yaml` by scanning key folders | Baseline memory system |
| `add_descriptions_to_memory` | Draft human-readable descriptions and tags | Easier navigation |
| `fetch_memory_item` | Retrieve memory entry by `file_path` or `tags` | Contextual memory lookup |
| `list_memory_by_tag` | List files by tag (e.g., `testplan`, `spec`) | Boost Pod reasoning |
| `validate_memory_links` | Ensure memory.yaml paths exist | Prevent broken links |
| *(Optional)* `vectorize_memory` | Embed descriptions for semantic search | Smarter memory retrieval |

---

# 🧩 Updated Git Repo Layout for AI-Native Delivery Projects

| **Folder** | **Purpose** | **Tag Automatically** |
|------------|-------------|------------------------|
| `/prompts/templates/` | Framework prompts/templates | `framework` |
| `/prompts/used/` | Project-specific prompts (used in tasks) | `project` |
| `/scripts/framework/` | Core framework scripts (e.g., `promote_patch`) | `framework` |
| `/scripts/project/` | Project-specific shell scripts or helpers | `project` |
| `/task_templates/` | Framework task templates only | `framework` |
| `/docs/framework/` | Core system documentation (e.g., delivery model, toolkit docs) | `framework` |
| `/docs/project/` | Project-specific docs (e.g., goals, research spikes) | `project` |
| `/outputs/` | Project deliverables (reports, model results, retrospectives) | `project` |
| `/chatgpt_repo/outputs/` | Raw Pod outputs (before patch promotion) | `project` |
| `/data/` | Project datasets (inputs or outputs) | `project` |
| `/notebooks/` | Project analysis notebooks (e.g., R&D) | `project` |
| `/src/server/`, `/src/client/`, etc. | Future — Source code organization | `project` |
| `/infra/` (optional) | Future — Deployment configs (e.g., Docker, Railway configs) | `framework` |
| `main.py`, `openapi.json` | Core system files (currently at repo root) | `framework` |

---

## ✅ Notes on `main.py` and `openapi.json`

- **Current:** Fine to leave them at the repo root (Railway expects this for builds).
- **Future:** Could move into `/src/server/` if Dockerfile build context and entrypoints are updated.

---

## 🧠 Tagging Strategy for Automation

We'll **automate memory tagging** based on file path patterns:

- If path includes `/prompts/templates/` → tag `framework`
- If path includes `/prompts/used/` → tag `project`
- If path includes `/docs/project/` → tag `project`
- If path includes `/scripts/framework/` → tag `framework`
- *(etc.)*

✨ **Automation-ready memory management!**

---

# 🚀 Memory Management Flow

| **Step** | **Action** |
|----------|------------|
| 1 | Human or Pod runs `memory_diff` |
| 2 | If files missing, Pod suggests metadata |
| 3 | Pod calls `add_to_memory` to patch `memory.yaml` |
| 4 | Human stages updated `memory.yaml` in Git |

✅ Unified memory management  
✅ Supports both framework + project expansion  
✅ Minimal friction for Humans + Pods

---

# 🛠️ Tool Profile: `add_to_memory`

| **Field** | **Value** |
|-----------|-----------|
| **Tool Name** | `add_to_memory` |
| **Route** | `POST /memory/add` |
| **What it does** | Adds one or more files into `memory.yaml` |
| **Inputs** | List of file paths, each with description and tags |
| **Output** | Updated `memory.yaml` structure |
| **Where Used** | After `memory_diff`, during patch promotion, during project file growth |

---

# ✨ New Plan for Memory Management v1

## Tools Update

| Tool | Purpose | Description |
|------|---------|-------------|
| `index_memory` (refactored) | Pull file list from GitHub repo (no Railway dependency) | Scan `prompts/`, `scripts/`, `task_templates/`, `main.py`, `openapi.json` |
| `memory_diff` (new) | Detect missing files between GitHub and `memory.yaml` | Return list of missing files |

---

## What Will Be Delivered

✅ Updated `index_memory` FastAPI route using GitHub proxy API  
✅ New `memory_diff` FastAPI route  
✅ Updated GPT prompts  
✅ OpenAPI schema updates  
✅ Template `task.yaml` entries  
✅ Clear human + Pod update process

---

## ⚙️ How It Will Work

### `index_memory`

- List files in:
  - `prompts/`
  - `scripts/`
  - `task_templates/`
  - `main.py`
  - `openapi.json`
- Refresh `memory.yaml`
- Default descriptions: `"To be updated"`

### `memory_diff`

- Compare GitHub file list with `memory.yaml`
- Return missing files for review
- Bonus: Pod can suggest metadata for missing files!

---

# 🚀 Immediate Next Steps

✅ Build `index_memory`  
✅ Build `add_descriptions_to_memory`

This will:

- Scaffold `memory.yaml`
- Populate meaningful descriptions
- Set up frictionless, human-friendly memory management
