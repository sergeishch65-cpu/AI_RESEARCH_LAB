#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/pip install --upgrade pip setuptools wheel
.venv/bin/pip install -r requirements.txt -e .
.venv/bin/python -m ai_research_lab.cli doctor

