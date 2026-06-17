#!/usr/bin/env bash

if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1
then
    echo "ERROR: Not inside a Git repository"
    exit 1
fi

echo "===== Git Repository Statistics ====="
echo

echo "1. Total number of commits:"
git rev-list --count HEAD
echo

echo "2. Number of commits per author:"
git log --format="%an" | sort | uniq -c | sort -rn
echo

echo "3. Three most recently modified files:"
git log --name-only --format="" -n 20 | grep -v '^$' | awk '!seen[$0]++' | head -3
echo

echo "4. File changed in the most commits:"
git log --name-only --format="" | grep -v '^$' | sort | uniq -c | sort -rn | head -1
