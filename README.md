# AI Agent School

Curated examples, templates, and experiments for building and evaluating autonomous agents and multi-agent flows.

This repository collects small, focused agent implementations and supporting materials for learning, prototyping and evaluating agent behaviors.

For Agents, I pick 2 non-trivial use cases and implement them using the following popular and enterprise-grade agentic frameworks:
- CrewAI
- LangGraph
- Nvidia NeMo

Here's how the repository is structured.  

**Repository layout**

- `agent-ecosystem/`: bird's eye view of the AI agent ecosystem including key concepts and components.
- `agent-evals/`: evaluation frameworks and tools for testing agent performance.
	- `trajectory-evaluator/`: agent trajectory match evaluators with strict/unordered/subset/superset matching modes.
	- `trajectory-evaluator-llm-judge/`: LLM-as-judge trajectory evaluators for agent evaluation without reference trajectories.
	- `graph-evaluator/`: graph trajectory evaluators for frameworks like LangGraph.
	- `graph-evaluator-llm-judge/`: LLM-as-judge graph trajectory evaluators.
- `multi-agent-samples/`: framework-specific multi-agent implementations.
	- `crewai/`: CrewAI multi-agent examples including code-reviewers project.
	- `langgraph/`: LangGraph multi-agent examples.
	- `nemo/`: Nvidia NeMo multi-agent examples.
- `doc-templates/`: Markdown templates for agent design and evaluation specs (e.g. `agent-design-spec.md`, `agent-evaluation-spec.md`, `agent-tech-spec.md`).
- `learning-resources/`: resources to learn and implement AI agents and workflows

**Quick start**

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install a project's dependencies before running examples. For the `code-reviewers` example:

```bash
cd multi-agent-samples/crewai/code-reviewers
pip install -e .
# or use the packaging tool declared in `pyproject.toml` (poetry/pep517)
```

3. Run examples, open notebooks, or explore evaluations:

- **Multi-agent demo**: inspect `multi-agent-samples/crewai/code-reviewers/README.md` and run its `main.py` for a local run.
- **Agent evaluations**: explore `agent-evals/` to understand evaluation frameworks and run trajectory or graph evaluators.
- **Ecosystem overview**: visit `agent-ecosystem/` for a mindmap of AI agent concepts and components.

**Contributing**

- Read `doc-templates/agent-design-spec.md` and `doc-templates/agent-evaluation-spec.md` for guidance on adding new agents and evaluations.
- Keep examples small and focused, include a short README for new agent folders, and add tests where appropriate.

**Notes**

- This repository is intended as a learning and prototyping playground — expect experimental code and small demos rather than production-ready systems.
- If you add long-running or resource-heavy examples, include instructions for required credentials and hardware in the example README.

**License**

See the `LICENSE` file at the repository root.

Enjoy exploring and building agents! If you'd like, I can also:
- add a top-level contribution guide (`CONTRIBUTING.md`),
- generate READMEs for the subprojects (e.g. `multi-agents/code-reviewers`), or
- add runnable examples and automated tests.