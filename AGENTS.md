# 🏛️ AI Courtroom Trailer Simulation — Coding Agent Spec

> **Project Type:** Multi-Agent AI System with RAG  
> **Stack:** Python · LangChain / LlamaIndex · Vector DB · LLM APIs  
> **Simulation Mode:** Courtroom Trailer (Pre-trial proceedings)

---

## 📌 Project Overview

Build an AI-powered courtroom **trailer simulation** — a pre-trial proceeding where three autonomous agents (Judge, Prosecutor, Defense Attorney) debate a legal case using **Retrieval-Augmented Generation (RAG)** over a provided case document corpus. The simulation runs as a turn-based dialogue loop, producing a structured transcript and a final ruling summary. A uv venv has initialised in the directory.

---

## 🎯 Goals

- [ ] Simulate a realistic courtroom trailer with three distinct AI agents
- [ ] Ground all agent responses in retrieved case evidence via RAG
- [ ] Produce a structured, exportable transcript
- [ ] Allow a human observer to inject questions or evidence mid-session
- [ ] Output a final Judge ruling with citations

---

## 🗂️ Repository Structure

```
courtroom-sim/
├── agents/
│   ├── judge.py              # Judge agent logic
│   ├── prosecutor.py         # Prosecutor agent logic
│   └── defense.py            # Defense attorney agent logic
├── rag/
│   ├── ingest.py             # Document ingestion & chunking
│   ├── retriever.py          # Vector store retrieval interface
│   └── embeddings.py         # Embedding model config
├── simulation/
│   ├── orchestrator.py       # Turn-based dialogue loop
│   ├── transcript.py         # Transcript builder & exporter
│   └── state.py              # Shared simulation state
├── data/
│   ├── case_files/           # Raw case documents (PDFs, TXTs)
│   └── vector_store/         # Persisted vector index
├── config/
│   └── settings.yaml         # Model names, chunk sizes, thresholds
├── tests/
│   ├── test_agents.py
│   ├── test_rag.py
│   └── test_orchestrator.py
├── main.py                   # Entrypoint
├── requirements.txt
└── AGENTS.md                 # ← This file
```

---

## 🔀 Git Commit Strategy

The repo is already initialised. The coding agent must run `git add`, `git commit`, and `git push` at each checkpoint below. **Never batch unrelated changes into a single commit.** Each commit should be atomic — one logical unit of work.

### Commit Message Format

```
<type>(<scope>): <short description>

[optional body: what changed and why]
```

| Type | When to use |
|---|---|
| `feat` | New file or capability added |
| `chore` | Config, deps, scaffolding |
| `fix` | Bug fix or correction |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `refactor` | Code restructure, no behaviour change |

### Commit Checkpoints

| # | Trigger | Files to Stage | Commit Message |
|---|---|---|---|
| 1 | After creating project scaffold (empty dirs + placeholder files) | All new files | `chore(scaffold): initialise project structure` |
| 2 | After `requirements.txt` and `config/settings.yaml` | `requirements.txt`, `config/settings.yaml` | `chore(config): add dependencies and base settings` |
| 3 | After `rag/embeddings.py` complete | `rag/embeddings.py` | `feat(rag): add embedding model config` |
| 4 | After `rag/ingest.py` complete | `rag/ingest.py` | `feat(rag): implement document ingestion and chunking` |
| 5 | After `rag/retriever.py` complete | `rag/retriever.py` | `feat(rag): add role-scoped vector store retriever` |
| 6 | After `simulation/state.py` complete | `simulation/state.py` | `feat(simulation): define SimulationState dataclass` |
| 7 | After `agents/judge.py` complete | `agents/judge.py` | `feat(agents): implement Judge agent with RAG retrieval` |
| 8 | After `agents/prosecutor.py` complete | `agents/prosecutor.py` | `feat(agents): implement Prosecutor agent` |
| 9 | After `agents/defense.py` complete | `agents/defense.py` | `feat(agents): implement Defense Attorney agent` |
| 10 | After `simulation/transcript.py` complete | `simulation/transcript.py` | `feat(simulation): add transcript builder and exporter` |
| 11 | After `simulation/orchestrator.py` complete | `simulation/orchestrator.py` | `feat(simulation): implement turn-based orchestrator loop` |
| 12 | After `main.py` complete | `main.py` | `feat: add CLI entrypoint` |
| 13 | After all tests written | `tests/` | `test: add agent, RAG, and orchestrator test suites` |
| 14 | After first full end-to-end run passes | Any fixes applied | `fix: resolve integration issues from e2e run` |
| 15 | After any refactor or cleanup pass | Changed files only | `refactor(<scope>): <describe what was cleaned up>` |

