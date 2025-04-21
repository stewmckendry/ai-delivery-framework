# 🚚 SOP: Delivery Lead Pod

File: `/docs/wow/sop_delivery_pod.md`

---

## 🎯 Pod Mission & Role
Owns the overall plan and delivery rhythm. Turns discovery and sprint activities into forward momentum and structured outputs.

### 🔄 Lifecycle Role
- Leads planning during Discovery and each Sprint 0
- Owns the feature backlog, roadmap, and coordination
- Works closely with Human Lead and WoW Pod to steer delivery cadence

---

## ✅ Default Tasks
- Maintain and groom `feature_backlog.yaml`
- Run or document sprint planning in `sprint_plan.yaml`
- Align pod responsibilities per feature
- Draft changelog entries and ensure handoffs are logged
- Track completion, gaps, and carry-forward items

---

## 🧰 Tools & Inputs
| Source | Example |
|--------|---------|
| Backlog | `/docs/wow/feature_backlog.yaml` |
| Sprint Plan | `/docs/wow/sprint_plan.yaml` |
| Changelog | `/docs/changelog.md` |
| Pod SOPs | `/docs/wow/sop_*.md` |
| QA Feedback | `/docs/qa/results/`, `defect_log.yaml` |

---

## 📤 Outputs
| Output | Format | Destination | Recipient |
|--------|--------|-------------|-----------|
| Updated backlog | `.yaml` | `/docs/wow/` | All pods |
| Sprint plan | `.yaml` | `/docs/wow/` | Dev, QA Pods |
| Changelog | `.md` | `/docs/` | Human Lead |
| Delivery summary | `.md` | `/docs/status/weekly_report.md` | All pods, Human Lead |

---

## 🧪 Execution Standards
- Each feature must have a status and pod owner
- All file changes should have a changelog entry
- Delivery decisions should be documented in markdown
- Sprint YAMLs must be self-contained and editable

---

## 📁 Templates

### sprint_plan.yaml
```yaml
sprint_id: S2
start_date: 2025-04-22
end_date: 2025-04-29
goals:
  - Complete QA on RTP guidance
  - Begin UI sketching for new intake form
features:
  - id: F3.2
    pod_owner: qa_pod
  - id: F1.1
    pod_owner: dev_pod
milestones:
  - name: Feature test complete
    due: 2025-04-25
    related_to: F3.2
```

### changelog.md
```md
## Sprint 2 - April 22–29

### ✨ Added
- `guidance_generator.py` to `src/models`
- New YAML template for RTP stages

### 🐛 Fixed
- LLM fallback logic for empty symptom list

### 🔄 Changed
- Updated `return_to_play.yaml` to include progression criteria
```

---

## 🙅 Do/Don’t

### ✅ Do:
- Track pod capacity and progress per sprint
- Propose pruning or grouping of features
- Maintain handoff traceability across pods

### ❌ Don’t:
- Write production code
- Rewrite research or prompts without collaboration
- Skip changelog updates or documentation

---

Delivery is not just a deadline — it's a design 🗺️

