
SecurePipeline.ai

> **DoD-grade CI/CD security automation with AI-powered NIST 800-53 triage and ATO evidence generation.**

A security automation pipeline purpose-built for DoD/federal environments. It enforces compliance gates at every stage of the software delivery lifecycle — from secrets scanning and SAST to container scanning and IaC analysis — then uses an LLM to triage findings, map them to NIST 800-53 controls, and produce ATO-ready evidence artifacts.

---

## Current Status

**Phase 1 — GitHub Actions CI/CD (Days 1–6 of 14)**

| Day | Milestone |
|-----|-----------|
| ✅ Day 1 | Repo initialized, `security.yml` committed, first Actions run completed |
| ✅ Day 2 | CodeQL SAST gate confirmed working, FastAPI placeholder committed, all three jobs green — maps to SA-11(1) |
| ✅ Day 3 | Semgrep integrated with `p/python` + `p/owasp-top-ten`, SARIF visible in Security tab alongside CodeQL, four-job pipeline green — maps to SA-11(1) + SA-11(4) |
| ✅ Day 4 | Gitleaks hardened with custom `.gitleaks.toml`, DoD-specific rules (Anthropic key, DISA/STIG, GovCloud), allowlisting for GH Actions expressions, full git history scan via `fetch-depth: 0` + direct CLI call, five-job pipeline green — maps to IA-5 + SI-12 |
| ✅ Day 5 | pip-audit hardened to hard-fail gate, 11 vulnerabilities remediated via dependency upgrades, clean venv-scoped `requirements.txt` + `requirements.in` committed, CycloneDX SBOM artifact generated each run — maps to SA-12 + SA-15 |
| ✅ Day 6 | Trivy filesystem + secrets scan added as 6th gate (CRITICAL/HIGH hard-fail, dual SARIF to Security tab), workflow permissions hardened to job-level least privilege — maps to RA-5 + SI-3 + AC-6 |

---

## Project Roadmap
Phase 1 — GitHub Actions CI/CD          ← CURRENT (Days 1–14)
Phase 2 — Container Security             (Podman + Trivy/Grype)
Phase 3 — IaC Security                   (Terraform + tfsec/Checkov)
Phase 4 — AI Layer                        (LLM triage + NIST mapping + ATO artifacts)

---

## Security Pipeline Architecture
┌─────────────────────────────────────────────────────────────┐
│                      security.yml                           │
│                GitHub Actions Workflow                      │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│ Gitleaks │  CodeQL  │ Semgrep  │pip-audit │     Trivy      │
│ Secrets  │  SAST    │  SAST    │   SCA    │  fs + secrets  │
│ Scanning │          │          │  + SBOM  │     scan       │
├──────────┴──────────┴──────────┴──────────┴────────────────┤
│               SARIF → GitHub Security Tab                   │
│          CycloneDX SBOM → Actions Artifacts                 │
└─────────────────────────────────────────────────────────────┘
---

## NIST 800-53 Control Coverage

| Control | Description | Implemented By |
|---------|-------------|----------------|
| SA-11(1) | Developer Security Testing — Static Code Analysis | CodeQL, Semgrep |
| SA-11(4) | Developer Security Testing — Manual Code Reviews | Semgrep (OWASP ruleset) |
| IA-5 | Authenticator Management (secrets hygiene) | Gitleaks + `.gitleaks.toml` |
| SI-12 | Information Management and Retention (secret history) | Gitleaks full-history scan |
| SA-12 | Supply Chain Protection | pip-audit hard-fail gate |
| SA-15 | Development Process, Standards, and Tools — SBOM | CycloneDX via pip-audit |
| RA-5 | Vulnerability Monitoring and Scanning | Trivy filesystem scan |
| SI-3 | Malicious Code Protection | Trivy secrets scan |
| AC-6 | Least Privilege | Job-scoped workflow permissions |

---

## Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11+ |
| API Framework | FastAPI |
| AI/LLM | LangChain, LangGraph, Anthropic SDK |
| Container Runtime | Podman (rootless) |
| Infrastructure | RHEL, Terraform |
| CI/CD | GitHub Actions |
| SAST | CodeQL, Semgrep (`p/python`, `p/owasp-top-ten`) |
| Secrets Scanning | Gitleaks + custom DoD ruleset |
| Dependency Audit | pip-audit + CycloneDX SBOM |
| Filesystem Scanning | Trivy (vuln + secrets, filesystem mode) |
| Container Scanning | Trivy / Grype *(Phase 2)* |
| IaC Scanning | tfsec / Checkov *(Phase 3)* |

---

## Repo Structure
securepipeline-ai/
├── .github/
│   └── workflows/
│       └── security.yml          # Main CI/CD security pipeline
├── .gitleaks.toml                # Custom DoD secrets ruleset
├── app/
│   └── main.py                   # FastAPI application placeholder
├── requirements.in               # Direct dependencies (pip-tools source)
├── requirements.txt              # Pinned, audited dependencies
└── README.md

---

## Security Gates

### Secrets Scanning — Gitleaks
- Full git history scan (`fetch-depth: 0`) on every push
- Custom `.gitleaks.toml` with DoD-specific rules: Anthropic API keys, DISA/STIG tokens, GovCloud identifiers
- GitHub Actions expression allowlist to eliminate false positives
- Hard-fail on any detection
- Maps to IA-5 + SI-12

### SAST — CodeQL
- GitHub-native static analysis for Python
- Results surfaced in Security tab as SARIF
- Maps to SA-11(1)

### SAST — Semgrep
- `p/python` + `p/owasp-top-ten` rulesets
- SARIF output alongside CodeQL in Security tab
- Maps to SA-11(1) + SA-11(4)

### Dependency Audit — pip-audit
- Hard-fail gate: any known CVE blocks the pipeline
- CycloneDX SBOM generated as a signed Actions artifact each run
- Scoped to venv — no system package noise
- Maps to SA-12 + SA-15

### Filesystem Scanning — Trivy
- Dual-mode scan: vulnerability detection + secrets detection
- Hard-fail on CRITICAL or HIGH severity findings
- `ignore-unfixed: true` — unfixed vulnerabilities tracked via POA&M, not used to block pipeline with no remediation path
- Dual SARIF upload: `trivy-filesystem` and `trivy-secrets` categories visible in Security tab
- Runs only after `secrets-scan` and `pip-audit` pass — gated execution
- Maps to RA-5 + SI-3

### Workflow Permissions — Least Privilege
- `security-events: write` scoped only to jobs that upload SARIF (CodeQL, Semgrep, Trivy)
- `secrets-scan` and `pip-audit` run with `contents: read` only
- Eliminates overbroad `GITHUB_TOKEN` grants — common CI/CD audit finding
- Maps to AC-6

---

## Compliance Context

This project is designed for DoD/FedRAMP-adjacent environments operating under:

- **NIST SP 800-53 Rev 5** — control mapping at every pipeline stage
- **RMF** — artifact generation intended to support ATO evidence packages
- **STIG alignment** — container and OS hardening patterns (Phase 2+)
- **Supply chain security** — SBOM generation from Day 5 forward

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/adam-stotler/securepipeline-ai.git
cd securepipeline-ai

# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install pip-tools
.venv/bin/pip-sync requirements.txt

# Run the FastAPI app locally
uvicorn app.main:app --reload
```

Required GitHub Actions secrets:

| Secret | Purpose |
|--------|---------|
| `ANTHROPIC_API_KEY` | LLM triage layer (Phase 4) |

---

## Author

**Adam Stotler**
Cybersecurity Professional — 12+ years DoD/federal contracting
TS/SCI | CISSP | CCSP | AWS SAA | Security+

> *Built to demonstrate production-grade DevSecOps practices for DoD/federal environments — not as a tutorial project.*