# 📁 task_templates/phase4_cutover_and_go_live.md

This file contains standardized `task.yaml`, `prompt_template.md`, and `memory.yaml` templates for Phase 4 – Cutover & Go Live.

---

## 🧾 Task 4.1 – Create Cutover Checklist and Plan
```yaml
template: true

tasks:
  4.1_create_cutover_plan:
    description: Define a clear and time-bound cutover checklist and go-live plan, covering key responsibilities and risks
    pod_owner: DeliveryPod
    status: pending
    prompt: prompts/delivery/4.1_create_cutover_plan.txt
    inputs:
      - docs/deployment/deployment_guide.md
    outputs:
      - docs/release/cutover_checklist.md
    feedback_file: .logs/feedback/4.1_create_cutover_plan.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T14:00:00
    updated_at: 2025-04-22T14:00:00
```

### 4.1 Prompt Template
```markdown
🎯 POD MISSION: DeliveryPod – Create Cutover Plan

🧾 TASK YAML:
task_id: 4.1_create_cutover_plan
pod: DeliveryPod
description: Define a clear and time-bound cutover checklist and go-live plan
inputs:
  - docs/deployment/deployment_guide.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Review deployment guide and identify:
   - Final pre-go-live tasks
   - Required validation or smoke tests
   - Responsible roles and fallback actions
2. Organize into a checklist and timeline
3. Include contingencies, rollback plan, and check-in cadence
4. Save to `docs/release/cutover_checklist.md`
```

📁 MEMORY:
```yaml
template: true

deployment_guide:
  - path: docs/deployment/deployment_guide.md
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/deployment/deployment_guide.md
    repo: stewmckendry/ai-delivery-framework
    file_type: markdown
    description: Technical and procedural deployment reference
    tags: [deployment, release]
    pod_owner: DevPod
    created_date: 2025-04-21
    last_updated_by: DevPod
    last_update_date: 2025-04-22
    notes: Basis for final cutover plan
```

---

## 🧾 Task 4.2 – Run Final Smoke Tests in Production
```yaml
template: true

tasks:
  4.2_final_smoke_tests:
    description: Execute critical smoke tests in the production environment to confirm readiness
    pod_owner: QAPod
    status: pending
    prompt: prompts/qa/4.2_final_smoke_tests.txt
    inputs:
      - test/e2e/e2e_test_plan.md
    outputs:
      - test/smoke/smoke_test_results.md
    feedback_file: .logs/feedback/4.2_final_smoke_tests.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T14:00:00
    updated_at: 2025-04-22T14:00:00
```

### 4.2 Prompt Template
```markdown
🎯 POD MISSION: QAPod – Run Final Smoke Tests

🧾 TASK YAML:
task_id: 4.2_final_smoke_tests
pod: QAPod
description: Run lightweight but critical tests in production to validate deployment readiness
inputs:
  - test/e2e/e2e_test_plan.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Select 5–10 representative test cases
2. Execute manually in the production environment
3. Log each:
   - Test ID
   - Scenario
   - Status
   - Result or error
4. Save results to `test/smoke/smoke_test_results.md`
```

📁 MEMORY:
```yaml
smoke_test_plan:
  - path: test/e2e/e2e_test_plan.md
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/test/e2e/e2e_test_plan.md
    repo: stewmckendry/ai-delivery-framework
    file_type: markdown
    description: List of end-to-end test scenarios used to select smoke tests
    tags: [qa, smoke, prod_tests]
    pod_owner: QAPod
    created_date: 2025-04-22
    last_updated_by: QAPod
    last_update_date: 2025-04-22
    notes: Used to identify critical flows to validate in prod
```

---

## 🧾 Task 4.3 – Execute Go Live Deployment
```yaml
template: true

tasks:
  4.3_go_live_deployment:
    description: Deploy the application into production following the final approved checklist
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/4.3_go_live_deployment.txt
    inputs:
      - docs/release/cutover_checklist.md
    outputs:
      - .logs/deployments/go_live_log.md
    feedback_file: .logs/feedback/4.3_go_live_deployment.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T14:00:00
    updated_at: 2025-04-22T14:00:00
```

### 4.3 Prompt Template
```markdown
🎯 POD MISSION: DevPod – Execute Go Live

🧾 TASK YAML:
task_id: 4.3_go_live_deployment
pod: DevPod
description: Execute deployment steps into production, following the cutover checklist
inputs:
  - docs/release/cutover_checklist.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Follow cutover sequence exactly as outlined
2. Log command output, issues, and timestamps
3. Save the deployment log to `.logs/deployments/go_live_log.md`
```

📁 MEMORY:
```yaml
cutover_checklist:
  - path: docs/release/cutover_checklist.md
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/release/cutover_checklist.md
    repo: stewmckendry/ai-delivery-framework
    file_type: markdown
    description: Final go-live sequence including rollback and checks
    tags: [cutover, production, deployment]
    pod_owner: DeliveryPod
    created_date: 2025-04-22
    last_updated_by: DeliveryPod
    last_update_date: 2025-04-22
    notes: Executed by DevPod
```

---

