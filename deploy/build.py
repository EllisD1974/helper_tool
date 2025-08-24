import shutil
from pathlib import Path
from typing import List
import subprocess


PYRCC5_BIN = shutil.which("pyrcc5")
PYUIC5_BIN = shutil.which("pyuic5")

TOOL_ROOT = Path(__file__).resolve().parents[1]
RESOURCES_DIR = TOOL_ROOT / "resources"
RESOURCES_INPUT = RESOURCES_DIR / "resources.qrc"
RESOURCES_OUTPUT = RESOURCES_DIR / "resources_rc.py"
SPEC_FILE = TOOL_ROOT / "helper.spec"

DELIMITER = "=" * 45

COMMANDS = {
    "resources": [PYRCC5_BIN, "-o", RESOURCES_OUTPUT, RESOURCES_INPUT],
    "build_exe": ["pyinstaller", SPEC_FILE],
}

def run_commands(commands: List[List[str]]) -> None:
    """ Run each command in sequence, waiting for previous to finish. """
    for cmd in commands:
        if cmd is not None:
            print(" ".join([str(c) for c in cmd]))
            subprocess.run(cmd, check=True)
            print(DELIMITER)

if __name__ == "__main__":
    run_commands([COMMANDS.get("resources")])
    run_commands([COMMANDS.get("build_exe")])
