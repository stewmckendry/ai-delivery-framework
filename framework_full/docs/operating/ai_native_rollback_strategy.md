## 🎯 Step 6.1.1 – Rollback Strategy Design

### Goal
Define what types of files or commits should be revertible, and how we enable safe, traceable rollback of recent changes — particularly those auto-committed via tools like `commit_and_log`.

---

### ✅ Proposed Rollback Scope

| Type           | Rollback? | Notes                                                  |
|----------------|-----------|--------------------------------------------------------|
| `task.yaml`    | ✅ Yes    | Tasks are updated frequently; high risk of accidental overwrites |
| `memory.yaml`  | ✅ Yes    | Central index — changes should be reversible           |
| `changelog.yaml`| ✅ Yes   | Audit trail itself should be revertible if corrupted   |
| `outputs/*`    | ✅ Yes    | Many are auto-generated; rollback useful if invalid    |
| `prompts/*`    | 🟡 Optional | Rarely updated by tools; may not need rollback         |
| `.logs/*`      | ❌ No     | Should be append-only and trace audit history          |

---

### ✅ Rollback Design Principles

- **Git-native**: Roll back using commit SHA to reset specific files
- **Traceable**: Log every rollback to `.logs/reverted_commits.yaml`
- **Tool-integrated**: Optional `undo_last_commit` flag in tools (e.g. `commit_and_log`)
- **Secure**: Only allow rollbacks within a configured time window or commit count (optional enhancement)

---

### ✅ Coming Next – Step 6.1.2

#### `/git/rollback_commit` Route

| Element      | Description |
|--------------|-------------|
| **Route**    | `POST /git/rollback_commit` |
| **Purpose**  | Reverts the repo to a prior commit for one or more files |
| **Inputs**   | `repo_name`, `commit_sha`, optionally `paths[]`, `reason` |
| **Behavior** | Uses PyGitHub to restore the file(s) to their previous state, logs to `.logs/reverted_commits.yaml` |

---

## 🧠 How Can GPT Retrieve the `commit_sha`?

When enabling rollback functionality, GPT Pods need a way to identify which commit SHA to revert. Here are three viable approaches:

---

### 🔹 Option A: Expose a New Route

Create an API route that lists recent commits, optionally filtered by path:

@app.post("/git/list_commits")
def list_commits(repo_name: str = Body(...), path: Optional[str] = Body(default=None)):
    repo = get_repo(repo_name)
    commits = repo.get_commits(path=path) if path else repo.get_commits()
    return [{
        "sha": c.sha,
        "message": c.commit.message,
        "timestamp": c.commit.author.date.isoformat(),
        "files": [f.filename for f in c.files] if hasattr(c, "files") else []
    } for c in commits[:20]]

- **Use case**: GPT can browse recent commits and pick the one to roll back.
- **Integration**: Add to OpenAPI schema for tool accessibility.

---

### 🔹 Option B: Human Supplies the SHA  [CURRENT STATE]

- **Use case**: Faster to implement; assumes human-in-the-loop can inspect GitHub or `changelog.yaml`.
- **Pro**: Minimal engineering work.
- **Con**: Less autonomous for GPT.

---

### 🔹 Option C: Use `changelog.yaml` or `reverted_commits.yaml`

- **Use case**: Build a helper tool that parses these logs to suggest rollback candidates.
- **Logic**: Filter for recent changes to key files like `task.yaml`, `memory.yaml`, or `outputs/*`.
- **Pro**: Enables GPT to infer rollback targets without GitHub access.

---

### ✅ Recommendation

Start with **Option B** (manual SHA input) for speed, then layer **Option A** to empower GPT with autonomous recovery capabilities. Use **Option C** for intelligent fallback and risk detection.
