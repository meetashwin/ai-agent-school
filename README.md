# AI Agent School

Curated examples, templates, and experiments for building and evaluating autonomous agents and multi-agent flows.

This repository collects small, focused agent implementations and supporting materials for learning, prototyping and evaluating agent behaviors.

Repository layout
- `agent-evals/`: evaluation assets and results for agent experiments.
- `doc-templates/`: Markdown templates for agent design and evaluation specs (e.g. `agent-design-spec.md`, `agent-evaluation-spec.md`).
- `hello-world-agents/`: simple example agents and notebooks to demonstrate patterns and developer workflows.
	- `code_reflection_agent.ipynb`: interactive notebook demonstrating a simple reflection agent.
	- `reflective-chartgen-agent/chartgen-agent.py`: a minimal chart-generation agent example.
- `multi-agent-flows/`: experiments and examples showing coordination between multiple agents.
- `multi-agents/`: reusable agent projects and tooling.
	- `code-reviewers/`: an example multi-agent project for automated code review.
		- `pyproject.toml`: project metadata and dependencies for the `code-reviewers` package.
		- `src/code-reviewers/`: package source, including `crew.py`, `main.py`, and `tools/`.
- `stock-analysis/`: (placeholder) workspace for financial/market agent experiments.

Quick start

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install a project's dependencies before running examples. For the `code-reviewers` example:

```bash
cd multi-agents/code-reviewers
pip install -e .
# or use the packaging tool declared in `pyproject.toml` (poetry/pep517)
```

3. Run examples or open notebooks:

- Notebook: open `hello-world-agents/code_reflection_agent.ipynb` in Jupyter/Lab.
- Script example: run `python hello-world-agents/reflective-chartgen-agent/chartgen-agent.py`.
- Multi-agent demo: inspect `multi-agents/code-reviewers/README.md` and run its `main.py` for a local run.

Contributing

- Read `doc-templates/agent-design-spec.md` and `doc-templates/agent-evaluation-spec.md` for guidance on adding new agents and evaluations.
- Keep examples small and focused, include a short README for new agent folders, and add tests where appropriate.

Notes

- This repository is intended as a learning and prototyping playground — expect experimental code and small demos rather than production-ready systems.
- If you add long-running or resource-heavy examples, include instructions for required credentials and hardware in the example README.

License

See the `LICENSE` file at the repository root.

Enjoy exploring and building agents! If you'd like, I can also:
- add a top-level contribution guide (`CONTRIBUTING.md`),
- generate READMEs for the subprojects (e.g. `multi-agents/code-reviewers`), or
- add runnable examples and automated tests.