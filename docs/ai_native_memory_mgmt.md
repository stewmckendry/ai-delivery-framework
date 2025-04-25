# 🧠 memory.yaml Overview

## What Problem Are We Solving?

You’re 100% right:

- ✅ We already have a Git repository holding everything (tasks, outputs, prompts, traces).
- ✅ GPT Pods can fetch individual files if they know the path.
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
- ✅ Future tools can retrieve related work before generating new patches (better context = better outputs)
- ✅ Humans can visualize project assets (e.g., all reasoning traces, all final outputs)
- ✅ It future-proofs scaling to 100s or 1000s of outputs

---

## 🛠️ How Will It Actually Be Used?

| **User**     | **How they use memory.yaml** | **Example** |
|--------------|-------------------------------|-------------|
| GPT Pod      | - Lookup a file needed for current task<br>- Suggest similar past outputs<br>- Improve generation quality | "Before writing test plan, fetch memory items tagged 'testplan'" |
| Human Lead   | - Browse memory easily<br>- Search for "all patches for feature X" or "all research spikes" | "Show me all DevPod outputs from Discovery phase" |
| Scripts / Tools | - Auto-attach links to PRs<br>- Preload pod work sessions with context | Auto-populate "related memory" section when launching a pod |

---

## 🔥 How We Make It Frictionless, Repeatable, Feasible

### 1. Frictionless

- Index automatically via FastAPI (`index_memory`)
- GPT can suggest, but Human approves/augments
- Tools like `add_descriptions_to_memory` can semi-automate enrichment

### 2. Repeatable

- Every project has a `memory.yaml`
- Every Pod knows: "Search `memory.yaml` first."

### 3. Feasible (Today’s Limits)

- GPT can't auto-push to Git
- But GPT can generate `memory.yaml` updates
- Human Lead approves + stages the updates manually with a `promote_patch`
- (Same flow as `task.yaml` patching!)

---

## ✨ In Short

- ✅ Yes, we're building a Git memory map
- ✅ Benefit: scale GPT Pods without brittleness, enable retrieval, improve quality
- ✅ Usage: Pods find past work, humans navigate repo easily
- ✅ Frictionless: index + human-in-loop enrichment, same `promote_patch` flow
- ✅ Feasible: fully doable with today's ChatGPT + Git + human tooling

---

## 🚀 What's Next?

- **Index First:** Build a good starting `memory.yaml`
- **Enrich Next:** Add descriptions and tags
- **Use It:** Retrieval tools (optional: search by tags, related items)

# 🧠 Memory Indexing Strategy

---

## 1. What Are We Indexing — Framework, Project Files, or Both?

✅ **Right now:**  
Your repo is mostly **framework** — the AI-native delivery system itself (e.g., `task.yaml`, `scripts/`, `prompts/`, etc.)

✅ **Later (when we field-test it to deliver an AI app):**  
You’ll generate **project-specific files** (e.g., project goals, specs, code, tests, outputs, logs)

✅ **Final Decision:**

| Type | Indexing Approach |
|------|-------------------|
| Framework files | ✅ Yes, **selectively** (only files Pods may actually need: prompts, templates, core scripts) |
| Project files   | ✅ Yes, **always** — these are the outputs GPT Pods build on |

---

### 🔵 Proposal: Add a Simple Tagging System When Indexing

| Type | Tag | Why |
|------|-----|-----|
| Framework/core asset | `framework` | Helps Pods differentiate reusable system parts |
| Project work product | `project` | Specific to an AI app being delivered |
| Both | Allowed | Some folders may mix initially |

#### Example in `memory.yaml`:

```yaml
memory:
  scripts_generate_patch_from_output_sh:
    file_path: scripts/generate_patch_from_output.sh
    description: "Script to create a patch from a Pod's outputs for Git commits."
    tags: ["framework", "infra", "automation"]

  docs/project_goals.md:
    file_path: docs/project_goals.md
    description: "Goals document for AI app delivery project."
    tags: ["project", "discovery", "spec"]
```

---

## 🕰️ 2. When to Index — At Patch Time?

✅ **YES.**  
Best practice: treat memory management as part of the **patch promotion flow**.

### 🔵 Proposal:

Whenever a Pod finishes a task:

1. They promote their output patch.
2. They also update `memory.yaml` if they created/modified important files.
3. Human Lead stages both together in Git.

✅ Frictionless  
✅ Git-based audit trail  
✅ Human-in-loop review  
✅ Works with today’s ChatGPT capabilities

---

## 🧠 3. Drafting Descriptions — GPT First, Human Refines

✅ **100% agree.**

- GPT will **auto-generate first-pass descriptions and tags** during memory indexing.
- If it’s obvious (e.g., filename includes `goals` or `test_plan`), GPT can guess.
- Otherwise, GPT will write a placeholder: `"To be filled."`

### Human Lead Can:

- Quickly skim + edit.
- Leave it for later (better partial than nothing).

---

## 🛠️ 4. Full Roadmap: Memory Tools + Functions

