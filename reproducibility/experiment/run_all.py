"""Reproduce proposed gold, predictions and evaluation with Python standard library."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
for script in ["build_gold.py","validate_gold.py","compare_matchers.py","evaluate.py"]:
 print("Running",script,flush=True)
 subprocess.run([sys.executable,str(root/script)],cwd=root,check=True)
print("Reproduction finished. These are provisional in-sample metrics, not final audited evidence.")
