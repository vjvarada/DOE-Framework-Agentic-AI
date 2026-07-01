#!/bin/bash
echo "Setting up: Agent Creator"
python3 -m venv .venv 2>/dev/null || python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
[ ! -f ".env" ] && [ -f ".env.example" ] && cp .env.example .env
echo "SETUP COMPLETE!"
