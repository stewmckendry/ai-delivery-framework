# 📁 ai-native-poc/github_tool/

## 1. GitHub OpenAPI Tool Spec (openapi.yaml)
openapi: 3.0.1
info:
  title: GitHub File Reader
  version: 1.0.0
paths:
  /repos/{owner}/{repo}/contents/{path}:
    get:
      summary: Get the contents of a file
      operationId: getFileContents
      parameters:
        - name: owner
          in: path
          required: true
          schema:
            type: string
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: path
          in: path
          required: true
          schema:
            type: string
        - name: ref
          in: query
          required: false
          schema:
            type: string
      responses:
        '200':
          description: File content returned
        '404':
          description: File not found


## 2. Tool Manifest (ai-native-github-tool/ai-plugin.json)
{
  "schema_version": "v1",
  "name_for_human": "GitHub File Tool",
  "name_for_model": "github_file_tool",
  "description_for_model": "Fetch file contents from GitHub using repository path.",
  "description_for_human": "Use this tool to read any file from a public or private GitHub repo using its path.",
  "auth": {
    "type": "user_http",
    "authorization_type": "bearer"
  },
  "api": {
    "type": "openapi",
    "url": "https://your-domain.com/github_tool/openapi.yaml"
  },
  "logo_url": "https://your-domain.com/github_tool/logo.png",
  "contact_email": "support@yourdomain.com",
  "legal_info_url": "https://your-domain.com/legal"
}


## 3. Prompt Template for DevPod (devpod_prompt.md)
```
🎯 POD MISSION: DevPod – Generate unit tests for concussion agent

🧾 TASK YAML:
```yaml
task_id: F1.1-test-concussion-agent
pod: DevPod
description: Write pytest unit tests for the core ConcussionAgent logic
inputs:
  - src/models/agent/concussion_agent.py
  - src/models/agent/concussion_validator.py
outputs:
  - test/models/agent/test_concussion_agent.py
priority: high
```

📁 MEMORY ENTRIES:
- path: src/models/agent/concussion_agent.py
  repo: stewmckendry/ai-delivery-framework
  raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/src/models/agent/concussion_agent.py

- path: src/models/agent/concussion_validator.py
  repo: stewmckendry/ai-delivery-framework
  raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/src/models/agent/concussion_validator.py

📂 FILE FETCH:
Use the GitHub File Tool to retrieve the two input files listed above using their paths.
Then analyze the logic and generate high-coverage `pytest` unit tests targeting key methods.

📌 OUTPUT FORMAT:
- One Python file: `test/models/agent/test_concussion_agent.py`
- Include test function names, edge cases, and fixtures if needed
- Use markdown code block for final output
```

---

✅ Ready to proceed with hosting + custom GPT setup next if you'd like. Just confirm your preferred domain or hosting method (GitHub Pages, Vercel, etc).