| Tool | Purpose | Benefit |
|------|---------|---------|
| `index_memory` | Create initial `memory.yaml` by scanning key folders | Baseline memory system for project |
| `add_descriptions_to_memory` | Draft human-readable descriptions and tags | Easier navigation, better recall |
| `fetch_memory_item` | Retrieve memory entry by `file_path` or `tags` | Let Pods find related past work |
| `list_memory_by_tag` | List files by tag (e.g., "testplan", "spec") | Contextual search to boost Pod reasoning |
| `validate_memory_links` | Ensure `memory.yaml` paths exist in repo | Prevent stale/broken references |
| *(optional)* `vectorize_memory` | Embed file descriptions for semantic search | Future upgrade: smarter memory retrieval |

---

## ✨ Crystallized Memory Management Strategy

| Step | Action | Who/What |
|------|--------|----------|
| 1 | Selectively index framework files now, all project files later | `index_memory` tool |
| 2 | Tag entries as `framework`, `project`, or both | During indexing |
| 3 | After each patch, promote updated `memory.yaml` if needed | Human + `promote_patch` |
| 4 | GPT drafts file descriptions, human refines optionally | `add_descriptions_to_memory` tool |
| 5 | Build lightweight retrieval helpers | `fetch_memory_item`, `list_memory_by_tag` |
| 6 | *(Optional later)* add semantic search if needed | `vectorize_memory` |

---

## 🚀 Suggested Immediate Next Move

✅ Start building `index_memory` now (as drafted).  
✅ Then immediately follow with `add_descriptions_to_memory` (GPT drafts).

This will:

- 🧱 Scaffold `memory.yaml`
- ✍️ Begin populating meaningful descriptions
- 👀 Set up human-friendly review
- 🔄 Keep memory tightly in sync with Git without heavy manual work

---

# 🧠 Memory Indexing Strategy

---

## 1. What Are We Indexing — Framework, Project Files, or Both?

✅ **Right now:**  
Your repo is mostly **framework** — the AI-native delivery system itself (e.g., `task.yaml`, `scripts/`, `prompts/`, etc.)

✅ **Later (when we field-test it to deliver an AI app):**  
You’ll generate **project-specific files** (e.g., project goals, specs, code, tests, outputs, logs)

✅ **Final Decision:**

| Type | Indexing Approach |
|------|-------------------|
| Framework files | ✅ Yes, **selectively** (only files Pods may actually need: prompts, templates, core scripts) |
| Project files   | ✅ Yes, **always** — these are the outputs GPT Pods build on |

---

### 🔵 Proposal: Add a Simple Tagging System When Indexing

| Type | Tag | Why |
|------|-----|-----|
| Framework/core asset | `framework` | Helps Pods differentiate reusable system parts |
| Project work product | `project` | Specific to an AI app being delivered |
| Both | Allowed | Some folders may mix initially |

#### Example in `memory.yaml`:

```yaml
memory:
  scripts_generate_patch_from_output_sh:
    file_path: scripts/generate_patch_from_output.sh
    description: "Script to create a patch from a Pod's outputs for Git commits."
    tags: ["framework", "infra", "automation"]

  docs/project_goals.md:
    file_path: docs/project_goals.md
    description: "Goals document for AI app delivery project."
    tags: ["project", "discovery", "spec"]
```

---

## 🕰️ 2. When to Index — At Patch Time?

✅ **YES.**  
Best practice: treat memory management as part of the **patch promotion flow**.

### 🔵 Proposal:

Whenever a Pod finishes a task:

1. They promote their output patch.
2. They also update `memory.yaml` if they created/modified important files.
3. Human Lead stages both together in Git.

✅ Frictionless  
✅ Git-based audit trail  
✅ Human-in-loop review  
✅ Works with today’s ChatGPT capabilities

---

## 🧠 3. Drafting Descriptions — GPT First, Human Refines

✅ **100% agree.**

- GPT will **auto-generate first-pass descriptions and tags** during memory indexing.
- If it’s obvious (e.g., filename includes `goals` or `test_plan`), GPT can guess.
- Otherwise, GPT will write a placeholder: `"To be filled."`

### Human Lead Can:

- Quickly skim + edit.
- Leave it for later (better partial than nothing).

---

## 🛠️ 4. Full Roadmap: Memory Tools + Functions

| Tool | Purpose | Benefit |
|------|---------|---------|
| `index_memory` | Create initial `memory.yaml` by scanning key folders | Baseline memory system for project |
| `add_descriptions_to_memory` | Draft human-readable descriptions and tags | Easier navigation, better recall |
| `fetch_memory_item` | Retrieve memory entry by `file_path` or `tags` | Let Pods find related past work |
| `list_memory_by_tag` | List files by tag (e.g., "testplan", "spec") | Contextual search to boost Pod reasoning |
| `validate_memory_links` | Ensure `memory.yaml` paths exist in repo | Prevent stale/broken references |
| *(optional)* `vectorize_memory` | Embed file descriptions for semantic search | Future upgrade: smarter memory retrieval |

---

## ✨ Crystallized Memory Management Strategy

