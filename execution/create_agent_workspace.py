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
    folders = ["directives", "execution", "memory", ".tmp", ".github/agents", ".vscode"]
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
        # Also copy tool_registry.json
        reg_src = EXECUTION_DIR / "tool_registry.json"
        if reg_src.exists():
            shutil.copy2(reg_src, dest_dir / "tool_registry.json")
            copied += 1
    else:
        for script in script_files:
            src = EXECUTION_DIR / script
            if src.exists():
                shutil.copy2(src, dest_dir / script)
                copied += 1
            else:
                print(f"  ⚠ Script not found: {script}")
        # Always copy tool_registry.json if tool_registry.py is included
        if "tool_registry.py" in script_files:
            reg_src = EXECUTION_DIR / "tool_registry.json"
            if reg_src.exists():
                shutil.copy2(reg_src, dest_dir / "tool_registry.json")
                copied += 1
    
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
    
    content += "\n# Memory system guardrail thresholds (optional)\n"
    content += "# DAILY_COST_BUDGET_USD=10.0\n"
    content += "# MAX_TOKENS_PER_TASK=100000\n"
    content += "# EMBEDDING_MODEL=all-MiniLM-L6-v2\n"
    
    with open(workspace_path / ".env.example", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated .env.example with {len(env_vars)} variable(s)")


def generate_requirements(workspace_path: Path, packages: list) -> None:
    """Generate requirements.txt file."""
    content = "# Auto-generated requirements for this agent workspace\n\n"
    for package in sorted(set(packages)):
        content += f"{package}\n"
    content += "\n# Optional: Enables semantic/hybrid search in memory system\n"
    content += "# sentence-transformers\n"
    
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

# Memory database (regenerated, contains local state)
memory/*.db
memory/*.db-wal
memory/*.db-shm

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

# Don't ignore .vscode - we want the settings
!.vscode/
"""
    
    with open(workspace_path / ".gitignore", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated .gitignore")


def generate_setup_script(workspace_path: Path, agent_name: str, packages: list) -> None:
    """
    Generate setup.ps1 script for one-command environment setup.
    
    This script:
    - Creates Python virtual environment
    - Installs all requirements
    - Copies .env.example to .env if not exists
    - Validates the setup
    """
    content = f'''# {agent_name} - Automated Setup Script
# Run this script to set up the agent environment from scratch
# Usage: .\\setup.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Setting up: {agent_name}" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python is installed
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {{
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}}
Write-Host "✓ Found $pythonVersion" -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {{
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {{
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }}
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}} else {{
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\\.venv\\Scripts\\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {{
    pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -ne 0) {{
        Write-Host "ERROR: Failed to install requirements" -ForegroundColor Red
        exit 1
    }}
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
}} else {{
    Write-Host "WARNING: requirements.txt not found" -ForegroundColor Yellow
}}

# Copy .env.example to .env if .env doesn't exist
if (-not (Test-Path ".env")) {{
    if (Test-Path ".env.example") {{
        Copy-Item ".env.example" ".env"
        Write-Host "✓ Created .env from .env.example" -ForegroundColor Green
        Write-Host "  IMPORTANT: Edit .env with your API keys!" -ForegroundColor Yellow
    }}
}} else {{
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}}

# Create .tmp directory if it doesn't exist
if (-not (Test-Path ".tmp")) {{
    New-Item -ItemType Directory -Path ".tmp" | Out-Null
    Write-Host "✓ Created .tmp directory" -ForegroundColor Green
}}

# Create memory directory if it doesn't exist
if (-not (Test-Path "memory")) {{
    New-Item -ItemType Directory -Path "memory" | Out-Null
    Write-Host "✓ Created memory directory" -ForegroundColor Green
}}

# Initialize memory database
Write-Host "Initializing memory database..." -ForegroundColor Yellow
python execution/memory_db.py status 2>$null
if ($LASTEXITCODE -eq 0) {{
    Write-Host "✓ Memory database initialized" -ForegroundColor Green
}} else {{
    Write-Host "WARNING: Memory database initialization skipped (run manually)" -ForegroundColor Yellow
}}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "✓ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Edit .env with your API keys (if any required)" -ForegroundColor White
Write-Host "  2. Open this folder in VS Code" -ForegroundColor White
Write-Host "  3. Select '{agent_name}' from Copilot Chat agent dropdown" -ForegroundColor White
Write-Host ""
Write-Host "To activate the environment manually:" -ForegroundColor Gray
Write-Host "  .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Gray
Write-Host ""
'''
    
    with open(workspace_path / "setup.ps1", "w", encoding="utf-8") as f:
        f.write(content)
    
    # Also create a bash script for Unix systems
    bash_content = f'''#!/bin/bash
# {agent_name} - Automated Setup Script
# Run this script to set up the agent environment from scratch
# Usage: ./setup.sh

echo "============================================"
echo "Setting up: {agent_name}"
echo "============================================"
echo ""

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi
echo "✓ Found $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install requirements
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo "✓ Dependencies installed"
else
    echo "WARNING: requirements.txt not found"
fi

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ Created .env from .env.example"
        echo "  IMPORTANT: Edit .env with your API keys!"
    fi
else
    echo "✓ .env file already exists"
fi

# Create .tmp directory if it doesn't exist
mkdir -p .tmp
echo "✓ Created .tmp directory"

# Create memory directory and initialize database
mkdir -p memory
echo "✓ Created memory directory"
python execution/memory_db.py status >/dev/null 2>&1 && echo "✓ Memory database initialized" || echo "WARNING: Memory DB init skipped"

echo ""
echo "============================================"
echo "✓ SETUP COMPLETE!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys (if any required)"
echo "  2. Open this folder in VS Code"
echo "  3. Select '{agent_name}' from Copilot Chat agent dropdown"
echo ""
echo "To activate the environment manually:"
echo "  source .venv/bin/activate"
echo ""
'''
    
    with open(workspace_path / "setup.sh", "w", encoding="utf-8", newline='\n') as f:
        f.write(bash_content)
    
    print(f"  ✓ Generated setup.ps1 and setup.sh (one-command setup)")


def generate_vscode_tasks(workspace_path: Path, agent_name: str) -> None:
    """
    Generate .vscode/tasks.json for automated setup and common operations.
    """
    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Setup Agent Environment",
                "type": "shell",
                "command": ".\\setup.ps1",
                "windows": {
                    "command": "powershell",
                    "args": ["-ExecutionPolicy", "Bypass", "-File", ".\\setup.ps1"]
                },
                "linux": {
                    "command": "bash",
                    "args": ["./setup.sh"]
                },
                "osx": {
                    "command": "bash",
                    "args": ["./setup.sh"]
                },
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                },
                "runOptions": {
                    "runOn": "folderOpen"
                },
                "problemMatcher": []
            },
            {
                "label": "Activate Virtual Environment",
                "type": "shell",
                "command": ".venv\\Scripts\\Activate.ps1",
                "windows": {
                    "command": "powershell",
                    "args": ["-ExecutionPolicy", "Bypass", "-Command", "& .venv\\Scripts\\Activate.ps1"]
                },
                "presentation": {
                    "reveal": "always",
                    "panel": "shared"
                },
                "problemMatcher": []
            },
            {
                "label": "Install Requirements",
                "type": "shell",
                "command": "pip install -r requirements.txt",
                "dependsOn": "Activate Virtual Environment",
                "presentation": {
                    "reveal": "always",
                    "panel": "shared"
                },
                "problemMatcher": []
            }
        ]
    }
    
    tasks_path = workspace_path / ".vscode" / "tasks.json"
    with open(tasks_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)
    
    print(f"  ✓ Generated .vscode/tasks.json (build tasks with auto-run on open)")


def generate_vscode_workspace_file(workspace_path: Path, agent_name: str, slug: str) -> None:
    """
    Generate a .code-workspace file for easy VS Code opening.
    
    Benefits:
    - Double-click to open VS Code with correct folder
    - All settings pre-loaded
    - Tasks auto-run on open (after user trusts workspace)
    - Custom agent immediately available
    """
    workspace_config = {
        "folders": [
            {
                "path": "."
            }
        ],
        "settings": {
            # Python settings
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
            "python.terminal.activateEnvironment": True,
            "python.analysis.autoImportCompletions": True,
            "python.analysis.typeCheckingMode": "basic",
            
            # Copilot settings
            "github.copilot.enable": {
                "*": True,
                "plaintext": True,
                "markdown": True,
                "python": True
            },
            
            # Editor settings
            "editor.formatOnSave": True,
            
            # Terminal settings
            "terminal.integrated.defaultProfile.windows": "PowerShell",
            "terminal.integrated.cwd": "${workspaceFolder}",
            
            # Search exclusions
            "search.exclude": {
                "**/.tmp": True,
                "**/__pycache__": True,
                "**/.venv": True
            },
            
            # Trust this workspace to allow auto-run tasks
            "task.allowAutomaticTasks": "on"
        },
        "extensions": {
            "recommendations": [
                "GitHub.copilot",
                "GitHub.copilot-chat",
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.debugpy"
            ]
        },
        "launch": {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Current File",
                    "type": "debugpy",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    }
                }
            ]
        }
    }

    workspace_file_path = workspace_path / f"agent-{slug}.code-workspace"
    with open(workspace_file_path, "w", encoding="utf-8") as f:
        json.dump(workspace_config, f, indent=2)

    print(f"  ✓ Generated agent-{slug}.code-workspace (double-click to open VS Code)")


