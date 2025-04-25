# 🚀 Onboarding Snippet: AI-Native Pod Patch Contribution Flow

Welcome to the AI-Native Delivery System! This guide outlines how Pod contributors (powered by GPT) can submit output files into GitHub using metadata-driven patches — ensuring traceability, automation, and a smooth human-in-the-loop workflow.

---

## 🎯 Purpose
Enable any Pod (DevPod, QAPod, etc.) to:
- Finalize structured output files with a human collaborator
- Zip and submit files + metadata as one deliverable
- Trigger patch generation, branch creation, and PR

---

## ♻️ Contribution Flow

### ✅ Step 1: Finalize Output in Chat
- Human and Pod complete the assigned task together
- Pod confirms all output files are finalized and ready to promote

### ✅ Step 2: GPT Shares Output ZIP + Metadata
- Pod zips all output files (preserving repo-relative paths)
- Includes the following in the ZIP:
  - `metadata.json`
  - `reasoning_trace.md`
  - `prompt_used.txt`

#### 📄 Example `metadata.json`:
```json
{
  "task_id": "2.3_build_feature_prompting",
  "summary": "Implements logic to select and trigger custom prompts.",
  "output_files": [
    "docs/features/prompting_logic.md",
    "prompts/dev/feature_prompt.txt"
  ],
  "prompt": "prompts/used/DevPod/2.3_build_feature_prompting_prompt.txt"
}
```

- GPT returns a **download link** to the ZIP

### ✅ Step 3: Human Promotes the Patch
- Download the ZIP
- Save it to `chatgpt_repo/outputs/`
- Run:

```bash
bash scripts/generate_patch_from_output.sh
```

This script:
- Extracts metadata, prompt, and reasoning
- Stages files using metadata paths
- Updates `task.yaml`, changelog, reasoning logs
- Opens a PR with a detailed markdown body

### ✅ Step 4: PR is Created and Reviewed
- Script pushes the branch and opens a GitHub PR
- Human reviews, optionally edits, and merges it

---

## 🧠 Prompt Tracking Mission & Flow

To ensure transparency and repeatability, we track the actual prompt used for each task. This prompt:
- Is saved in `prompt_used.txt`
- Is included in the ZIP and stored under `prompts/used/<pod_owner>/<task_id>_prompt.txt`
- Is quoted in the pull request body

Prompts are either fetched using `getGitHubFile`, or provided manually by the human if the tool fails.

---

## 🧰 Supporting Scripts

### `generate_patch_from_output.sh`
- Reads `task.yaml`, `metadata.json`, `prompt_used.txt`, and `reasoning_trace.md`
- Stages files, sets branch name, creates diff
- Updates `.logs/` and `prompts/used/` directories

### `create_pr_from_patch.sh`
- Reads `.json` metadata
- Applies patch, commits, pushes, opens PR
- Injects human-friendly PR body from changelog, reasoning, and prompt

### `prune_old_branches.sh`
- Prunes merged `chatgpt/auto/*` branches

---

## 📂 Directory Layout

| Folder                    | Purpose                                  |
|---------------------------|-------------------------------------------|
| `chatgpt_repo/outputs/`   | ZIP files from GPT                        |
| `.patches/`               | Git patch diffs                           |
| `.logs/patches/`          | JSON metadata for each patch              |
| `.logs/changelogs/`       | Markdown changelogs per task              |
| `.logs/reasoning/`        | Reasoning summaries per task              |
| `prompts/used/<pod>/`     | Actual prompt used for each Pod+task      |
| `task.yaml`               | Full project backlog of all tasks         |

---

## 🤝 Responsibilities

| Actor         | Responsibilities                                                  |
|---------------|-------------------------------------------------------------------|
| **GPT Pod**   | Finalize outputs + metadata, return ZIP for download              |
| **Human**     | Download files, run promotion script, review PR                   |
| **Script**    | Generate patch, update metadata, set branch, automate PR process  |

