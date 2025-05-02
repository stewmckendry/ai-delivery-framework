## ✅ (1) Playback: What You’re Asking For

You're at a pivotal moment with your AI-native delivery framework, aiming to:

- Launch a **"sandbox GPT pod"** for public experimentation.  
- Establish a **secure, reliable infrastructure** that supports others safely building apps.  
- **Avoid rework or overly restrictive controls**, while protecting work from accidental or malicious loss.  
- Introduce **branching/versioning discipline**, especially before others start writing to your repos.

**Your stack includes:**

- A FastAPI server on Railway using a GitHub PAT.  
- Two repos:  
  - `ai-delivery-framework` (framework and tools)  
  - `nhl-predictor` (testbed for outputs)  
- All tools write using `commit_and_log()` and assume access to main branches directly.

---

## 🧠 (2) Strategy Recommendation

A balanced and phased plan to manage **security, collaboration, and resilience** without major overhaul.

### ✅ Phase 1: Quick Wins to Reduce Risk

- Create a `sandbox` branch in `nhl-predictor` for all sandbox GPT pods.  
- Modify `commit_and_log()` to:  
  - Support writing to a named branch (default: `main`)  
  - Include metadata about authoring pod/user  
- Introduce GitHub branch protection on `main`:  
  - Disable force pushes  
  - Require PRs for writes (allow auto-merge for internal tools)  
  - Log all write access with a commit signature (metadata or GPG)

### 🛡️ Phase 2: Securing Multi-user Sandbox Mode

- Provision a "sandbox GPT pod" with scoped access:  
  - Reads from `main`, writes to `sandbox`  
  - Cannot update changelog or memory in production branches  
- Consider **JWT auth** over PAT for per-user/session access  
- Isolate `memory.yaml` / `changelog.yaml` per pod or branch

### 🚨 Phase 3: Protection Against Loss or Mistakes

- Enable GitHub branch-level backups or:  
  - Auto-clone `main` to `backup/{timestamp}` daily  
  - Periodically archive `changelog`/`memory` files  
- Use the existing `rollback_commit` endpoint to recover commits

### ⚙️ Optional Enhancements

- Introduce a `PRBot` tool that:  
  - Suggests diffs for review  
  - Auto-approves sandbox changes under 5 LOC  

---

## 🔧 (3) Implementation Plan + Backlog

### 🔹 Infrastructure & Branching

- Create sandbox branches in both repos  
- Update `commit_and_log()` to support target branch (default: `main`)  
- Create env variable for `DEFAULT_WRITE_BRANCH`

### 🔹 Access Control

- Rotate and restrict GitHub PAT used in server  
- Implement GitHub repo branch protections via API/settings  
- Use Railway secrets to manage sandbox vs production tokens

### 🔹 Sandbox Pod Prep

- Launch `sandbox-gpt-pod` with write access only to `nhl-predictor@sandbox`  
- Disable memory/changelog updates for sandbox pods  
- Track usage/commits for audit logging

### 🔹 Resilience

- Add daily backup cronjob: clone `main` to `backup/YYYY-MM-DD`  
- Create `/system/backup` endpoint to snapshot key files (memory, changelog)  
- Document rollback via `/git/rollback_commit`

---

## ❓ (4) Inputs Needed from You

To make this live, I need:

- ✅ **Confirmation:** Is `sandbox` branch your preferred name?  
- 🔐 **Restrictions:** Should sandbox users be limited to a subset of tools?  
- 📜 **Branches:** Should I update `commit_and_log()` for multi-branch now?  
- 👥 **Pods:** Are you planning multiple sandbox pods or one shared?  
- 🧾 **Metadata:** Any extra metadata you want logged per commit (e.g. user ID)?

---

## ✅ STRATEGY (Refined with Your Inputs)

### 💡 Core Principles

- **Safety First**: Avoid data loss with backups and rollback tools.  
- **User Isolation**: Each sandbox user gets their own branch copy.  
- **Frictionless Experience**: No need for every user to learn Git.  
- **Minimal Refactor**: We upgrade existing tools, not redesign them.  
- **Gradual Rollout**: Begin with a shared GPT pod in a protected sandbox.

---

### 🔑 KEY CONCEPTS FOR YOU

