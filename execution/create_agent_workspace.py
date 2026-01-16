#!/usr/bin/env python3
"""
Agent Workspace Generator

Creates a standalone agent workspace in the outputs/ folder with all necessary
files, scripts, and configurations based on the selected agent type.

Usage:
    python create_agent_workspace.py --name "my-agent" --type lead_generation
    python create_agent_workspace.py --name "my-agent" --type custom --additional-scripts script1.py,script2.py
    python create_agent_workspace.py --list-types
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

# Get the directory where this script lives
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
TEMPLATES_FILE = SCRIPT_DIR / "agent_templates.json"
TEMPLATES_DIR = SCRIPT_DIR / "templates"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DIRECTIVES_DIR = PROJECT_ROOT / "directives"
EXECUTION_DIR = PROJECT_ROOT / "execution"


def load_templates() -> dict:
    """Load agent templates configuration."""
    with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def list_agent_types(templates: dict) -> None:
    """Print available agent types."""
    print("\n" + "=" * 60)
    print("AVAILABLE AGENT TYPES")
    print("=" * 60)
    
    for type_key, type_info in templates["agent_types"].items():
        print(f"\n  {type_key}")
        print(f"    Name: {type_info['name']}")
        print(f"    Description: {type_info['description']}")
        print(f"    Directives: {len(type_info['directives'])}")
        scripts = type_info['scripts']
        script_count = "ALL" if scripts == "ALL" else len(scripts)
        print(f"    Scripts: {script_count}")
    
    print("\n" + "=" * 60)


def slugify(name: str) -> str:
    """Convert name to a valid folder name."""
    return name.lower().replace(" ", "-").replace("_", "-")


def create_workspace_structure(workspace_path: Path) -> None:
    """Create the basic folder structure."""
    folders = ["directives", "execution", ".tmp"]
    for folder in folders:
        (workspace_path / folder).mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Created folder structure")


def copy_directives(workspace_path: Path, directive_files: list) -> None:
    """Copy directive files to the new workspace."""
    dest_dir = workspace_path / "directives"
    copied = 0
    for directive in directive_files:
        src = DIRECTIVES_DIR / directive
        if src.exists():
            shutil.copy2(src, dest_dir / directive)
            copied += 1
        else:
            print(f"  ⚠ Directive not found: {directive}")
    print(f"  ✓ Copied {copied} directive(s)")


def copy_scripts(workspace_path: Path, script_files: list | str, all_scripts: bool = False) -> None:
    """Copy execution scripts to the new workspace."""
    dest_dir = workspace_path / "execution"
    copied = 0
    
    if script_files == "ALL" or all_scripts:
        # Copy all Python scripts except the generator itself
        exclude = ["create_agent_workspace.py", "agent_templates.json", "__pycache__"]
        for src in EXECUTION_DIR.glob("*.py"):
            if src.name not in exclude:
                shutil.copy2(src, dest_dir / src.name)
                copied += 1
    else:
        for script in script_files:
            src = EXECUTION_DIR / script
            if src.exists():
                shutil.copy2(src, dest_dir / script)
                copied += 1
            else:
                print(f"  ⚠ Script not found: {script}")
    
    print(f"  ✓ Copied {copied} script(s)")


def generate_agents_md(workspace_path: Path, agent_type: dict, agent_name: str) -> None:
    """Generate customized AGENTS.md for the workspace."""
    template_path = TEMPLATES_DIR / "AGENTS_BASE.md"
    
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # Fallback to reading the main AGENTS.md
        with open(PROJECT_ROOT / "AGENTS.md", "r", encoding="utf-8") as f:
            content = f.read()
    
    # Add agent-specific section
    specialization = f"""

## Agent Specialization

**Type:** {agent_type['name']}

{agent_type['system_prompt_additions']}

