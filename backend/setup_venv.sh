#!/usr/bin/env bash
# One-time setup: creates a venv INSIDE backend/, local to this project only,
# and installs the exact package versions this app needs (backend/requirements.txt) —
# not the course-wide "nlp" environment.
#
# Run from Git Bash:
#   cd "/c/College Full/Projects/ExpenseTrackerAI/backend"
#   bash setup_venv.sh

set -e
cd "$(dirname "$0")"

if [ -d "venv" ]; then
  echo "backend/venv already exists."
  echo "Delete it first (rm -rf venv) if you want a totally clean rebuild."
else
  echo "Creating venv in backend/venv ..."
  python -m venv venv
fi

source venv/Scripts/activate

echo "Installing pinned dependencies from backend/requirements.txt ..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Done. Interpreter: $(python -c 'import sys; print(sys.executable)')"
echo ""
echo "From now on, activate this venv (instead of 'nlp') with:"
echo "    source venv/Scripts/activate"
echo ""
echo "See ../AUTO_ACTIVATE_VENV.md to make that happen automatically."
