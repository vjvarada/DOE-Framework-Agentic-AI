#!/usr/bin/env python3
"""
Campaign data manager — shared utility for output/ state management.

Provides helpers to create campaign folders, save step outputs,
and manage campaign config files.
"""
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Optional


def create_campaign(
    outputs_dir: Path,
    slug: str,
    metadata: Optional[dict] = None,
) -> Path:
    """Create a new campaign folder with config."""
    campaign_dir = outputs_dir / slug
    campaign_dir.mkdir(parents=True, exist_ok=True)

    config = {
        "slug": slug,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
        "steps": [],
    }
    config_path = campaign_dir / "campaign_config.json"
    if not config_path.exists():
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return campaign_dir


def save_step(
    campaign_dir: Path,
    step_number: int,
    step_name: str,
    data: Any,
    status: str = "completed",
) -> Path:
    """Save a step output file and update campaign config."""
    filename = f"step_{step_number}_{step_name}.json"
    filepath = campaign_dir / filename
    filepath.write_text(json.dumps(data, indent=2, default=str),
                        encoding="utf-8")

    # Update campaign config
    config_path = campaign_dir / "campaign_config.json"
    if config_path.exists():
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        cfg.setdefault("steps", [])
        # Remove existing step entry if present
        cfg["steps"] = [s for s in cfg["steps"]
                        if s.get("step") != step_number]
        cfg["steps"].append({
            "step": step_number,
            "name": step_name,
            "file": filename,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

    return filepath


def get_latest_step(campaign_dir: Path) -> Optional[dict]:
    """Get the most recent completed step."""
    config_path = campaign_dir / "campaign_config.json"
    if not config_path.exists():
        return None
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    steps = cfg.get("steps", [])
    completed = [s for s in steps if s.get("status") == "completed"]
    if not completed:
        return None
    return max(completed, key=lambda s: s.get("step", 0))


__all__ = ["create_campaign", "save_step", "get_latest_step"]
