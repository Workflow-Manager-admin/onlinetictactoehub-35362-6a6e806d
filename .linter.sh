#!/bin/bash
cd /home/kavia/workspace/code-generation/onlinetictactoehub-35362-6a6e806d/tic_tac_toe_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

