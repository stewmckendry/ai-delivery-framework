Test Scenario: Prompt-Tracking Contribution Flow (Task 1.1)

Let’s validate everything using 1.1_capture_project_goals.

🔧 Test Setup
- Task ID: 1.1_capture_project_goals
- Pod: DevPod
- Prompt path: prompts/used/DevPod/1.1_capture_project_goals_prompt.txt
- Repo: ai-delivery-framework
- Files produced: docs/project_goals.md, metadata.json, reasoning_trace.md, prompt_used.txt
- Human lead: You!

✅ Test Steps

1. Prep Prompt Input
Human pastes prompt into ChatGPT and into prompts/used/DevPod/1.1_capture_project_goals_prompt.txt

2. GPT Returns ZIP
Includes:
metadata.json with prompt path
reasoning_trace.md with grounded reflection (see above)
prompt_used.txt (same contents as prompt pasted by human)
docs/project_goals.md

3. Human Downloads and Places ZIP
Save to: chatgpt_repo/outputs/patch_1.1_capture_project_goals_<timestamp>.zip

4. Run Promotion Script
bash scripts/generate_patch_from_output.sh

5. Script Performs:
Unzips files
Stages outputs
Extracts reasoning_trace.md, prompt_used.txt
Saves prompt to: prompts/used/DevPod/1.1_capture_project_goals_prompt.txt
Updates .logs/patches, .logs/changelogs, .logs/reasoning
Marks task done: true
Calls create_pr_from_patch.sh
Script Creates PR
PR body includes:
Output summary
Reasoning summary
Quoted prompt

6. Human Reviews & Merges PR