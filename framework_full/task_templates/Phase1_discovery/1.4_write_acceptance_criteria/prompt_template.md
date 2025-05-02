🎯 POD MISSION: QAPod – Write Acceptance Criteria

🧾 TASK YAML:
task_id: 1.4_write_acceptance_criteria
pod: QAPod
description: Write or refine acceptance criteria based on feature specs and QA matrix
inputs:
  - docs/features/feature_*.md

📁 MEMORY:
- path: docs/features/feature_*.md
  repo: stewmckendry/ai-delivery-framework
- path: docs/qa/acceptance_matrix.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Then:
1. Summarize and refine feature intent and requirements
2. Draft clear acceptance criteria per feature including the following metadata where applicable:

📋 Acceptance Criteria Metadata
- `criteria_id`: Unique ID for the acceptance criterion (e.g., AC-101)
- `feature_id`: ID of the associated feature
- `description`: Clear, concise statement of the condition to be met (e.g., “User can reset password via email”)
- `type`: Type of criterion (e.g., functional, non-functional, UI, performance, accessibility)
- `given_when_then`: Structured BDD-style version (optional but encouraged)
  - `given`: Precondition or setup
  - `when`: Action or trigger
  - `then`: Expected outcome
- `role`: User role this applies to (if relevant)
- `priority`: Criticality of this criterion (e.g., Must have, Should have)
- `testable`: Boolean flag — can it be objectively tested? (yes/no)
- `linked_test_case`: ID or link to manual/automated test (if defined)
- `status`: Current validation status (e.g., Pending, In Review, Passed, Failed)
- `comments`: Notes, clarifications, or open questions
- `created_by`: Author of the criterion
- `created_at`: When the criterion was defined
- `last_updated_by`: Who last modified it
- `last_updated_at`: Timestamp of last update

3. Identify any gaps or vagueness to clarify with the human
4. Update or extend the acceptance matrix and feature spec
