## 🧠 Memory Toolset Inventory

---

### ✅ Existing Tools (FastAPI Routes)

| Route                         | Purpose                                                     |
|------------------------------|-------------------------------------------------------------|
| POST `/memory/index`         | Indexes all files under base paths into `memory.yaml`       |
| POST `/memory/add`           | Adds specific files to memory with enriched metadata        |
| POST `/memory/diff`          | Identifies files present in repo but missing from memory    |
| POST `/memory/validate-files`| Verifies files are present in both repo and memory index    |
| POST `/memory/search`        | Finds memory entries matching a keyword or tag              |

---

### 🔎 Audit Summary

#### ✅ What’s Working Well

- Full lifecycle support: index ➝ validate ➝ diff ➝ enrich ➝ search  
- Custom enrichment: `describe_file_for_memory()` integrates GPT metadata  
- Incremental patching: memory auto-updates on `commit_and_log`

---

### ⚠️ Gaps and Opportunities

#### 🛠 Tooling Gaps

| Gap                                        | Recommendation                                                   |
|-------------------------------------------|-------------------------------------------------------------------|
| No way to delete memory entries           | Add `DELETE /memory/remove` or patch index to detect missing     |
| No way to update metadata manually        | Add `PATCH /memory/update_entry` with fields like tags, owner    |
| No way to list memory entries by filters  | Add `GET /memory/list_entries` with filters (owner, tag, type…)  |

#### 🧠 UX Improvements

| Area             | Suggestion                                                                 |
|------------------|----------------------------------------------------------------------------|
| Diff Tool        | Return as structured table of missing paths; optionally taggable           |
| Search Tool      | Add support for boolean logic (e.g., tag AND phase)                        |
| Indexing         | Already underway: enrich incomplete entries during `/memory/index`         |

#### 🔄 Consistency Gaps

- Some tools assume `memory.yaml` is preloaded; others bypass it  
- No summary view of memory size, entry count, or structure overview  

---

### 🧭 Recommended Enhancements (Prioritized)

| Priority   | Task                                                                 |
|------------|----------------------------------------------------------------------|
| 🔼 High     | Add `DELETE /memory/remove` (by path)                               |
| 🔼 High     | Add `PATCH /memory/update_entry` (description, tags, owner)         |
| 🔼 High     | Finalize `/memory/index` enrichment for incomplete entries          |
| 🟡 Medium   | Add `GET /memory/list_entries` (filterable view of memory contents) |
| 🟡 Medium   | Add `GET /memory/stats` to summarize total entries, types, and gaps |