def generate_readme(workspace_path: Path, agent_type: dict, agent_name: str) -> None:
    """Generate a README for the new workspace."""
    slug = slugify(agent_name)
    content = f"""# {agent_name}

> Generated by DOE Framework Agent Workspace Generator

**Type:** {agent_type['name']}

{agent_type['description']}

## 🚀 Instant Start

**Just double-click:** `agent-{slug}.code-workspace`

VS Code will automatically:
1. Open the workspace
2. Prompt to trust the folder (click **Yes**)
3. Run setup (creates venv, installs dependencies)
4. Prompt to install recommended extensions

Then select **"{agent_name}"** from the Copilot Chat agent dropdown and start working!

## Alternative: Manual Setup

**Windows (PowerShell):**
```powershell
.\\setup.ps1
```

**macOS/Linux:**
```bash
chmod +x setup.sh && ./setup.sh
```

This automatically:
- ✅ Creates Python virtual environment
- ✅ Installs all dependencies
- ✅ Copies `.env.example` to `.env`
- ✅ Creates `.tmp/` directory

## Manual Setup (Alternative)

1. **Create and activate virtual environment:**
   ```powershell
   python -m venv .venv
   .\\.venv\\Scripts\\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```powershell
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Using the Agent

1. **Open in VS Code** - The custom agent is pre-configured
2. **Open Copilot Chat** - Press `Ctrl+Shift+I`
3. **Select your agent** - Choose "{agent_name}" from the agent dropdown
4. **Start working** - The agent knows the directives and scripts available

## VS Code Tasks (Optional)

Press `Ctrl+Shift+B` to run the default build task (Setup Agent Environment).

Other tasks available:
- **Setup Agent Environment** - Full one-command setup
- **Activate Virtual Environment** - Activate .venv
- **Install Requirements** - Install/update dependencies

## Structure

```
{agent_name}/
├── agent-{slug}.code-workspace # ← Double-click to open VS Code!
├── setup.ps1 / setup.sh  # One-command setup scripts
├── AGENTS.md             # System prompt for AI agents
├── .env.example          # Template for API keys
├── requirements.txt      # Python dependencies
├── .github/agents/       # VS Code custom agent config
├── .vscode/              # VS Code settings & tasks
├── memory/               # Persistent memory database (auto-created)
├── directives/           # What to do (SOPs)
└── execution/            # How to do it (scripts)
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
        content += "- None required for this agent type\n"
    
    content += """
