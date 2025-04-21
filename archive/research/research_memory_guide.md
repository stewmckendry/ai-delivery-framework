# **memory.yaml** (Starter Index)

```yaml
features:
  - path: docs/features/feature_summary.md  
    tags: [summary, MVP, DevPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md

qa_refs:
  - path: docs/qa/acceptance_matrix.md  
    tags: [acceptance, QAPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
  - path: docs/qa/e2e_test_plan.md  
    tags: [E2E, QAPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md

architecture:
  - path: docs/architecture/solution_overview.md  
    tags: [architecture, DevPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
  - path: docs/architecture/standards.md  
    tags: [standards, ResearchPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md

user_flows: []  # (No user flow files yet)

cutover_plan:
  - path: docs/workflows/cutover_plan.md  
    tags: [release, DeliveryPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md

prompts:
  - path: prompts/dev/implement_feature.txt  
    tags: [DevPod, patch]  
    description: "Prompt for implementing a new feature"  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: txt
  - path: prompts/qa/write_tests.txt  
    tags: [QAPod, test]  
    description: "Prompt for writing test cases for a feature"  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: txt
  - path: prompts/delivery/metrics_summary.txt  
    tags: [DeliveryPod, metrics]  
    description: "Prompt for compiling a metrics summary"  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: txt

research_spikes: []  # (No research spike files yet)

deployment_book:
  - path: docs/release/deployment_book.md  
    tags: [release, DeliveryPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md

run_book:
  - path: docs/release/run_book.md  
    tags: [release, DevPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md

utility_scripts:
  - path: scripts/generate_patch.py  
    tags: [script, patch]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: py

protocols:
  - path: docs/workflows/definition_of_ready.md  
    tags: [protocol, WoWPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
  - path: docs/workflows/definition_of_done.md  
    tags: [protocol, WoWPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md

workflow_automation:
  - path: scripts/link_feedback.py  
    tags: [script, feedback]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: py
  - path: scripts/validate_ready.py  
    tags: [script, DoR]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: py
  - path: scripts/validate_done.py  
    tags: [script, DoD]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: py

system_docs:
  - path: docs/project_goals.md  
    tags: [goals, DevPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
  - path: docs/release/launch_announcement.md  
    tags: [announcement, release]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
  - path: docs/rituals/go_live_retrospective.md  
    tags: [retrospective, WoWPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
  - path: docs/metrics/weekly_summary.md  
    tags: [metrics, DeliveryPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
  - path: docs/metrics/e2e_summary.md  
    tags: [metrics, DeliveryPod]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
  - path: README.md  
    tags: [overview, documentation]  
    related_tasks: []  
    updated_at: 2025-04-21  
    file_type: md
```

# **Maintaining and Automating `memory.yaml` Updates Over Time**

Maintaining an up-to-date `memory.yaml` is crucial for an AI-native delivery system, since this file serves as the index of all key project artifacts (features, documents, scripts, prompts, etc.) along with their context (tags, roles, purpose) ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,and%20knowledge%20references%20with%20tags)). To ensure traceability and consistency as the project evolves, the team should adopt a clear process and automation for updating `memory.yaml` whenever files are added, modified, or deprecated.

## **Proposed Update Process**

1. **Integrate Updates into Definition of Done:** Make updating `memory.yaml` part of the workflow whenever new outputs are created. In fact, a task isn’t fully “Done” until all output files are present *and* `memory.yaml` is updated with references to them ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,done)). This means each time a feature is implemented or a document produced, the corresponding entry should be added or revised in `memory.yaml` before closing the task.

