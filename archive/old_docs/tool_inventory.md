# 🛠️ Tool Overview: `add_to_memory`

| **Field** | **Value** |
|-----------|-----------|
| **Tool Name** | `add_to_memory` |
| **Route** | `POST /memory/add` |
| **What it does** | Adds one or more files into `memory.yaml` |
| **Inputs** | List of file paths, each with description and tags |
| **Output** | Updated `memory.yaml` structure |
| **Where Used** | After `memory_diff`, during patch promotion, during project file growth |