## Google Credentials (if using Google Sheets)

If your agent uses Google Sheets scripts:
1. Place `credentials.json` in this folder
2. Run any sheet script once to generate `token.json`

---

*This workspace was generated from the [DOE Framework](https://github.com/vjvarada/DOE-Framework-Agentic-AI)*
"""
    
    with open(workspace_path / "README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated README.md")


def generate_custom_agent_file(workspace_path: Path, agent_type: dict, agent_name: str, slug: str) -> None:
    """
    Generate a VS Code custom agent file (.agent.md) in .github/agents/.
    
    This creates a ready-to-use custom agent for GitHub Copilot that users can
    immediately switch to in VS Code without any manual configuration.
    """
    # Get Copilot tools for this agent type
    tools = agent_type.get('copilot_tools', ['search', 'fetch', 'terminal', 'editFiles'])
    tools_str = str(tools).replace("'", '"')  # Convert to JSON-style array
    
    # Build the agent file content with YAML frontmatter
    content = f"""---
description: {agent_type['description']}
name: {agent_name}
tools: {tools_str}
---
# {agent_name}

{agent_type['system_prompt_additions']}

## Operating Framework

You operate within the **DOE Framework** (Directive, Orchestration, Execution):

1. **Directives** (`directives/`): SOPs in Markdown that define WHAT to do
2. **Orchestration** (You): Read directives, make routing decisions, call execution scripts
3. **Execution** (`execution/`): Deterministic Python scripts that do the actual work

## Core Principles

1. **Check for existing tools first** - Before writing a script, check `execution/` for existing solutions
2. **Self-anneal when things break** - Fix errors, update scripts, test, and document learnings in directives
3. **Reserve LLM for judgment** - Use scripts for mechanical operations; they're faster and deterministic
4. **Use memory across sessions** - Read working memory at session start. Store learnings after. See below.

## Memory System (Dual-Tier)

**Tier 1 — Working Memory** (JSON/Markdown, loaded at session start):
```bash
python execution/memory_bank.py --read all            # Load everything
python execution/memory_bank.py --update context --key "stage" --value "active"
python execution/memory_bank.py --log-interaction --summary "..."
python execution/memory_bank.py --log-decision --decision "..." --context "..."
python execution/memory_bank.py --add-insight "Lesson learned..."
python execution/memory_bank.py --search "keyword"
```

**Tier 2 — Long-Term Memory** (SQLite FTS, queried on demand):
```bash
python execution/memory_db.py search "<keywords>"     # Search deep history
python execution/memory_db.py add-fact "..." --category x
python execution/memory_db.py add-insight "..."
```

**Session Protocol:**
1. Before every task: `memory_bank.py --read all` + `memory_db.py search "<task keywords>"`
2. During tasks: Update memory immediately when new info arrives (don't wait until end)
3. After tasks: Log interaction, store facts/insights, update context

For full memory management details, see `directives/memory_management.md`.

## Available Resources

**Directives (SOPs):**
"""
    
    # List directives
    for directive in agent_type.get('directives', []):
        directive_name = directive.replace('.md', '').replace('_', ' ').title()
        content += f"- `directives/{directive}` - {directive_name}\n"
    
    if not agent_type.get('directives'):
        content += "- Create your own directives in `directives/`\n"
    
    content += """
**Key Files:**
- `AGENTS.md` - Full system prompt and framework details
- `.env` - API keys (copy from `.env.example`)
- `requirements.txt` - Python dependencies

## Workflow

When given a task:
1. Check if a relevant directive exists in `directives/`
2. Read the directive to understand the process
3. Execute the appropriate scripts from `execution/`
4. Handle errors by fixing and documenting
5. Return deliverables (usually Google Sheet URLs or file outputs)

For detailed instructions, read the `AGENTS.md` file in this workspace.
"""
    
    agent_file_path = workspace_path / ".github" / "agents" / f"{slug}.agent.md"
    with open(agent_file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✓ Generated custom agent file: .github/agents/{slug}.agent.md")


def generate_vscode_settings(workspace_path: Path, agent_name: str, slug: str) -> None:
    """
    Generate .vscode/settings.json with Copilot and Python configurations.
    
    This ensures:
    - The custom agent is set as the default
    - Python environment is configured
    - Copilot has access to workspace files
    - File associations are set up
    """
    settings = {
        "// DOE Framework Agent Workspace Settings": "",
        "// Generated automatically - customize as needed": "",
        
        # Python settings
        "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
        "python.terminal.activateEnvironment": True,
        "python.analysis.autoImportCompletions": True,
        "python.analysis.typeCheckingMode": "basic",
        
        # Copilot settings - enable all features
        "github.copilot.enable": {
            "*": True,
            "plaintext": True,
            "markdown": True,
            "python": True
        },
        "github.copilot.chat.codesearch.enabled": True,
        
        # Editor settings for agent workflows
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        },
        
        # File associations
        "files.associations": {
            "*.agent.md": "markdown",
            ".env.example": "dotenv",
            ".env": "dotenv"
        },
        
        # Terminal settings
        "terminal.integrated.defaultProfile.windows": "PowerShell",
        "terminal.integrated.cwd": "${workspaceFolder}",
        
        # Search exclusions (don't search in temp files)
        "search.exclude": {
            "**/.tmp": True,
            "**/__pycache__": True,
            "**/.venv": True
        }
    }
    
    settings_path = workspace_path / ".vscode" / "settings.json"
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    
    print(f"  ✓ Generated .vscode/settings.json")


def generate_vscode_extensions(workspace_path: Path) -> None:
    """
    Generate .vscode/extensions.json with recommended extensions.
    
    This prompts users to install necessary extensions when opening the workspace.
    """
    extensions = {
        "recommendations": [
            # Essential for Copilot agent functionality
            "GitHub.copilot",
            "GitHub.copilot-chat",
            
            # Python development
            "ms-python.python",
            "ms-python.vscode-pylance",
            
            # Helpful for agent workflows
            "ms-python.debugpy",
            "esbenp.prettier-vscode",
            "redhat.vscode-yaml",
            "DotJoshJohnson.xml"
        ],
        "unwantedRecommendations": []
    }
    
    extensions_path = workspace_path / ".vscode" / "extensions.json"
    with open(extensions_path, "w", encoding="utf-8") as f:
        json.dump(extensions, f, indent=2)
    
    print(f"  ✓ Generated .vscode/extensions.json (recommended extensions)")


def initialize_memory(workspace_path: Path) -> None:
    """
    Initialize the memory directory with default working memory files.
    
    Creates empty JSON files and a starter insights.md so agents have
    working memory (Tier 1) ready from first use.
    """
    memory_dir = workspace_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    default_files = {
        "context.json": {},
        "interaction_log.json": {"interactions": [], "total_interactions": 0},
        "decision_journal.json": {"decisions": [], "total_decisions": 0},
    }
    
    created = 0
    for filename, default_content in default_files.items():
        filepath = memory_dir / filename
        if not filepath.exists():
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default_content, f, indent=2)
            created += 1
    
    # Create insights.md
    insights_path = memory_dir / "insights.md"
    if not insights_path.exists():
        with open(insights_path, "w", encoding="utf-8") as f:
            f.write("# Accumulated Insights\n\n_Lessons learned, patterns observed, and wisdom collected over time._\n\n")
        created += 1
    
    print(f"  ✓ Initialized memory/ with {created} working memory file(s)")


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
    # ── agent-* naming convention ─────────────────────────────────────────
    # Folder/repo name always gets the "agent-" prefix per DOE Framework
    # convention. The bare slug (without prefix) is used for config.json
    # name, .agent.md filename, and internal references.
    agent_folder = f"agent-{slug}"
    workspace_path = OUTPUTS_DIR / agent_folder
    
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
    
    # Copy directives (always include memory_management and infrastructure_tools)
    directives = type_config.get("directives", []).copy()
    for infra_dir in ["memory_management.md", "infrastructure_tools.md"]:
        if infra_dir not in directives:
            directives.append(infra_dir)
    if additional_directives:
        directives.extend(additional_directives)
    copy_directives(workspace_path, directives)
    
    # Copy scripts (always include memory_db and infrastructure tools)
    scripts = type_config.get("scripts", [])
    if scripts != "ALL":
        scripts = scripts.copy()
        # Always include core infrastructure scripts
        for infra_script in ["memory_db.py", "memory_bank.py", "tool_registry.py", "task_graph.py", "confirm_action.py", "execution_trace.py"]:
            if infra_script not in scripts:
                scripts.append(infra_script)
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
    
    # Generate setup scripts (one-command setup)
    generate_setup_script(workspace_path, name, packages)
    
    # Generate README
    generate_readme(workspace_path, type_config, name)
    
    # Generate VS Code custom agent file (.github/agents/*.agent.md)
    generate_custom_agent_file(workspace_path, type_config, name, slug)
    
    # Generate VS Code settings and extension recommendations
    generate_vscode_settings(workspace_path, name, slug)
    generate_vscode_extensions(workspace_path)
    
    # Generate VS Code tasks for automated setup
    generate_vscode_tasks(workspace_path, name)
    
    # Generate VS Code workspace file for easy opening
    generate_vscode_workspace_file(workspace_path, name, slug)
    
    # Initialize memory directory with default working memory files
    initialize_memory(workspace_path)
    
    print(f"\n{'=' * 60}")
    print(f"✓ WORKSPACE CREATED SUCCESSFULLY!")
    print(f"{'=' * 60}")
    print(f"\n🚀 INSTANT START - Just double-click:")
    print(f"   {workspace_path / ('agent-' + slug + '.code-workspace')}")
    print(f"")
    print(f"   VS Code will:")
    print(f"   • Open the workspace")
    print(f"   • Prompt to trust the folder (click Yes)")
    print(f"   • Auto-run setup (installs deps, creates .env)")
    print(f"   • Prompt to install recommended extensions")
    print(f"")
    print(f"   Then select '{name}' from Copilot Chat dropdown.")
    print(f"")
    print(f"Alternative (manual):")
    print(f"  cd \"{workspace_path}\"")
    print(f"  .\\setup.ps1   # Windows")
    print(f"  ./setup.sh     # macOS/Linux")
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
