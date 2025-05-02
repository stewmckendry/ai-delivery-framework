# 📁 task_templates/discovery/1.2_to_1.4_batch

This file contains standardized task templates for Discovery Phase tasks 1.2 to 1.4 based on the AI-native operating system.

---

## 🧾 Task 1.2 – Define User Flows & Delivery Flows
```yaml
template: true

tasks:
  1.2_define_user_and_delivery_flows:
    description: Define and capture user flows (personas, journeys) and delivery flows (SDLC, pods)
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/define_user_and_delivery_flows.txt
    inputs:
      - docs/personas/user_roles.md
      - docs/journeys/app_walkthrough.md
      - docs/workflows/delivery_flow.md
    outputs:
      - docs/personas/user_roles.md
      - docs/journeys/app_walkthrough.md
      - docs/workflows/delivery_flow.md
    feedback_file: .logs/feedback/1.2_define_user_and_delivery_flows.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T10:00:00
    updated_at: 2025-04-22T10:00:00
```

---

## 🧾 Task 1.3 – Break Work into Features or Hypotheses
```yaml
template: true

tasks:
  1.3_break_into_features:
    description: Analyze project scope and break it into features, experiments, or hypotheses
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/break_into_features.txt
    inputs:
      - docs/project_goals.md
      - docs/personas/user_roles.md
      - docs/journeys/app_walkthrough.md
    outputs:
      - docs/features/feature_*.md
    feedback_file: .logs/feedback/1.3_break_into_features.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T10:00:00
    updated_at: 2025-04-22T10:00:00
```

---

## 🧾 Task 1.4 – Write Acceptance Criteria
```yaml
template: true

tasks:
  1.4_write_acceptance_criteria:
    description: Write or refine acceptance criteria based on feature specs and QA matrix
    pod_owner: QAPod
    status: pending
    prompt: prompts/qa/write_acceptance_criteria.txt
    inputs:
      - docs/features/feature_*.md
    outputs:
      - docs/qa/acceptance_matrix.md
      - docs/features/feature_*.md
    feedback_file: .logs/feedback/1.4_write_acceptance_criteria.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T10:00:00
    updated_at: 2025-04-22T10:00:00
```

---

---

## 🧠 memory.yaml (templates)

```yaml
template: true

user_roles:
    - path: docs/personas/user_roles.md
      repo: stewmckendry/ai-delivery-framework
      raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/personas/user_roles.md
      file_type: markdown
      description: Personas and user roles that interact with the application
      tags: [personas, user_flows]
      pod_owner: DevPod
      created_date: 2025-04-22
      last_updated_by: Human
      last_update_date: 2025-04-22
        notes: Initial persona sketches
app_walkthrough:
      - path: docs/journeys/app_walkthrough.md
        repo: stewmckendry/ai-delivery-framework
        raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/journeys/app_walkthrough.md
        file_type: markdown
        description: End-to-end walkthrough of the app from a user perspective
        tags: [journeys, user_flows]
        pod_owner: DevPod
        created_date: 2025-04-22
        last_updated_by: Human
        last_update_date: 2025-04-22
        notes: App experience draft
delivery_flow:
      - path: docs/workflows/delivery_flow.md
        repo: stewmckendry/ai-delivery-framework
        raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/workflows/delivery_flow.md
        file_type: markdown
        description: Delivery flow including SDLC phases and pod roles
        tags: [delivery_flow, workflows]
        pod_owner: WoWPod
        created_date: 2025-04-22
        last_updated_by: Human
        last_update_date: 2025-04-22
        notes: Draft for review based on ai_delivery_operating_system.md
ai_delivery_operating_system:
      - path: docs/ai_delivery_operating_system.md
        repo: stewmckendry/ai-delivery-framework
        raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/ai_delivery_operating_system.md
        file_type: markdown
        description: Canonical SDLC model and pod role definitions
        tags: [delivery_flow, architecture, sdlc]
        pod_owner: WoWPod
        created_date: 2025-04-22
        last_updated_by: Human
        last_update_date: 2025-04-22
        notes: Source of truth for delivery_flow.md
  

1.3_break_into_features:
    memory:
      - path: docs/project_goals.md
        repo: stewmckendry/ai-delivery-framework
        raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/project_goals.md
        file_type: markdown
        description: Describes overall project goals and vision
        tags: [project_goals]
        pod_owner: Human
        created_date: 2025-04-22
        last_updated_by: Human
        last_update_date: 2025-04-22
        notes: Captured at project kickoff

      - path: docs/personas/user_roles.md
        raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/personas/user_roles.md
        file_type: markdown
        description: Personas and user roles that interact with the application
        tags: [personas, user_flows]
        pod_owner: DevPod
        created_date: 2025-04-22
        last_updated_by: Human
        last_update_date: 2025-04-22
        notes: Initial persona sketches

      - path: docs/journeys/app_walkthrough.md
        raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/journeys/app_walkthrough.md
        file_type: markdown
        description: End-to-end walkthrough of the app from a user perspective
        tags: [journeys, user_flows]
        pod_owner: DevPod
        created_date: 2025-04-22
        last_updated_by: Human
        last_update_date: 2025-04-22
        notes: App experience draft

  1.4_write_acceptance_criteria:
    memory:
      - path: docs/features/feature_*.md
        repo: stewmckendry/ai-delivery-framework
        raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/features/feature_sample.md
        file_type: markdown
        description: Feature descriptions, functionality specs, hypotheses
        tags: [features]
        pod_owner: DevPod
        created_date: 2025-04-22
        last_updated_by: Human
        last_update_date: 2025-04-22
        notes: Draft feature specs

      - path: docs/qa/acceptance_matrix.md
        repo: stewmckendry/ai-delivery-framework
        raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/qa/acceptance_matrix.md
        file_type: markdown
        description: Acceptance criteria for key features and flows
        tags: [qa, acceptance_criteria]
        pod_owner: QAPod
        created_date: 2025-04-22
        last_updated_by: Human
        last_update_date: 2025-04-22
        notes: QA framework draft
```

