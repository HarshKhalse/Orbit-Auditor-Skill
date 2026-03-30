# CLAUDE.md - Orbit Auditor Skill Integration

This repository contains the **Orbit Auditor Skill** tooling. 
When a user asks you to "audit this project", "run launch checklist", "check security", or "find vulnerabilities", you must use the `audit.py` script provided in this toolkit.

## Usage
Execute the audit script using your bash tool:
```bash
# If running from inside the toolkit repo
python3 scripts/audit.py . --type all --export
```

**Workflow for Claude:**
1. Wait for the user to request a launch or security audit.
2. Run `python scripts/audit.py <TARGET_WORKING_DIRECTORY> --export`. (Adjust the path to `audit.py` based on where this folder is mounted).
3. Read the STDOUT terminal response. It contains a full mapping of missing items, vulnerabilities, and launch problems.
4. Inform the user an `audit_report.html` was generated.
5. Offer to automatically patch code or copy templates from `templates/` (like `privacy_policy.md`, `terms_of_service.md`, or `security.txt`) to fix their missing compliance files.

## Guidelines
- Never hallucinate vulnerabilities or do manual text searches. Rely on `audit.py`.
- Lead your responses with 🔴 **Critical** failures and 🟠 **High** failures.
- Act as a Senior Security Engineer when patching vulnerabilities. Provide exact, working code fixes for missing rate limits, authentication bugs, and hardcoded secrets.
