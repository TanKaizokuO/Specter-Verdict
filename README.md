In this AI-powered courtroom simulation, we have three GPT agents playing the roles of Prosecutor, Defense Attorney, and Judge. These agents are connected through a basic RAG (Retrieval-Augmented Generation) pipeline, which allows them to retrieve relevant legal principles to ground their arguments.

The RAG pipeline works by having the agents generate a query based on the current state of the simulation, which is then used to retrieve relevant legal principles from a database. These principles are then used by the agents to generate more detailed and grounded arguments, which can be used to persuade the Judge in their favor.

This simulation allows us to explore how AI agents can be used to simulate complex legal scenarios and how they can be used to generate arguments and legal principles in a more efficient and effective manner.| ------------------ | --------------------------------------------------------- | ----------- |
| **Prosecutor GPT** | Argues the defendant is GUILTY | 0.75 |
| **Defense GPT** | Argues the defendant is NOT GUILTY | 0.75 |
| **Judge GPT** | Evaluates both sides, delivers verdict + confidence score | 0.3 |

Each agent has a distinct system prompt that defines its persona, objectives, and a strict structured output format.

---

## 📚 RAG Pipeline

- **Corpus**: 15 hand-crafted legal principles (extensible in `rag.py`)
- **Embeddings**: `all-MiniLM-L6-v2` via `sentence-transformers`
- **Index**: FAISS flat inner-product index (cosine similarity on L2-normalised vectors)
- **Retrieval**: Top-k passages (default `k=4`) injected into every agent prompt

---

## 🗂️ Project Structure

```
AI Courtroom/
├── agents.py        # Prosecutor, Defense, Judge GPT agents
├── rag.py           # RAG retriever (FAISS + sentence-transformers)
├── courtroom.py     # Main trial orchestration pipeline + CLI
├── requirements.txt # Python dependencies
├── .env.example     # Environment variable template
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/TanKaizokuO/AI_Courtroom.git
cd "AI Courtroom"
pip install -r requirements.txt
```

### 2. Configure API key

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

### 3. Run

```bash
# Interactive mode
python courtroom.py

# Or type 'demo' at the prompt to use the built-in example
```

---

## 📋 Example

**Input (demo case):**

```
A man was seen running away from a jewelry store moments after the alarm went
off. Security camera footage shows a person matching his description near the
scene. No stolen items were found on him. He claims he was jogging in the area
and panicked when he heard the alarm.
```

**Output (abbreviated):**

```
======================================================================
  ⚖️  AI COURTROOM SIMULATION  ⚖️
======================================================================

======================================================================
  📚  STEP 1: RAG — Retrieving Legal Context
======================================================================
Retrieved 4 relevant legal principles:
  1. The prosecution must prove guilt beyond a reasonable doubt.
  2. Circumstantial evidence can support a conviction if it is strong ...
  3. Defendants are presumed innocent until proven guilty ...
  4. Flight from the scene may be considered as consciousness of guilt.

...

## Final Verdict
**NOT GUILTY**

## Confidence Score
0.68
```

---

## ⚙️ Configuration

| Variable         | Default       | Description                 |
| ---------------- | ------------- | --------------------------- |
| `OPENAI_API_KEY` | _(required)_  | Your OpenAI API key         |
| `OPENAI_MODEL`   | `gpt-4o-mini` | Model to use for all agents |

Change `top_k` in `run_trial()` to retrieve more or fewer legal passages.

---

## 🔧 Extending

- **Add corpus entries**: Edit `LEGAL_CORPUS` in `rag.py`
- **Swap model**: Change `OPENAI_MODEL` in `.env`
- **Add agents**: Follow the pattern in `agents.py` — define a system prompt + a function
- **Swap retriever**: Replace the FAISS index with any vector DB (Chroma, Pinecone, etc.)


Last updated: 2026-03-21 23:20:13