---

## ✨ Prompt Templates (PoC-style)

### Task 1.2 – Define User & Delivery Flows
```markdown
🎯 POD MISSION: DevPod – Define User & Delivery Flows

🧾 TASK YAML:
task_id: 1.2_define_user_and_delivery_flows
pod: DevPod
description: Define and capture user flows (personas, journeys) and delivery flows (SDLC, pods)
inputs:
  - docs/personas/user_roles.md
  - docs/journeys/app_walkthrough.md
  - docs/workflows/delivery_flow.md

📁 MEMORY:
- path: docs/personas/user_roles.md
  repo: stewmckendry/ai-delivery-framework
- path: docs/journeys/app_walkthrough.md
  repo: stewmckendry/ai-delivery-framework
- path: docs/workflows/delivery_flow.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Then:
1. Summarize and elaborate on user flows and key personas
2. For each user role, describe the following:

👤 User Role Metadata
- `role_id`: Unique ID for the role (e.g., admin, caregiver)
- `role_name`: Human-readable name (e.g., “Coach”, “Athlete”, “Clinician”)
- `description`: Brief overview of who this user is
- `goals`: Key outcomes or needs this user has
- `pain_points`: Frustrations or problems they face today
- `permissions`: What this role can do in the system (create, view, edit, etc.)
- `context`: Where and how this user interacts with the product (mobile, field, desktop)
- `frequency_of_use`: How often they typically use the app (daily, weekly, occasionally)
- `tech_savviness`: Level of comfort with digital tools (e.g., low, medium, high)
- `example_users`: Real-world examples or personas (optional but helpful)
- `created_by`: Who authored the role description
- `created_at`: When it was defined

3. For each user journey, describe the following:

🧭 Application Journey / Walkthrough Metadata
- `journey_id`: Unique ID for the journey (e.g., onboarding_caregiver, report_symptoms)
- `title`: Clear, short name for the journey
- `description`: What the journey covers and its purpose
- `entry_point`: How the user enters the flow (e.g., “Tap ‘Start’ on homepage”)
- `exit_point`: What marks the journey’s completion (e.g., “Receives report summary”)
- `steps`: Ordered list of key steps or screens in the flow
- `roles_involved`: Which user roles experience this journey
- `screens`: Linked screen IDs or mockups per step (if available)
- `goals`: What the user wants to achieve by completing this journey
- `emotional_state`: How the user is likely to feel at each stage (optional, but insightful)
- `success_criteria`: How the product team knows the journey worked as intended
- `error_paths`: Known places where users might drop off or need help
- `version`: If walkthroughs are iterated over time
- `created_by`: Author of the journey
- `created_at`: When it was documented

4. Describe each step in the delivery flow and which pod owns it
5. Identify ambiguities or missing steps to discuss with the human
6. Propose markdown updates for each input file

```

### Task 1.3 – Break Into Features
```markdown
🎯 POD MISSION: DevPod – Break Into Features

🧾 TASK YAML:
task_id: 1.3_break_into_features
pod: DevPod
description: Analyze project scope and break it into features, experiments, or hypotheses
inputs:
  - docs/project_goals.md

📁 MEMORY:
- path: docs/project_goals.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the project goals.

Then:
1. Summarize and refine the project scope into 3–7 features or hypotheses
2. For each proposed feature, provide the following:

📋 Core Metadata
- `feature_id`: Unique identifier
- `title`: Short, descriptive name of the feature
- `description`: What the feature does, user problem it solves
- `status`: Current state (e.g., Draft, In Progress, Done, Blocked)
- `type`: Feature, Enhancement, Bugfix, Tech Debt, Spike
- `priority`: Importance relative to other work (e.g., P0–P3)
- `tags`: Keywords for filtering (e.g., "auth", "mobile", "payments")
- `created_by`: Who added the feature
- `created_at`: Date the feature was logged

🧠 Product & UX Context
- `user_story`: Value from the user's perspective (e.g., “As a user, I want to...”) 
- `personas`: Target user types/personas
- `acceptance_criteria`: Conditions that define “done”
- `mockups`: Link to designs (e.g., Figma, images)
- `journey_stage`: Where this fits in the user journey (e.g., Onboarding, Retention)

🛠 Delivery Context
- 'epic:' Larger initiative or Epic this belongs to
- 'dependencies:' Blocking or related features
- 'estimated_effort:' Story points or t-shirt size (e.g., S, M, L)
- 'tech_owner:' Dev team member responsible
- 'product_owner:' PM or stakeholder lead
- 'repo:' Codebase or directory this touches
- 'test_cases:' Tests to validate behavior
- 'qa_owner:' Responsible for testing
- 'release_target:' Sprint, milestone, or version

✅ Post-Delivery Insights (Optional)
- 'metrics:' KPIs or outcomes to measure success
- 'release_notes:' What was announced or documented externally
- 'retro_notes:' Lessons learned during delivery

3. Identify any ambiguities, unknowns, or decisions to confirm with the human
4. Propose markdown-formatted outputs for `docs/features/feature_*.md`  
```

### Task 1.4 – Write Acceptance Criteria
```markdown
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
Use the GitHub File Tool to retrieve both feature spec(s) and QA matrix.

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
```

Let me know when you want to run one of these or scaffold the next batch.
