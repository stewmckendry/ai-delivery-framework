# NHL Playoff Predictor PoC Tooling Issues (April 26, 2025)

## 🧠 Reasoning Trace

### Context:
- Attempted NHL Playoff Predictor PoC launch.
- Encountered multiple tooling friction points across task activation, cloning, and creation.

### Issues Observed:
1. **Task Activation Failure**:  
   - Root cause: bad formatting in `prompts/dev/capture_project_goals.txt`.
2. **Task Metadata Update Failure**:  
   - Root cause: no dynamic metadata update endpoint (HTTP 405).
3. **Clone Task Error**:  
   - Root cause: original prompt broken; internal server error without graceful fallback.
4. **New Task Activation Failure**:  
   - Root cause: no automatic memory reindex after new task create.

### Risks:
- High fragility around prompt format and metadata correctness.
- Manual recreation becomes the only workaround, wasting cycle time.
- Frustrating user experience (especially for time-sensitive PoCs).

### Root Causes (5 Whys):
| Issue | Root Cause |
|:-----|:------------|
| Activation fails | No prompt validation pre-activation |
| Cannot fix metadata | No PATCH or flexible update route |
| Clone fails | Clone expects perfect source state without fallback |
| New task activation fails | No auto-memory refresh after create |

---

## 📝 Handoff Notes

### Scope:
- Capture current state of NHL Playoff Predictor PoC launch friction.
- Propose specific, prioritized tooling improvements.

### Assumptions:
- We *can* improve backend behavior (not hard-coded limitations).
- Short-term fixes (validate + reindex) could dramatically unblock flow.

### Risks:
- Fixes might require minor architectural updates (e.g., memory service behaviors).
- Overfitting error messages could add tech debt if not thoughtfully designed.

### Next Steps:
1. **Prioritize Quick Wins**:
   - Add prompt validation during upload or task creation.
   - Trigger reindex immediately after new task creation.
2. **Mid-Term**:
   - Introduce dynamic task metadata update route.
   - Improve error transparency during clone operations (capture root causes better).
3. **Strategic**:
   - Introduce "Safe Mode" activation: try to auto-repair/skip broken parts if possible.

---

# ✅ Tickets To Track

- [ ] **Prompt Validation on Upload/Create**
- [ ] **Auto Reindex After Task Creation**
- [ ] **Dynamic Metadata Update Endpoint**
- [ ] **Graceful Clone Failure Handling**
- [ ] **Safe Mode Activation (Future Stretch Goal)**