| Concept             | Explanation                                 | Our Plan                                           |
|---------------------|---------------------------------------------|----------------------------------------------------|
| **sandbox branch**  | An isolated playground in your test repo    | Users write here, not `main`                      |
| **Per-user branch** | User X gets `sandbox-alice`, User Y gets `sandbox-bob` | Avoids conflict and enables traceability      |
| **Write isolation** | Tools write to branches with guardrails     | Prevents users from damaging shared code           |
| **commit_and_log() upgrade** | Adds a branch parameter to control target branch | Default is `main`, sandbox uses `sandbox-*` |
| **PAT safety**      | GitHub tokens currently allow full write access | Scope usage, then rotate to per-user/app tokens |
| **GitHub protections** | GitHub lets you protect branches (e.g. require PRs) | Apply to `main`, not `sandbox-*`             |
| **GPT pod sandboxing** | All users share a single GPT pod          | Actions isolated by assigned branch                |

---

## 🛠️ IMPLEMENTATION PLAN

### PHASE 1: Safe Sandbox Launch

#### 🧩 Core Changes
- Create `sandbox` branch in `nhl-predictor`
- Update `commit_and_log()`:
  - Add `branch` parameter (default = `main`)
  - Include commit metadata: `committed_by`, `task_id`
- Update API endpoint + OpenAPI spec to accept `branch` (non-breaking)
- Update GPT custom actions: add optional `branch` param, default to `sandbox` for sandbox pods

#### 🔒 Safety Layers
- Enable branch protections:
  - On `main` for both repos (no direct pushes, optional PR requirement)
  - No protections on `sandbox-*` branches (for now)
- Add `/git/rollback_commit` fallback to UI/tooling

---

### PHASE 2: Per-User Branching + GPT Integration

#### 👤 User Isolation
- Add `user_id` (e.g. `sandbox-alice`) into GPT session context
- Fork `sandbox` branch as `sandbox-{user}` on first use
- Auto-switch tool calls to write to user’s branch

#### 🚥 Traceability
- Log per-commit metadata:
  - `committed_by` (e.g. GPT user ID)
  - `task_id` (if known)
  - Optional: `timestamp`, `GPT version`

#### 🧠 Tool Access Scope
- Assess tool access needs:
  - Minimum: `commit_and_log`, `fetchFiles`, `initProject`, `listActions`
  - Possibly omit: `rollback`, `handoff`, `completeTask` unless needed

---

### PHASE 3: Security & Scale Readiness

#### 🔄 Backups & Recovery
- Nightly snapshot of `main` to `backup/YYYY-MM-DD`
- Export `memory.yaml` and `changelog.yaml` as JSON weekly

#### 🛡️ Token & Auth Hardening
- Replace PAT with a GitHub App (fine-grained permissions)
- Limit write scope to `sandbox-*` branches
- Expire tokens for users after inactivity

#### 🔍 Monitoring
- Audit logs on branch usage, file writes, and errors
- Alert on invalid `memory.yaml` or large write diffs

---

## ✍️ NEXT STEPS

I can now:
- Refactor `commit_and_log()` to support multi-branch  
- Suggest `OpenAPI` + `main.py` edits  
- Draft a spec for user-branch auto-provisioning  

---

## How we'll work together
### 🛠️ Collaboration Process
The way we will work together is:
1. I queue up next steps in the backlog, present the plan, and ask the inputs you need from me
2. I confirm the plan and provide inputs
3. You update plan if needed, and generate the "patch" (which could be code, instructions, etc.)
4. I "execute" the patch, and confirm if issues or done
5. You update the backlog, and we go back to step 1

---

## (1a) ✨ “Try it yourself!” Setup Flow

Once everything is live, the user flow might be:

> *"Try it yourself! Head to [chat.openai.com/gpts](https://chat.openai.com/gpts) and search for **'AI Native Sandbox GPT'** or use this link [insert link]. Once inside, just start chatting — the system will create a safe working branch for you and help you build an AI-native app from scratch."*

No installation or Git knowledge required — the GPT guides each step.

---

## (1b) 🤝 What Users Need from You

**Nothing manual per user.** The GPT pod will:

- Auto-generate a `sandbox-{unique_id}` branch if it doesn’t exist  
- Route all actions to their isolated branch  

