#!/bin/bash
# Runs the seven steps, then the checks. About 15 seconds on a laptop; nothing to install.
set -e
cd "$(dirname "$0")"
for step in step1_action step2_arrows step3_mirror step4_diagrams step5_limit step6_trick step7_oring; do
  echo
  echo "=== $step.py"
  python3 $step.py
done
echo
python3 tests.py