2. **Automate Entry Creation/Modification:** Use a script (e.g. `scripts/update_memory.py`) to append new entries or update existing ones in `memory.yaml` automatically ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,memory.yaml)). This script can be triggered whenever the repository’s content changes:
   - **During Development:** Developers (or AI pods like DevPod) can run `update_memory.py` after creating a new file. The script could scan known directories (e.g. `docs/features/`, `docs/qa/`, `scripts/`, etc.) to find files not yet listed in `memory.yaml` and then prompt for metadata (tags, etc.) or infer some automatically (like file_type from extension).
   - **Pre-Commit Hook:** Set up a Git hook or CI step that runs before changes are merged. It can detect added/removed files and invoke `update_memory.py` to ensure the index reflects those changes. This prevents forgetting to update the memory index during code reviews and merges.
   - **Post-Merge Audit:** As a safety net, a scheduled job or CI workflow can periodically run a **sync** check (using a script like `scripts/sync_task_memory.py`) to compare `task.yaml` outputs and the actual repo files with `memory.yaml` ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,memory.yaml)). Any discrepancy (e.g. a file present in the repo but missing in memory, or vice versa) would alert the team to reconcile it.

3. **Maintain Timestamps and Consistency:** The automation should update the `updated_at` field for a file’s entry whenever the file changes. This could be done by pulling the last commit date of the file from Git or simply using the current date when the script runs. Consistently updating this timestamp helps track when content was last modified. Similarly, if a file is renamed or moved, the script should adjust the `path` and perhaps log the change (either updating in place or marking the old reference as deprecated).

4. **Handle Deletions and Deprecation:** When files are removed or deprecated:
   - Ideally, remove their entries from `memory.yaml` to avoid confusion during retrieval. The update script can flag missing files (present in memory, not in repo) and either auto-remove them or list them for manual review.
   - In cases where historical traceability is needed (e.g. a research spike document that was relevant but later archived), consider moving the entry to an **archive** section in `memory.yaml` or adding a `status: deprecated` tag. This way the AI can be made aware that a file existed but is no longer active, without cluttering active memory.

5. **Human-in-the-Loop Verification:** Although automation will cover most updates, it’s wise to have a quick human review of `memory.yaml` changes. For example, when a new file is added, a team member can verify the chosen tags and description make sense. This aligns with the human oversight inherent in the AI-native process (human providing feedback and approval). Over time, as confidence in the automation grows, this step can be minimal.

By following this process, the project ensures that `memory.yaml` remains a reliable “source of truth” about project artifacts. This reliability is essential for prompt-based agents to retrieve context accurately during development.

## **Automation Scripts and Workflow Integration**

To implement the above process, the team should leverage or build the following automation tools (many of which have been envisioned in the project design):

- **`scripts/update_memory.py`:** As mentioned, this script would add new file entries or update metadata for existing files automatically. It can be run manually by developers or triggered in CI. The design document already suggests such a script to maintain memory entries ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,memory.yaml)).

- **`scripts/sync_task_memory.py`:** A validation script that cross-references `task.yaml` and `memory.yaml` ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,memory.yaml)). For each output listed in a task, it can check that an entry exists in memory. Running this in a CI pipeline (e.g., on pull requests) will enforce the rule that every deliverable is indexed. This upholds the Definition of Done requirement that all outputs are recorded in memory ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,done)).

- **CI Workflow Integration:** Configure a GitHub Actions workflow (or other CI) to run the above scripts on events like push or PR merge. For example:
  - After merges to main, run `sync_task_memory.py` and `validate_done.py` to ensure nothing was missed in the update process. 
  - Optionally, a nightly job could run a broader audit (scanning the file system against memory). However, if hooks on each change are effective, nightly audits might just confirm all is well.

- **Feedback Loop Automation:** Although not directly about `memory.yaml` content, related automation like `scripts/link_feedback.py` can tie into this maintenance. For instance, when feedback logs (.logs/feedback) are linked to tasks, if those feedback files are considered significant knowledge, they could be added to a “feedback” section in memory or annotated in the related task’s context. This ensures even ad-hoc knowledge (like design review notes) is traceable. The key is that all relevant information finds its way into the memory index one way or another, either as a first-class entry or as a related task link.

In summary, automation scripts should handle the heavy lifting of keeping memory in sync, while the development workflow is structured so that updating memory is a natural part of completing any unit of work. By embedding these practices, the team can trust `memory.yaml` to always reflect the current state of the project’s knowledge.