**You’ll need to:**

- Publish the GPT to the public via OpenAI  
- Point it to your live FastAPI server + token with branch support  

---

## (1c) 🌱 How Will Users Know What Branch to Use?

They won’t need to — the GPT pod handles it behind the scenes.

**For transparency**, include in responses:
> *“Saving your work to branch: sandbox-celestial-river”*

---

## (2) 🕵️‍♂️ Tracking Without Personal Info

We can generate **anonymous, non-identifiable** `user_id`s like:

- `sandbox-emerald-hawk`  
- `sandbox-crimson-wave`

**Generation methods:**

- Hashed session start time  
- OpenAI conversation ID (if available)  
- Random adjective–noun combinations  

**Logged metadata:**

- `branch`: sandbox-{user}  
- `committed_by`: same  
- `task_id`: optional  
- **No IPs, names, or emails**

---

## (3) Is This for Just Experiment or Full-Use?

**Right now:** Experiment phase — isolated sandbox, no shared state.

**For full adoption**, users/orgs will need:

- Their own repo or fork of the framework  
- GPT pod configuration for their projects  
- Optional self-hosted backends  

**Additional steps:**

- Admin portal for usage/branch monitoring  
- Fine-grained permission controls (read/write scope)  
- OAuth-based GitHub integration  

What we’re building now lays a **reusable foundation for both**.

---

## 🔁 STRATEGY (FINALIZED)

| Phase                  | Goal                             | Actions                                                                 |
|------------------------|----------------------------------|-------------------------------------------------------------------------|
| 1. Sandbox Safe Launch | Protect `main`, enable sandbox   | `commit_and_log()` update, add branch param, GitHub protections         |
| 2. Isolated User Flow  | Each user gets a safe workspace  | Auto-branch creation, GPT branch routing, user-friendly UX              |
| 3. Security & Audit    | Prevent damage, enable rollback  | Nightly backups, rollback endpoint, commit logs                         |
| 4. Scale to Adoption   | Prep for org-level use           | Configurable pods, GitHub App install, repo linking                     |

---

## ✅ IMPLEMENTATION BACKLOG

## ✅ IMPLEMENTATION BACKLOG

| ID   | Task                                              | Owner       | Status | Notes                                                  |
|------|---------------------------------------------------|-------------|--------|--------------------------------------------------------|
| 1.1  | Create sandbox branch in `nhl-predictor`          | Human       | ⬜️     | Base for all user work                                 |
| 1.2  | Update `commit_and_log()` to support branch param | ProductPod  | ⬜️     | Backward-compatible (defaults to `main`)               |
| 1.3  | Update OpenAPI spec to include branch param       | ProductPod  | ⬜️     | Update `/commit_and_log_output`                        |
| 1.4  | Update FastAPI handler to extract branch          | ProductPod  | ⬜️     | Route to `repo.get_branch()`                           |
| 1.5  | Add `committed_by` and `task_id` to writes        | ProductPod  | ⬜️     | Already supported — just standardize                   |
| 1.6  | Apply branch protections to `main`                | Human       | ⬜️     | GitHub settings UI or API                              |
| 2.1  | GPT logic to generate sandbox-{user} IDs          | ProductPod  | ⬜️     | Randomized or session-based                            |
| 2.2  | Auto-create branch from sandbox template          | ProductPod  | ⬜️     | On first write if not exists                           |
| 2.3  | Route tool calls to user branch                   | ProductPod  | ⬜️     | GPT or API preprocessor layer                          |
| 2.4  | Display current branch in GPT replies             | ProductPod  | ⬜️     | Improves transparency                                  |
| 3.1  | Add rollback instructions to docs/tools           | ProductPod  | ⬜️     | Use `/git/rollback_commit`                             |
| 3.2  | Backup script: copy main to `backup/YYYY-MM-DD`   | Human/GPT   | ⬜️     | Optional GitHub Action                                 |
| 4.1  | Document sandbox experience (blog post)           | Human       | ⬜️     | Describe flow and link to GPT                          |
| 4.2  | Define infrastructure plan for full adoption      | ProductPod  | ⬜️     | Includes repo ownership, auth, and deployment models   |

---

