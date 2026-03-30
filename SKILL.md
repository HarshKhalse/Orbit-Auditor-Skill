---
name: orbit-auditor-skill
description: >
  Run a full app/website launch readiness audit AND a comprehensive security audit using a custom Python scanning toolkit. 
  Use this skill whenever a user mentions "launch checklist", "ready to launch", "pre-launch
  audit", "security audit", "check my auth", "IDOR", "rate limiting", "secrets scan", 
  "pentest", "vulnerability scan", etc.
  The skill uses a local script `audit.py` to scan the project accurately and outputs a rich HTML report.
---

# Orbit Auditor Skill

A fully automated, two-phase pre-launch system powered by a custom Python scanning toolkit.
Instead of manually guessing patterns, this skill uses its native `audit.py` engine to scan for launch readiness and security misconfigurations.

## Using the Toolkit

This skill is bundled with an automated scanning script containing rulesets for both Product Launch Readiness and Security Hardening. 

**Workflow:**
1. **Find the Tool**: The toolkit is located in the `orbit-auditor-skill` directory (usually located wherever this SKILL.md file resides).
2. **Execute the Scan**: Open the user's workspace directory and run the audit script using your command runner tool. Ensure you use the exact path to `orbit-auditor-skill\scripts\audit.py`:
   - For a full audit: `python "/path/to/orbit-auditor-skill/scripts/audit.py" . --type all --export`
   - For launch focus: `python "/path/to/orbit-auditor-skill/scripts/audit.py" . --type launch --export`
   - For security focus: `python "/path/to/orbit-auditor-skill/scripts/audit.py" . --type security --export`
3. **Parse the Results**: 
   - The script will output raw findings into the terminal context.
   - An `audit_report.html` will be generated in the user's root folder.
4. **Offer Auto-Fixes**: 
   - You act as a Senior Security Engineer. Read the terminal output.
   - For missing legal/compliance files (Privacy Policy, ToS, security.txt), read the standard templates from the `templates/` directory and implement them for the user.
   - For code-level security issues (missing Helmet, hardcoded secrets, lack of rate-limits), immediately apply code patches using your file editing tools to fix the problems.

## Core Rules
- **Do not manually search the whole codebase linearly**. Rely on the `audit.py` script output. It already performs AST size constraints, regex grouping, and directory exclusions.
- Lead with 🔴 **Critical** failures and 🟠 **High** failures.
- Be direct, specific, and patch the problems immediately if the user allows.
