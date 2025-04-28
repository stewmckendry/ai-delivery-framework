# 🧪 Memory Pod – Batch File Test Pack

This is the second proof-of-concept test for the GitHub File Tool, focusing on the new `POST /batch-files` endpoint to support multiple file fetches in one tool call.

---

## 🎯 Test Prompt for GPT (Paste into your Custom GPT)

```markdown
🎯 POD MISSION: DevPod – Generate unit tests for concussion agent logic using multiple input files.

🧾 TASK YAML:
```yaml
task_id: F1.2-generate-tests-batch
pod: DevPod
description: Generate unit tests using agent logic and validator
inputs:
  - src/models/agent/concussion_agent.py
  - src/models/agent/concussion_validator.py
```

📁 MEMORY:
```yaml
- path: src/models/agent/concussion_agent.py
  repo: stewmckendry/ai-delivery-framework
- path: src/models/agent/concussion_validator.py
  repo: stewmckendry/ai-delivery-framework
```

📡 TOOL USE:
Use the GitHub File Tool’s `POST /batch-files` endpoint to fetch all inputs in a single call. Return each file’s content.

Then:
1. Analyze both files for testable behaviors
2. Generate a single `test_concussion_logic.py` with unit tests that:
   - Test ConcussionAgent logic
   - Test ConcussionValidator logic
   - Confirm integrated behavior (e.g. parsing → validation)
3. Return the complete test file as a code block
```

---

## 🧾 Supporting Mock Files

📄 `concussion_agent.py`
```python
class ConcussionAgent:
    def __init__(self):
        self.symptoms = []

    def parse_input(self, text):
        if "nausea" in text:
            self.symptoms.append("nausea")
        return self.symptoms
```

📄 `concussion_validator.py`
```python
class ConcussionValidator:
    def __init__(self):
        self.red_flags = ["loss of consciousness", "vomiting"]

    def validate(self, symptoms):
        return any(symptom in self.red_flags for symptom in symptoms)
```

✅ Place these in your repo at:
```
ai-delivery-framework/src/models/agent/concussion_agent.py
ai-delivery-framework/src/models/agent/concussion_validator.py
```

---

## ✅ Expected Output

📄 `test/models/agent/test_concussion_logic.py`
Should include:
- At least 2–3 unit tests for ConcussionAgent
- 1–2 unit tests for ConcussionValidator
- At least 1 test that integrates both classes together

Example test cases:
- `test_parse_input_adds_symptoms()`
- `test_validator_flags_red_flags()`
- `test_agent_validator_integration()`

---

Once successful, this test confirms:
- ✅ Batch file retrieval is working
- ✅ Memory + task system can support multi-file execution
- ✅ DevPods can reason across related modules
