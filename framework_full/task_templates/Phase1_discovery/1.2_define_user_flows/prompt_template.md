### Task 1.2 – Define User & Delivery Flows
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
2. For each user role, describe the following where applicable:

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