## **Additional Metadata for Enhanced Traceability**

Beyond the required fields (path, tags, related_tasks, dates, file_type), a few additional metadata fields could be introduced in `memory.yaml` to improve traceability and role-awareness in this AI-native model:

- **`owner_pod` or `owner_role`:** An explicit field to denote which pod or role is primarily responsible for the file. For example, `owner_pod: DevPod` for a source code module or `owner_pod: QAPod` for a test plan. This complements the tags by providing a structured way to know who should maintain or use this artifact. It helps an AI agent decide who might need to be consulted for changes (e.g., if a test plan is outdated, it knows QAPod should update it).

- **`description`:** While we included a `description` for prompt files, adding a short description for **all** entries can be valuable. A one-line summary of a document or script’s purpose can help both humans and AI agents quickly grasp the content of the file without opening it. For instance, a feature spec might say `description: "Specifies the concussion symptom tracking feature"`. This is especially useful when retrieving context: the agent can decide relevance from the description before loading the entire file.

- **`created_by` / `updated_by`:** Tracking which agent (human or pod) created or last modified the file could aid accountability and context. For example, `created_by: DevPod (Alice)` or `updated_by: QAPod (2025-04-30)`. In an AI context, if a certain pod consistently updates a file, the system could route future related tasks to that pod. It also helps in understanding the lineage of information (e.g., a research spike answer authored by ResearchPod vs. a user guide written by Human stakeholder).

- **`created_at`:** We already track the last update time, but logging the original creation date could help trace the evolution of artifacts. This is a minor addition (since one could find it via version control history), but having it in memory.yaml makes it accessible to the AI without querying git. It provides temporal context (e.g., a document created early in the project vs. recently might have different relevance).

- **`phase` or `lifecycle_stage`:** Indicate which phase of the delivery process the file is associated with (e.g., Discovery, Development, Testing, Release). While our category sections loosely map to this (for example, **features** and **architecture** are Discovery phase outputs, **cutover_plan** and **run_book** are Release phase), an explicit marker could be useful for the AI to filter artifacts by development stage. For instance, if the AI is working on a Phase 2 task, it might prioritize using artifacts from Discovery and Development phases for context.

- **`status` or `active`:** A field to mark whether a file is current, deprecated, or superseded. For example, `status: deprecated` if we decided to replace a document but keep it for record. This can signal the AI to perhaps ignore or give less weight to deprecated files when searching for information. (In practice, deprecated files might be moved to an archive folder as done here, but a status flag is another way to handle it if we keep them in place.)

- **Linking to External Sources:** In some cases, especially for research spikes or reference documents, we might include a field for external source links or citations (e.g., `source: "Journal XYZ 2024"`). This goes beyond current needs, but would enhance traceability of knowledge origin (useful if the AI needs to validate facts or if humans want to see where information came from).

Implementing these additional fields can improve the **AI’s contextual awareness**. For example, role-awareness fields (like owner_pod) directly inform the AI which expertise area the file represents, and description fields summarize content, potentially allowing the AI to pick the right files more intelligently during Retrieval-Augmented Generation steps.

By combining a robust **automation process** with richer metadata, the `memory.yaml` will remain a living document of the project’s knowledge. This ensures that both developers and AI agents have an up-to-date map of the codebase and documentation at all times, fulfilling the vision of an AI-native delivery operating system where memory, tasks, and code are tightly synchronized ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,and%20knowledge%20references%20with%20tags)) ([ai-concussion-agent/docs/ai_delivery_operating_system.md at main · stewmckendry/ai-concussion-agent · GitHub](https://github.com/stewmckendry/ai-concussion-agent/blob/main/docs/ai_delivery_operating_system.md#:~:text=,done)). Such traceability and organization will make it easier to onboard AI pods to new tasks, run analyses (like coverage of features vs. documentation), and maintain a high-confidence development cadence even as the project grows in complexity. 