### Available Directives
"""
    for directive in agent_type.get('directives', []):
        directive_name = directive.replace('.md', '').replace('_', ' ').title()
        specialization += f"- `directives/{directive}` - {directive_name}\n"
    
    if not agent_type.get('directives'):
        specialization += "- Create your own directives in the `directives/` folder\n"
    
    specialization += """
### Getting Started

1. Copy your Google OAuth credentials (`credentials.json`) to this folder
2. Fill in the `.env` file with your API keys
3. Install dependencies: `pip install -r requirements.txt`
4. Start working with your agent!
"""
    
    # Insert specialization before the Summary section or at the end
    if "## Summary" in content:
        content = content.replace("## Summary", specialization + "\n## Summary")
    else:
        content += specialization
    
    # Update the header
    content = content.replace(
        "# Agent Instructions",
        f"# Agent Instructions - {agent_name}"
    )
    
    with open(workspace_path / "AGENTS.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated AGENTS.md")


def generate_env_example(workspace_path: Path, env_vars: list) -> None:
    """Generate .env.example file."""
    content = """# Environment Variables
# Copy this file to .env and fill in your API keys
# NEVER commit .env to git!

"""
    for var in env_vars:
        content += f"{var}=\n"
    
    if not env_vars:
        content += "# Add your environment variables here\n"
    
    with open(workspace_path / ".env.example", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated .env.example with {len(env_vars)} variable(s)")


def generate_requirements(workspace_path: Path, packages: list) -> None:
    """Generate requirements.txt file."""
    content = "# Auto-generated requirements for this agent workspace\n\n"
    for package in sorted(set(packages)):
        content += f"{package}\n"
    
    with open(workspace_path / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated requirements.txt with {len(packages)} package(s)")


def generate_gitignore(workspace_path: Path) -> None:
    """Generate .gitignore file."""
    content = """# Environment variables and secrets
.env
.env.local
.env.*.local

# Google OAuth credentials
credentials.json
token.json

# Temporary files
.tmp/
*.tmp
*.temp

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/
"""
    
    with open(workspace_path / ".gitignore", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated .gitignore")


def generate_readme(workspace_path: Path, agent_type: dict, agent_name: str) -> None:
    """Generate a README for the new workspace."""
    content = f"""# {agent_name}

> Generated by DOE Framework Agent Workspace Generator

**Type:** {agent_type['name']}

{agent_type['description']}

## Quick Start

1. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Google credentials** (if using Google Sheets):
   - Place `credentials.json` in this folder
   - Run any sheet script once to generate `token.json`

4. **Open in VS Code with GitHub Copilot:**
   - The agent will read `AGENTS.md` automatically
   - Ask the agent to help you with tasks defined in `directives/`

## Structure

```
{agent_name}/
├── AGENTS.md           # System prompt for AI agents
├── .env.example        # Template for API keys
├── requirements.txt    # Python dependencies
├── directives/         # What to do (SOPs)
└── execution/          # How to do it (scripts)
```

## Available Directives

"""
    for directive in agent_type.get('directives', []):
        directive_name = directive.replace('.md', '').replace('_', ' ').title()
        content += f"- [{directive_name}](directives/{directive})\n"
    
    if not agent_type.get('directives'):
        content += "- Create your own directives in `directives/`\n"
    
    content += f"""
## Required API Keys

"""
    for var in agent_type.get('env_vars', []):
        content += f"- `{var}`\n"
    
    if not agent_type.get('env_vars'):
        content += "- Add your own as needed\n"
    
    content += """
---

