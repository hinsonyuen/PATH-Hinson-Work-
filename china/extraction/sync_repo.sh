#!/bin/bash
# Copy the Japan and China arms-trade work from the project folder into the GitHub repo and push.
# Usage: bash sync_repo.sh "commit message"
set -e
P=/mnt/project-files
R=/home/user/path-hinson-work-
if ! git -C "$R" rev-parse --git-dir >/dev/null 2>&1; then
  git clone https://github.com/hinsonyuen/path-hinson-work- "$R"
fi
cd "$R"
git checkout -q -B main
git fetch -q origin main 2>/dev/null && git reset -q --soft origin/main || true
mkdir -p japan/workbooks japan/reports japan/sources china/workbooks china/sources china/extraction/staging
cp "$P"/workbooks/Japan_Arms_*.xlsx japan/workbooks/
cp "$P"/workbooks/blanked-cells.md japan/workbooks/
cp "$P"/reports/*.docx japan/reports/
cp "$P"/sources/source-volumes-1860-1898.md "$P"/sources/verification-pages.md japan/sources/
cp "$P"/exports/japan-arms-trade-prompts.md japan/
cp "$P"/workbooks/China_Arms_*.xlsx china/workbooks/
cp "$P"/sources/china-*.md "$P"/sources/returns-of-trade-*.md china/sources/
cp "$P"/china-gazette/EXTRACTION_RULES.md "$P"/china-gazette/build_workbooks.py "$P"/china-gazette/sync_repo.sh "$P"/china-gazette/progress.log china/extraction/
cp "$P"/china-gazette/staging/No*.json china/extraction/staging/ 2>/dev/null || true
cp "$P"/china-gazette/README.md README.md
git add -A
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
git commit -q -m "${1:-Update arms trade data}

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016XgqMF48XwpvRrJZ9cVQvD"
for d in 0 2 4 8 16; do sleep $d; git push -u origin main && { echo pushed; exit 0; }; done
echo "PUSH FAILED"; exit 1