## 🧠 RESPONSES TO YOUR QUESTIONS

### ✅ Should All Tools Accept `branch`?

**Yes** — any tool that writes to Git via `commit_and_log()` should accept an optional `branch` parameter, just like `repo_name`.

**Why?**
- Keeps GPT routing logic consistent
- Future-proofs workflows (diffing, patching, rollback)

✅ **Backlog item added:** Update all tool routes to accept `branch`.

---

### 🤔 How Does the GPT Pod Know What Branch to Use?

#### ❌ Option 1: GPT Invents Branch Name

- **Risk:** Name collisions, human error
- GPT must invent a valid, unique name and remember it
- **Not recommended**

#### ✅ Option 2: System Assigns a Unique Sandbox Branch

**Best approach:**
1. GPT starts session by calling a `/sandbox/init_branch` (or `/get_started`) route
2. Server:
   - Checks for a prior branch via session token or ID
   - If not found, generates new branch (e.g. `sandbox-emerald-wolf`)
   - Forks from `sandbox` branch
   - Returns: branch name + repo name + welcome message
3. GPT stores response and uses it in all tool calls:
   ```json
   {
     "repo_name": "nhl-predictor",
     "branch": "sandbox-emerald-wolf"
   }
    ```

---

## ✅ SYSTEM DESIGN: Branch Routing & Safety

✅ **This is safest, traceable, and repeatable.**  
✅ **Backlog item added:** Implement `/sandbox/init_branch` endpoint

---

## ✅ UPDATED IMPLEMENTATION BACKLOG (ADDITIONS)

| ID   | Task                                                | Owner       | Status | Notes                                                    |
|------|-----------------------------------------------------|-------------|--------|----------------------------------------------------------|
| 1.7  | Update all tool routes to accept `branch` param     | ProductPod  | ⬜️     | Mirrors `commit_and_log()` pattern                      |
| 2.5  | Implement `/sandbox/init_branch` endpoint           | ProductPod  | ⬜️     | Creates/fetches user sandbox branch on session start    |

---

## 🛠️ INSTRUCTIONS: Create `sandbox` Branch (Task 1.1)

You can do this via **GitHub UI** or **CLI**:

### 🖥️ Option A: GitHub Web UI

1. Go to the `nhl-predictor` repo.
2. Click the **Branch: main** dropdown.
3. Type `sandbox` in the input box.
4. Click **“Create branch: sandbox from ‘main’”**.

----

## ✅ UPDATED BACKLOG

| ID   | Task                                                      | Owner       | Status | Notes                                                        |
|------|-----------------------------------------------------------|-------------|--------|--------------------------------------------------------------|
| 1.1  | Create `sandbox` branch in `nhl-predictor`                | Human       | ⬜️     | See instructions above                                       |
| 1.2  | Update `commit_and_log()` to support `branch` param       | ProductPod  | ✅     | Backward-compatible                                          |
| 1.3  | Update OpenAPI spec to include `branch` param             | ProductPod  | ✅     | Done in `/commit_and_log_output`                            |
| 1.4  | Update FastAPI handler to extract `branch`                | ProductPod  | ✅     | Applied using `Body(...)`                                   |
| 1.5  | Add `committed_by` and `task_id` to all writes            | ProductPod  | ⬜️     | Already supported, standardize for GPT tools                |
| 1.6  | Apply branch protections to `main`                        | Human       | ⬜️     | Guide needed                                                 |
| 2.1  | Add `/sandbox/init_branch` route                          | ProductPod  | ⬜️     | Assigns unique user branch; returns branch, repo_name, welcome |
| 2.2  | Auto-create branch from `sandbox` if not exists           | ProductPod  | ⬜️     | Reuse GitHub API                                             |
| 2.3  | Route tool calls to user branch (`sandbox-*`)             | ProductPod  | ⬜️     | System-level or GPT memory                                  |
| 2.4  | Display current branch to GPT user                        | ProductPod  | ⬜️     | Shown in reply from `/sandbox/init_branch`                  |
| 2.5  | Refactor all tools to accept `branch` param               | ProductPod  | ⬜️     | Touches all write-enabled tools                             |
| 3.1  | Add rollback instruction to docs or GPT tools             | ProductPod  | ⬜️     | Use `/git/rollback_commit`                                  |
| 3.2  | Implement backup script: clone `main` to `backup/YYYY-MM-DD` | Human or GPT | ⬜️  | GitHub Action or script                                     |
| 4.1  | Document sandbox experience for users (blog post)         | Human       | ⬜️     | Includes GPT flow and link                                  |
| 4.2  | Define infrastructure plan for full adoption              | ProductPod  | ⬜️     | Scalable auth, install flow, repo linking                   |
| 5.1  | Run QA test of multi-branch sandbox                       | QAPod       | ⬜️     | Validate memory/changelog/rollback                          |
| 5.2  | Create how-to guide for branch protections                | ProductPod  | ⬜️     | For step 1.6 GitHub setup                                   |