| Step | Action | Who/What |
|------|--------|----------|
| 1 | Selectively index framework files now, all project files later | `index_memory` tool |
| 2 | Tag entries as `framework`, `project`, or both | During indexing |
| 3 | After each patch, promote updated `memory.yaml` if needed | Human + `promote_patch` |
| 4 | GPT drafts file descriptions, human refines optionally | `add_descriptions_to_memory` tool |
| 5 | Build lightweight retrieval helpers | `fetch_memory_item`, `list_memory_by_tag` |
| 6 | *(Optional later)* add semantic search if needed | `vectorize_memory` |

---

## 🚀 Suggested Immediate Next Move

✅ Start building `index_memory` now (as drafted).  
✅ Then immediately follow with `add_descriptions_to_memory` (GPT drafts).

This will:

- 🧱 Scaffold `memory.yaml`
- ✍️ Begin populating meaningful descriptions
- 👀 Set up human-friendly review
- 🔄 Keep memory tightly in sync with Git without heavy manual work

---

# ✨ New Plan for Memory Management v1

---

## 🛠️ Tools Overview

| Tool | Purpose | Description |
|------|---------|-------------|
| `index_memory` (refactored) | Pull file list directly from GitHub repo (no Railway file dependency) | Will scan `prompts/`, `scripts/`, `task_templates/`, plus `main.py`, `openapi.json` |
| `memory_diff` (new) | Detect missing files between GitHub and `memory.yaml` | Return a list of missing files that can be added |

---

## 📦 What Will Be Delivered in the Batch

✅ Updated `index_memory` FastAPI route using your GitHub proxy API  
✅ New `memory_diff` FastAPI route  
✅ Updated GPT prompt(s) for each tool  
✅ OpenAPI schema updates for both  
✅ Template `task.yaml` entries to track each tool  
✅ Clear process for how Human Lead + Pod will collaborate to update memory

---

## ⚙️ Quick Notes on How It Will Work

### `index_memory`

- Call GitHub proxy to list contents of:
  - `prompts/`
  - `scripts/`
  - `task_templates/`
  - `main.py`
  - `openapi.json`
- Build/refresh `memory.yaml` with these files
- Default description: `"To be updated"`

---

### `memory_diff`

- Fetch same folder/file lists from GitHub
- Compare to `memory.yaml` entries
- Return missing file paths for GPT or Human Lead to review and add

---

### 🎁 Bonus Option

- GPT Pod could **auto-suggest descriptions and tags** for missing files found by `memory_diff`!


---

# Older memory management content

## 🎯 Mission
Enable ChatGPT Pods to dynamically retrieve source-of-truth knowledge directly from a Git repository, instead of relying on manually pasted content or static memory. This empowers:

- 🔍 Context-aware reasoning over live files
- 🧱 Modular knowledge linking via `task.yaml` + `memory.yaml`
- 🧠 AI-native delivery flows grounded in structured source control

## 🚫 Why Raw URLs Didn’t Work
Originally, we tried giving Pods raw GitHub URLs from `memory.yaml`, expecting them to fetch file content on demand. But this failed due to:

- ❌ **ChatGPT’s tools can't reliably fetch multiple raw URLs**
- ❌ `fetch_text_with_context` fails silently for GitHub raw links
- ❌ GPT doesn’t know when/why a fetch fails

This broke the delivery model where `task.yaml` + `memory.yaml` should be enough to execute a Pod's mission.

## ✅ Our Solution: Custom Git Access Tool via OpenAPI
We built a dedicated GitHub File Tool that integrates with Custom GPTs using OpenAPI, powered by:

### 🧠 Tech Stack
- **Custom GPT** with Action support via OpenAPI
- **FastAPI proxy server** hosted on Railway to relay GitHub file requests
- **Bearer-authenticated GitHub API calls**
- **Custom OpenAPI schema** with full metadata and correct validators
- **Schema served directly** from the same domain to pass validation
- **Legal info & logo hosted on GitHub Pages**

## 🔁 How It Works (Step-by-Step)

### Example: DevPod Task
```yaml
task_id: F1.1-generate-tests
pod: DevPod
description: Generate pytest unit tests for ConcussionAgent
inputs:
  - src/models/agent/concussion_agent.py
  - src/models/agent/concussion_validator.py
```

### Pod Execution Flow
1. **task.yaml is given to the pod**
2. **Pod extracts file paths from `inputs`**
3. **Pod matches inputs to `memory.yaml` to get repo + path**
4. **Pod calls GitHub File Tool (via Actions)**:
   ```http
   GET /repos/{owner}/{repo}/contents/{path}
   ```
5. **Tool returns Base64-encoded file content**
6. **Pod decodes + reasons on the code**
7. **Pod outputs test file**

✅ This flow works seamlessly inside ChatGPT with no file uploads or manual copy/paste.

## ⚠️ Risks + Constraints
| Constraint | Risk | Mitigation |
|------------|------|------------|
| OpenAPI schema validation | High | We host both the schema and the API under the same domain (Railway) |
| Token limits on GitHub | Medium | Use read-only tokens with scoped repo access |
| File size & GPT context limit | High | Limit input files per task; instruct pods to fetch selectively |
| Custom GPT memory reset | Medium | Re-feed task + memory on every session |