*This workspace was generated from the [DOE Framework](https://github.com/vjvarada/DOE-Framework-Agentic-AI)*
"""
    
    with open(workspace_path / "README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated README.md")


def create_agent_workspace(
    name: str,
    agent_type: str,
    additional_scripts: Optional[list] = None,
    additional_directives: Optional[list] = None,
    additional_packages: Optional[list] = None
) -> Path:
    """
    Create a complete agent workspace.
    
    Args:
        name: Name for the agent workspace
        agent_type: Type of agent (from templates)
        additional_scripts: Extra scripts to include
        additional_directives: Extra directives to include
        additional_packages: Extra packages to include
    
    Returns:
        Path to the created workspace
    """
    templates = load_templates()
    
    if agent_type not in templates["agent_types"]:
        available = ", ".join(templates["agent_types"].keys())
        raise ValueError(f"Unknown agent type: {agent_type}. Available: {available}")
    
    type_config = templates["agent_types"][agent_type]
    slug = slugify(name)
    workspace_path = OUTPUTS_DIR / slug
    
    # Check if workspace already exists
    if workspace_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        workspace_path = OUTPUTS_DIR / f"{slug}-{timestamp}"
    
    print(f"\n{'=' * 60}")
    print(f"CREATING AGENT WORKSPACE: {name}")
    print(f"Type: {type_config['name']}")
    print(f"Location: {workspace_path}")
    print(f"{'=' * 60}\n")
    
    # Create structure
    create_workspace_structure(workspace_path)
    
    # Copy directives
    directives = type_config.get("directives", []).copy()
    if additional_directives:
        directives.extend(additional_directives)
    copy_directives(workspace_path, directives)
    
    # Copy scripts
    scripts = type_config.get("scripts", [])
    if scripts != "ALL":
        scripts = scripts.copy()
        if additional_scripts:
            scripts.extend(additional_scripts)
    copy_scripts(workspace_path, scripts)
    
    # Generate AGENTS.md
    generate_agents_md(workspace_path, type_config, name)
    
    # Generate .env.example
    generate_env_example(workspace_path, type_config.get("env_vars", []))
    
    # Generate requirements.txt
    packages = type_config.get("packages", []).copy()
    if additional_packages:
        packages.extend(additional_packages)
    generate_requirements(workspace_path, packages)
    
    # Generate .gitignore
    generate_gitignore(workspace_path)
    
    # Generate README
    generate_readme(workspace_path, type_config, name)
    
    print(f"\n{'=' * 60}")
    print(f"✓ WORKSPACE CREATED SUCCESSFULLY!")
    print(f"{'=' * 60}")
    print(f"\nNext steps:")
    print(f"  1. cd {workspace_path}")
    print(f"  2. cp .env.example .env")
    print(f"  3. Edit .env with your API keys")
    print(f"  4. pip install -r requirements.txt")
    print(f"  5. Open in VS Code and start using your agent!")
    print()
    
    return workspace_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate a standalone agent workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_agent_workspace.py --list-types
  python create_agent_workspace.py --name "My Lead Agent" --type lead_generation
  python create_agent_workspace.py --name "Custom Bot" --type custom --additional-scripts enrich_emails.py
        """
    )
    
    parser.add_argument("--list-types", action="store_true", help="List available agent types")
    parser.add_argument("--name", "-n", type=str, help="Name for the agent workspace")
    parser.add_argument("--type", "-t", type=str, help="Type of agent to create")
    parser.add_argument("--additional-scripts", type=str, help="Comma-separated list of additional scripts")
    parser.add_argument("--additional-directives", type=str, help="Comma-separated list of additional directives")
    parser.add_argument("--additional-packages", type=str, help="Comma-separated list of additional packages")
    
    args = parser.parse_args()
    
    templates = load_templates()
    
    if args.list_types:
        list_agent_types(templates)
        return
    
    if not args.name or not args.type:
        parser.print_help()
        print("\nError: --name and --type are required (or use --list-types)")
        sys.exit(1)
    
    # Parse additional items
    additional_scripts = args.additional_scripts.split(",") if args.additional_scripts else None
    additional_directives = args.additional_directives.split(",") if args.additional_directives else None
    additional_packages = args.additional_packages.split(",") if args.additional_packages else None
    
    try:
        create_agent_workspace(
            name=args.name,
            agent_type=args.type,
            additional_scripts=additional_scripts,
            additional_directives=additional_directives,
            additional_packages=additional_packages
        )
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