## 🧾 Task 4.4 – Communicate Release and Transition Ownership
```yaml
template: true

tasks:
  4.4_announce_go_live:
    description: Notify stakeholders of the successful release, outline changes, next steps, and support transition
    pod_owner: Human
    status: pending
    prompt: prompts/human/4.4_announce_go_live.txt
    inputs:
      - .logs/deployments/go_live_log.md
    outputs:
      - docs/release/release_announcement.md
    feedback_file: .logs/feedback/4.4_announce_go_live.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T14:00:00
    updated_at: 2025-04-22T14:00:00
```

### 4.4 Prompt Template
```markdown
🎯 POD MISSION: Human – Communicate Release

🧾 TASK YAML:
task_id: 4.4_announce_go_live
pod: Human
description: Announce the go-live milestone and transition responsibilities
inputs:
  - .logs/deployments/go_live_log.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Summarize release highlights, new capabilities, and key contributors
2. Clarify who owns what post go-live
3. Save to `docs/release/release_announcement.md`
```

📁 MEMORY:
```yaml
go_live_log:
  - path: .logs/deployments/go_live_log.md
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/.logs/deployments/go_live_log.md
    repo: stewmckendry/ai-delivery-framework
    file_type: markdown
    description: Timestamped log of go-live deployment
    tags: [release, handoff, announcement]
    pod_owner: DevPod
    created_date: 2025-04-22
    last_updated_by: DevPod
    last_update_date: 2025-04-22
    notes: Input for release comms and ownership
```

---

## 🧾 Task 4.5 – Facilitate Go-Live Retro and Stabilization
```yaml
template: true

tasks:
  4.5_go_live_retro:
    description: Facilitate a short retrospective and capture initial stabilization issues or learnings
    pod_owner: WoWPod
    status: pending
    prompt: prompts/wow/4.5_go_live_retro.txt
    inputs:
      - .logs/deployments/go_live_log.md
    outputs:
      - docs/rituals/go_live_retro.md
    feedback_file: .logs/feedback/4.5_go_live_retro.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T14:00:00
    updated_at: 2025-04-22T14:00:00
```

### 4.5 Prompt Template
```markdown
🎯 POD MISSION: WoWPod – Facilitate Go-Live Retro

🧾 TASK YAML:
task_id: 4.5_go_live_retro
pod: WoWPod
description: Host a go-live retro and document stabilization feedback
inputs:
  - .logs/deployments/go_live_log.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Review key moments, blockers, wins from go live
2. Capture notes and mitigation ideas
3. Save output to `docs/rituals/go_live_retro.md`
```

📁 MEMORY:
```yaml
go_live_log:
  - path: .logs/deployments/go_live_log.md
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/.logs/deployments/go_live_log.md
    repo: stewmckendry/ai-delivery-framework
    file_type: markdown
    description: Log of deployment sequence for post-mortem review
    tags: [retrospective, release]
    pod_owner: WoWPod
    created_date: 2025-04-22
    last_updated_by: DevPod
    last_update_date: 2025-04-22
    notes: Used to facilitate go-live retro
```

---

## 🧾 Task 4.6 – Update Deployment and Run Book
```yaml
template: true

tasks:
  4.6_update_runbook:
    description: Update deployment steps, rollback plan, infra configs, and post-release runbook
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/4.6_update_runbook.txt
    inputs:
      - docs/deployment/deployment_guide.md
      - .logs/deployments/go_live_log.md
    outputs:
      - docs/deployment/runbook.md
    feedback_file: .logs/feedback/4.6_update_runbook.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T14:00:00
    updated_at: 2025-04-22T14:00:00
```

### 4.6 Prompt Template
```markdown
🎯 POD MISSION: DevPod – Update Run Book

🧾 TASK YAML:
task_id: 4.6_update_runbook
pod: DevPod
description: Update deployment steps and add a runbook for post-release operations
inputs:
  - docs/deployment/deployment_guide.md
  - .logs/deployments/go_live_log.md

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch both inputs.

1. Add or revise:
   - Step-by-step deploy commands
   - Infra and config checklists
   - Known issues and fallbacks
2. Include: health checks, access paths, logging tips
3. Save to `docs/deployment/runbook.md`
```

📁 MEMORY:
```yaml
runbook_inputs:
  - path: docs/deployment/deployment_guide.md
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/deployment/deployment_guide.md
    repo: stewmckendry/ai-delivery-framework
    file_type: markdown
    description: Deployment procedures and configurations
    tags: [deployment, guide]
    pod_owner: DevPod
    created_date: 2025-04-21
    last_updated_by: DevPod
    last_update_date: 2025-04-22
    notes: Used to update runbook

  - path: .logs/deployments/go_live_log.md
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/.logs/deployments/go_live_log.md
    repo: stewmckendry/ai-delivery-framework
    file_type: markdown
    description: Execution log from production cutover
    tags: [deployment, runbook, logs]
    pod_owner: DevPod
    created_date: 2025-04-22
    last_updated_by: DevPod
    last_update_date: 2025-04-22
    notes: Added to capture live behavior and corrections
```

---

Let me know when you’d like the PoC test pack or stub files for this final phase!