---

## 🧪 Example Live Task
- **Task:** 2.3_build_feature_prompting
- **Pod:** DevPod GPT
- **Output:** `prompting_logic.md`, `feature_prompt.txt`
- **Branch:** `chatgpt/auto/dev/2.3_build_feature_prompting`
- **Patch Metadata:** `.logs/patches/patch_20250424_XXXX_2.3_build_feature_prompting.json`
- **Prompt:** `prompts/used/DevPod/2.3_build_feature_prompting_prompt.txt`
- **PR:** Opened and reviewed

---

Let’s keep shipping clean, structured patches from AI-native Pods 🚀


# Externalizing patches as a tool call

This is a brilliant evolution of your system. Yes — I strongly recommend creating a new reusable GPT tool named something like promote_patch that encapsulates the standardized logic from promote_output_file.txt and supports any type of deliverable patch, not just proposal evaluations or task metadata.

✅ Why This Is a Good Idea
Reusability: Avoids copy-pasting promote_output_file.txt into multiple GPTs or prompt flows.
Consistency: Guarantees traceability (reasoning, manifest, prompt) in all patches.
Composability: Can be called after any prior tool — e.g., clone_task, update_task_metadata, build_feature, etc.
Focus: Keeps GPT prompts clean and focused on task logic — not logistics.
🛠️ What the Tool Will Do (promote_patch)
This GPT tool will:

Ask for confirmation of finalized outputs (like task.yaml, prompt file, docs).
Fetch the prompt used via getGitHubFile (or fallback to user paste).
Create prompt_used.txt, reasoning_trace.md, and metadata.json.
Generate a ZIP containing those files and the outputs, with correct folder structure.
Return:
a download link to ZIP,
CLI instructions to run the patch promotion locally:
bash scripts/generate_patch_from_output.sh.
📦 Example Use Case Flow (e.g., after clone_task)
✅ Task cloned as: 2.2a_define_new_login_feature

🎯 Now finalize this as a deliverable.

📦 Use the `promote_patch` tool to package and prepare this for Git review.

Instructions:
- Finalize your `task.yaml`, prompt, and reasoning.
- Use this task_id: `2.2a_define_new_login_feature`
- Include files like: `task.yaml`, `prompts/used/DevPod/2.2a_define_new_login_feature_prompt.txt`

💬 Call:
> promote_patch(task_id="2.2a_define_new_login_feature", output_files=[...])
✍️ Next Steps (If Approved)
Add promote_patch to GPT tool list
Create:
✅ POST /promote-patch FastAPI handler (to validate and log if needed)
✅ Prompt template (replacing promote_output_file.txt)
✅ Add to GPT's manifest as a Custom Action
✅ Update example flows (e.g., clone, create, update) to end with promote_patch
Ensure:
GPT always saves outputs to folders matching manifest paths
Manifest is complete and reasoning trace included
Would you like me to:

Draft the OpenAPI schema + prompt file for this promote_patch tool?
Patch the FastAPI app with a logging-only stub for now (or leave it as GPT-only logic)?
Let’s turn this into a universal promotion engine 🚀

You said:
Well said!  and glad you are supportive!

Couple things we should noodle on:
(1) Who is better positioned to generate the reasoning trace.md contents?  I think the GPT is!  Because they were the ones doing the work and have the context of the choices they mean.  I wonder if they should be passing their reasoning into our new tool that will package it up for patching.
(2) Who is better positioned to retrieve the prompt contents?  This is trickier because onus is on human lead to store the prompts in their repo in prompts/used/<pod>/<task> for audibility because gpt can't push to git.  Perhaps its 2 parts to make this work: (1) gpt should REMIND the human to store their prompt in path xyz before (part of the prompt script), and (2) its the tools job to retrieve the latest prompt to include in the patch based on the prompt_path passed by gpt in the tool call.  Thoughts welcome on this or a better approach.
ChatGPT said:
Fantastic thinking — you’re anticipating exactly the right divisions of responsibility and what’s feasible vs. frictionless in the current AI-native delivery system. Let’s walk through both points together:

