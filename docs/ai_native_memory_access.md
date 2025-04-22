# 🧠 Memory Pod Git Access - System Design & Implementation Plan

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

## 🛠️ Implementation Plan

### ✅ Phase 1: Build Live Git Access Tool (✔ Done)
- FastAPI proxy to GitHub
- Railway deployment
- Custom schema override
- Custom GPT Action registration

### 🚀 Phase 2: Finish PoC
- Register the DevPod GPT with this tool
- Run full sample task using `task.yaml` + `memory.yaml`
- Measure tool use + output trace

### 🔄 Phase 3: Extend
- Add batch memory fetch
- Add caching
- Extend to other pods (e.g. QAPod, ResearchPod)

---

This markdown file will evolve as we complete the PoC and move into full deployment. Next up: run the DevPod end-to-end using the live GPT and tool. 💪
