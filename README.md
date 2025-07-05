# Conversation Evaluator

A scalable system for evaluating conversation turns on hundreds to thousands of linguistic, pragmatic, safety, and emotional facets using open-weight LLMs.

---

## Tech Stack

| Component         | Technology/Framework         | Purpose/Notes                                  |
|------------------|-----------------------------|------------------------------------------------|
| Language         | Python 3.13                  | Core programming language                      |
| LLM Backend      | Ollama + Llama 3 (8B)        | Open-weight language model for scoring         |
| Embeddings Model | Ollama + nomic-embed-text    | For facet/category embedding & similarity      |
| Data Processing  | pandas, numpy, scikit-learn  | Data cleaning, manipulation, and similarity    |
| Async Engine     | asyncio                      | High-performance concurrent evaluation         |
| Prompt Chaining  | langchain, langchain-ollama  | LLM orchestration and prompt management        |
| UI               | Streamlit                    | Interactive web interface                      |  |
| Containerization | Docker                       | Reproducible deployment                        |

---

## Features

- **Facet evaluation:** Supports 300+ facets, easily extensible to 5000+ without code changes.
- **Preprocessing:** Cleans, normalizes, and categorizes facets using embeddings and cosine similarity(embeddings based classification).
- **Asynchronous LLM inference:** Faster evaluation by running all category evaluations concurrently.
- **Open-weight LLMs:** Uses Llama 3 (via Ollama) for scoring, fully compliant with open-weight requirements.
- **Confidence scoring:** Each facet score includes a justification and a confidence value.
- **Streamlit UI:** Simple web interface for interactive evaluation.
- **Docker-ready:** Easily containerized for reproducible deployment.

---

## Directory Structure

```
.
├── data/
│   ├── Facets_Assignment.csv         # Raw facet definitions (input)
│   └── processed_facets.parquet      # Cleaned, categorized facets (generated)
├── preprocessing.py                  # Data cleaning, embedding, and categorization
├── evaluator.py                      # Asynchronous facet evaluation engine
├── ui.py                             # Streamlit web UI
├── parquet_head.py                   # Utility: preview processed facets
├── requirements.txt                  # Python dependencies
├── pyproject.toml                    # Project metadata and dependencies
├── .python-version                   # Python version (3.13)
├── .gitignore                        # Standard Python ignores
└── README.md                         # (You are here)
```

---

## Setup

### 1. **Python Environment**

- Requires **Python 3.13** (see `.python-version`)
- Recommended: Use `venv` or `conda` for isolation

```bash
python3.13 -m venv .venv
.venv\Scripts\activate # on Windows
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```
or, if using `pyproject.toml`:
```bash
pip install .
```

### 3. **Ollama LLM Backend**

- Install and run [Ollama](https://ollama.com/) locally.
- Pull the required model (e.g.,nomic-embed-text, Llama3):

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

- By default, Ollama should run at `http://localhost:11434`.
- For Dockerized runs, the system will use `host.docker.internal`.

---

## Data Preparation

1. Place your raw facet definitions in `data/Facets_Assignment.csv`.
2. Run the preprocessing script to clean and categorize facets:

```bash
python preprocessing.py
```

- This generates `data/processed_facets.parquet` for use by the evaluator.

---

## Running the Evaluator

### **Asynchronous Evaluation**

The core evaluation logic is in `evaluator.py` and is fully asynchronous for speed.

**Example usage:**
```python
import asyncio
from evaluator import evaluate_conversation_turn_async

text = "Your conversation turn here."
results = asyncio.run(evaluate_conversation_turn_async(text))
print(results)
```

- Each facet is scored 1–5, with justification and confidence (1–5).

---

## Web UI

A simple Streamlit UI is provided for interactive evaluation.

```bash
streamlit run ui.py
```

- Enter text and view all facet-wise scores, justifications, and confidence values in JSON format.

---

## Docker Usage

Build and run the containerized app (ensure Ollama is running on the host):

```bash
docker build -t conversation-evaluator .
docker run -p 8501:8501 --add-host=host.docker.internal:host-gateway conversation-evaluator
```

---

## Notes

- Ensure Ollama is running and the required model is available before evaluation.
- For large-scale evaluation, the async engine provides significant speedup.
- The UI and Docker setup are provided for demonstration and reproducibility.

---
