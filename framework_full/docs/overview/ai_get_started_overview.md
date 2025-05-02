# 🔑 How to Get Started with Your Sandbox Workspace

A step-by-step guide to creating and using your **private AI workspace** — powered by the AI Delivery Framework.

---

## 🟢 Step 1: Start a Chat with Our Custom GPT

1. Visit our [Custom GPT](#) — preloaded with AI Delivery Framework tools.
2. Say something like:  
   > *“Help me start a new app project”*

👉 **Behind the scenes**: GPT will call `/sandbox/init` with `mode: "branch"`.

---

## 🔐 Step 2: Save Your Token and Branch Name

GPT will reply with something like:

> ✅ *Your personal sandbox is `sandbox-golden-otter` in the GitHub repo `nhl-predictor`.*  
> *To return to this workspace later, save this token:*  
> `c2FuZGJveC1nb2xkZW4tb3R0ZXI=`

**Important:** Save this token somewhere safe — it’s how you reconnect to your branch later.

---

## 🧱 Step 3: Scaffold Your Project *(Optional)*

GPT may ask if you want to set up a blank project structure.  
If you say **yes**, it will call `/sandbox/init` again with `mode: "project"` using:

- Your project name  
- A short description  
- The branch from Step 2  

👉 This creates:

- `project/task.yaml` – defines delivery tasks  
- `project/memory.yaml` – indexed files and metadata  
- `outputs/project_init/` – reasoning trace and prompt log  

---

## 🛠️ Step 4: Build with Tools

Now you can use AI-powered tools to:

- ✍️ Edit or create files  
- 🧠 Log reasoning and context  
- ✅ Assign and complete tasks  
- 📦 Export your session trace  
- 🔁 Rollback commits  

All tool calls include your **branch** and **repo** context — so your work stays fully sandboxed.

---

## 🔄 Step 5: Resume Later (Across Chats)

If you return in a new GPT session:

1. Say:  
   > *“I’d like to resume my project”*

2. Paste your saved token.

GPT will **decode** it and reconnect you to your sandbox branch.  
You're now ready to **pick up where you left off** — with your project fully intact.

---

# 🧱 Infrastructure Maturity Plan

## 🎯 Vision

Deliver a **secure**, **scalable**, and **developer-friendly** platform where any user — internal or external — can build, manage, and ship AI-native apps using GPT and GitHub, without compromising on **reliability**, **access control**, or **auditability**.

---

## 🪜 PHASED PLAN

### **Phase 1: Harden Sandbox Architecture** *(Current → Short Term)*

| Capability              | Description                                                        |
|--------------------------|--------------------------------------------------------------------|
| ✅ Branch Isolation      | Users get safe GitHub branches for experimentation                |
| ✅ Token-Based Access    | Resumable sessions via `reuse_token`                              |
| 🟡 Branch Access Limits  | Enforce user access to only their branch (informal now, needs auth later) |
| 🔜 Rate Limiting         | Prevent spammy use or repo overload                               |
| 🔜 Project Limits        | Cap files, commits, or lifetime per user                          |

**Goals:** Secure isolation, durability, undo, and easy re-entry.

---

### **Phase 2: Support Multi-Org Use**

| Capability               | Description                                                       |
|---------------------------|-------------------------------------------------------------------|
| 🔜 Org-Aware Routing       | Enable users to specify `org_slug` or repo pattern               |
| 🔜 Auth-Aware GPT Tools    | Use GitHub App or OAuth tokens per org                          |
| 🔜 Private Repos & Secrets | Store secrets/config securely; isolate tokens by org or project |
| 🔜 Per-Org Logging & Quotas| Metered usage + billing hooks if needed                         |

**Goals:** Let orgs adopt the framework safely — without leakage or conflicts.

---

### **Phase 3: Infrastructure Ops & Observability**

| Capability               | Description                                                       |
|---------------------------|-------------------------------------------------------------------|
| 🔜 Central Admin Console   | View usage, errors, metrics across users/projects                |
| 🔜 Error Reporting         | Detect + auto-rollback broken tasks or failed GPT calls          |
| 🔜 GitHub Webhooks         | Sync external GitHub changes to memory/changelog                 |
| 🔜 Release Pipelines       | Promote sandbox → PR or release via GPT                         |

**Goals:** Enable observability and control at operational scale.

---

### **Phase 4: Ecosystem Integration**

| Capability               | Description                                                       |
|---------------------------|-------------------------------------------------------------------|
| 🔜 Templates Marketplace   | Reusable starter kits (project archetypes, prompt packs)         |
| 🔜 Extension Framework     | Let orgs create custom GPT tools via plugin APIs                |
| 🔜 Versioned Toolchain     | Track tool versions; allow GPT to adapt to schema changes       |
| 🔜 Audit + Compliance Hooks| Log changes for compliance-bound orgs                           |

**Goals:** Expand reach and reuse while meeting compliance needs.

---

## 📌 Next Steps (Short-Term)

| ID     | Task                                        | Owner       | Notes                                      |
|--------|---------------------------------------------|-------------|--------------------------------------------|
| INF-1  | Define user/org identifiers strategy        | ProductPod  | Needed for Phase 2 (e.g., slug or token)   |
| INF-2  | Secure GitHub token handling                | ProductPod  | Switch to GitHub App or rotate PAT safely  |
| INF-3  | Add retry + error guardrails to tool routes | ProductPod  | Improve reliability for GPT failures       |
| INF-4  | Add metrics dashboard per repo/branch       | ProductPod  | First step toward observability            |
| INF-5  | Sketch GitHub PR/merge route from sandbox   | ProductPod  | Needed to support full promote-to-main flow|

---

# 🪜 Infrastructure Maturity Plan

A human-first explanation of how we scale the AI Delivery Framework — from single-user sandboxes to enterprise-ready platforms.

---

## 🪜 PHASE 1: Harden the Sandbox *(Where We Are Now)*

### 🧠 What It Is

This phase ensures **every user has a safe, private space** to work with the AI — without affecting others, losing data, or damaging the core repo.

### 🔧 Key Concepts

- **Branch Isolation**  
  Every user works in their own Git branch (e.g., `sandbox-golden-fox`).  
  _Like giving each person a separate copy of the whiteboard._

- **Token-Based Resume**  
  Each branch has a unique token so users can return to it later.  
  _Think of it as a room key._

- **Audit + Rollback**  
  Every change is logged and reversible.

### 🛠 Why It Matters

It gives people **confidence to experiment** and gives you **peace of mind** that the AI won’t wreck anything.  
_It’s like putting bumpers on a bowling lane._

---

## 🪜 PHASE 2: Multi-Org Readiness

### 🧠 What It Is

Once individuals succeed, the next step is to support **teams and organizations**:

- Each team has its own space  
- Data is isolated  
- Access is scoped to the right people

### 🔧 Key Concepts

- **Org Routing**  
  Let orgs or projects be uniquely identified (`acme-ml`, `beta-lab`)

- **GitHub App Tokens**  
  Replace shared tokens with scoped GitHub App installs — more secure

- **Private Repo Access**  
  Support credentials and token storage per org/project

### 🛠 Why It Matters

Now you can **invite other companies to use the framework** safely.  
_It’s the difference between a public demo and a private beta._

---

## 🪜 PHASE 3: Infrastructure Ops & Monitoring

### 🧠 What It Is

As usage scales, you need to see what’s happening and **respond to issues**.  
_This is your dashboard and control panel._

### 🔧 Key Concepts

- **Admin Console**  
  See which branches, users, or tools are active

- **Error Logging**  
  Be notified when GPT calls fail or commits break

- **GitHub Webhooks**  
  Sync human-made changes back into GPT memory (`memory.yaml`)

### 🛠 Why It Matters

You gain **visibility and control at scale** — to support many teams without flying blind.

---

## 🪜 PHASE 4: Ecosystem and Extensions

### 🧠 What It Is

This transforms the framework into a true **platform** others can build on.

### 🔧 Key Concepts

- **Templates Marketplace**  
  Starter kits for common use cases (e.g., LLM chatbot)

- **Custom Tools API**  
  Let others build and plug in their own GPT tools

- **Versioning**  
  Manage tool updates over time (like packages in NPM)

- **Audit Compliance**  
  Store trace logs for SOC2, GDPR, or internal audits

### 🛠 Why It Matters

It makes the AI Delivery Framework **adaptable and enterprise-ready** — a platform, not just a product.

---


