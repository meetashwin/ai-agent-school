# Agent Technical Specification — Security Engineer Agent

## Summary
This tech spec translates the `agent-design-spec.md` into concrete implementation details to generate agent code for target frameworks (e.g., CrewAI). It defines components, data schemas, APIs, configuration, prompt templates, tool integrations, tests, and deployment requirements.

## 1. Responsibilities
- Run fast, diff-based security checks on PRs.
- Run deeper repository scans on demand (dependencies, IaC).
- Aggregate and prioritize findings and emit results as PR comments, SARIF/JSON, and ticketing alerts.
- Provide remediation suggestions and reproducible reproduction steps where possible.

## 2. System Overview & Runtime Components
- Input Receiver (Webhook/CI hook)
- Fetcher (Git adapter): clones repo or fetches PR diff and file contexts
- Analyzer Pipeline:
  - Pre-filter (file globs, size limits)
  - Fast ruleset (Semgrep / lightweight heuristics)
  - Deep analyzers (Bandit, Trivy, dependency scanners)
  - LLM Assistant (optional) for context-aware triage and remediation
- Aggregator & Normalizer: merges outputs, deduplicates, scores
- Reporter: posts PR comments, generates SARIF/JSON, creates tickets
- Persisted Store (optional): small DB for findings, feedback, and history
- Orchestration / Worker: schedules runs, retries, rate-limits

### Runtime Process Flow
1. Receive PR event
2. Fetch PR diff and N lines of context for changed files
3. Run Pre-filter to decide quick vs deep scan
4. Execute analyzers (parallelized) and collect findings
5. Normalize to `Finding` schema, dedupe and score
6. Produce reporter outputs (comment, SARIF, JSON) and persist

## 3. Interfaces & API Contracts

### Incoming Event (Webhook)
- POST /events/pull_request
- Payload (GitHub-style minimal): { "repo": "org/repo", "pr": 123, "head_ref": "branch", "changed_files": ["a.py"], "actor": "user" }

### Analyzer Executor API (internal)
- POST /analyze/pr
- Request: { "repo": "org/repo", "pr": 123, "diff_url": "https://...", "config_id": "default" }
- Response (202 Accepted): { "run_id": "uuid" }

### Findings Reporter API
- POST /report/findings
- Request payload (JSON array of Findings): [Finding]

## 4. Data Schemas

Finding (JSON):
- id: string (uuid)
- run_id: string
- source: string (semgrep|bandit|llm|trivy)
- file: string (relative path)
- line: integer | null
- snippet: string (redacted)
- severity: enum (critical|high|medium|low|info)
- confidence: float (0.0-1.0)
- title: string
- description: string (one-paragraph)
- remediation: string (code snippet or commands)
- references: [url]
- cwe: optional string
- cve: optional string

SARIF export: map `Finding` to SARIF v2.1.0 result schema; include `startLine`, `endLine`, `ruleId`, and `fullDescription`.

Feedback Schema (for FP/Triage):
- finding_id, reporter, verdict (false_positive|true_positive|ignored), notes, timestamp

## 5. Configuration

config.yaml (example keys):
- rulesets: [semgrep:baseline, semgrep:custom]
- languages: [python, javascript]
- max_files: 500
- context_lines: 5
- severity_threshold: medium
- tools:
  semgrep: { enabled: true, ruleset_urls: [...] }
  bandit: { enabled: true }
  trivy: { enabled: true }
  llm_assistant: { enabled: false, model: "local-llm-v1", prompt_template: "default" }

## 6. CrewAI-style Agent Config (sample)
This YAML is a sample mapping to a target agent framework. Adapt keys to your framework.

```yaml
agent:
  id: security-engineer-agent
  display_name: "Security Engineer Agent"
  description: "Per-PR and scheduled repo security analysis"
  triggers:
    - on: pull_request.opened
    - on: pull_request.synchronize
    - on: schedule.daily
  runtime:
    max_concurrency: 4
    timeout_seconds: 600
  tools:
    - name: git
      type: connector
    - name: semgrep
      type: tool
    - name: bandit
      type: tool
    - name: trivy
      type: tool
    - name: osv_lookup
      type: api
  memory:
    store_findings: true
    retention_days: 90
  outputs:
    - type: pr_comment
    - type: sarif
    - type: json
```