---

## ✅ DESIGN: `/sandbox/init_branch`

### Goal

Allow a GPT pod to initialize or resume a **safe, unique sandbox branch per user** — without exposing personal information or risking collisions.

---

### 🔄 Request Body
```json
{
  "repo_owner": "YOUR_ORG",
  "repo_name": "nhl-predictor",
  "reuse_token": "aHR0cDovL3NvbWVnaXQ=", // Optional — if set, reuse prior branch
  "force_new": false // Optional — override reuse behavior
}
```
### 🔄 Response Body
```json
{
"branch": "sandbox-emerald-wave",
"reuse_token": "aHR0cDovL3NvbWVnaXQ=", // base64 or HMAC-safe
"repo_name": "nhl-predictor",
"created": true,
"message": "Welcome! Your sandbox is ready in branch sandbox-emerald-wave."
}
```


---

### ⚙️ Logic

- If `reuse_token` is **present and valid**:
  - Decode to get branch name
  - Return it if it still exists  
  - Or recreate from base branch (`sandbox`) if `force_new = false`

- If **no token** or `force_new = true`:
  - Generate a random, collision-checked branch name (e.g. `sandbox-cosmic-eagle`)
  - Create branch from `sandbox`
  - Generate a secure `reuse_token` tied to the branch (e.g. HMAC + salt or encrypted string)

---

### 🔐 Security

- **Reuse token** should not expose branch name in plain text  
- Options:
  - Base64-encoded string with a prefix salt (**fast**)  
  - HMAC(key + branch_name + nonce) (**safer**)  
- System **never trusts or uses branch names** directly from the token  

---

## ✅ BACKLOG UPDATED: Sub-Tasks for 2.1

| ID     | Task                                         | Owner       | Status | Notes                                     |
|--------|----------------------------------------------|-------------|--------|-------------------------------------------|
| 2.1a   | Create `/sandbox/init_branch` endpoint       | ProductPod  | ⬜️     | POST route with `reuse_token`, `force_new` |
| 2.1b   | Generate unique branch names                 | ProductPod  | ⬜️     | Adjective–animal or hash prefix            |
| 2.1c   | Generate and validate secure reuse tokens    | ProductPod  | ⬜️     | Encoded or HMAC token                      |
| 2.1d   | Fallback to create new branch from base      | ProductPod  | ⬜️     | Uses `sandbox` as source                   |

---

## 🧠 WHAT THE USER NEEDS TO REMEMBER

### 🎯 Minimal Info: Just the `reuse_token`

- This token:
  - Encodes their assigned branch (e.g. `sandbox-emerald-wave`)
  - Can be reused across sessions or GPT chats
  - Cannot be easily reverse-engineered to guess other tokens

- 🔐 The **branch name is not required** to resume work — but can be shown for transparency.

---

## 🗣️ WHO TELLS THE USER?

After calling `/sandbox/init_branch`, the **GPT pod** will reply with something like:

> ✅ *Your personal sandbox is ready on branch `sandbox-emerald-wave`.*  
> *To return to this workspace in the future, save this token:*  
> `aHR0cDovL3NvbWVnaXQ=`  
> *(keep this safe — it links back to your work!)*

For added usability (especially outside ChatGPT), consider:

- A **copy-to-clipboard** UI button  
- A **file download** link with the token embedded

---

## ✅ Task 2.2: Auto-create Branch from `sandbox` If Not Exists

This behavior is **already implemented** as part of the `/sandbox/init_branch` route. Task 2.2 is now considered complete.