### Git Commands to Run at Each Checkpoint

```bash
git add <specific files or .>
git commit -m "<message from table above>"
git push
```

> ⚠️ **Agent Rule:** Do not use `git add .` indiscriminately. Stage only files relevant to the current checkpoint. Never commit `data/vector_store/`, `.env`, or generated output files — add these to `.gitignore` before the first commit if not already present.

### `.gitignore` Entries to Verify Exist

```
.env
data/vector_store/
output/
__pycache__/
*.pyc
.chroma/
```

---

## 🤖 Agent Definitions

### 1. ⚖️ Judge Agent

| Property | Detail |
|---|---|
| **Role** | Neutral arbiter. Opens proceedings, rules on objections, delivers final verdict summary. |
| **Persona Prompt** | Formal, measured, strictly procedural. Cites legal standards. |
| **RAG Access** | Retrieves procedural law, precedent rulings, evidentiary rules. |
| **Triggers** | Starts each round, responds to objections, closes session. |
| **Output** | Structured rulings: `SUSTAINED`, `OVERRULED`, `DEFERRED`, or `FINAL RULING`. |

**System Prompt Template:**
```
You are a neutral federal judge presiding over a pre-trial hearing.
You have access to relevant case law and procedural rules via retrieval.
Speak formally. Issue rulings concisely. Always cite retrieved precedent.
Current phase: {phase}
Retrieved context: {context}
```

---

### 2. 🔴 Prosecutor Agent

| Property | Detail |
|---|---|
| **Role** | Represents the state. Argues for the charges. Presents evidence. |
| **Persona Prompt** | Assertive, methodical, evidence-driven. References case facts. |
| **RAG Access** | Retrieves police reports, forensic evidence, witness statements, statutes. |
| **Triggers** | Opening argument, evidence presentation, cross-examination responses. |
| **Output** | Arguments with inline evidence citations `[Doc: {source}, p.{page}]`. |

**System Prompt Template:**
```
You are a prosecutor in a pre-trial hearing. Your goal is to demonstrate
probable cause and argue for the charges to proceed to full trial.
Cite only retrieved evidence. Be persuasive but accurate.
Retrieved context: {context}
Opposing argument (if any): {defense_last_argument}
```

---

### 3. 🔵 Defense Attorney Agent

| Property | Detail |
|---|---|
| **Role** | Represents the defendant. Challenges evidence, raises procedural issues. |
| **Persona Prompt** | Sharp, skeptical, rights-focused. Looks for gaps in prosecution's case. |
| **RAG Access** | Retrieves defendant testimony, alibi records, rights violations, counter-evidence. |
| **Triggers** | Rebuttal, objections, motions to suppress. |
| **Output** | Counter-arguments with citations and objection flags `[OBJECTION: {type}]`. |

**System Prompt Template:**
```
You are a defense attorney in a pre-trial hearing. Your goal is to protect
your client's rights and challenge the sufficiency of the prosecution's evidence.
Raise objections when warranted. Cite retrieved documents to support your position.
Retrieved context: {context}
Prosecution's last argument: {prosecutor_last_argument}
```

---

## 📚 RAG Pipeline

### Ingestion (`rag/ingest.py`)

```python
# Responsibilities:
# - Load PDFs, TXTs, DOCXs from data/case_files/
# - Chunk with overlap (chunk_size=512, overlap=64)
# - Tag each chunk with metadata: {source, doc_type, date, page}
# - Embed and store in vector DB
```

**Supported Document Types:**

| Type | Tag | Examples |
|---|---|---|
| Case Law | `precedent` | Prior rulings, statutes |
| Evidence | `evidence` | Forensic reports, photos (captioned) |
| Testimony | `testimony` | Witness statements, depositions |
| Procedural | `procedure` | Court rules, motions |
| Defendant Records | `defense_doc` | Alibi, character witnesses |

### Retriever (`rag/retriever.py`)

