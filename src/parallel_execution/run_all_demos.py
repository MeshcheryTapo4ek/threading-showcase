#!/usr/bin/env python3
"""
run_all_demos.py — Read, print and execute every Python demo in this folder.

For each .py file (except this one):
  • Prints a header and the file’s contents (raw, preserving formatting)
  • Executes it with the same interpreter
  • Prints its stdout and stderr under a divider
"""

import os
import sys
import glob
import subprocess

def main():
    # Name of this script, so we can skip it
    this = os.path.basename(__file__)

    # Find all .py files in current directory
    py_files = sorted(glob.glob("*.py"))

    for fname in py_files:
        if fname == this:
            continue

        # Section header
        print("\n" + "="*80)
        print(f"FILE: {fname}")
        print("="*80 + "\n")

        # Print source code
        with open(fname, "r", encoding="utf-8") as f:
            code = f.read()
        print(code)

        # Divider before output
        print("\n" + "-"*80)
        print(f"OUTPUT of {fname}")
        print("-"*80 + "\n")

        # Execute the script, capture output
        proc = subprocess.run(
            [sys.executable, fname],
            capture_output=True,
            text=True
        )

        # Print stdout
        if proc.stdout:
            print(proc.stdout, end="")

        # Print stderr (if any) under a warning
        if proc.stderr:
            print("\n" + "!"*20 + " ERRORS " + "!"*20)
            print(proc.stderr)
            print("!"*53 + "\n")

if __name__ == "__main__":
    main()
