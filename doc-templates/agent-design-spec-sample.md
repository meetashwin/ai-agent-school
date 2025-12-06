# Agent Design Specification — Security Engineer Agent (Sample)

## 1. Overview
- **Purpose:** Automatic security analysis of software repositories and change sets to identify vulnerabilities, insecure patterns, and risky configuration changes; produce prioritized, actionable findings for engineers.
- **Scope:** Static analysis of source code and diffs, dependency scanning, IaC (infrastructure-as-code) checks, and basic threat modelling of changes. Not responsible for runtime scanning, penetration testing, or executing untrusted code.
- **Stakeholders:** Security team (owners), engineering teams (consumers), release managers, and SRE/ops.

## 2. Goals & Success Criteria
- **Primary Goals:** Detect high-confidence security issues in pull requests, reduce mean time to remediation (MTTR) for security findings, and reduce false positives to avoid alert fatigue.
- **Success Metrics:** % of high-severity findings confirmed by engineers, average time from detection to fix, false positive rate, reviewer adoption rate, and per-PR analysis latency (< 30s for quick diffs, < 5min for full repo scan).

## 3. Target Users & Use Cases
- **User Profiles:** Security engineers (triage), Devs/Code owners (remediation), CI systems (automated gating), Release managers (policy enforcement).
- **Key Use Cases:**
  - On pull request: analyze diff and comment with findings and remediation steps.
  - Pre-commit/CI: run fast checks and fail builds for critical issues.
  - Scheduled scans: full repo scans for dependency & secret detection.
  - Security review assistant: summarize risk and produce checklist for human reviewers.

## 4. Capabilities & Behavior
- **Capabilities:**
  - Parse diffs, file contexts, and repo metadata.
  - Run language-specific static analysis heuristics and invoke third-party SAST tools.
  - Identify vulnerable dependencies and insecure configurations.
  - Suggest concrete remediation code snippets or configuration changes.
  - Produce prioritized report with confidence scores and exploitability notes.
- **Expected Behavior:** Polite, concise comments in PRs, clear severity levels, and reproducible reproduction steps when applicable.
- **Failure Modes:** Missed logic that is only detectable at runtime (false negatives), occasional false positives on complex code patterns, and inability to analyze generated or obfuscated code.

## 5. Inputs, Outputs & Interfaces
- **Inputs:** Git repo URL, branch name, pull request diff, file context (n lines), dependency manifests (`requirements.txt`, `package.json`, `pyproject.toml`), and IaC files (`*.tf`, `helm`, `k8s/*.yaml`).
- **Outputs:** Markdown-formatted PR comments, JSON report (findings with fields: id, file, line, severity, confidence, description, remediation, references), SARIF file export, and optional alerts to Slack/Jira.
- **APIs / Integrations:** GitHub/GitLab APIs for comments, CI (GitHub Actions / GitLab CI), SAST tools (Semgrep, Bandit, Trivy), vulnerability DBs (OSV, NVD), and ticketing systems (Jira).

## 6. Architecture & Components
- **High-level Architecture:**
  - Input Receiver: webhook / CI integration that receives PR events.
  - Analyzer Pipeline: pre-filter -> language parsers -> heuristics & LLM assistant -> tool orchestrator.
  - Findings Aggregator: merges outputs, deduplicates, scores and prioritizes.
  - Output Renderer: formats comments, JSON/SARIF exports, and alerts.
  - Storage & Memory: findings DB and short-term contextual memory for follow-ups.
- **Components:** Planner (decides which tools to run), Executor (runs SAST tools and LLM prompts), Knowledge DB (vuln database), Reporter (renders outputs).
- **Data Flow:** Event -> fetch diff -> quick lint -> deep scan (if needed) -> aggregate findings -> post results.

## 7. Models, Algorithms & Tools
- **Models:** LLM assistant for contextual analysis and remediation suggestions (e.g., small LLM for private deployments; specify model version and prompt templates in config).
- **Algorithms/Heuristics:** Pattern-based rules, taint-flow heuristics, dependency CVE lookups, and risk scoring heuristics (CVSS + exploitability + code exposure).
- **Third-party Tools:** Semgrep, Bandit, ESLint security plugins, Trivy, pip-audit, OSV API, and optional fuzzing hooks.

## 8. Data, Knowledge & Memory
- **Data Sources:** Internal vulnerability DB, public CVE/OSV feeds, past findings history, and common-repair templates.
- **Knowledge Representation:** Findings stored as JSON with context, normalized identifiers, and links to references; short-lived memory for multi-comment conversational follow-ups.
- **Privacy & Retention:** Store minimal code context (only necessary lines), redact secrets, and follow org retention policy (e.g., findings kept 90 days unless persisted in ticketing system).

## 9. Safety, Ethics & Constraints
- **Safety Rules:** Never expose or post secrets found in code to public logs or comments; avoid returning full reproduction payload that contains sensitive data.
- **Ethical Considerations:** Avoid biased scoring that unfairly targets specific authors or teams; provide rationale for each finding to allow human review.
- **Regulatory Constraints:** Do not transfer source code outside approved regions; comply with data residency and export-control policies.

## 10. Evaluation & Testing
- **Evaluation Plan:** Compare agent findings to human triage on a labeled dataset of PRs; run A/B tests for triage speed and acceptance.
- **Metrics:** Precision/recall per severity tier, time-to-detect, time-to-fix, reviewer satisfaction score, and rate of accepted remediation suggestions.
- **Test Cases:** Synthetic PRs introducing SQL injection, hard-coded credentials, insecure deserialization, vulnerable dependency upgrades, and misconfigured cloud storage ACLs.

## 11. Deployment & Operations
- **Deployment Targets:** Cloud-hosted service behind org SSO or on-prem deployment for sensitive repos; CI-integrated runner for fast checks.
- **Runtime Requirements:** Small-latency LLM endpoint (if used), compute for SAST tools, and ephemeral containers for safe analysis.
- **Monitoring & Alerting:** Track analysis latency, error rates, findings per run, and feedback signals (false positive flags). Alert on service failures and high-severity regressions.

## 12. Maintenance & Versioning
- **Update Process:** Update rules and model prompts via PRs; schedule periodic vulnerability feed updates; maintain changelog of rules.
- **Versioning:** Semantic versioning for agent releases (major.minor.patch) and pinned model/tool versions recorded in releases.
- **Ownership:** Security team owns rules; engineering teams triage and own remediation.

## 13. Roadmap & Priorities
- **Planned Features:** Add taint analysis, ML-based false-positive reduction, support for more languages, automated fix proposals (code action PRs), and integration with runtime chaos tests.
- **Priority Rationale:** Focus on high-confidence detection and integration with developer workflows first to maximize adoption.

## 14. Appendix
- **Glossary:** SAST (Static Application Security Testing), IaC (Infrastructure as Code), SARIF (Standardized Analysis Results Interchange Format), OSV (Open Source Vulnerability Database).
- **References:** Semgrep rulesets, OSV API docs, OWASP Top 10, internal security playbooks.
- **Change Log:** Initial sample created — 2025-12-06.

---

### Example PR Comment (short)

> Security: High — SQL injection in `src/db/query.py:42` (confidence: high)

- Why: Unsanitized string interpolation with user input passed to `execute()`.
- Fix: Use parameterized queries (example snippet) and add unit tests; see reference: https://owasp.org/...

### Acceptance Criteria (example)

- On a sample vulnerable PR, agent posts a clear, reproducible finding with remediation and references.
- False positive rate for high-severity findings < 10% on validation set.
- Analysis time for PR diffs < 60s in CI environment.
