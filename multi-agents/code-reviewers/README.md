# AI Crew for Stock Analysis

Introduction
This repository contains an example multi-agent "code-reviewers" setup built on top of the CrewAI-style framework. The agents collaborate to analyze, review, and produce code and analysis for stock-related tasks. It demonstrates how to define agents, configure tasks, and run the system locally.

**Key Features**
- **Multi-agent orchestration**: Multiple independent agents coordinate to complete stock analysis workflows.
- **Config-driven**: Agents and tasks are defined using YAML configuration files for easy experimentation.
- **Extensible tools**: Add or swap tools that agents use (data fetchers, analysis helpers, formatters).

**Repository Layout**
- `src/` : Main application code and agent implementations.
- `src/config/agents.yaml` : Agent definitions and roles.
- `src/config/tasks.yaml` : Task templates and workflows for agents.
- `src/test/` : Example inputs and test artifacts.

**Getting Started**

Prerequisites
- Python 3.10+ or a compatible runtime.
- `poetry` (recommended) or `pip` to install dependencies.

Install dependencies (using Poetry)
```
poetry install
```

Run the agents (example)
```
poetry run python3 src/main.py
```

**Configuration**

- To modify which agents run or change their roles, edit `src/config/agents.yaml`.
- To change tasks or add new workflows, edit `src/config/tasks.yaml`.

**Development Notes**
- The entrypoint is `src/main.py`; it loads agent and task configuration and starts the orchestrator.
- To add a new agent, implement it under `src/` and reference it from `agents.yaml`.

**Contributing**

- Open an issue or PR with a clear description of the change.
- Keep changes focused and add tests where appropriate.

**License**

- See the repository `LICENSE` for license terms.

**Questions or Help**
- For quick checks you can run the example command above. If you need help extending agents or tasks, open an issue describing your use case.