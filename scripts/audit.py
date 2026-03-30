#!/usr/bin/env python3
import os
import csv
import re
import argparse
from pathlib import Path

# Fallback for colors if colorama is not installed
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'

SKILL_ROOT = Path(__file__).parent.parent

def load_rules(csv_path):
    rules = []
    if not csv_path.exists():
        return rules
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rules.append(row)
    return rules

def is_ignored(path):
    ignored_dirs = {'.git', 'node_modules', 'dist', 'build', '.next', '.venv', 'venv', '__pycache__'}
    for part in path.parts:
        if part in ignored_dirs:
            return True
    return False

def scan_workspace(directory):
    files_content = {}
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            path = Path(root) / file
            if is_ignored(path.relative_to(directory)):
                continue
            try:
                rel_path = str(path.relative_to(directory))
                file_paths.append(rel_path)
                # limit size constraints
                if path.stat().st_size < 500000:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        files_content[rel_path] = f.read()
            except Exception:
                pass
    return file_paths, files_content

def check_rule(rule, file_paths, files_content):
    pattern = rule.get('scan_pattern', '')
    if not pattern or pattern == 'manual':
        return {"status": "manual", "matches": []}
    
    matches = []
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error:
        return {"status": "error", "matches": []}

    for path in file_paths:
        if regex.search(path):
            matches.append(path)
            
    for path, content in files_content.items():
        if len(matches) > 5: break
        if path not in matches and regex.search(content):
            matches.append(path)
            
    if matches:
        return {"status": "pass", "matches": matches[:3]}
    else:
        return {"status": "fail", "matches": []}

def format_html_report(launch_results, security_results):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Launch & Security Audit Report</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 40px auto; max-width: 1000px; line-height: 1.6; color: #333; background: #fafafa; }
            h1 { color: #111; border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }
            h2 { color: #333; margin-top: 40px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }
            th, td { padding: 14px 16px; border-bottom: 1px solid #f0f0f0; text-align: left; }
            th { background-color: #f8f9fa; font-weight: 600; color: #555; }
            tr:last-child td { border-bottom: none; }
            .pass { color: #166534; background: #dcfce7; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8em; }
            .fail { color: #991b1b; background: #fee2e2; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8em; }
            .manual { color: #854d0e; background: #fef08a; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8em; }
            .severity-Critical { color: #dc2626; font-weight: bold; }
            .severity-High { color: #ea580c; font-weight: bold; }
            .severity-Medium { color: #ca8a04; }
            .severity-Low { color: #16a34a; }
            .notes { color: #666; font-size: 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
        </style>
    </head>
    <body>
        <h1>🚀 Launch & Security Audit Report</h1>
    """
    
    if launch_results:
        html += "<h2>Launch Readiness Checklist</h2><table><tr><th>Item</th><th>Severity</th><th>Status</th><th>Notes (Matches)</th></tr>"
        for res in launch_results:
            rule = res['rule']
            status_class = res['status']
            status_text = res['status'].upper()
            notes = ", ".join(res['matches']) if res['matches'] else ""
            html += f"<tr><td>{rule['item']}</td><td class='severity-{rule['severity']}'>{rule['severity']}</td><td><span class='{status_class}'>{status_text}</span></td><td class='notes'>{notes}</td></tr>"
        html += "</table>"
        
    if security_results:
        html += "<h2>Security Hardening Audit</h2><table><tr><th>Domain</th><th>Check</th><th>Severity</th><th>Status</th><th>Notes (Matches)</th></tr>"
        for res in security_results:
            rule = res['rule']
            status_class = res['status']
            status_text = res['status'].upper()
            notes = ", ".join(res['matches']) if res['matches'] else ""
            html += f"<tr><td>{rule['domain']}</td><td>{rule['check']}</td><td class='severity-{rule['severity']}'>{rule['severity']}</td><td><span class='{status_class}'>{status_text}</span></td><td class='notes'>{notes}</td></tr>"
        html += "</table>"
        
    html += "</body></html>"
    return html

def run_audit(target_dir, args):
    launch_rules = load_rules(SKILL_ROOT / 'data' / 'launch_rules.csv')
    security_rules = load_rules(SKILL_ROOT / 'data' / 'security_rules.csv')
    
    print(f"{Colors.CYAN}Scanning workspace at: {target_dir}{Colors.RESET}")
    file_paths, files_content = scan_workspace(target_dir)
    print(f"Indexed {len(files_content)} files.\n")
    
    launch_results = []
    security_results = []
    
    if args.type in ['all', 'launch']:
        print(f"{Colors.MAGENTA}=== Launch Readiness Phase ==={Colors.RESET}")
        pts = 0; max_pts = 0
        for rule in launch_rules:
            res = check_rule(rule, file_paths, files_content)
            launch_results.append({"rule": rule, "status": res['status'], "matches": res['matches']})
            if res['status'] == 'pass':
                print(f"[{Colors.GREEN}OK{Colors.RESET}] {rule['item']}")
                pts += 1
                max_pts += 1
            elif res['status'] == 'fail':
                print(f"[{Colors.RED}FAIL{Colors.RESET}] {rule['item']} {Colors.RED}({rule['severity']}){Colors.RESET}")
                max_pts += 1
            elif res['status'] == 'manual':
                print(f"[{Colors.YELLOW}MANUAL{Colors.RESET}] {rule['item']}")
        if max_pts > 0:
            print(f"\n{Colors.MAGENTA}Launch Score: {int((pts/max_pts)*100)}% ({pts}/{max_pts}){Colors.RESET}\n")

    if args.type in ['all', 'security']:
        print(f"{Colors.MAGENTA}=== Security Hardening Phase ==={Colors.RESET}")
        for rule in security_rules:
            res = check_rule(rule, file_paths, files_content)
            security_results.append({"rule": rule, "status": res['status'], "matches": res['matches']})
            if res['status'] == 'pass':
                print(f"[{Colors.GREEN}OK{Colors.RESET}] {rule['check']}")
            elif res['status'] == 'fail':
                print(f"[{Colors.RED}FAIL{Colors.RESET}] {rule['check']} {Colors.RED}({rule['severity']}){Colors.RESET}")
            elif res['status'] == 'manual':
                print(f"[{Colors.YELLOW}MANUAL{Colors.RESET}] {rule['check']}")

    if args.export:
        html = format_html_report(launch_results, security_results)
        export_path = Path("audit_report.html")
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n{Colors.GREEN}✨ Professional HTML report exported to {export_path.absolute()}{Colors.RESET}")

    print(f"\n{Colors.CYAN}Audit execution complete.{Colors.RESET}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch & Security Auditor (Pro-Max)')
    parser.add_argument('dir', nargs='?', default='.', help='Directory to scan')
    parser.add_argument('--type', choices=['all', 'launch', 'security'], default='all', help='Which audit to run')
    parser.add_argument('--export', action='store_true', help='Export HTML report')
    args = parser.parse_args()
    
    run_audit(Path(args.dir).absolute(), args)
