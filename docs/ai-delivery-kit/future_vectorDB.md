# Git + Vector DB + Pre-Query Pod Memory Guide

This guide explains how to implement a lightweight **pod memory system** that uses:
- **Git** as the system of record
- **Vector DB** for semantic memory
- **Pre-querying scripts** to fetch relevant past content and pass it to ChatGPT pods as input context

This is the recommended “**soon**” upgrade to your AI-native delivery system.

---

## Overview

### Workflow Summary

1. **Pod outputs** (markdown, logs) are committed to Git
2. **Embedding script** indexes new content into a vector store
3. **Pre-query script** retrieves relevant memory snippets
4. Results are saved to a context file (e.g. `memory/context_snippets.md`)
5. This context file is passed into the next pod’s input

---

## Retrieval Options: File vs. Snippet-Level Memory

You can configure your system to retrieve **entire files** or **precise content snippets**.

### Option 1: Retrieve Entire Files (Coarse-Grained)

#### How it works:
- Each pod output file (e.g., `outputs/20250418/research.md`) is embedded as a single document
- Vector DB returns full documents ranked by semantic similarity

#### Pros:
- Simple to set up and fast to index
- Good when files are short and topically focused

#### Cons:
- May include irrelevant content in results
- Less targeted pod memory

---

### Option 2: Retrieve Snippets Within Files (Fine-Grained)

#### How it works:
- Each file is split into **sections or paragraphs**, and each is embedded individually
- Vector DB returns only the **most relevant chunks**, regardless of file

#### Pros:
- Highly precise memory retrieval
- Reduces context window waste for LLMs
- Ideal for Research and QA pods needing reusable insights

#### Cons:
- Requires splitting logic
- Slightly more complex indexing and metadata handling

---

### Recommendation

| Phase | Use |
|-------|-----|
| **Start** | Use Option 1 to index full pod output files |
| **Enhance** | Move to Option 2 with chunking logic and metadata (e.g., heading, run_id, pod) for better recall |

Use [`langchain.text_splitter`](https://docs.langchain.com/docs/modules/data_connection/document_transformers/text_splitter/) or custom paragraph logic to chunk markdowns cleanly.

---

## Step-by-Step Setup

### 1. Organize Pod Outputs

Ensure pod outputs are saved in a structured format:
```
outputs/
  └── {run_id}/
      ├── dev.md
      ├── qa.md
      ├── research.md
logs/
  └── {run_id}/trace.json
```

Each markdown should include frontmatter metadata:
```markdown
---
pod: research
task: symptom_analysis
run_id: 20250418_research_01
---
Insights:
- Clustered symptoms around vision and balance
```

---

### 2. Set Up the Vector DB

We recommend **Chroma** for quick local use.

#### Install dependencies
```bash
pip install chromadb sentence-transformers
```

#### Basic embedding script (`scripts/embed_and_index.py`) — Option 1
```python
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = "memory/vector_db"
DOCS_DIR = Path("outputs/")
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="pod_memory")

for file in DOCS_DIR.rglob("*.md"):
    text = file.read_text()
    embedding = model.encode(text)
    collection.add(documents=[text], embeddings=[embedding.tolist()], ids=[str(file)])
```

---

### 3. Add Pre-Query Script (`scripts/query_memory.py`)
```python
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

query = "What did Research Pod say about symptom clusters?"
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_collection("pod_memory")

embedding = model.encode(query).tolist()
results = collection.query(query_embeddings=[embedding], n_results=3)

Path("memory").mkdir(exist_ok=True)
with open("memory/context_snippets.md", "w") as f:
    f.write(f"# Context Snippets for: {query}\n\n")
    for doc in results["documents"][0]:
        f.write(f"---\n{doc}\n\n")
```

---

### 4. Use in Pod Workflow

When launching a ChatGPT Pod:
1. Run `query_memory.py` with the current task prompt
2. Include `context_snippets.md` as part of system prompt or pod input

---

### 5. Automate with GitHub Actions (optional)

```yaml
name: Sync Memory

on:
  push:
    branches: [main]

jobs:
  embed:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install deps
        run: pip install chromadb sentence-transformers
      - name: Embed + Index
        run: python scripts/embed_and_index.py
```

---

## Benefits

- **Semantic recall** of pod outputs across time
- **Clear traceability** (everything still lives in Git)
- **Customizable scope** (by file or section)
- **LLM-efficient**: Precise memory = less wasted tokens

---

## Folder Structure
```
scripts/
  ├── embed_and_index.py
  └── query_memory.py
outputs/
memory/
  ├── vector_db/
  └── context_snippets.md
```

---

## Optional Next Steps

- Move to **chunk-based memory retrieval** for better granularity
- Add **metadata tags** to each chunk for pod, run_id, task
- Build **dashboards** showing memory usage per pod or sprint

Let us know when you're ready to activate this — we can scaffold scripts and folders to plug in directly.

