✅ **(1) Tool Catalog — Endpoint and Actions Reference**

| **Endpoint** | **Supported Actions / Modes** | **Description** |
|--------------|-------------------------------|-----------------|
| `/memory/manage` | add, index, diff, validate | File-level memory management |
| `/memory/manage_entry` | update, remove | Edit or remove memory entries |
| `/memory/query` | search, stats, list_entries | Query indexed memory content |
| `/tasks/manage_metadata` | update_metadata, clone | Edit or duplicate tasks |
| `/tasks/lifecycle` | activate, start, complete, reopen, next, scale_out, create | Task state transitions |
| `/tasks/handoff` | append, fetch, generate_auto, execute_auto | Cross-pod coordination |
| `/tasks/chain_of_thought` | append, fetch | Thought capture & reflection |
| `/tasks/reasoning_trace` | fetch, summary | View individual or aggregated reasoning traces |
| `/tasks/query` | list, list_phases, graph, dependencies, get_details | Task structure and navigation |
| `/system/manage_issues` | log, fetch, update_status | Issue tracking and resolution |
| `/system/changelog` | validate, update | Audit and update project changelogs |
| `/system/metrics` | summary, export | Reasoning and delivery metrics |
| `/system/fetch_files` | single, batch | Retrieve one or many files |
| `/system/guide` | — | Provides onboarding guidance |
| `/actions/list` | — | Lists available tools |
| `/project/init_project` | — | Initialize project structure |
| `/tasks/commit_and_log_output` | — | Save final task outputs |
| `/git/rollback_commit` | — | Revert last commit |
| `/tasks/artifacts/{task_id}` | — | Retrieve saved task artifacts |

---

📘 **(2) Onboarding Guide – For Non-Technical Users**

---

🤔 **Why These Tools Matter**  
In traditional apps, you're limited to fixed screens and buttons. With AI tools like this one, you talk to a smart assistant — but that assistant still needs a reliable set of tools to do useful work.  
These tools give the AI “hands and memory.” Without them:
- You’d have to explain everything every time (no memory).
- The AI wouldn’t know how to fetch files or save progress.
- You couldn’t build or ship real apps or documents with help from the AI.

Now, instead of just chatting, your GPT-powered teammates can:
- Browse your files  
- Create and complete tasks  
- Pass off work to others  
- Track issues and metrics  
- Leave thoughtful comments or lessons learned  

It’s like giving your GPT a project dashboard, filing cabinet, and notepad — so you don’t have to explain or redo everything each time.

---

🛠️ **What Can You Do?**

| **Goal** | **Use this Tool** |
|----------|-------------------|
| Start working on a task | `/tasks/lifecycle` → `start` |
| Save your output and progress | `/tasks/commit_and_log_output` |
| Review what you thought or learned | `/tasks/chain_of_thought` |
| Pass your work to another Pod | `/tasks/handoff` |
| Search or update project files | `/memory/query`, `/memory/manage` |
| Report a bug or suggest a fix | `/system/manage_issues` |
| Check how well the AI reasoned | `/system/metrics` |
| Backfill project changelog | `/system/changelog` → `validate` |

---

🧱 **How the System Works**  
Each task, file, and issue is tracked in structured YAML files on GitHub.  
GPTs use these tools to read, write, and log their reasoning — not just chat.  
Every output is traceable, auditable, and saved in version control.

---

🚀 **What’s Coming Next?**

- ✅ Auto-suggestions: GPT recommends next actions or tasks  
- 🧠 Better memory browsing: like a smart index of project ideas  
- 🪪 Roles and permissions: so Pods only see what they need  
- 📊 More visual feedback: like dashboards for progress or performance  
- 📁 Smarter file fetch: retrieve whole sections or prompt-ready summaries  

You’ll be able to get more done, with less explaining, every time.

---

**What can you do with the tools?**  
You’re working with a smart AI delivery system. Each tool helps guide your project from start to finish. Here’s how to think about it:

🧠 **Memory Tools**  
- Add or describe files using `/memory/manage`  
- Update or clean entries using `/memory/manage_entry`  
- Search the project knowledge base using `/memory/query`  

📋 **Task Tools**  
- Create, start, complete, or reopen tasks with `/tasks/lifecycle`  
- View all tasks or dependencies via `/tasks/query`  
- Clone or update tasks via `/tasks/manage_metadata`  

🔁 **Collaboration + Workflow**  
- Use `/tasks/handoff` to pass work between teammates or Pods  
- Log thoughts or lessons with `/tasks/chain_of_thought`  
- Track your thought process with `/tasks/reasoning_trace`  

🔎 **Support & Oversight**  
- Report bugs and ideas using `/system/manage_issues`  
- Check changelogs or backfill missing notes via `/system/changelog`  
- Analyze how well your team (or Pods) reasoned with `/system/metrics`  

