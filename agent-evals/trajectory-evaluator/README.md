# Trajectory Evaluator

This folder contains a small demonstration script, `trajectory-eval.py`, which uses the `agentevals` package to evaluate agent trajectories.

## Prerequisites ✅

- Python 3.10+ (or a compatible 3.x)
- An OpenAI API key with the environment variable `OPENAI_API_KEY` exported
- `agentevals` Python package installed

---

## Setup (recommended) 🔧

1. Create and activate a virtual environment:

```bash
# from Linux/macOS
python -m venv .venv
source .venv/bin/activate

# from Windows (PowerShell)
# python -m venv .venv
# .\.venv\Scripts\Activate.ps1
```

2. Upgrade pip and install dependencies:

```bash
pip install --upgrade pip
# Install the AgentEvals package from PyPI
pip install agentevals

# Or install the latest from the GitHub repo:
# pip install git+https://github.com/langchain-ai/agentevals.git
```

> Tip: If you are working from the top-level project and want an editable install, you can use `pip install -e .` from the package root where a `setup.py` or `pyproject.toml` exists.

---

## Export OpenAI API Key 🔐

Before running the script, export your OpenAI API key:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

(For Windows PowerShell use `setx OPENAI_API_KEY "your-openai-api-key-here"` or set in your session with `$env:OPENAI_API_KEY = "..."`.)

---

## Run the script ▶️

From this `trajectory-evaluator` directory run:

```bash
python trajectory-eval.py
```

Or run it via explicit path from the repo root:

```bash
python agent-evals/trajectory-evaluator/trajectory-eval.py
```

---

## Notes 💡

- Ensure the `agentevals` package is available in the active virtual environment (see **Setup** above).
- Ensure `OPENAI_API_KEY` is set in the environment of the process that runs the script.
- If you see import errors for `agentevals`, verify installation with `pip show agentevals` or re-install into the active venv.

---

