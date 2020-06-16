import subprocess
import sys
from pathlib import Path


def freeze(requirements: Path) -> Path:
    Path(__file__).parent.parent / "templates" / "environment.yml"
    with open(requirements, "wb") as f:
        f.write("""""")
    return requirements
