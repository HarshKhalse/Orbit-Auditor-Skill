# 🚀 Orbit Auditor Skill

A dual-phase Launch Readiness & Security Hardening toolkit designed specifically to act as an open-source "Skill" for AI Agents (Cursor, Claude, Gemini).

If you ask an AI to "check my security" using a standard text prompt, it will hallucinate bugs or simply guess. **Orbit Auditor** gives your AI a real software tool (`audit.py`) with a dedicated vulnerability database to execute lightning-fast deterministic scans across 10,000 files in milliseconds. 

If you are a Developer, you can also just run it yourself!

---

## 🔥 Features
* **Automated Python Scanning Engine**: Instantly regex-parses workspaces, bypassing slow, manual AI hallucination.
* **Dual Reporting**: Exports a beautiful `audit_report.html` file covering:
  - 1. Launch Readiness (SEO, Privacy, ToS, App Store limits)
  - 2. Security Hardening (Authentication, IDOR, Rate Limiting, Secrets)
* **Agent Auto-Fixes**: The toolkit includes raw markdown templates for legal compliance. When the AI detects you missing a `security.txt` or a `privacy_policy.md`, it injects these right into your repository for you.
* **Multi-Agent Compatibility**: Drop-in ready for `.cursorrules`, `CLAUDE.md`, and AntiGravity `SKILL.md`.

---

## 💻 Installation & Usage

### Method 1: Use it via AI (Cursor, Claude, Gemini)
1. Clone this repository into your project root (or inside `.cursor/skills/`).
2. The AI will automatically read `.cursorrules` or `CLAUDE.md`.
3. Just ask your AI: *"Run a full launch audit"* or *"Act as a senior security engineer and scan my app"*.
4. Your AI will execute `python scripts/audit.py . --export` in its hidden terminal, summarize the results, and patch your code!

### Method 2: Use it as a Developer Toolkit (CLI)
You don't need an AI to use the engine!
```bash
git clone https://github.com/HarshKhalse/Orbit-Auditor-Skill.git
cd Orbit-Auditor-Skill
python3 scripts/audit.py <TARGET_DIRECTORY> --type all --export
```
*Tip: Adjust the target directory to scan any project on your machine.*

---

## 🛠️ Why use this instead of a "Skill Creator"?
Most custom AI skills rely exclusively on Prompt Engineering (Markdown guidelines). When an AI reads 100 pages of prompt rules, its context window rapidly drains, and it fails at consistently parsing huge codebases.

**Orbit Auditor is the "Pro-Max" tier of skills**. Instead of forcing an LLM to manually read 100,000 lines of your code, we provide the AI with a deterministic Python script. The AI runs the script, parses the terminal STDOUT output, and only takes action where it matters. It is significantly faster, cheaper, and more reliable.

---

## 🤝 Contributing
Want to add more security rules? Better SEO checks? 
1. Fork the repo.
2. Edit `data/launch_rules.csv` or `data/security_rules.csv`.
3. Submit a Pull Request! We welcome all contributions to expand the toolkit's capabilities.

*Created by [Harsh Khalse](https://github.com/HarshKhalse) under the MIT License.*
