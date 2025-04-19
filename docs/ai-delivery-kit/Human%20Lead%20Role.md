# 🧑‍🚀 Human Lead Role – AI-Native Delivery

This guide defines your role as the **Human Lead** in an AI-native delivery system. You are the mission commander — setting direction, guiding pods, and approving all decisions and code.

---

## 🎯 Mission Summary
You lead fast-moving, AI-powered app projects by combining:
- Human judgment
- AI-generated work from ChatGPT pods
- Version control and traceable delivery

You are:
- 👤 Strategist
- 🧪 Reviewer
- 🧠 Teacher and Editor
- ✅ Final Approver

---

## 🧭 Core Responsibilities

| Area | Description |
|------|-------------|
| Vision | Define what we’re building and why (user need, mission) |
| Flow | Design end-to-end flows and file structures |
| Feedback | Guide pods with clear questions, priorities, and edits |
| Review | Approve or revise proposed pod outputs (patches, YAMLs) |
| GitOps | Merge pull requests and maintain repo structure |
| Traceability | Ensure everything has a changelog, log, or reasoning trace |

---

## 🤝 Interacting with Pods

| Pod | You provide | You get back |
|-----|-------------|--------------|
| `dev_pod` | Backlog item, YAML, flow sketch | Code, templates, new files |
| `qa_pod` | Test plan, feature to test | Test cases, results, coverage gaps |
| `research_pod` | Question or unknown | Reference summaries, structured YAMLs |
| `delivery_pod` | Sprint goals or status | Backlog grooming, changelog updates |
| `wow_pod` | Ritual needs, delivery pain points | SOPs, process upgrades |

Pods are scoped ChatGPT conversations — you guide them with prompts and files. Each pod contributes specific, versioned artifacts.

---

## 🧰 Where You Work & Why

| Tool | Used For |
|------|----------|
| **ChatGPT** | Brainstorming, pod tasks, generating patches, writing YAML/tests |
| **GitHub (Repo UI)** | Reviewing PRs, approving changes, viewing changelogs |
| **VS Code or Terminal** | Optional for manual edits or applying `.diff` files |

---

## ✅ Daily How-To Workflow

### 🔁 When a Pod Proposes a Patch:
1. Open [GitHub Pull Requests tab](https://github.com/stewmckendry/ai-native-delivery/pulls)
2. Review:
   - Code/YAML diffs
   - `changelog.md`
   - `thought_trace.md` (if included)
   - `handoff_log.yaml`
3. Approve or request changes
4. Merge to `main`

### 📦 When Creating a New Feature:
1. Start a ChatGPT pod (e.g. Dev Pod)
2. Provide: feature name, `feature_backlog.yaml` snippet, any inputs
3. Ask for:
   - Code or YAML
   - Patch file (or raw diff)
   - Changelog entry
4. Drop `.diff` in `.patches/` to trigger automation

---

## 🕐 What Does My Day Look Like?

Here’s a typical rhythm for the Human Lead:

1. **Morning Mission Check**
   - Review GitHub for open PRs
   - Merge approved pods’ work
   - Skim changelog and metrics

2. **Pod Kickoff**
   - Start a dev, research, or QA pod for a new task
   - Provide context, inputs, or feedback

3. **Creative Work Block**
   - Draft new features, YAML flows, specs
   - Update playbooks or SOPs

4. **Review + Approve**
   - Validate incoming `.diff` files
   - Confirm outputs make sense
   - Ensure changelog and trace log are included

5. **Daily Wrap**
   - Reflect in `status/` logs or sprint plan
   - Guide the WoW pod to propose system improvements

This role is part strategist, part reviewer, and part collaboration architect — and it evolves as your AI team scales.

---

## 💡 Tips for Leading Effectively
- Always assign pod work in small, focused chunks
- Use `feature_backlog.yaml` as a single source of truth
- Ask pods to explain their thinking — capture in `thought_trace.md`
- Every file change should have a reason and a changelog entry
- Stay in control, but let pods take initiative within bounds

---

## 🔐 You Are the Source of Trust
Your approvals make AI-powered work reliable.
Your judgment makes it purposeful.
Your leadership makes it scale.

Let’s ship like a team of 10 with the clarity of 1. 🚀

