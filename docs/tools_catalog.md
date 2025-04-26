# 📚 AI-Native Delivery Tool Catalog

---

## 🎯 Mission

Build modular, traceable, AI-native systems where humans and AI collaborate through structured, auditable workflows — accelerating end-to-end delivery cycles.

---

## 🛠️ Approach

- GitHub-first memory and task management
- Lightweight, composable API tools
- Promote structured thinking (tasks, memory, outputs, reasoning)
- Frictionless patches → pull requests → scalable AI-native delivery

---

## 🧰 Technology Stack

- **Backend:** FastAPI (Python)
- **Memory + Metadata:** YAML files (task.yaml, memory.yaml)
- **Repo Hosting:** GitHub
- **Containerization/Hosting:** Railway (Docker)
- **Client:** GPT Custom Actions
- **Task Tracking:** Git patches + task.yaml linking

---

# 🧩 Tools Catalog

## 📚 Quick Navigation

- [Fetch Single GitHub File](#-fetch-single-github-file)
- [Fetch Multiple GitHub Files](#-fetch-multiple-github-files)
- [Update Task Metadata](#-update-task-metadata)
- [List All Tasks](#-list-all-tasks)
- [Activate Task](#-activate-task)
- [Clone Existing Task](#-clone-existing-task)
- [Get Task Details](#-get-task-details)
- [Create New Task](#-create-new-task)
- [Promote Patch](#-promote-patch)
- [Index Memory Files](#-index-memory-files)
- [Diff Memory Files](#-diff-memory-files)
- [Add Files to Memory](#-add-files-to-memory)
- [Validate Memory Files](#-validate-memory-files)
- [Search Memory by Keyword](#-search-memory-by-keyword)
- [List Available Actions](#-list-available-actions)

----

## 📦 Fetch Single GitHub File

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Fetch Single GitHub File |
| **Route** | `/repos/{owner}/{repo}/contents/{path}` |
| **What It Does** | Fetch a single GitHub file’s content |
| **Inputs** | `owner`, `repo`, `path` |
| **Outputs** | file content (base64) |
| **Where Used** | Memory updates, Inputs loading |

---

## 📦 Fetch Multiple GitHub Files

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Fetch Multiple GitHub Files |
| **Route** | `/batch-files` |
| **What It Does** | Fetch multiple GitHub files in one call |
| **Inputs** | `owner`, `repo`, `paths list` |
| **Outputs** | files content array |
| **Where Used** | Bulk memory/index tasks |

---

## 📦 Update Task Metadata

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Update Task Metadata |
| **Route** | `/tasks/update-metadata` |
| **What It Does** | Modify fields of a task (status, description, etc.) |
| **Inputs** | `task_id`, fields dict |
| **Outputs** | updated `task.yaml` |
| **Where Used** | Managing backlog |

---

## 📦 List All Tasks

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | List All Tasks |
| **Route** | `/tasks/list` |
| **What It Does** | List tasks with optional filters (status, pod, category) |
| **Inputs** | query params |
| **Outputs** | tasks object |
| **Where Used** | Browsing backlog |

---

## 📦 Activate Task

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Activate Task |
| **Route** | `/tasks/activate` |
| **What It Does** | Start a task: update status, retrieve prompt |
| **Inputs** | `task_id` |
| **Outputs** | task details, prompt |
| **Where Used** | Pod kickoff workflows |

---

## 📦 Clone Existing Task

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Clone Existing Task |
| **Route** | `/tasks/clone` |
| **What It Does** | Clone a task with a new descriptor/variant |
| **Inputs** | `original_task_id`, `descriptor` |
| **Outputs** | new task metadata |
| **Where Used** | Variant tasks, forks |

---

## 📦 Get Task Details

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Get Task Details |
| **Route** | `/tasks/{task_id}` |
| **What It Does** | Fetch full metadata for a single task |
| **Inputs** | `task_id` |
| **Outputs** | metadata |
| **Where Used** | Contextual lookup |

---

## 📦 Create New Task

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Create New Task |
| **Route** | `/tasks/create` |
| **What It Does** | Create a task from scratch |
| **Inputs** | `phase`, `category`, `description`, `pod_owner`, `descriptor` |
| **Outputs** | new task metadata |
| **Where Used** | Growing the backlog |

---

## 📦 Promote Patch

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Promote Patch |
| **Route** | `/patches/promote` |
| **What It Does** | Package outputs, reasoning trace, memory.yaml into a zip |
| **Inputs** | `task_id`, `output_files`, `summary`, `reasoning_trace`, `prompt_path`, `output_folder` |
| **Outputs** | downloadable ZIP |
| **Where Used** | Finalizing Pod work |

---

## 📦 Index Memory Files

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Index Memory Files |
| **Route** | `/memory/index` |
| **What It Does** | Index repo files into memory.yaml (baseline) |
| **Inputs** | `base_paths` |
| **Outputs** | memory index |
| **Where Used** | Setup, periodic sync |

---

## 📦 Diff Memory Files

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Diff Memory Files |
| **Route** | `/memory/diff` |
| **What It Does** | Detect missing files (memory vs GitHub) |
| **Inputs** | `base_paths` |
| **Outputs** | missing files list |
| **Where Used** | Memory hygiene audits |

---

## 📦 Add Files to Memory

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Add Files to Memory |
| **Route** | `/memory/add` |
| **What It Does** | Add or update memory.yaml entries |
| **Inputs** | files array (`file_path`, `description`, `tags`) |
| **Outputs** | updated memory.yaml |
| **Where Used** | After diffs, new outputs, patch promotion |

---

## 📦 Validate Memory Files

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Validate Memory Files |
| **Route** | `/memory/validate-files` |
| **What It Does** | Validate if files exist in memory.yaml and/or GitHub |
| **Inputs** | files list |
| **Outputs** | validation results |
| **Where Used** | Pre-task input checks, health checks |

---

## 📦 Search Memory by Keyword

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | Search Memory by Keyword |
| **Route** | `/memory/search` |
| **What It Does** | Search memory.yaml by keyword (file_path, description, tags) |
| **Inputs** | `keyword` |
| **Outputs** | matches array |
| **Where Used** | Find related files for tasks, reusing context |

---

## 📦 List Available Actions

| **Field** | **Details** |
|-----------|-------------|
| **Tool Name** | List Available Actions |
| **Route** | `/actions/list` |
| **What It Does** | List all tools and capabilities |
| **Inputs** | none |
| **Outputs** | grouped action list |
| **Where Used** | Pod startup discovery, Human overview |


---

# 🔥 Highlights

- **Memory-Driven:** Tasks and Pods operate with structured memory
- **Patchable:** Everything designed to cleanly patch → commit → PR
- **Composable:** APIs can be flexibly orchestrated in any Pod flow
- **Self-Improving:** Memory grows with each output, automatically
- **Cross-Validated:** Memory cross-checks GitHub live
- **Searchable:** Lightweight keyword search over project knowledge
- **Fully Extendable:** Framework supports adding dependency graphs, embeddings, smart retrieval in future phases

---

# 📢 Final Notes

- ✅ **Pods have full autonomy**: list tasks, pick one, fetch context, validate, work, promote patch.
- ✅ **Human Leads maintain control**: approve patches, validate memory integrity.
- ✅ **AI-native workflows**: designed for speed, traceability, and learning by doing.

---

# 🎯 Appendix: API Endpoint Plan 

## GitHub Files
- `/repos/{owner}/{repo}/contents/{path}`
- `/batch-files`

## Tasks
- `/tasks/update-metadata`
- `/tasks/list`
- `/tasks/activate`
- `/tasks/clone`
- `/tasks/{task_id}`
- `/tasks/create`

## Patches
- `/patches/promote`

## Memory
- `/memory/index`
- `/memory/diff`
- `/memory/add`
- `/memory/validate-files`
- `/memory/search`

## Utilities
- `/actions/list`
