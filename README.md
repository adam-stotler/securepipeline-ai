# SecurePipeline.ai

DoD-niche security automation pipeline with AI-assisted NIST 800-53 mapping and ATO evidence generation.

## Stack
- **CI/CD:** GitHub Actions
- **Container Scanning:** Trivy / Grype via Podman on RHEL
- **IaC Scanning:** Terraform + tfsec / Checkov
- **AI Layer:** Anthropic SDK + LangGraph

## Security Gates
| Gate | Tool | Status |
|------|------|--------|
| Secrets Detection | Gitleaks | ✅ Active |
| Dependency Audit | pip-audit | ✅ Active |
| SAST | Semgrep | 🔜 Phase 1 Day 2 |
| Container Scan | Trivy/Grype | 🔜 Phase 2 |
| IaC Scan | tfsec/Checkov | 🔜 Phase 3 |
| AI Triage | Anthropic SDK | 🔜 Phase 4 |

## ATO Evidence
Scan artifacts retained 90 days per GitHub Actions policy, mapped to NIST 800-53 controls.
