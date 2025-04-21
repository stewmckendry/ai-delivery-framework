# 🔍 SOP: Discovery Phase

File: `/docs/wow/sop_discovery_phase.md`

---

## 🎯 Purpose & Goals
The Discovery Phase exists to:
- Frame the user problem and intended outcomes
- Understand constraints (tech, data, timeline)
- Validate feasibility with lightweight research
- Define an initial solution architecture
- Produce sprint-ready artifacts

---

## 🚀 Outputs
| Artifact | Format | Path |
|----------|--------|------|
| Discovery Report | `.md` | `/docs/discovery/discovery_report.md` |
| Research Log | `.md` | `/docs/research/research_log.md` |
| Feature Backlog | `.yaml` | `/docs/wow/feature_backlog.yaml` |
| Solution Architecture | `.md` | `/docs/solution_architecture.md` |
| End-to-End Flow | `.md` | `/docs/end_to_end_flow.md` |
| Data Model | `.yaml` | `/data/model/data_model.yaml` |
| Risk Log | `.md` | `/docs/discovery/risk_log.md` |
| Sprint Plan | `.yaml` | `/docs/wow/sprint_plan.yaml` |

---

## 👥 Active Pods
| Pod | Responsibility |
|-----|----------------|
| Research Pod | Evidence gathering, benchmark scans |
| Delivery Pod | Backlog creation, architecture definition |
| WoW Pod | Templates, structure, logging setup |

---

## 🪜 Transition to Sprint
1. Review discovery artifacts with Human Lead
2. Refine backlog items and assign initial pod owners
3. Create first `sprint_plan.yaml`
4. Update `changelog.md` to note discovery completion
5. Kick off Sprint 0

---

## 📑 Example Template: feature_backlog.yaml
```yaml
features:
  - id: F1.1
    name: Concussion Intake Form
    pod_owner: dev_pod
    status: not_started
    priority: high
    dependencies: []
    description: "Form for capturing user input on possible concussion events."
    discovery_notes: "SCAT6 protocol reference, YAML-driven layout"
```

---

Discovery is your north star 🌟 — don’t skip it.

