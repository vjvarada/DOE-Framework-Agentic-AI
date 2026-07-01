#!/usr/bin/env python3
"""
Agent Validator

Validates an agent workspace against CommandCenter agent-repo
compatibility standards. Reports issues and compliance status.

Usage:
    python validate_agent.py --path /path/to/agent
    python validate_agent.py --path /path/to/agent --json
"""

import sys
import json
import argparse
from pathlib import Path


REQUIRED_FILES = [
    "agents.py",
    "config.json",
    "AGENTS.md",
    "instructions.md",
    "pyproject.toml",
    ".github/prompts/system.md",
    ".github/copilot-instructions.md",
    ".gitignore",
    ".env.example",
    "tests/test_agents.py",
    "agent-data/INDEX.md",
]

REQUIRED_DIRS = [
    ".github/skills",
    ".tmp/scripts",
    "agent-data",
    "inputs",
    "outputs",
    "tests",
]

OPTIONAL_FILES = [
    ".github/agents/",  # at least one .agent.md
    "setup.ps1",
    "setup.sh",
    "README.md",
]


def validate_workspace(ws: Path) -> dict:
    """Validate workspace and return results dict."""
    results = {
        "path": str(ws),
        "name": ws.name,
        "exists": ws.exists(),
        "required_files": {},
        "required_dirs": {},
        "optional_files": {},
        "config_valid": False,
        "agents_py_valid": False,
        "errors": [],
        "warnings": [],
        "compliant": False,
    }

    if not ws.exists():
        results["errors"].append("Workspace path does not exist")
        return results

    # Check required files
    for f in REQUIRED_FILES:
        exists = (ws / f).exists()
        results["required_files"][f] = exists
        if not exists:
            results["errors"].append(f"Missing required file: {f}")

    # Check required dirs
    for d in REQUIRED_DIRS:
        exists = (ws / d).is_dir()
        results["required_dirs"][d] = exists
        if not exists:
            results["errors"].append(f"Missing required directory: {d}")

    # Check optional files
    for f in OPTIONAL_FILES:
        if f.endswith("/"):
            # Check if directory has at least one matching file
            d = ws / f
            exists = d.is_dir() and any(d.iterdir())
        else:
            exists = (ws / f).exists()
        results["optional_files"][f] = exists
        if not exists:
            results["warnings"].append(f"Missing optional file: {f}")

    # Validate config.json
    config_path = ws / "config.json"
    if config_path.exists():
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            # Check required fields
            for field in ["name", "description", "integrations", "tags",
                          "max_mutation_attempts"]:
                if field not in cfg:
                    results["errors"].append(
                        f"config.json missing field: {field}")

            # Check max_mutation_attempts is 1
            if cfg.get("max_mutation_attempts") != 1:
                results["errors"].append(
                    "config.json: max_mutation_attempts must be 1")

            # Check name format
            name = cfg.get("name", "")
            import re
            if not re.match(r'^[a-z0-9][a-z0-9-]{0,48}[a-z0-9]$', name):
                results["warnings"].append(
                    f"config.json: name '{name}' may not match "
                    f"required pattern")

            # Check name doesn't look like a repo-prefixed slug
            # (e.g., "agent-lead-generation" should just be "lead-generation")
            # But "agent-creator" as a compound name is fine
            prefix_parts = name.split("-")
            if prefix_parts[0] == "agent" and len(prefix_parts) >= 3:
                results["warnings"].append(
                    f"config.json: name '{name}' may include "
                    f"'agent-' repo prefix — consider shortening")

            results["config_valid"] = True
        except json.JSONDecodeError as e:
            results["errors"].append(f"config.json is invalid JSON: {e}")

    # Validate agents.py exports build_agents
    agents_py = ws / "agents.py"
    if agents_py.exists():
        content = agents_py.read_text(encoding="utf-8", errors="replace")
        if "def build_agents()" not in content:
            results["errors"].append(
                "agents.py: missing build_agents() function")
        if "def build_agent()" not in content:
            results["warnings"].append(
                "agents.py: missing build_agent() function")
        if "GitHubCopilotAgent" not in content:
            results["warnings"].append(
                "agents.py: may not use GitHubCopilotAgent")
        if "SYSTEM_PROMPT" not in content:
            results["warnings"].append(
                "agents.py: missing SYSTEM_PROMPT constant")
        results["agents_py_valid"] = True

    # Check .github/skills has at least one SKILL.md
    skills_dir = ws / ".github" / "skills"
    if skills_dir.is_dir():
        skill_mds = list(skills_dir.glob("*/SKILL.md"))
        if not skill_mds:
            results["warnings"].append(
                ".github/skills/: no SKILL.md files found")
    else:
        results["errors"].append(".github/skills/ directory missing")

    # Determine compliance
    results["compliant"] = (
        len(results["errors"]) == 0
        and results["config_valid"]
        and results["agents_py_valid"]
    )

    return results


def print_results(results: dict, json_output: bool = False) -> None:
    """Print validation results."""
    if json_output:
        print(json.dumps(results, indent=2))
        return

    print(f"\nAgent: {results['name']}")
    print(f"Path: {results['path']}")
    print(f"\n{'=' * 50}")

    if results["errors"]:
        print(f"\n❌ ERRORS ({len(results['errors'])}):")
        for e in results["errors"]:
            print(f"  ✗ {e}")

    if results["warnings"]:
        print(f"\n⚠ WARNINGS ({len(results['warnings'])}):")
        for w in results["warnings"]:
            print(f"  ⚠ {w}")

    print(f"\n{'=' * 50}")
    print("Required Files:")
    for f, present in results["required_files"].items():
        print(f"  {'✓' if present else '✗'} {f}")

    print("\nRequired Directories:")
    for d, present in results["required_dirs"].items():
        print(f"  {'✓' if present else '✗'} {d}")

    print(f"\n{'=' * 50}")
    if results["compliant"]:
        print("✓ AGENT IS COMPLIANT with CommandCenter standards.")
    else:
        print("✗ AGENT IS NOT COMPLIANT. Fix errors above.")
        if not results["config_valid"]:
            print("  → config.json needs fixing")
        if not results["agents_py_valid"]:
            print("  → agents.py needs fixing")

    sys.exit(0 if results["compliant"] else 1)


def main():
    parser = argparse.ArgumentParser(
        description="Validate agent against CommandCenter standards")
    parser.add_argument("--path", required=True,
                        help="Path to agent workspace")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    args = parser.parse_args()

    ws = Path(args.path).resolve()
    results = validate_workspace(ws)
    print_results(results, json_output=args.json)


if __name__ == "__main__":
    main()