📂 **Files and Project Setup**  
- Use `/system/fetch_files` to preview files  
- Start fresh with `/project/init_project`  
- Save results with `/tasks/commit_and_log_output`  

**Start with your goals:**  
- Want to begin a task? Use `lifecycle > start`  
- Need help from another Pod? Use `handoff > append`  
- Curious how reasoning went? Use `reasoning_trace > summary`  

---

🧑‍💻 **(3) Onboarding Guide – For Technical Users**

---

⚙️ **Why These Tools Matter**  
In non-AI systems, developers wire up everything manually — routes, logic, states.  
With plain ChatGPT or Custom GPTs, you're limited to ephemeral, stateless interactions.  
What’s missing?

✅ Tool-based design bridges the gap between freeform LLMs and real-world system integration:
- Tools serve as contracted, versionable APIs to external systems (GitHub, memory, changelogs, metrics)
- Each route is discoverable by GPT, enabling autonomous action via `openapi.json`
- Actions are modular, parameterized, and state-aware (e.g., which task is in progress)

This lets us simulate a real AI-native SDLC, where Pods:
- Write and track tasks
- Share reasoning and artifacts
- Log bugs, changelogs, and system traces
- Evolve based on feedback, metrics, and dependencies

---

🧱 **Technology Stack Overview**

- **FastAPI**: Backend API service with JSON-based OpenAPI routes  
- **GitHub + PyGitHub**: Source of truth for all project artifacts (`task.yaml`, `memory.yaml`, logs, etc.)  
- **Custom GPT + OpenAPI Spec**: Each Pod reads and writes via GPT + tool calls  
- **YAML**: All memory and metadata stored in Git-readable YAML, not databases  
- **In-memory routing**: Tools route requests by `mode` or `action`, enabling flexible consolidation  

**Example:**

```json
POST /tasks/lifecycle
{
  "action": "complete",
  "repo_name": "project-x",
  "task_id": "2.2",
  "outputs": [...],
  "reasoning_trace": {...}
}
```

This consolidates what used to be 7 separate routes into a maintainable, extensible schema.

---

📈 **Future Enhancements (Technical View)**

| **Area**           | **Roadmap Ideas**                                                                 |
|--------------------|------------------------------------------------------------------------------------|
| **Tooling**        | Add dependency-aware auto-call logic, smarter retries, and fuzzy task lookups     |
| **Schema Management** | Dynamic OpenAPI generation based on repo structure                             |
| **Pod Reasoning**  | Fine-tune prompt templates per action for better behavior                         |
| **Testing**        | Auto-generate test suites from schema definitions and example payloads            |
| **Memory/Context** | Integrate vector-based retrieval with YAML index fallback                         |
| **Monitoring**     | Add audit routes for GPT tool call stats, failure types, reasoning metrics        |

---

Each API route serves as a functional tool interface, invoked via Custom GPT or automation. Here’s how they’re structured:

📦 **Unified Tools with Modes**

**Memory:**  
- `POST /memory/manage` with mode:  
  - `"add"` → Add files to memory  
  - `"index"` → Scan and auto-describe new files  
  - `"diff"` → Detect untracked files  
  - `"validate"` → Check memory consistency  
- `POST /memory/manage_entry` with action:  
  - `"update"` → Edit metadata for a file  
  - `"remove"` → Delete from memory index  
- `POST /memory/query` with mode:  
  - `"search"` → Search keywords  
  - `"list_entries"` → List all indexed entries  
  - `"stats"` → Show memory gaps or owner summaries  

**Tasks:**  
- `POST /tasks/manage_metadata` with action: `"update_metadata"` or `"clone"`  
- `POST /tasks/lifecycle` with action: `"activate"`, `"start"`, `"complete"`, `"reopen"`, `"next"`, `"scale_out"`, `"create"`  
- `POST /tasks/handoff` with action: `"append"`, `"fetch"`, `"generate_auto"`, `"execute_auto"`  
- `POST /tasks/chain_of_thought` with action: `"append"` or `"fetch"`  
- `POST /tasks/reasoning_trace` with action:  
  - `"fetch"` (with optional `full: true`)  
  - `"summary"` (aggregated CSV/JSON via `format`)  
- `POST /tasks/query` with mode:  
  - `"list"`, `"list_phases"`, `"graph"`, `"dependencies"`, `"get_details"`  

**System:**  
- `POST /system/manage_issues` with action: `"log"`, `"fetch"`, `"update_status"`  
- `POST /system/changelog` with action:  
  - `"validate"` → Check for missing entries  
  - `"update"` → Append new entry  
- `POST /system/metrics` with mode: `"summary"` or `"export"` (with `format: csv|json`)  
- `POST /system/fetch_files` with mode: `"single"` or `"batch"`  