- **Vector Store:** ChromaDB (local) or Pinecone (cloud)
- **Embedding Model:** `text-embedding-3-small` (OpenAI) or `nomic-embed-text` (local)
- **Top-K:** 5 chunks per query
- **Filter:** Each agent queries with a **role-scoped metadata filter** to bias retrieval toward relevant doc types
- **Reranking:** Cross-encoder reranking after initial retrieval (optional, improves quality)

```python
def retrieve(query: str, role: str, top_k: int = 5) -> list[Document]:
    role_filters = {
        "judge":      ["precedent", "procedure"],
        "prosecutor": ["evidence", "testimony", "precedent"],
        "defense":    ["defense_doc", "testimony", "procedure"],
    }
    # Filter + similarity search + optional rerank
```

---

## 🔄 Simulation Orchestrator

### Turn Order (`simulation/orchestrator.py`)

```
Round N:
  1. Judge   → Opens round / rules on pending motions
  2. Prosecutor → Presents argument / evidence
  3. Defense  → Rebuts / raises objections
  4. Judge   → Rules on objections raised this round
  [Repeat for N rounds]
  Final:
  5. Prosecutor → Closing statement
  6. Defense  → Closing statement
  7. Judge   → Final ruling
```

### State Object (`simulation/state.py`)

```python
@dataclass
class SimulationState:
    case_id: str
    phase: str                        # "opening" | "evidence" | "rebuttal" | "closing"
    round: int
    transcript: list[Turn]
    pending_objections: list[str]
    rulings: list[Ruling]
    human_interventions: list[str]    # Observer injections
```

### Termination Conditions

- Max rounds reached (configurable, default: `5`)
- Judge issues `CASE DISMISSED` or `PROCEED TO TRIAL` ruling
- Human observer ends session via CLI input `exit`

---

## 🧾 Transcript Format

Each turn is logged as:

```json
{
  "round": 2,
  "speaker": "Prosecutor",
  "phase": "evidence",
  "content": "The forensic report indicates...",
  "citations": ["forensic_report.pdf, p.4", "lab_analysis.txt, §3"],
  "objections_raised": [],
  "timestamp": "2026-04-28T10:34:22Z"
}
```

Export formats: **JSON** · **Markdown** · **PDF** (via `transcript.py`)

---

## ⚙️ Configuration (`config/settings.yaml`)

```yaml
llm:
  model: claude-sonnet-4-20250514   # or gpt-4o
  temperature: 0.4
  max_tokens: 1024

rag:
  chunk_size: 512
  chunk_overlap: 64
  top_k: 5
  reranking: true
  vector_store: chroma              # chroma | pinecone

simulation:
  max_rounds: 5
  allow_human_injection: true
  export_transcript: true
  export_format: markdown           # json | markdown | pdf

case:
  case_id: "CASE-2026-001"
  case_name: "State v. Example"
  data_dir: ./data/case_files/
```

---

## 🧪 Testing Plan

| Test File | Coverage |
|---|---|
| `test_rag.py` | Ingestion, chunking, retrieval accuracy, metadata filtering |
| `test_agents.py` | Persona adherence, citation format, objection detection |
| `test_orchestrator.py` | Turn order, state transitions, termination conditions |

### Key Test Cases

- [ ] Retrieval returns role-appropriate documents
- [ ] Judge correctly rules `SUSTAINED` on valid hearsay objection
- [ ] Defense raises `[OBJECTION: Relevance]` when prosecution cites unrelated evidence
- [ ] Transcript captures all turns with correct metadata
- [ ] Simulation terminates cleanly after max rounds
- [ ] Human injection mid-round is handled without breaking state

---

## 🚀 Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ingest case documents
python -m rag.ingest --case-dir ./data/case_files/

# 3. Run simulation
python main.py --config config/settings.yaml

# 4. Export transcript
python -m simulation.transcript --format markdown --out ./output/transcript.md
```

---

## 📦 Key Dependencies

```
langchain>=0.2
langchain-anthropic / langchain-openai
chromadb
sentence-transformers
pypdf
python-docx
pyyaml
rich                  # CLI formatting
pytest
```

---

## 🔐 Environment Variables

```
ANTHROPIC_API_KEY=...     # or OPENAI_API_KEY
PINECONE_API_KEY=...      # if using Pinecone
PINECONE_ENV=...
```

---


