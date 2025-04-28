# 🧪 Memory Pod PoC – Test Pack

This is a self-contained test pack to validate the live integration of:
- Custom GPT (DevPod)
- GitHub File Tool (via Railway)
- Git memory (task.yaml + memory.yaml)

---

## 🧠 Test Prompt
Use this prompt inside your Custom GPT:

```markdown
🎯 POD MISSION: DevPod – Generate unit tests for concussion agent logic

🧾 TASK YAML:
```yaml
task_id: F1.1-generate-tests
pod: DevPod
description: Generate pytest unit tests for ConcussionAgent
inputs:
  - src/models/agent/concussion_agent.py
```

📁 MEMORY:
```yaml
- path: src/models/agent/concussion_agent.py
  repo: stewmckendry/ai-delivery-framework
  raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/src/models/agent/concussion_agent.py
```

🧰 TOOL USE:
Use the GitHub File Tool to fetch the file listed in the input.

Then:
1. Analyze the file structure and top-level methods
2. Generate a `test_concussion_agent.py` file using `pytest`
3. Include one test for each major behavior (e.g., parsing, stage transition)
4. Return it as a code block
```

---

## 🧾 Supporting Files
> Use this mock file for testing – place it at:
```
ai-delivery-framework/src/models/agent/concussion_agent.py
```

```python
# src/models/agent/concussion_agent.py

class ConcussionAgent:
    def __init__(self):
        self.symptoms = []
        self.stage = "initial"

    def parse_input(self, text):
        if "headache" in text:
            self.symptoms.append("headache")
        if "dizzy" in text:
            self.symptoms.append("dizziness")

    def advance_stage(self):
        if self.stage == "initial":
            self.stage = "monitoring"
        elif self.stage == "monitoring":
            self.stage = "cleared"
        return self.stage

    def is_clear(self):
        return self.stage == "cleared"
```

✅ Confirm file is committed and available to the GitHub File Tool
✅ Safe for single-message test (~25 lines)

---

## ✅ Expected Output
- One Python test file:
  `test/models/agent/test_concussion_agent.py`
- Should contain 3–5 test functions
- Should use pytest syntax
- May include helper fixtures or mocks

---

## 📌 Follow-ups
Once this works:
- Add second input to test tool limit
- Enhance proxy with `POST /batch-files`
- Rerun using multi-input `task.yaml`
- Extend to more complex pod tasks (e.g. QAPod, ResearchPod)

Let’s ship this PoC ✅