# 🔬 SOP: Research Pod

File: `/docs/wow/sop_research_pod.md`

---

## 🎯 Pod Mission & Role
Collect, synthesize, and structure knowledge relevant to user needs, problem context, AI techniques, and best practices.

### 🔄 Lifecycle Role
- Active in Discovery Phase
- Supports all pods during sprints with focused investigations or source reviews
- Maintains structured knowledge base for reuse

---

## ✅ Default Tasks
- Write research briefs on AI methods, tools, UX/clinical best practices
- Extract structured data from protocols, standards, or references
- Evaluate LLM performance across known benchmarks or heuristics
- Support prompt refinement, scoring frameworks, evaluation metrics

---

## 🧰 Tools & Inputs
| Source | Example |
|--------|---------|
| Research prompts | `/data/prompts/research_queries.yaml` |
| Source docs | `/docs/research_sources/`, `.pdf` uploads |
| Knowledge logs | `/docs/research/research_log.md` |
| Evaluations | `/outputs/eval/`, `/logs/llm_eval/*.md` |

---

## 📤 Outputs
| Output | Format | Destination | Recipient |
|--------|--------|-------------|-----------|
| Research log | `.md` | `/docs/research/research_log.md` | WoW, Delivery Pods |
| Structured YAML data | `.yaml` | `/data/reference/` | Dev Pod, QA Pod |
| Research briefs | `.md` | `/docs/research/briefs/` | All pods |
| Prompt references | `.yaml` | `/data/prompts/` | Dev Pod, QA Pod |

---

## 🧪 Execution Standards
- Use citation format: `Author (Year) - Title`
- Highlight risks, trade-offs, bias, or quality caveats
- Link research logs to feature backlog entries where relevant
- Maintain prompt hygiene (clarity, roles, token-efficient)

---

## 📁 Templates

### research_log.md
```md
## Entry: Return-to-Play Guidelines (F4.1)
- Goal: Extract stages from Canadian RTP PDF
- Sources: Parachute (2019), CDC HEADS UP
- Summary: 6-stage progression with activity descriptions and criteria
- Output file: `/data/protocols/return_to_play.yaml`
- Linked to: `feature_backlog.yaml > F4.1`
```

### research_data.yaml
```yaml
reference: return_to_play
source: parachute_canada
stages:
  - id: stage_1
    name: Symptom-limited activity
    description: "Daily activities that do not provoke symptoms"
    allowed_activities:
      - "Short walks"
      - "Reading"
    progression_criteria:
      - "Symptoms are improving"
```

---

## 🙅 Do/Don’t

### ✅ Do:
- Link every research finding to a feature or decision
- Structure findings in YAML when possible
- Flag when evidence is weak or speculative

### ❌ Don’t:
- Generate prompts without Dev Pod input
- Make final architectural or coding decisions
- Use GPT results without tracing sources

---

Knowledge fuels capability 🔎

