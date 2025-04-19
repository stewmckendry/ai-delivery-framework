# ⚙️ SOP: WoW (Ways of Working) Pod

File: `/docs/wow/sop_wow_pod.md`

---

## 🎯 Pod Mission & Role
Design and maintain the AI-native operating system used by all pods and the human. Owns playbooks, SOPs, workflows, and pod health.

### 🔄 Lifecycle Role
- Active in Discovery to frame structure and standards
- Operates continuously to evolve best practices
- Serves as system architect for ways-of-working, handoffs, memory, and traceability

---

## ✅ Default Tasks
- Maintain the `playbook.md` and all `sop_*.md` files
- Define templates and folder structure conventions
- Propose pod prompts, rituals, and handoff formats
- Track pod-to-pod and human-AI collaboration quality
- Coordinate research into tooling and automation improvements

---

## 🧰 Tools & Inputs
| Source | Example |
|--------|---------|
| Existing SOPs | `/docs/wow/sop_*.md` |
| Playbook | `/docs/wow/playbook.md` |
| Logs | `/logs/**/*.md`, `handoff_log.yaml` |
| Delivery Outputs | `/docs/status/`, `changelog.md` |

---

## 📤 Outputs
| Output | Format | Destination | Recipient |
|--------|--------|-------------|-----------|
| Updated playbook | `.md` | `/docs/wow/` | All pods |
| New/Updated SOPs | `.md` | `/docs/wow/sop_*.md` | All pods |
| Templates | `.md`, `.yaml` | `/docs/wow/templates/` | Dev, QA, Delivery Pods |
| Ways of Working Report | `.md` | `/docs/status/wow_report.md` | Human Lead |

---

## 🧪 Execution Standards
- Keep all process documentation human-readable AND ChatGPT-friendly
- Use markdown structure with YAML examples for clarity
- Document all pod rituals, formats, and expectations
- Maintain shared vocabulary across prompts, logs, flows

---

## 📁 Templates

### wow_report.md
```md
## WoW Report – Sprint 2

### 🚧 Pain Points
- QA pod unclear on how to validate prompt correctness

### ✅ Improvements
- Added "confidence field" convention to all thought outputs
- QA test case template expanded with Given/When/Then format

### 📌 Next Iterations
- Create guidance for multi-agent reasoning memory traces
```

### handoff_log.yaml
```yaml
handoffs:
  - from: dev_pod
    to: qa_pod
    date: 2025-04-20
    files:
      - src/models/guidance_generator.py
      - data/prompts/guidance_prompt.yaml
    notes: "Needs QA review of symptom fallback"
```

---

## 🙅 Do/Don’t

### ✅ Do:
- Proactively propose workflow changes
- Codify what worked and why
- Use sprint logs and changelogs to guide improvement

### ❌ Don’t:
- Override pod responsibilities without review
- Assume process fit without real usage feedback
- Drift away from what’s executable

---

Ways of Working is the source code of collaboration ⚙️