---

### 🔁 Auto-Branch Creation Logic Recap

Within the `/sandbox/init_branch` logic:

- If `reuse_token` is **missing or invalid**  
- And no valid `sandbox-{...}` branch exists  
- Then:
  - A **random branch name** is generated (e.g. `sandbox-cosmic-fox`)
  - A **new branch is created** from the base `sandbox` branch
  - This new branch is returned to the GPT pod

---

### ✅ Implications

- **No separate setup or patch** is needed for this logic  
- GPT pods can **safely request** a new or reused workspace on every session  

---

## 🧼 Backlog Update

| ID   | Task                                      | Owner       | Status | Notes                                         |
|------|-------------------------------------------|-------------|--------|-----------------------------------------------|
| 2.2  | Auto-create branch from `sandbox` if not exists | ProductPod  | ✅     | Handled in `/sandbox/init_branch`             |

---

## 🎯 Goal

Ensure GPT pods **communicate clearly** which branch the user is working in, so users:

- Understand their sandbox is isolated  
- Can note the branch for future reference  
- Feel confident about their working environment

---

## ✅ Implementation Plan

This task doesn’t require a backend patch — it’s about **standardizing GPT behavior**.

We already return the `branch` in the `/sandbox/init_branch` response. The goal is to ensure:

- GPT **stores** the `branch` and `reuse_token` in memory  
- GPT **echoes** the `branch` in key responses

---

## 💬 Recommendation for GPT Messaging

When GPT receives a response from `/sandbox/init_branch`:

1. **Store**:
   - `branch`
   - `reuse_token`

2. **Reply** to the user with something like:

> ✅ *You're now working in branch `sandbox-crimson-fox` of the `nhl-predictor` repo.*  
> *To resume this later, keep your token:*  
> `c2FuZGJveC1jcmltc29uLWZveA==`

---

## 🧠 Integration Tip

In your GPT instructions or action handlers, encourage the GPT pod to:

- **Remind the user** of their active branch and `repo_name` during key events:
  - First commit
  - Completing a task
  - Displaying a diff or rollback option

- Say something like:

> *“I've saved that file to branch `sandbox-emerald-owl`. Let me know if you'd like to push to main or share your work.”*

---

## 🧠 (2) System Prompt Addition for GPT Pod

### 🔧 Update your GPT system prompt with:

> *You will receive a `repo_name`, `branch`, and `reuse_token` from the `/sandbox/init_branch` tool. Store them all in memory and use them in every tool call. Always tell the user what repo and branch you're working in.*

### 💬 Example Reply:

> *You're now working in the `nhl-predictor` repo on branch `sandbox-emerald-fox`. Save this token to resume later: `c2FuZGJveC1lbWVyYWxkLWZveA==`*

This ensures clear user orientation and reliable reuse of context across sessions.

---

## 🧾 BACKLOG UPDATE

| ID   | Task                                            | Owner  | Status | Notes                                                              |
|------|--------------------------------------------------|--------|--------|--------------------------------------------------------------------|
| 4.3  | Rename `nhl-predictor` repo to a more generic name | Human  | ⬜️     | Suggested: `gpt-sandbox`, `ai-builder-lab`, `gpt-devspace`         |

---

## 🔒 AUTH: Are Users Authenticated by Branch Name?

### Current Behavior

Right now, **having the `branch` + `repo_name`** is sufficient to write to that branch.

✅ **That’s OK for Sandbox Use:**

- Each branch is **randomized and non-discoverable**
- `reuse_token` provides convenience, **not additional security**
- This is effectively a **private link** model — secure by obscurity

---

### For Production

We’ll eventually migrate to stronger models:

- GitHub App installation with per-user access  
- **Token-bound branch validation**  
- Server-side **mapping of tokens → allowed branches**

✅ **Added to long-term security plan** (see backlog Task 4.2)

---

## 🧾 BACKLOG UPDATE

| ID   | Task                                            | Owner      | Status | Notes                                                                 |
|------|--------------------------------------------------|------------|--------|-----------------------------------------------------------------------|
| 4.2  | Define infrastructure plan for full adoption     | ProductPod | ⬜️     | Includes auth model: GitHub App, token-branch binding, repo mapping  |