## 7. Prompt Templates & LLM Usage
- Use small, deterministic prompt templates; avoid leaking secrets. Examples below.

LLM Triage Prompt (example):
"""
You are a security analyst assistant. Given the file path, the changed code snippet, and tool findings, produce a single concise finding with severity (critical/high/medium/low), a short explanation (one line), and a remediation suggestion with code snippet if applicable. Output JSON with fields: title, severity, confidence, description, remediation, references.
"""

Example LLM Output (JSON):
{
  "title": "SQL injection in user query",
  "severity": "critical",
  "confidence": 0.92,
  "description": "User input concatenated into SQL query passed to execute().",
  "remediation": "Use parameterized queries: cursor.execute(\"SELECT ... WHERE id=%s\", (user_id,))",
  "references": ["https://owasp.org/" ]
}

## 8. Tool Integration Details
- Semgrep: run with `--json` output and transform rules to `Finding` schema. Keep rule IDs and severity mapping.
- Bandit: parse `bandit -f json` and map to `Finding`.
- Trivy/pip-audit: run dependency scan and map CVEs to `Finding` with `cve` and `cvss` meta.
- OSV/NVD: use APIs for vulnerability metadata and to check if dependency version is vulnerable.

## 9. Deduplication & Scoring
- Deduplicate by file+fingerprint where fingerprint = hash(rule_id + file + start_line + code_hash).
- Score = base_severity_score * confidence_multiplier * exposure_factor.
- exposure_factor: derived from whether code is reachable from changed PR entrypoints, or if secret/config affects production.

## 10. Tests & Validation
- Unit tests: parser transforms (Semgrep/Bandit -> Finding), reporter formatting, and config parsing.
- Integration tests: run analyzers against a small sample repo with seeded vulnerabilities and assert expected findings.
- E2E: simulate PR webhook and validate PR comment created and SARIF uploaded.

Test dataset (sample cases):
- sql-injection.py
- hardcoded-secret.py
- insecure-deserialization.js
- vulnerable-dependency-manifest

## 11. Logging, Metrics & Observability
- Logs: structured JSON logs with `run_id`, `stage`, `elapsed_ms`, `errors`.
- Metrics (Prometheus style): `pr_runs_total`, `findings_total`, `findings_by_severity`, `analysis_latency_seconds`, `tool_errors_total`.
- Traces: instrument Analyzer Pipeline for spans (fetch, semgrep, bandit, aggregate, report).

## 12. Security & Privacy
- Redact detected secrets before persisting or posting. Replace values with `<REDACTED>` and store only context lines.
- Restrict LLM prompt context to non-sensitive lines; mark LLM usage in audit logs.
- Enforce least-privilege for Git tokens and avoid sending private repos to external services unless explicitly allowed.

## 13. CI / Deployment
- Build container image with pinned versions of Semgrep, Bandit, Trivy, and runtime dependencies.
- Example GitHub Action job to run analyzer as PR check: check out PR, run `analyze/pr` API, wait for result, then post annotations.

## 14. Developer Experience & SDK Mapping
- Code structure recommended (Python example):
  - `src/agent/ingest.py` — webhook and git fetcher
  - `src/agent/analyzers/semgrep.py` — adapter
  - `src/agent/analyzers/bandit.py` — adapter
  - `src/agent/llm.py` — prompt runner
  - `src/agent/aggregator.py` — normalizer and dedupe
  - `src/agent/reporter.py` — pr comment & sarif
  - `src/agent/config.py` — loads `config.yaml`

Map these modules to CrewAI tool interfaces: implement `Tool` classes that expose `run()` and `parse()` methods.

## 15. Acceptance Criteria
- Agent runs on PR events and posts findings for seeded vulnerabilities in test repo.
- SARIF output conforms to SARIF v2.1.0 and loads into GitHub code scanning UI.
- High-severity findings validated by security reviewer in > 80% of cases on validation set.

## 16. Open Questions / Next Steps
- Decide on LLM provider and on-prem vs cloud for private code.
- Agree retention period and schema for persisted findings.
- Define CI gating policy thresholds (e.g., fail PR if critical finding present).

---

If you want, I can:
- Generate a starter Python implementation scaffold matching this spec.
- Produce a GitHub Action workflow that calls the analyzer.
- Create Semgrep rule examples and mapping scripts to the Finding schema.
