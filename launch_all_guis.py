import subprocess
import os
import sys

# List of script filenames
scripts = [
    "PySide6_dark_ui_test.py",
    "Wxpython_dark_ui_test.py",
    "Kevy_dark_ui_test.py"
]

# Use the current working directory
cwd = os.path.dirname(os.path.abspath(__file__))

# Use sys.executable to ensure the same Python environment
processes = []
for script in scripts:
    script_path = os.path.join(cwd, script)
    if os.path.exists(script_path):
        # Start each script in a new process
        p = subprocess.Popen([sys.executable, script_path], cwd=cwd)
        processes.append(p)
    else:
        print(f"Script not found: {script}")

# Optionally, wait for all GUIs to close before exiting this launcher
for p in processes:
    p.wait()