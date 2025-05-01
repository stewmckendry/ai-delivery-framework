## 🔧 Patch 6.10 – GitHub API Failsafes + Retry Logic 
**Not implemented yet**

---

### 🎯 Goal

Introduce automatic retries with exponential backoff for critical GitHub API calls to improve robustness, especially under transient network issues or GitHub rate limits.

**Targeted Calls:**
- `get_repo()`
- `repo.get_contents()`
- `repo.update_file()`
- `repo.create_file()`

---

### 🛠 Patch Plan

1. **Define Retry Decorator**  
Create a decorator named `@with_retries` to:
- Retry on common transient errors (e.g., GitHub exceptions, timeouts)
- Use exponential backoff (e.g., 0.5s, 1s, 2s, up to a cap)

2. **Apply to Critical Calls**  
Wrap GitHub-related function calls with `@with_retries`:

@with_retries  
def get_repo(...): ...

3. **Modularize**  
If the retry logic grows complex, extract into:  
`utils/github_retry.py`

4. **Log Failures**  
Log each retry attempt and the final error (if retries fail) for traceability.

---

### ✅ Benefits
- Prevents flakiness due to transient GitHub API errors  
- Enables more resilient automated workflows  
- Simplifies future debugging via consistent retry logs


## 🎯 What Patch 6.10 (Retry Logic) Is Solving

---

### ✅ Problem We're Targeting

Your AI-native delivery system relies heavily on live GitHub API calls through PyGitHub, such as:

- `get_repo(repo_name)`
- `repo.get_contents(path)`
- `repo.create_file(...)`
- `repo.update_file(...)`

These operations can intermittently fail due to:

- **🌐 Network Flakiness:** Especially in cloud environments like Railway or Azure
- **🚦 API Rate Limits:** Triggered by unauthenticated access or high-frequency calls
- **🛠️ 5xx Server Errors:** Temporary issues on GitHub’s end
- **⚔️ Race Conditions:** Arising from concurrent pod operations or auto-indexing

---

### 🧾 Evidence We've Encountered the Problem

You've already observed several symptoms linked to GitHub instability:

- ⚠️ Errors during `/tasks/start` or `get_contents()` (e.g., 500 Internal Server Error)
- 🧪 Patch promotion intermittently fails to fetch or push files
- ⛔ App logs include PyGitHub stack traces from failed repo operations
- 🔄 Manual retry workarounds (e.g., retrying after a delay) are scattered in current code

These indicate a systemic fragility in GitHub interactions.

---

### 💡 Why Retry Logic Is Valuable

- **✅ Resilience:** Prevents task failures from transient API issues
- **🔁 Continuity:** Keeps chained operations from breaking mid-flow (e.g., memory → commit → handoff)
- **🧠 Diagnostics:** Enables structured logs for post-mortem analysis
- **📈 Scalability:** Prepares for increased concurrency in multi-pod deployments

---

## ✅ Best Practice: Wrap GitHub Methods Centrally in a Helper Layer

---

### 🎯 Goal

Replace all raw `repo.get_contents(...)` and similar calls with retry-safe wrappers like:

```python
from utils.github_wrappers import safe_get_contents, safe_update_file

file = safe_get_contents(repo, "project/task.yaml")

---

🔧 Next Step: Create utils/github_wrappers.py
Here’s what it will include:
# utils/github_wrappers.py

from utils.github_retry import with_retries

@with_retries()
def safe_get_contents(repo, path, ref=None):
    return repo.get_contents(path, ref=ref)

@with_retries()
def safe_create_file(repo, path, message, content, branch=None, **kwargs):
    return repo.create_file(path, message, content, branch=branch, **kwargs)

@with_retries()
def safe_update_file(repo, path, message, content, sha, branch=None, **kwargs):
    return repo.update_file(path, message, content, sha, branch=branch, **kwargs)
🧠 Benefits
Clean: Centralized logic, no nested retry wrappers inside endpoints
Consistent: All API calls automatically retry 3x with backoff
Easy to swap or log: You can add metrics, tracing, or error tags inside the wrappers later