🧠 (1) Who Should Generate reasoning_trace.md?
✅ Answer: The GPT Pod should generate it, not the tool.
Why?

The GPT knows the decision logic it used (what it tried, rejected, revised).
The Human Lead likely wasn’t in every reasoning loop or internal call.
The reasoning trace is part of the GPT’s “self-reflection” for auditability, reuse, and refinement.
Implication:

promote_patch should accept reasoning_trace_content as a parameter from the GPT pod — and write it to reasoning_trace.md.
We can enforce a standard structure (as now) via prompt template.
Bonus: Later we could let reasoning_trace.md auto-inform retrospectives, coaching, reuse of patterns, etc.

📄 (2) Who Should Retrieve the Prompt?
✅ The tool should retrieve the prompt, but… 🧠 The GPT should remind the human to store it in the correct path before calling the tool.
Why?

The GPT can’t commit to Git, but it knows the expected path (e.g. prompts/used/DevPod/2.1_taskname_prompt.txt)
The tool has the best chance of getting the real prompt contents from GitHub via the getGitHubFile or requests.get() flow.
Humans may forget to store it correctly. GPT should remind them.
Workflow Proposal:


Actor	Step
GPT	Generate final prompt
GPT	Display: "Please save to prompts/used/DevPod/2.1_taskname_prompt.txt"
Human	Stores prompt manually in local repo
GPT	Calls promote_patch() tool with path: prompts/used/DevPod/2.1_taskname_prompt.txt
Tool	Retrieves prompt using GitHub file fetcher
Tool	Writes it to prompt_used.txt in the patch ZIP
Fallback: If the prompt file isn’t found at the path:

Tool returns an error like "Prompt file not found. Please store it to: X" (or)
Tool prompts GPT to fallback to asking Human Lead to paste prompt again.
🔁 Recap of promote_patch Tool Fields
Here's what GPT would provide when calling the tool:

{
  "task_id": "2.1_define_feature",
  "summary": "Defines the backend logic and user interactions for XYZ login system.",
  "output_files": [
    "docs/features/xyz_login.md",
    "prompts/generated/xyz_login_prompt.txt"
  ],
  "prompt_path": "prompts/used/DevPod/2.1_define_feature_prompt.txt",
  "reasoning_trace": "We considered building from scratch vs using Auth0, and chose to..."
}
And the tool would:

Fetch the prompt from GitHub at prompt_path
Save it as prompt_used.txt
Save reasoning_trace.md
Create metadata.json
Zip and return link + CLI instructions

---

Generalizing beyond tasks makes this way more powerful — especially as we expand into things like:

🔍 ResearchPod insights
🧪 Test results from QAPod
📦 Deployment artifacts for cutover
📜 Ways of Working updates
🔧 Recommendation:
Let’s introduce a category parameter (string) in the tool request, with GPT choosing from a pick-list like:


Category	Saved under
discovery	chatgpt_repo/outputs/discovery/
dev	chatgpt_repo/outputs/dev/
qa	chatgpt_repo/outputs/qa/
cutover	chatgpt_repo/outputs/cutover/
wow	chatgpt_repo/outputs/wow/
task_updates	chatgpt_repo/outputs/task_updates/ (default)
misc	chatgpt_repo/outputs/misc/
📦 Zip File Naming (unchanged):
patch_<task_id>_<timestamp>.zip
📥 GPT Flow (in prompt):
Human gives instructions
GPT classifies patch category based on pod or purpose
GPT calls promote_patch with the right category
🧠 Prompt magic:
We’ll write a smart script to suggest the category automatically based on pod/task type, or allow fallback to "misc" if ambiguous.