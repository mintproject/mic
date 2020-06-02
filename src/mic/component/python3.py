import subprocess
import sys
from pathlib import Path


def freeze(requirements: Path) -> Path:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    with open(requirements, "wb") as f:
        f.write(reqs)
    return requirements
